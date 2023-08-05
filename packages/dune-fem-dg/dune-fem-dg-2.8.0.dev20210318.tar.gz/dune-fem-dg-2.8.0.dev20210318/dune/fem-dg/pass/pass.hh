#ifndef DUNE_FEM_DG_PASS_HH
#define DUNE_FEM_DG_PASS_HH

#ifdef DUNE_FEM_PASS_COMMON_PASS_HH
#error "pass.hh and local.hh from dune-fem are outdated!"
#endif

#include <limits>
#include <memory>
#include <string>
#include <sstream>
#include <tuple>
#include <type_traits>

#include <dune/common/timer.hh>

#include <dune/fem/common/memory.hh>
#include <dune/fem/common/tupleutility.hh>
#include <dune/fem/operator/common/operator.hh>
#include <dune/fem/space/common/allgeomtypes.hh>

namespace Dune
{

  namespace Fem
  {

    // empty non-blocking communication for start pass as default argument
    struct EmptyNonBlockingComm
    {
      // initialize communication
      template <class Destination>
      void initComm( const Destination& ) const {}

      // receive data of previously initialized communication
      template <class Destination>
      void receiveComm( const Destination& ) const {}

      // cleanup overwritten data, i.e. ghost values
      template <class Destination>
      void finalizeComm( const Destination& ) const {}
    };

    /*! @addtogroup Pass
     *
     */
    /*!
     * @brief End marker for a compile-time list of passes.
     *
     */
    template < class ArgumentImp , int passIdImp,
               class NonBlockingCommunication = EmptyNonBlockingComm  >
    class StartPass
    {
      NonBlockingCommunication nonBlockingComm_;
    public:
      //! position in pass tree (0 for start pass)
      static const int passNum = 0;
      static const int passId = passIdImp;

      //! pass ids up to here (tuple of integral constants)
      typedef std::tuple< std::integral_constant< int, passIdImp > > PassIds;

      //! The argument (and destination) type of the overall operator
      typedef ArgumentImp GlobalArgumentType;
      //! End marker for tuple of return types of the passes
      typedef std::tuple<> NextArgumentType;

    public:
      //! empty constructor
      StartPass() : nonBlockingComm_() {}
      //! copy constructor
      StartPass(const StartPass&) : nonBlockingComm_() {}

      //- Public methods
      //! The pass method initialized the communication only
      void pass( const GlobalArgumentType& arg ) const
      {
        nonBlockingComm_.initComm( arg );
      }

      //! receive data for previously initialized communication
      void receiveCommunication( const GlobalArgumentType& arg ) const
      {
        nonBlockingComm_.receiveComm( arg );
      }

      //! cleanup of overwritten data. i.e. ghost values if neccessary
      void finalizeCommunication( const GlobalArgumentType& arg ) const
      {
        nonBlockingComm_.finalizeComm( arg );
      }

      //! Returns the closure of the destination tuple.
      NextArgumentType localArgument() const { return NextArgumentType(); }

      //! No memory needs to be allocated.
      void allocateLocalMemory() {}

      //! StartPass does not need a time
      void setTime(const double) {}

      //! return time step estimate
      double timeStepEstimate() const
      {
        return std::numeric_limits<double>::max();
      }
    };

