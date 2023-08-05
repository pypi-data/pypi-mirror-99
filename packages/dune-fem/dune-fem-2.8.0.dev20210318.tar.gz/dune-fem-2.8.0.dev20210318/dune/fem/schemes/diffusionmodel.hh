#ifndef ELLIPTC_MODEL_HH
#define ELLIPTC_MODEL_HH

#include <cassert>
#include <cmath>

#include <dune/common/visibility.hh>

#include <dune/fem/solver/timeprovider.hh>
#include <dune/fem/io/parameter.hh>
#include <dune/fem/space/common/functionspace.hh>
#include <dune/fem/function/common/gridfunctionadapter.hh>
#include <dune/fem/quadrature/cachingquadrature.hh>
#include <dune/fempy/quadrature/fempyquadratures.hh>

#define VirtualDiffusionModelMethods(POINT) \
  virtual void source ( const POINT &x,\
                const DRangeType &value,\
                const DJacobianRangeType &gradient,\
                RRangeType &flux ) const = 0;\
  virtual void linSource ( const DRangeType& uBar,\
                   const DJacobianRangeType &gradientBar,\
                   const POINT &x,\
                   const DRangeType &value,\
                   const DJacobianRangeType &gradient,\
                   RRangeType &flux ) const = 0;\
  virtual void diffusiveFlux ( const POINT &x,\
                       const DRangeType &value,\
                       const DJacobianRangeType &gradient,\
                       RJacobianRangeType &flux ) const = 0;\
  virtual void linDiffusiveFlux ( const DRangeType& uBar,\
                          const DJacobianRangeType& gradientBar,\
                          const POINT &x,\
                          const DRangeType &value,\
                          const DJacobianRangeType &gradient,\
                          RJacobianRangeType &flux ) const = 0;\
  virtual void fluxDivergence( const POINT &x,\
                         const DRangeType &value,\
                         const DJacobianRangeType &jacobian,\
                         const DHessianRangeType &hessian,\
                         RRangeType &flux) const = 0;\
  virtual void alpha(const POINT &x,\
             const DRangeType &value,\
             RRangeType &val) const = 0;\
  virtual void linAlpha(const DRangeType &uBar,\
                const POINT &x,\
                const DRangeType &value,\
                RRangeType &val) const = 0;\
  virtual void dirichlet( int bndId, const POINT &x,\
                RRangeType &value) const = 0;

#define WrapperDiffusionModelMethods(POINT) \
  virtual void source ( const POINT &x,\
                const DRangeType &value,\
                const DJacobianRangeType &gradient,\
                RRangeType &flux ) const \
  { impl().source(x, value, gradient, flux); } \
  virtual void linSource ( const DRangeType& uBar,\
                   const DJacobianRangeType &gradientBar,\
                   const POINT &x,\
                   const DRangeType &value,\
                   const DJacobianRangeType &gradient,\
                   RRangeType &flux ) const \
  { impl().linSource(uBar, gradientBar, x, value, gradient, flux); } \
  virtual void diffusiveFlux ( const POINT &x,\
                       const DRangeType &value,\
                       const DJacobianRangeType &gradient,\
                       RJacobianRangeType &flux ) const \
  { impl().diffusiveFlux(x, value, gradient, flux); } \
  virtual void linDiffusiveFlux ( const DRangeType& uBar,\
                          const DJacobianRangeType& gradientBar,\
                          const POINT &x,\
                          const DRangeType &value,\
                          const DJacobianRangeType &gradient,\
                          RJacobianRangeType &flux ) const \
  { impl().linDiffusiveFlux(uBar, gradientBar, x, value, gradient, flux); } \
  virtual void fluxDivergence( const POINT &x,\
                         const DRangeType &value,\
                         const DJacobianRangeType &jacobian,\
                         const DHessianRangeType &hessian,\
                         RRangeType &flux) const \
  { impl().fluxDivergence(x, value, jacobian, hessian, flux); } \
  virtual void alpha(const POINT &x,\
             const DRangeType &value,\
             RRangeType &val) const \
  { impl().alpha(x, value, val); } \
  virtual void linAlpha(const DRangeType &uBar,\
                const POINT &x,\
                const DRangeType &value,\
                RRangeType &val) const \
  { impl().linAlpha(uBar, x, value, val); } \
  virtual void dirichlet( int bndId, const POINT &x,\
                RRangeType &value) const \
  { impl().dirichlet(bndId, x, value); }

