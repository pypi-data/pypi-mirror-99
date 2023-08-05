from math import sqrt
from dune.femdg import femDGOperator, rungeKuttaSolver

class FemDGStepper:
    def __init__(self,op,parameters):
        if parameters is None:
            self.rkScheme = rungeKuttaSolver( op )
        else:
            self.rkScheme = rungeKuttaSolver( op, parameters=parameters )
    def __call__(self,u,dt=None):
        if dt is not None:
            self.rkScheme.setTimeStepSize(dt)
        self.rkScheme.solve(u)
        return self.rkScheme.deltaT()
    @property
    def deltaT(self):
        return self.rkScheme.deltaT()
    @deltaT.setter
    def deltaT(self,dt):
        self.rkScheme.setTimeStepSize(dt)

def femdgStepper(*,order=None,rkType=None,operator=None,cfl=0.45,parameters=True):
    if parameters is True: parameters = {}
    elif parameters is False: parameters = None
    if rkType == "default": rkType = None
    def _femdgStepper(op,cfl=None):
        if parameters is not None:
            if not "fem.timeprovider.factor" in parameters:
                if cfl is not None:
                    parameters["fem.timeprovider.factor"] = cfl
                else:
                    parameters["fem.timeprovider.factor"] = 0.45
            if not "fem.ode.odesolver" in parameters:
                if rkType is not None:
                    parameters["fem.ode.odesolver"] = rkType
                elif op._hasAdvFlux and op._hasDiffFlux:
                    parameters["fem.ode.odesolver"] = "IMEX"
                elif op._hasAdvFlux:
                    parameters["fem.ode.odesolver"] = "EX"
                else:
                    parameters["fem.ode.odesolver"] = "IM"
            if not "fem.ode.order" in parameters:
                assert order is not None, "need to pass the order of the rk method to the 'femDGStepper' as argument or set it in the parameters"
                parameters["fem.ode.order"] = order
            if not "fem.ode.maxiterations" in parameters:
                parameters["fem.ode.maxiterations"] = 100 # the default (16) seems to lead to very small time steps
        return FemDGStepper(op,parameters)
    if operator is None:
        return _femdgStepper
    else:
        return _femdgStepper(operator,cfl)

# Set up problem: L[baru+a*k] - k = 0
class HelmholtzButcher:
    def __init__(self,op):
        self.op = op
        self._alpha = None
        self.res = op.space.interpolate(op.space.dimRange*[0],name="res")
        self.x   = op.space.interpolate(op.space.dimRange*[0],name="res")
        self.counter = 0
        self.inner_counter = 0
    @property
    def alpha(self):
        return self._alpha
    @alpha.setter
    def alpha(self,value):
        self._alpha = value
    def f(self, x_coeff):
        ## the following produces a memory leak - needs fixing!
        # x = self.op.space.function("tmp", dofVector=x_coeff)
        ## for now copy dof vector
        self.x.as_numpy[:]  = x_coeff[:]
        self.x.as_numpy[:] *= self.alpha
        self.x.as_numpy[:] += self.baru.as_numpy[:]
        #self.x *= self.alpha
        #self.x += self.baru
        self.op(self.x, self.res)
        self.res -= self.x
        return self.res.as_numpy
    def solve(self,baru,target):
        from scipy.optimize import newton_krylov
        counter = 0
        inner_counter = 0
        def callb(x,Fx): nonlocal counter;       counter+=1
        def icallb(rk):  nonlocal inner_counter; inner_counter+=1
        self.baru = baru

        sol_coeff = target.as_numpy
        sol_coeff[:] = newton_krylov(self.f, sol_coeff,
                                         verbose=False,
                                         callback=callb, inner_callback=icallb)
        self.counter = counter
        self.inner_counter = inner_counter # linear iterations not crrect