    /**
     * @brief Base class for specific pass implementations.
     *
     * Pass not only provides the interface for the specialised implementations,
     * but also organizes the calls to other passes and assembles the results
     * of the preceding passes in a tuple of discrete functions which can be
     * used in the computations of the pass. The computations must be implemented
     * in the compute method of the derived classes.
     */
    template <class DiscreteModelImp, class PreviousPassImp , int passIdImp>
    class Pass :
      public Operator<typename PreviousPassImp::GlobalArgumentType,
                      typename DiscreteModelImp::Traits::DestinationType>
    {
      template <class PT, class PP, int PI>
      friend class Pass;
    public:
      //! Type of the preceding pass.
      typedef PreviousPassImp PreviousPassType;

      //! position in pass tree
      static const int passNum = PreviousPassType::passNum + 1;
      static const int passId  = passIdImp;

      //! pass ids up to here (tuple of integral constants)
      typedef typename Dune::PushBackTuple< typename PreviousPassType::PassIds, std::integral_constant< int, passIdImp > >::type PassIds;

      //! Type of the discrete function which stores the result of this pass'
      //! computations.
      typedef typename DiscreteModelImp::Traits::DestinationType DestinationType;

      typedef typename DestinationType :: DiscreteFunctionSpaceType :: CommunicationManagerType
            :: NonBlockingCommunicationType  NonBlockingCommunicationType;

      //! Type of the discrete function which is passed to the overall operator
      //! by the user
      typedef typename PreviousPassType::GlobalArgumentType GlobalArgumentType;
      //! Tuple containing destination types of all preceding passes.
      typedef typename PreviousPassType::NextArgumentType LocalArgumentType;
      //! Tuple containing destination types of all preceding passes plus the
      //! global argument. This serves as the argument for this pass'
      //! computations
      typedef typename PushFrontTuple< LocalArgumentType, const GlobalArgumentType* >::type TotalArgumentType;
      //! Tuple containing destination types of all passes up to this one.
      typedef typename PushBackTuple< LocalArgumentType, DestinationType* >::type NextArgumentType;

    public:
      // return pass number
      int passNumber() const { return passNum; }

      //- Public methods
      //! Constructor
      //! \param pass Previous pass
      Pass(PreviousPassType& pass) :
        destination_(0),
        destinationMemory_(),
        previousPass_(pass),
        time_(0.0),
        finalizeCommunication_( true )
      {
        // this ensures that the last pass doesn't allocate temporary memory
        // (its destination discrete function is provided from outside).
        previousPass_.allocateLocalMemory();
      }

      //! Destructor
      virtual ~Pass()
      {
        destinationMemory_.reset();
        destination_ = nullptr;
      }

      //! printTex info of operator
      void printTexInfo(std::ostream& out) const
      {
        previousPass_.printTexInfo(out);
      }

      //! \brief Application operator.
      //! The application operator is called by the client directly. It makes
      //! only sense to call this operator directly on the last pass.
      void operator()(const GlobalArgumentType& arg, DestinationType& dest) const
      {
        previousPass_.pass(arg);
        LocalArgumentType prevArg = previousPass_.localArgument();
        const TotalArgumentType totalArg = tuple_push_front( prevArg, &arg );
        this->compute(totalArg, dest);

        // if initComm has not been called for this pass, we have to
        // call finalizeCommunication for all previous passes
        if( finalizeCommunication_ )
          finalizeCommunication( arg );
      }

      //! Allocates the local memory of a pass, if needed and stores it in destinationMemory_
      virtual void allocateLocalMemory() = 0;

      //! Set time provider (which gives you access to the global time).
      void setTime(const double t)
      {
        previousPass_.setTime(t);
        time_ = t;
      }

      /** \brief return time step estimate for explicit Runge Kutta solver, calls
           recursively the method timeStepEstimateImpl of all previous passes.
           Make sure to overload the method timeStepEstimateImpl in your
           implementation if this method really does something. */
      double timeStepEstimate() const
      {
        double ret= std::min( previousPass_.timeStepEstimate(),
                              this->timeStepEstimateImpl() );
        return ret;
      }

      //! return current time of calculation
      double time() const { return time_; }

      //! return reference to internal discrete function
      const DestinationType & destination () const
      {
        assert(destination_);
        return *destination_;
      }

    public:
      //! Same as application operator, but uses own memory instead of the
      //! discrete function provided by the client. This method is called on all
      //! passes except the last one.
      void pass(const GlobalArgumentType& arg) const
      {
        // send my destination data needed by the next pass
        initComm();
        // since initComm was called we are not the last pass
        // and thus must not call finalizeCommunication
        finalizeCommunication_ = false ;
        operator()(arg, *destination_);
      }

      //! Returns a compilation of the results of the preceding passes
      NextArgumentType localArgument () const
      {
        typename PreviousPassType::NextArgumentType nextArg( previousPass_.localArgument() );
        return tuple_push_back( nextArg, destination_ );
      }

      /** \brief finalizeCommunication collects possbily initiated non-blocking
                 communications for all passes including the global argument
                 this method will be called from the next pass
      */
      void finalizeCommunication(const GlobalArgumentType& arg) const
      {
        // we only need the first argument
        // the other argument are known to the previous passes
        previousPass_.finalizeCommunication( arg );

        // this method has to be overloaded in the pass implementation
        finalizeComm();
        // reset finalizeCommunication flag
        finalizeCommunication_ = true;
      }

      /** \brief finalizeCommunication collects possbily initiated non-blocking
                 communications for all passes including the global argument
                 this method will be called from the next pass
      */
      void receiveCommunication(const GlobalArgumentType& arg) const
      {
        // we only need the first argument
        // the other argument are known to the previous passes
        previousPass_.receiveCommunication( arg );

        // this method has to be overloaded in the pass implementation
        receiveComm();
      }

      //! derived passes have to implement this method
      //! returning the time step estimate
      virtual double timeStepEstimateImpl() const
      {
        return std::numeric_limits<double>::max();
      }

      /** \brief requireCommunication returns true if the pass needs communication at all
       *         \note The default implementation returns \b true \b
       */
      virtual bool requireCommunication () const { return true; }

    protected:
      //! Does the actual computations. Needs to be overridden in the derived
      //! clases
      virtual void compute(const TotalArgumentType& arg,
                           DestinationType& dest) const = 0;

      /** \brief finalizeCommunication collects possbily initiated non-blocking
                 communications for all passes
      */
      void finalizeCommunication( const TotalArgumentType& totalArg ) const
      {
        // this method is called on the last pass which needs no
        // finalizing of communication, so call the correct method
        // on the previous pass
        // std::get<0> ( totalArg ) is the global argument type
        previousPass_.finalizeCommunication( *(std::get<0> ( totalArg )) );
      }

      /** \brief receiveCommunication collects possbily initiated non-blocking
                 communications for all passes
      */
      void receiveCommunication( const TotalArgumentType& totalArg ) const
      {
        // this method is called on the last pass which needs no
        // finalizing of communication, so call the correct method
        // on the previous pass
        // std::get<0> ( totalArg ) is the global argument type
        previousPass_.receiveCommunication( *(std::get<0> ( totalArg )) );
      }

      /** \brief initializeCommunication of this pass, this will initialize
                 the communication of destination_ and has to be overloaded in
                 the implementation
      */
      virtual void initComm() const {}

      /** \brief finalizeCommunication of this pass, this will collect
                 the communication of destination_ and has to be overloaded in
                 the implementation
      */
      virtual void finalizeComm() const {}

      /** \brief receiveCommunication of this pass,
                 which will reset changes the communication
                 did to the destination_ and has to be overloaded in
                 the implementation
      */
      virtual void receiveComm() const {}

    protected:
      //! destination (might be set from outside)
      DestinationType* destination_;

      //! object to delete destination pointer
      std::unique_ptr< DestinationType > destinationMemory_;

      // previous pass
      PreviousPassType& previousPass_;

      // current calculation time
      double time_;

      // flag whether we are the last pass, i.e. we have to finalize the communication
      mutable bool finalizeCommunication_ ;
    }; // end class Pass