template< class GridPart, int dimDomain, int dimRange=dimDomain, class RangeField = double >
struct DiffusionModel
{
  typedef GridPart GridPartType;
  static const int dimD = dimDomain;
  static const int dimR = dimRange;
  typedef DiffusionModel<GridPartType, dimD, dimR, RangeField> ModelType;
  typedef RangeField RangeFieldType;

  typedef Dune::Fem::FunctionSpace< double, RangeFieldType,
              GridPart::dimensionworld, dimD > DFunctionSpaceType;
  typedef Dune::Fem::FunctionSpace< double, RangeFieldType,
              GridPart::dimensionworld, dimR > RFunctionSpaceType;
  typedef typename DFunctionSpaceType::DomainType DomainType;
  typedef typename DFunctionSpaceType::RangeType DRangeType;
  typedef typename DFunctionSpaceType::JacobianRangeType DJacobianRangeType;
  typedef typename DFunctionSpaceType::HessianRangeType DHessianRangeType;
  typedef typename DFunctionSpaceType::DomainFieldType DDomainFieldType;
  typedef typename RFunctionSpaceType::RangeType RRangeType;
  typedef typename RFunctionSpaceType::JacobianRangeType RJacobianRangeType;
  typedef typename RFunctionSpaceType::HessianRangeType RHessianRangeType;
  typedef typename RFunctionSpaceType::DomainFieldType rDomainFieldType;

  typedef typename GridPartType::template Codim<0>::EntityType EntityType;
  typedef typename GridPartType::IntersectionType IntersectionType;
  typedef typename EntityType::Geometry::LocalCoordinate LocalDomainType;

  // quadrature points from dune-fempy quadratures
  template <class F,int d>
  using Traits = Dune::FemPy::FempyQuadratureTraits<F,d>;
  typedef typename Dune::Fem::CachingQuadrature< GridPartType, 0, Traits >::
                   QuadraturePointWrapperType Point;
  typedef typename Dune::Fem::CachingQuadrature< GridPartType, 1, Traits >::
                   QuadraturePointWrapperType IntersectionPoint;
  typedef typename Dune::Fem::ElementQuadrature< GridPartType, 0, Traits >::
                   QuadraturePointWrapperType ElementPoint;
  typedef typename Dune::Fem::ElementQuadrature< GridPartType, 1, Traits >::
                   QuadraturePointWrapperType ElementIntersectionPoint;

  // quadrature points from dune-fem quadratures
  typedef typename Dune::Fem::CachingQuadrature< GridPartType, 0 >::
                   QuadraturePointWrapperType OriginalPoint;
  typedef typename Dune::Fem::CachingQuadrature< GridPartType, 1 >::
                   QuadraturePointWrapperType OriginalIntersectionPoint;
  typedef typename Dune::Fem::ElementQuadrature< GridPartType, 0 >::
                   QuadraturePointWrapperType OriginalElementPoint;
  typedef typename Dune::Fem::ElementQuadrature< GridPartType, 1 >::
                   QuadraturePointWrapperType OriginalElementIntersectionPoint;

  /*
  static const bool isLinear;
  static const bool isSymmetric;
  */

public:
  DiffusionModel( )
  { }
  virtual ~DiffusionModel() {}

  virtual std::string name() const = 0;

  virtual bool init( const EntityType &entity) const = 0;