# Set up problem: rhs + a*L[y] - y = 0
class HelmholtzShuOsher:
    def __init__(self,op):
        self.op = op
        self._alpha = None
        self.res = op.space.interpolate(op.space.dimRange*[0],name="res")
        self.x   = op.space.interpolate(op.space.dimRange*[0],name="res")
        self.counter = 0
        self.inner_counter = 0
    @property
    def alpha(self):
        return self._alpha
    @alpha.setter
    def alpha(self,value):
        self._alpha = value
    def f(self, x_coeff):
        ## the following produces a memory leak - needs fixing!
        # x = self.op.space.function("tmp", dofVector=x_coeff)
        self.x.as_numpy[:] = x_coeff[:]
        self.op(self.x, self.res)
        # needs speedup, e.g.
        # - 2011: https://technicaldiscovery.blogspot.com/2011/06/speeding-up-python-numpy-cython-and.html
        try:
            import numexpr, numpy
            a = numpy.array([self.alpha])
            res = self.res.as_numpy
            rhs = self.rhs.as_numpy
            self.res.as_numpy[:] = numexpr.evaluate('a*res-x_coeff+rhs')
        except ModuleNotFoundError:
            # compute alpha*res -x + rhs (by calling routines on discrete functions)
            self.res *= self.alpha
            self.res -= self.x
            self.res += self.rhs
        return self.res.as_numpy

    def solve(self,rhs,target):
        from scipy.optimize import newton_krylov
        counter = 0
        inner_counter = 0
        def callb(x,Fx): nonlocal counter;       counter+=1
        def icallb(rk):  nonlocal inner_counter; inner_counter+=1
        self.rhs = rhs

        sol_coeff = target.as_numpy
        sol_coeff[:] = newton_krylov(self.f, sol_coeff,
                    verbose=False,
                    callback=callb, inner_callback=icallb)
        self.counter = counter
        self.inner_counter = inner_counter # linear iterations not crrect

class RungeKutta:
    def __init__(self,op,cfl, A,b,c):
        self.op = op
        self.A = A
        self.b = b
        self.c = c
        self.stages = len(b)
        self.cfl = cfl
        self.dt = None
        self.k = self.stages*[None]
        for i in range(self.stages):
            self.k[i] = op.space.interpolate(op.space.dimRange*[0],name="k")
        self.tmp = op.space.interpolate(op.space.dimRange*[0],name="tmp")
        self.explicit = all([abs(A[i][i])<1e-15 for i in range(self.stages)])
        if not self.explicit:
            self.helmholtz = HelmholtzButcher(self.op)
    def __call__(self,u,dt=None):
        if self.explicit:
            assert abs(self.c[0])<1e-15
            self.op.stepTime(0,0)
            self.op(u,self.k[0])
            if dt is None and self.dt is None:
                dt = self.op.localTimeStepEstimate[0]*self.cfl
            elif dt is None:
                dt = self.dt
            self.dt = 1e10
            for i in range(1,self.stages):
                self.tmp.assign(u)
                for j in range(i):
                    self.tmp.axpy(dt*self.A[i][j],self.k[j])
                self.op.stepTime(self.c[i],dt)
                self.op(self.tmp,self.k[i])
                self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
        else:
            if dt is None and self.dt is None:
                self.op.stepTime(0,0)
                self.op(u,self.k[0])
                dt = self.op.localTimeStepEstimate[0]*self.cfl
            elif dt is None:
                dt = self.dt
            self.dt = 1e10
            for i in range(0,self.stages):
                self.tmp.assign(u)
                for j in range(i):
                    self.tmp.axpy(dt*self.A[i][j],self.k[j])
                self.op.stepTime(self.c[i],dt)
                self.op(self.tmp,self.k[i]) # this seems like a good initial guess for dt small
                self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
                self.helmholtz.alpha = dt*self.A[i][i]
                self.helmholtz.solve(baru=self.tmp,target=self.k[i])

        for i in range(self.stages):
            u.axpy(dt*self.b[i],self.k[i])
        self.op.applyLimiter( u )
        self.op.stepTime(0,0)
        return self.op.space.grid.comm.min(dt)