    // LocalPass
    // ---------

    /** \brief Specialisation of Pass which provides a grid walk-through,
     *         but leaves open what needs to be done on each elements.
     *
     *  \tparam  DiscreteModelImp  discrete model
     *  \tparam  PreviousPassImp   previous pass
     *  \tparam  passIdImp         id for this pass
     */
    template< class DiscreteModelImp, class PreviousPassImp , int passIdImp >
    class LocalPass
    : public Pass< DiscreteModelImp , PreviousPassImp , passIdImp>
    {
    public:
      //! \brief type of the preceding pass
      typedef PreviousPassImp PreviousPassType;

      //! \brief base class
      typedef Pass< DiscreteModelImp , PreviousPassImp , passIdImp > BaseType;

      /** \brief The type of the argument (and destination) type of
       *         the overall operator
       */
      typedef typename BaseType::TotalArgumentType ArgumentType;

      //! \brief the discrete function representing the return value of this pass
      typedef typename DiscreteModelImp::Traits::DestinationType DestinationType;
      //! \brief the discrete function space belonging to destinationtype
      typedef typename DiscreteModelImp::Traits::DiscreteFunctionSpaceType DiscreteFunctionSpaceType;
      //! \brief iterator over the space
      typedef typename DiscreteFunctionSpaceType::IteratorType IteratorType;
      //! \brief the codim 0 entity
      typedef typename DiscreteFunctionSpaceType::EntityType EntityType;

      /** \brief constructor
       *  \param pass Previous pass
       *  \param spc Space belonging to the discrete function of this pass.
       *  \param passName an identifier for this pass
       */
      LocalPass (PreviousPassImp &pass,
                 const DiscreteFunctionSpaceType &spc,
                 std::string passName = "LocalPass")
      : BaseType(pass),
        spc_( Dune::Fem::referenceToSharedPtr( spc ) ),
        passName_(passName),
        computeTime_(0.0),
        numberOfElements_( 0 ),
        passIsActive_( true )
      {}

      //! \brief destructor
      virtual ~LocalPass () {}

      //! \brief build up local memory
      virtual void allocateLocalMemory ()
      {
        if (!this->destination_)
        {
          std::ostringstream funcName;
          funcName << passName_ << "_" << this->passNumber();
          this->destinationMemory_.reset( new DestinationType(funcName.str(), space()));
          this->destination_ = this->destinationMemory_.operator->();
        }
      }

      //! \brief return reference to space
      const DiscreteFunctionSpaceType &space () const { return *spc_; }

      /** \brief return accumulated time needed by pass's operator () this method
       *         also resets the compute time to zero
       */
      virtual double computeTime () const
      {
        double ct = computeTime_;
        computeTime_ = 0.0;
        return ct;
      }

      /** \brief return number of elements visited during operator computation */
      virtual size_t numberOfElements() const { return numberOfElements_; }

      /** \brief return true if pass is active */
      bool active () const { return passIsActive_; }

      /** \brief set pass status to active */
      void enable () const { passIsActive_ = true ; }

      /** \brief set pass status to inactive */
      void disable() const { passIsActive_ = false ; }

    protected:
      //! Actions to be carried out before a global grid walkthrough.
      //! To be overridden in a derived class.
      virtual void prepare (const ArgumentType &arg, DestinationType &dest) const = 0;

      using BaseType::finalize;
      //! Actions to be carried out after a global grid walkthrough.
      //! To be overridden in a derived class.
      virtual void finalize (const ArgumentType &arg, DestinationType &dest) const = 0;
      //! Actions to be taken on every element. To be overridden in a derived
      //! class.
      virtual void applyLocal (const EntityType &en ) const = 0;

    public:
      //! The actual computations are performed as follows. First, prepare
      //! the grid walkthrough, then call applyLocal on each entity and then
      //! call finalize.
      void compute (const ArgumentType &arg, DestinationType &dest) const
      {
        // if pass was disable, don't do computation
        if( ! active() ) return ;

        // get stopwatch
        Dune::Timer timer;

        prepare(arg, dest);

        numberOfElements_ = 0 ;
        const IteratorType endit = space().end();
        for (IteratorType it = space().begin(); it != endit; ++it, ++ numberOfElements_ )
        {
          applyLocal(*it);
        }

        finalize(arg, dest);

        // accumulate time
        computeTime_ += timer.elapsed();
      }

      // called from ThreadPass to initialize quadrature singleton storages
      static void initializeQuadratures( const DiscreteFunctionSpaceType& space,
                                         const int volQuadOrder  = -1,
                                         const int faceQuadOrder = -1)
      {
        // do nothing here, should be overloaded in derived class if needed
      }


    protected:
      //! initialize all quadratures used in this Pass (for thread parallel runs)
      static void initializeQuadratures( const DiscreteFunctionSpaceType& space,
                                         const std::vector<int>& volQuadOrders,
                                         const std::vector<int>& faceQuadOrders )
      {
        typedef typename DiscreteModelImp::Traits::VolumeQuadratureType VolumeQuadratureType;
        typedef typename DiscreteModelImp::Traits::FaceQuadratureType   FaceQuadratureType;

        typedef typename DiscreteFunctionSpaceType :: GridPartType GridPartType;
        typedef typename GridPartType :: IndexSetType IndexSetType;
        typedef typename GridPartType :: GridType    GridType ;
        typedef AllGeomTypes< IndexSetType, GridType> GeometryInformationType;

        GeometryInformationType geomInfo( space.gridPart().indexSet() );
        const std::vector< GeometryType >& elemTypes = geomInfo.geomTypes( 0 );
        const bool singleGeomType = elemTypes.size() == 1;

        // for all geometry types
        for( const GeometryType& type : elemTypes )
        {
          for( const auto order : volQuadOrders )
          {
            // get quadrature for destination space order
            VolumeQuadratureType quad( type, order );
          }
        }

        const auto& gridPart = space.gridPart();
        for( const auto& entity : space )
        {
          for( const auto order : volQuadOrders )
          {
            // get quadrature for destination space order
            VolumeQuadratureType quad( entity, order );
          }

          const auto end = gridPart.iend( entity );
          for( auto it = gridPart.ibegin( entity ); it != end; ++it )
          {
            const auto& intersection = *it ;
            for( const int order : faceQuadOrders )
            {
              FaceQuadratureType interQuad( gridPart, intersection, order, FaceQuadratureType::INSIDE);
            }
          }

          // if only one geometry present we can stop here
          if( singleGeomType )
            return ;
        }
      }

    protected:
      std::shared_ptr< const DiscreteFunctionSpaceType > spc_;
      const std::string passName_;
      mutable double computeTime_;
      mutable size_t numberOfElements_;
      mutable bool passIsActive_;
    };

  } // namespace Fem

} // namespace Dune

#endif // #ifndef DUNE_FEM_PASS_LOCAL_HH