  // if the ModelImpl provides a time method (constant) then
  // it maybe be set using this method
  virtual void setTime( const double t ) const = 0;

  // if the ModelImpl provides a 'double& time()' method then
  // it maybe retrieved by this method
  virtual double time() const = 0;

  // virtual methods for fempy quadratures
  VirtualDiffusionModelMethods(Point)
  VirtualDiffusionModelMethods(ElementPoint)
  VirtualDiffusionModelMethods(IntersectionPoint)
  VirtualDiffusionModelMethods(ElementIntersectionPoint)

  // virtual methods for fem quadratures
  VirtualDiffusionModelMethods(OriginalPoint)
  VirtualDiffusionModelMethods(OriginalElementPoint)
  VirtualDiffusionModelMethods(OriginalIntersectionPoint)
  VirtualDiffusionModelMethods(OriginalElementIntersectionPoint)

  VirtualDiffusionModelMethods(LocalDomainType)

  typedef Dune::FieldVector<int, dimRange> DirichletComponentType;
  virtual bool hasDirichletBoundary () const = 0;
  virtual bool hasNeumanBoundary () const = 0;
  virtual bool isDirichletIntersection( const IntersectionType& inter, DirichletComponentType &dirichletComponent ) const = 0;
};

namespace detail {

  template <class M>
  class CheckTimeMethod
  {
      template <class T>
      static std::true_type testSignature(double& (T::*)());

      template <class T>
      static decltype(testSignature(&T::time)) test(std::nullptr_t);

      template <class T>
      static std::false_type test(...);

      using type = decltype(test<M>(nullptr));
  public:
      static const bool value = type::value;
  };


  template <class Model, bool>
  struct CallSetTime
  {
    static void setTime( Model&, const double ) {}
    static double time( const Model& ) { return -1.0; }
  };

  template <class Model>
  struct CallSetTime< Model, true >
  {
    static void setTime( Model& model, const double t ) { model.time() = t; }
    static double time ( const Model& model ) { return model.time(); }
  };
} // end namespace detail