class Heun(RungeKutta):
    def __init__(self, op, cfl=None):
        A = [[0,0],
             [1,0]]
        b = [0.5,0.5]
        c = [0,1]
        cfl = 0.45 if cfl is None else cfl
        RungeKutta.__init__(self,op,cfl,A,b,c)
# The following seems an inefficient implementation in the sense that it
# converges very slowly - there is a better implementation below using a
# Shu-Osher form of the method - the dune-fem implementation of DIRK also
# uses some transformation of the Butcher tableau which could be
# reimplemented here.
# A lot about DIRK - worth looking into more closely
# https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20160005923.pdf

class ExplEuler(RungeKutta):
    def __init__(self, op, cfl=None):
        A = [[0.]]
        b = [1.]
        c = [0.]
        cfl = 0.45 if cfl is None else cfl
        RungeKutta.__init__(self,op,cfl,A,b,c)
class ImplEuler(RungeKutta):
    def __init__(self, op, cfl=None):
        A = [[1.]]
        b = [1]
        c = [1.]
        cfl = 0.45 if cfl is None else cfl
        RungeKutta.__init__(self,op,cfl,A,b,c)
def euler(explicit=True):
    if explicit:
        return lambda op,cfl=None: ExplEuler(op,cfl)
    else:
        return lambda op,cfl=None: ImplEuler(op,cfl)

class Midpoint(RungeKutta):
    def __init__(self, op, cfl=None):
        A = [[0.5]]
        b = [1]
        c = [0.5]
        cfl = 0.45 if cfl is None else cfl
        RungeKutta.__init__(self,op,cfl,A,b,c)
class ImplSSP2: # with stages=1 same as above - increasing stages does not improve anything
    def __init__(self,stages,op,cfl=None):
        self.stages = stages
        self.op     = op

        self.mu11   = 1/(2*stages)
        self.mu21   = 1/(2*stages)
        self.musps  = 1/(2*stages)
        self.lamsps = 1

        self.q2     = op.space.interpolate(op.space.dimRange*[0],name="q2")
        self.tmp    = self.q2.copy()
        self.cfl    = 0.45 if cfl is None else cfl
        self.dt     = None
        self.helmholtz = HelmholtzShuOsher(self.op)
    def c(self,i):
        return i/(2*self.stages)
    def __call__(self,u,dt=None):
        if dt is None and self.dt is None:
            self.op.stepTime(0,0)
            self.op(u, self.tmp)
            dt = self.op.localTimeStepEstimate[0]*self.cfl
        elif dt is None:
            dt = self.dt
        self.dt = 1e10
        self.helmholtz.alpha = dt*self.mu11

        self.q2.assign(u)
        self.op.stepTime(self.c(1),dt)
        self.helmholtz.solve(u,self.q2) # first stage
        for i in range(2,self.stages+1):
            self.op.stepTime(self.c(i),dt)
            self.op(self.q2, self.tmp)
            self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
            self.q2.axpy(dt*self.mu21, self.tmp)
            self.q2.assgin(tmp)
            self.helmholtz.solve(self.tmp, self.q2)
        u.as_numpy[:] *= (1-self.lamsps)
        u.axpy(self.lamsps, self.q2)
        self.op(self.q2, self.tmp)
        self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
        u.axpy(dt*self.musps, self.tmp)
        self.op.applyLimiter( u )
        self.op.stepTime(0,0)
        return self.op.space.grid.comm.min(dt)
