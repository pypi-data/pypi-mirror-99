#!/bin/bash

WORKDIR=${PWD}

if [ "$DUNE_CONTROL_PATH" != "" ]; then
  if [ "$WORKDIR" != "$DUNE_CONTROL_PATH" ]; then
    echo "DUNE_CONTROL_PATH is already set to $DUNE_CONTROL_PATH"
    exit 1
  fi
fi

# create necessary python virtual environment
# this script assumes the name venv.
# Otherwise copy the instructions from the script
# to build you own

CMAKE_VERSION=`cmake --version | head -1 | cut -d " " -f 3 | cut -d " " -f 1`
REQUIRED_VERSION="3.13.3"
# check if cmake version is ok
if awk 'BEGIN {exit !('$CMAKE_VERSION' < '$REQUIRED_VERSION')}'; then
  CMAKEPIP=cmake
  echo "Installing cmake since current version is not new enough!"
fi

# create necessary python virtual environment
VENVDIR=$WORKDIR/venv
if ! test -d $VENVDIR ; then
  python3 -m venv $VENVDIR
  source $VENVDIR/bin/activate
  pip install --upgrade pip
  pip install $CMAKEPIP fenics-ufl numpy matplotlib mpi4py
else
  source $VENVDIR/bin/activate
fi

#change appropriately, i.e. 2.8 or leave empty which refers to master
DUNEVERSION=

FLAGS="-O3 -DNDEBUG -funroll-loops -finline-functions -Wall -ftree-vectorize -fno-stack-protector -mtune=native"

DUNECOREMODULES="dune-common dune-istl dune-geometry dune-grid dune-localfunctions"
DUNEEXTMODULES="dune-alugrid dune-spgrid"
DUNEFEMMODULES="dune-fem dune-fempy dune-fem-dg"

# build flags for all DUNE modules
# change according to your needs
if test -f config.opts ; then
  read -p "Found config.opts. Overwrite with default? (y,n) " YN
  if [ "$YN" == "y" ] ;then
    echo "Overwriting config.opts!"
    rm -f config.opts
  fi
fi

if ! test -f config.opts ; then
echo "\
DUNEPATH=`pwd`
BUILDDIR=build-cmake
USE_CMAKE=yes
MAKE_FLAGS=-j4
CMAKE_FLAGS=\"-DCMAKE_CXX_FLAGS=\\\"$FLAGS\\\"  \\
 -DDUNE_ENABLE_PYTHONBINDINGS=ON \\
 -DADDITIONAL_PIP_PARAMS="-upgrade" \\
 -DCMAKE_LD_FLAGS=\\\"$PY_LDFLAGS\\\" \\
 -DCMAKE_POSITION_INDEPENDENT_CODE=TRUE \\
 -DDISABLE_DOCUMENTATION=TRUE \\
 -DCMAKE_DISABLE_FIND_PACKAGE_LATEX=TRUE\" " > config.opts
fi

FOUND_DUNE_ACTIVATE=`grep "DUNE_VENV_SPECIFIC_SETUP" $VENVDIR/bin/activate`

if [ "$FOUND_DUNE_ACTIVATE" == "" ]; then
echo "
## DUNE_VENV_SPECIFIC_SETUP

# setVariable( varname newvalue )
setVariable() {
  if [ -n \"\${!1}\" ]; then
    export _OLD_VIRTUAL_\${1}=\"\${!1}\"
  fi
  export \${1}=\"\${2}\"
}

# set current main working directory
setVariable DUNE_CONTROL_PATH \$PWD
setVariable DUNE_LOG_LEVEL \"info\"

# defines CMAKE_FLAGS
source \${DUNE_CONTROL_PATH}/config.opts

setVariable DUNE_PY_DIR \${DUNE_CONTROL_PATH}/cache/
setVariable DUNE_CMAKE_FLAGS \"\$CMAKE_FLAGS\"

DUNEPYTHONPATH=
MODULES=\`\$DUNE_CONTROL_PATH/dune-common/bin/dunecontrol --print 2> /dev/null\`
for MOD in \$MODULES; do
  MODPATH=\"\${PWD}/\${MOD}/build-cmake/python\"
  MODFOUND=\`echo \$DUNEPYTHONPATH | grep \$MODPATH\`
  if [ \"\$MODFOUND\" == \"\" ]; then
    DUNEPYTHONPATH=\$DUNEPYTHONPATH:\$MODPATH
  fi
done

setVariable PYTHONPATH \$DUNEPYTHONPATH

echo \"DUNE_LOG_LEVEL=\$DUNE_LOG_LEVEL\"
echo \"Change with 'export DUNE_LOG_LEVEL={none,critical,info,debug}' if necessary!\"

# python \$DUNE_CONTROL_PATH/dune-common/bin/setup-dunepy.py
save_function() {
    local ORIG_FUNC=\$(declare -f \$1)
    local NEWNAME_FUNC=\"\$2\${ORIG_FUNC#\$1}\"
    eval \"\$NEWNAME_FUNC\"
}

restoreVariable() {
  VARNAME=_OLD_VIRTUAL_\$1
  if [ -n \"\${!VARNAME}\" ]; then
    export \${1}=\${!VARNAME}
    unset \${VARNAME}
  else
    unset \${1}
  fi
}

save_function deactivate venv_deactivate
deactivate() {
  restoreVariable DUNE_CONTROL_PATH
  restoreVariable DUNE_PY_DIR
  restoreVariable DUNE_CMAKE_FLAGS
  restoreVariable DUNE_LOG_LEVEL
  restoreVariable PYTHONPATH

  # call original deactivate
  venv_deactivate
  # self destroy
  unset venv_deactivate
  unset deactivate
}
" >> $VENVDIR/bin/activate
#> activate.sh
fi

DUNEBRANCH=
if [ "$DUNEVERSION" != "" ] ; then
  DUNEBRANCH="-b releases/$DUNEVERSION"
fi

# get all dune modules necessary
for MOD in $DUNECOREMODULES ; do
  git clone $DUNEBRANCH https://gitlab.dune-project.org/core/$MOD.git
done

# get all dune extension modules necessary
for MOD in $DUNEEXTMODULES ; do
  if [ "$MOD" == "dune-alugrid" ]; then
    git clone $DUNEBRANCH https://gitlab.dune-project.org/extensions/$MOD.git
  elif [ "$MOD" == "dune-spgrid" ]; then
    git clone $DUNEBRANCH https://gitlab.dune-project.org/extensions/$MOD.git
  else
    git clone $DUNEBRANCH https://gitlab.dune-project.org/staging/$MOD.git
  fi
done

# get all dune extension modules necessary
for MOD in $DUNEFEMMODULES ; do
  git clone $DUNEBRANCH https://gitlab.dune-project.org/dune-fem/$MOD.git
done

# load environment variables
source $VENVDIR/bin/activate

# build all DUNE modules using dune-control
./dune-common/bin/dunecontrol --opts=config.opts all
python ./dune-common/bin/setup-dunepy.py

echo "####################################################

Build finished (hopefully successful). Use

source ./$VENVDIR/bin/activate

to activate the virtual environment!"