template < class ModelImpl >
struct DiffusionModelWrapper : public DiffusionModel<typename ModelImpl::GridPartType, ModelImpl::dimD, ModelImpl::dimR,
                                      typename ModelImpl::RRangeFieldType>
{
  typedef ModelImpl Impl;
  typedef typename ModelImpl::GridPartType GridPartType;
  static const int dimD  = ModelImpl::dimD;
  static const int dimR  = ModelImpl::dimR;
  typedef DiffusionModel<GridPartType, dimD, dimR, typename ModelImpl::RRangeFieldType> Base;

  typedef typename Base::Point Point;
  typedef typename Base::IntersectionPoint IntersectionPoint;
  typedef typename Base::ElementPoint ElementPoint;
  typedef typename Base::ElementIntersectionPoint ElementIntersectionPoint;
  typedef typename Base::OriginalPoint OriginalPoint;
  typedef typename Base::OriginalIntersectionPoint OriginalIntersectionPoint;
  typedef typename Base::OriginalElementPoint      OriginalElementPoint;
  typedef typename Base::OriginalElementIntersectionPoint OriginalElementIntersectionPoint;
  typedef typename Base::LocalDomainType LocalDomainType;
  typedef typename Base::DomainType DomainType;
  typedef typename Base::DRangeType DRangeType;
  typedef typename Base::DJacobianRangeType DJacobianRangeType;
  typedef typename Base::DHessianRangeType DHessianRangeType;
  typedef typename Base::RRangeType RRangeType;
  typedef typename Base::RJacobianRangeType RJacobianRangeType;
  typedef typename Base::RHessianRangeType RHessianRangeType;
  typedef typename Base::EntityType EntityType;
  typedef typename Base::IntersectionType IntersectionType;

  template< class... Args, std::enable_if_t< std::is_constructible< ModelImpl, Args &&... >::value, int > = 0 >
  explicit DiffusionModelWrapper ( Args &&... args )
    : impl_( std::forward< Args >( args )... )
  {}

  ~DiffusionModelWrapper()
  {
  }

  // virtual methods for fempy quadratures
  WrapperDiffusionModelMethods(Point);
  WrapperDiffusionModelMethods(ElementPoint);
  WrapperDiffusionModelMethods(IntersectionPoint);
  WrapperDiffusionModelMethods(ElementIntersectionPoint);

  // virtual methods for fem quadratures
  WrapperDiffusionModelMethods(OriginalPoint);
  WrapperDiffusionModelMethods(OriginalElementPoint);
  WrapperDiffusionModelMethods(OriginalIntersectionPoint);
  WrapperDiffusionModelMethods(OriginalElementIntersectionPoint);

  WrapperDiffusionModelMethods(LocalDomainType);

  // other virtual functions
  virtual std::string name() const
  {
    return impl().name();
  }

  // if the ModelImpl provides a 'double& time()' method then
  // it maybe be set using this method
  virtual void setTime( const double t ) const
  {
    detail::CallSetTime< ModelImpl, detail::CheckTimeMethod< ModelImpl >::value >
      ::setTime( const_cast< ModelImpl& > (impl()), t );
  }

  // if the ModelImpl provides a 'double& time()' method then
  // it maybe be set using this method
  virtual double time() const
  {
    return detail::CallSetTime< ModelImpl, detail::CheckTimeMethod< ModelImpl >::value >::time( impl() );
  }

  typedef Dune::FieldVector<int, dimR> DirichletComponentType;
  virtual bool hasDirichletBoundary () const
  {
    return impl().hasDirichletBoundary();
  }
  virtual bool hasNeumanBoundary () const
  {
    return impl().hasNeumanBoundary();
  }
  virtual bool isDirichletIntersection( const IntersectionType& inter, DirichletComponentType &dirichletComponent ) const
  {
    return impl().isDirichletIntersection(inter, dirichletComponent);
  }
  virtual bool init( const EntityType &entity) const
  {
    return impl().init(entity);
  }
  const ModelImpl &impl() const
  {
    return impl_;
  }
  ModelImpl &impl()
  {
    return impl_;
  }
  private:
  ModelImpl impl_;
};

#define VirtualPenaltyMethods(POINT) \
  virtual RRangeType penalty ( const POINT &x,\
                const DRangeType &value ) const = 0;\
  virtual RRangeType linPenalty ( const POINT &x,\
                   const DRangeType &value ) const = 0;
#define WrapperPenaltyMethods(POINT) \
  virtual RRangeType penalty ( const POINT &x,\
                const DRangeType &value ) const \
  { return impl().penalty(x, value); } \
  virtual RRangeType linPenalty ( const POINT &x,\
                   const DRangeType &value ) const \
  { return impl().linPenalty( x, value); }

template< class GridPart, int dimDomain, int dimRange=dimDomain, class RangeField = double >
struct DGDiffusionModel
{
  typedef GridPart GridPartType;
  static const int dimD = dimDomain;
  static const int dimR = dimRange;
  typedef DGDiffusionModel<GridPartType, dimD, dimR, RangeField> ModelType;
  typedef RangeField RangeFieldType;

  typedef Dune::Fem::FunctionSpace< double, RangeFieldType,
              GridPart::dimensionworld, dimD > DFunctionSpaceType;
  typedef Dune::Fem::FunctionSpace< double, RangeFieldType,
              GridPart::dimensionworld, dimR > RFunctionSpaceType;
  typedef typename DFunctionSpaceType::DomainType DomainType;
  typedef typename DFunctionSpaceType::RangeType DRangeType;
  typedef typename DFunctionSpaceType::JacobianRangeType DJacobianRangeType;
  typedef typename DFunctionSpaceType::HessianRangeType DHessianRangeType;
  typedef typename DFunctionSpaceType::DomainFieldType DDomainFieldType;
  typedef typename RFunctionSpaceType::RangeType RRangeType;
  typedef typename RFunctionSpaceType::JacobianRangeType RJacobianRangeType;
  typedef typename RFunctionSpaceType::HessianRangeType RHessianRangeType;
  typedef typename RFunctionSpaceType::DomainFieldType rDomainFieldType;