class ExplSSP2:
    def __init__(self,stages,op,cfl=None):
        self.op     = op
        self.stages = stages
        self.q2     = op.space.interpolate(op.space.dimRange*[0],name="q2")
        self.tmp    = self.q2.copy()
        self.cfl    = 0.45 * (stages-1)
        self.dt     = None
    def c(self,i):
        return (i-1)/(self.stages-1)
    def __call__(self,u,dt=None):
        if dt is None and self.dt is None:
            self.op.stepTime(0,0)
            self.op(u, self.tmp)
            dt = self.op.localTimeStepEstimate[0]*self.cfl
        elif dt is None:
            dt = self.dt
        self.dt = 1e10
        fac = dt/(self.stages-1)
        self.q2.assign(u)
        for i in range(1,self.stages):
            self.op.stepTime(self.c(i),dt)
            self.op(u,self.tmp)
            self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
            u.axpy(fac, self.tmp)
        self.op.stepTime(self.c(i),dt)
        self.op(u,self.tmp)
        self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
        u.as_numpy[:] *= (self.stages-1)/self.stages
        u.axpy(dt/self.stages, self.tmp)
        u.axpy(1/self.stages, self.q2)
        self.op.applyLimiter( u )
        self.op.stepTime(0,0)
        return self.op.space.grid.comm.min(dt)
def ssp2(stages,explicit=True):
    if explicit:
        return lambda op,cfl=None: ExplSSP2(stages,op,cfl)
    else:
        return lambda op,cfl=None: ImplSSP2(stages,op,cfl)
# optimal low storage methods:
# http://www.sspsite.org
# https://arxiv.org/pdf/1605.02429.pdf
# https://openaccess.leidenuniv.nl/bitstream/handle/1887/3295/02.pdf?sequence=7
# https://epubs.siam.org/doi/10.1137/07070485X
# implicit: https://www.sciencedirect.com/science/article/abs/pii/S0168927408000688
class ExplSSP3:
    def __init__(self,stages,op,cfl=None):
        self.op     = op
        self.n      = int(sqrt(stages))
        self.stages = self.n*self.n
        assert self.stages == stages, "doesn't work if sqrt(s) is not integer"
        self.r      = self.stages-self.n
        self.q2     = op.space.interpolate(op.space.dimRange*[0],name="q2")
        self.tmp    = self.q2.copy()
        self.cfl    = 0.45 * stages*(1-1/self.n) if cfl is None else cfl
        self.dt     = None
    def c(self,i):
        return (i-1)/(self.n*self.n-self.n) \
               if i<=(self.n+2)*(self.n-1)/2+1 \
               else (i-self.n-1)/(self.n*self.n-self.n)
    def __call__(self,u,dt=None):
        if dt is None and self.dt is None:
            self.op.stepTime(0,0)
            self.op(u, self.tmp)
            dt = self.op.localTimeStepEstimate[0]*self.cfl
        elif dt is None:
            dt = self.dt
        self.dt = 1e10
        fac = dt/self.r
        i = 1
        while i <= (self.n-1)*(self.n-2)/2:
            self.op.stepTime(self.c(i),dt)
            self.op(u,self.tmp)
            self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
            u.axpy(fac, self.tmp)
            i += 1
        self.q2.assign(u)
        while i <= self.n*(self.n+1)/2:
            self.op.stepTime(self.c(i),dt)
            self.op(u,self.tmp)
            self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
            u.axpy(fac, self.tmp)
            i += 1
        u.as_numpy[:] *= (self.n-1)/(2*self.n-1)
        u.axpy(self.n/(2*self.n-1), self.q2)
        while i <= self.stages:
            self.op.stepTime(self.c(i),dt)
            self.op(u,self.tmp)
            self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
            u.axpy(fac, self.tmp)
            i += 1
        self.op.applyLimiter( u )
        self.op.stepTime(0,0)
        return self.op.space.grid.comm.min(dt)