  typedef typename GridPartType::template Codim<0>::EntityType EntityType;
  typedef typename GridPartType::IntersectionType IntersectionType;
  typedef typename EntityType::Geometry::LocalCoordinate LocalDomainType;

  // quadrature points from dune-fempy quadratures
  template <class F,int d>
  using Traits = Dune::FemPy::FempyQuadratureTraits<F,d>;
  typedef typename Dune::Fem::CachingQuadrature< GridPartType, 0, Traits >::
                   QuadraturePointWrapperType Point;
  typedef typename Dune::Fem::CachingQuadrature< GridPartType, 1, Traits >::
                   QuadraturePointWrapperType IntersectionPoint;
  typedef typename Dune::Fem::ElementQuadrature< GridPartType, 0, Traits >::
                   QuadraturePointWrapperType ElementPoint;
  typedef typename Dune::Fem::ElementQuadrature< GridPartType, 1, Traits >::
                   QuadraturePointWrapperType ElementIntersectionPoint;

  // quadrature points from dune-fem quadratures
  typedef typename Dune::Fem::CachingQuadrature< GridPartType, 0 >::
                   QuadraturePointWrapperType OriginalPoint;
  typedef typename Dune::Fem::CachingQuadrature< GridPartType, 1 >::
                   QuadraturePointWrapperType OriginalIntersectionPoint;
  typedef typename Dune::Fem::ElementQuadrature< GridPartType, 0 >::
                   QuadraturePointWrapperType OriginalElementPoint;
  typedef typename Dune::Fem::ElementQuadrature< GridPartType, 1 >::
                   QuadraturePointWrapperType OriginalElementIntersectionPoint;

  /*
  static const bool isLinear;
  static const bool isSymmetric;
  */

public:
  DGDiffusionModel( )
  { }
  virtual ~DGDiffusionModel() {}

  virtual std::string name() const = 0;

  virtual bool init( const EntityType &entity) const = 0;

  // if the ModelImpl provides a 'double& time()' method then
  // it maybe be set using this method
  virtual void setTime( const double t ) const = 0;

  // if the ModelImpl provides a 'double& time()' method then
  // it maybe retrieved by this method
  virtual double time() const = 0;

  // virtual methods for fempy quadratures
  VirtualDiffusionModelMethods(Point)
  VirtualDiffusionModelMethods(ElementPoint)
  VirtualDiffusionModelMethods(IntersectionPoint)
  VirtualDiffusionModelMethods(ElementIntersectionPoint)

  // virtual methods for fem quadratures
  VirtualDiffusionModelMethods(OriginalPoint)
  VirtualDiffusionModelMethods(OriginalElementPoint)
  VirtualDiffusionModelMethods(OriginalIntersectionPoint)
  VirtualDiffusionModelMethods(OriginalElementIntersectionPoint)

  VirtualDiffusionModelMethods(LocalDomainType)

  typedef Dune::FieldVector<int, dimRange> DirichletComponentType;
  virtual bool hasDirichletBoundary () const = 0;
  virtual bool hasNeumanBoundary () const = 0;
  virtual bool isDirichletIntersection( const IntersectionType& inter, DirichletComponentType &dirichletComponent ) const = 0;

  VirtualPenaltyMethods(Point)
  VirtualPenaltyMethods(ElementPoint)
  VirtualPenaltyMethods(IntersectionPoint)
  VirtualPenaltyMethods(ElementIntersectionPoint)

  // virtual methods for fem quadratures
  VirtualPenaltyMethods(OriginalPoint)
  VirtualPenaltyMethods(OriginalElementPoint)
  VirtualPenaltyMethods(OriginalIntersectionPoint)
  VirtualPenaltyMethods(OriginalElementIntersectionPoint)

  VirtualPenaltyMethods(LocalDomainType)

};

template < class ModelImpl >
struct DGDiffusionModelWrapper : public DGDiffusionModel<typename ModelImpl::GridPartType, ModelImpl::dimD, ModelImpl::dimR,
                                        typename ModelImpl::RRangeFieldType>
{
  typedef ModelImpl Impl;
  typedef typename ModelImpl::GridPartType GridPartType;
  static const int dimD  = ModelImpl::dimD;
  static const int dimR  = ModelImpl::dimR;
  typedef DGDiffusionModel<GridPartType, dimD, dimR, typename ModelImpl::RRangeFieldType> Base;

  typedef typename Base::Point Point;
  typedef typename Base::IntersectionPoint IntersectionPoint;
  typedef typename Base::ElementPoint ElementPoint;
  typedef typename Base::ElementIntersectionPoint ElementIntersectionPoint;
  typedef typename Base::OriginalPoint OriginalPoint;
  typedef typename Base::OriginalIntersectionPoint OriginalIntersectionPoint;
  typedef typename Base::OriginalElementPoint      OriginalElementPoint;
  typedef typename Base::OriginalElementIntersectionPoint OriginalElementIntersectionPoint;
  typedef typename Base::LocalDomainType LocalDomainType;
  typedef typename Base::DomainType DomainType;
  typedef typename Base::DRangeType DRangeType;
  typedef typename Base::DJacobianRangeType DJacobianRangeType;
  typedef typename Base::DHessianRangeType DHessianRangeType;
  typedef typename Base::RRangeType RRangeType;
  typedef typename Base::RJacobianRangeType RJacobianRangeType;
  typedef typename Base::RHessianRangeType RHessianRangeType;
  typedef typename Base::EntityType EntityType;
  typedef typename Base::IntersectionType IntersectionType;

  template< class... Args, std::enable_if_t< std::is_constructible< ModelImpl, Args &&... >::value, int > = 0 >
  explicit DGDiffusionModelWrapper ( Args &&... args )
    : impl_( std::forward< Args >( args )... )
  {}

  ~DGDiffusionModelWrapper()
  {
  }

  // virtual methods for fempy quadratures
  WrapperDiffusionModelMethods(Point);
  WrapperDiffusionModelMethods(ElementPoint);
  WrapperDiffusionModelMethods(IntersectionPoint);
  WrapperDiffusionModelMethods(ElementIntersectionPoint);

  // virtual methods for fem quadratures
  WrapperDiffusionModelMethods(OriginalPoint);
  WrapperDiffusionModelMethods(OriginalElementPoint);
  WrapperDiffusionModelMethods(OriginalIntersectionPoint);
  WrapperDiffusionModelMethods(OriginalElementIntersectionPoint);

  WrapperDiffusionModelMethods(LocalDomainType);

  WrapperPenaltyMethods(Point)
  WrapperPenaltyMethods(ElementPoint)
  WrapperPenaltyMethods(IntersectionPoint)
  WrapperPenaltyMethods(ElementIntersectionPoint)

  // virtual methods for fem quadratures
  WrapperPenaltyMethods(OriginalPoint);
  WrapperPenaltyMethods(OriginalElementPoint);
  WrapperPenaltyMethods(OriginalIntersectionPoint);
  WrapperPenaltyMethods(OriginalElementIntersectionPoint);

  WrapperPenaltyMethods(LocalDomainType);
  // other virtual functions
  virtual std::string name() const
  {
    return impl().name();
  }

  // if the ModelImpl provides a 'double& time()' method then
  // it maybe be set using this method
  virtual void setTime( const double t ) const
  {
    detail::CallSetTime< ModelImpl, detail::CheckTimeMethod< ModelImpl >::value >
      ::setTime( const_cast< ModelImpl& > (impl()), t );
  }

  // if the ModelImpl provides a 'double& time()' method then
  // it maybe be set using this method
  virtual double time() const
  {
    return detail::CallSetTime< ModelImpl, detail::CheckTimeMethod< ModelImpl >::value >::time( impl() );
  }

  typedef Dune::FieldVector<int, dimR> DirichletComponentType;
  virtual bool hasDirichletBoundary () const
  {
    return impl().hasDirichletBoundary();
  }
  virtual bool hasNeumanBoundary () const
  {
    return impl().hasNeumanBoundary();
  }
  virtual bool isDirichletIntersection( const IntersectionType& inter, DirichletComponentType &dirichletComponent ) const
  {
    return impl().isDirichletIntersection(inter, dirichletComponent);
  }
  virtual bool init( const EntityType &entity) const
  {
    return impl().init(entity);
  }
  const ModelImpl &impl() const
  {
    return impl_;
  }
  ModelImpl &impl()
  {
    return impl_;
  }
  private:
  ModelImpl impl_;
};