class ImplSSP3:
    def __init__(self,stages,op,cfl=None):
        self.stages = stages
        self.op     = op

        self.mu11   = 0.5*( 1 - sqrt( (stages-1)/(stages+1) ) )
        self.mu21   = 0.5*( sqrt( (stages+1)/(stages-1) ) - 1 )
        q           = stages*(stages+1+sqrt(stages*stages-1))
        self.musps  = (stages+1)/q
        self.lamsps = (stages+1)/q*(stages-1+sqrt(stages*stages-1))

        self.q2     = op.space.interpolate(op.space.dimRange*[0],name="q2")
        self.tmp    = self.q2.copy()
        self.cfl    = 0.45 * (stages-1+sqrt(stages*stages-1)) if cfl is None else cfl
        self.dt     = None
        self.helmholtz = HelmholtzShuOsher(self.op)
    def c(self,i):
        assert False, "not yet implemented"
    def __call__(self,u,dt=None):
        # y_1 = u + dt mu_{i,i-1}L[y_{i-1}]
        # y_i = y_{i-1} + dt mu_{i,i-1}L[y_{i-1}] + dt mu_{i,i}L[y_i]   i>1
        # or
        # (1 - dt mu_{ii} L)y_1 = u
        # (1 - dt mu_{ii} L)y_i = (1 + dt * mu_{i,i-1} L)y_{i-1}        i>1
        # and u = (1-lamsps)u + (lamsps + dt musps L)y_s

        if dt is None and self.dt is None:
            # self.op.stepTime(0,0)
            self.op(u, self.tmp)
            dt = self.op.localTimeStepEstimate[0]*self.cfl
        elif dt is None:
            dt = self.dt
        self.dt = 1e10
        self.helmholtz.alpha = dt*self.mu11

        # self.op.stepTime(self.c(1),dt)
        self.helmholtz.solve(u,self.q2) # first stage
        for i in range(2,self.stages+1):
            # self.op.stepTime(self.c(i),dt)
            self.op(self.q2, self.tmp)
            self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
            self.q2.axpy(dt*self.mu21, self.tmp)
            self.helmholtz.solve(self.q2,self.tmp)
            self.q2.assign(self.tmp)
        u.as_numpy[:] *= (1-self.lamsps)
        u.axpy(self.lamsps, self.q2)
        self.op(self.q2, self.tmp)
        self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
        u.axpy(dt*self.musps, self.tmp)
        self.op.applyLimiter( u )
        self.op.stepTime(0,0)
        return self.op.space.grid.comm.min(dt)
def ssp3(stages,explicit=True):
    if explicit:
        return lambda op,cfl=None: ExplSSP3(stages,op,cfl)
    else:
        return lambda op,cfl=None: ImplSSP3(stages,op,cfl)

class ExplSSP4_10:
    def __init__(self, op,cfl=None):
        self.op     = op
        self.stages = 10
        self.q2     = op.space.interpolate(op.space.dimRange*[0],name="q2")
        self.tmp    = self.q2.copy()
        self.cfl    = 0.45 * self.stages*0.6 if cfl is None else cfl
        self.dt     = None
    def c(self,i):
        return (i-1)/6 if i<=5 else (i-4)/6
    def __call__(self,u,dt=None):
        if dt is None and self.dt is None:
            self.op.stepTime(0,0)
            self.op(u, self.tmp)
            dt = self.op.localTimeStepEstimate[0]*self.cfl
        elif dt is None:
            dt = self.dt
        self.dt = 1e10

        i = 1
        self.q2.assign(u)
        while i <= 5:
            self.op.stepTime(self.c(i), dt)
            self.op(u, self.tmp)
            self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
            u.axpy(dt/6, self.tmp)
            i += 1

        self.q2.as_numpy[:] *= 1/25
        self.q2.axpy(9/25, u)
        u.as_numpy[:] *= -5
        u.axpy(15, self.q2)

        while i <= 9:
            self.op.stepTime(self.c(i), dt)
            self.op(u, self.tmp)
            self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
            u.axpy(dt/6, self.tmp)
            i += 1

        self.op.stepTime(self.c(i), dt)
        self.op(u, self.tmp)
        self.dt = min(self.dt, self.op.localTimeStepEstimate[0]*self.cfl)
        u.as_numpy[:] *= 3/5
        u.axpy(1, self.q2)
        u.axpy(dt/10, self.tmp)
        self.op.applyLimiter( u )
        self.op.stepTime(0,0)
        return self.op.space.grid.comm.min(dt)