#if 0 // doesn't seem to be used anymore - needs checking
template < class ModelTraits >
struct DiffusionModelEngine : public DiffusionModel<typename ModelTraits::GridPartType, ModelTraits::dimD, ModelTraits::dimR, typename ModelTraits::RRangeFieldType>
{
  typedef typename ModelTraits::GridPartType GridPartType;
  static const int dimD  = ModelTraits::dimD;
  static const int dimR  = ModelTraits::dimR;
  typedef DiffusionModel<GridPartType, dimD, dimR> Base;

  typedef typename Base::Point Point;
  typedef typename Base::IntersectionPoint IntersectionPoint;
  typedef typename Base::ElementPoint ElementPoint;
  typedef typename Base::ElementIntersectionPoint ElementIntersectionPoint;
  typedef typename Base::LocalDomainType LocalDomainType;
  typedef typename Base::DomainType DomainType;
  typedef typename Base::DRangeType DRangeType;
  typedef typename Base::DJacobianRangeType DJacobianRangeType;
  typedef typename Base::DHessianRangeType DHessianRangeType;
  typedef typename Base::RRangeType RRangeType;
  typedef typename Base::RJacobianRangeType RJacobianRangeType;
  typedef typename Base::RHessianRangeType RHessianRangeType;
  typedef typename Base::EntityType EntityType;
  typedef typename Base::IntersectionType IntersectionType;

  typedef typename ModelTraits::ModelType ModelImpl;

  DiffusionModelEngine(ModelImpl &model) : impl_(model) {}
  ~DiffusionModelEngine()
  {
  }

  WrapperDiffusionModelMethods(Point);
  WrapperDiffusionModelMethods(ElementPoint);
  WrapperDiffusionModelMethods(IntersectionPoint);
  WrapperDiffusionModelMethods(ElementIntersectionPoint);
  WrapperDiffusionModelMethods(LocalDomainType);

  // other virtual functions
  virtual std::string name() const
  {
    return impl().name();
  }
  virtual bool hasDirichletBoundary () const
  {
    return impl().hasDirichletBoundary();
  }
  virtual bool hasNeumanBoundary () const
  {
    return impl().hasNeumanBoundary();
  }
  virtual bool isDirichletIntersection( const IntersectionType& inter, Dune::FieldVector<int, dimR> &dirichletComponent ) const
  {
    return impl().isDirichletIntersection(inter, dirichletComponent);
  }
  virtual bool init( const EntityType &entity) const
  {
    return impl().init(entity);
  }
  const ModelImpl &impl() const
  {
    return impl_;
  }
  ModelImpl &impl()
  {
    return impl_;
  }
  private:
  ModelImpl &impl_;
};
#endif

#endif // #ifndef ELLIPTC_MODEL_HH
