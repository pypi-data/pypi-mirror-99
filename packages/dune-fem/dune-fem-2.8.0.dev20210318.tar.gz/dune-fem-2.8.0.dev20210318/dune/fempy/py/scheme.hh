#ifndef DUNE_FEMPY_PY_SCHEME_HH
#define DUNE_FEMPY_PY_SCHEME_HH

#include <dune/fempy/pybind11/pybind11.hh>

#include <dune/common/typeutilities.hh>

#include <dune/fem/misc/l2norm.hh>
#include <dune/fem/operator/matrix/colcompspmatrix.hh>
#include <dune/fem/solver/parameter.hh>

#include <dune/fempy/function/virtualizedgridfunction.hh>
#include <dune/fempy/parameter.hh>
#include <dune/fempy/py/common/numpyvector.hh>
#include <dune/fempy/py/discretefunction.hh>
#include <dune/fempy/py/space.hh>
#include <dune/fempy/py/operator.hh>
#include <dune/fempy/pybind11/pybind11.hh>

#if 0
     namespace pybind11
     {
       namespace detail
       {
          template <> class type_caster<_p_Mat>
          {
            public:
            PYBIND11_TYPE_CASTER(Mat, _("mat"));
            // Python to C++
            bool load(handle src, bool)
            {
              value = PyPetscMat_Get(src.ptr());
              return true;
            }
            static handle cast(Mat src, pybind11::return_value_policy policy, handle parent)
            {
               return pybind11::handle(PyPetscMat_New(src));
            }
            operator Mat() { return value; }
          };
        }
      }
#endif

namespace Dune
{

  namespace FemPy
  {

    // registerScheme
    // --------------

    namespace detail
    {

      // registerSchemeConstructor
      // -------------------------

      template< class Scheme, class... options >
      inline static auto registerSchemeConstructor ( pybind11::class_< Scheme, options... > cls, PriorityTag< 1 > )
        -> std::enable_if_t< std::is_constructible< Scheme, const typename Scheme::DiscreteFunctionSpaceType &, typename Scheme::ModelType & >::value >
      {
        typedef typename Scheme::DiscreteFunctionSpaceType Space;
        typedef typename Scheme::ModelType ModelType;

        using pybind11::operator""_a;

        cls.def( pybind11::init( [] ( Space &space, ModelType &model ) {
            return new Scheme( space, std::ref(model) );
          } ), "space"_a, "model"_a, pybind11::keep_alive< 1, 2 >(), pybind11::keep_alive< 1, 3 >() );
        cls.def( pybind11::init( [] ( Space &space, ModelType &model, const pybind11::dict &parameters ) {
            return new Scheme( space, std::ref(model),
                pyParameter( "fem.solver.", parameters, std::make_shared< std::string >() ) );
          } ), "space"_a, "model"_a, "parameters"_a, pybind11::keep_alive< 1, 2 >(), pybind11::keep_alive< 1, 3 >() );
      }

      template< class Scheme, class... options >
      inline static void registerSchemeConstructor ( pybind11::class_< Scheme, options... > cls, PriorityTag< 0 > )
      {}

      template< class Scheme, class... options >
      inline static void registerSchemeConstructor ( pybind11::class_< Scheme, options... > cls )
      {
        registerSchemeConstructor( cls, PriorityTag< 42 >() );
      }

      template< class Scheme, class... options, std::enable_if_t<
        std::is_constructible<typename Scheme::LinearInverseOperatorType,const Dune::Fem::ParameterReader&>::value,int > _i=0 >
      inline static void registerInverseLinearOperator ( pybind11::class_< Scheme, options... > cls, PriorityTag< 1 > )
      {
        using pybind11::operator""_a;
        cls.def("inverseLinearOperator",[] (Scheme &self, const pybind11::dict &parameters) {
          return std::make_unique<typename Scheme::LinearInverseOperatorType>
            ( pyParameter( "fem.solver.", parameters, std::make_shared< std::string >() ) );
        }, "parameters"_a );
        cls.def("inverseLinearOperator",[] (Scheme &self, typename Scheme::JacobianOperatorType &jOp, const pybind11::dict &parameters) {
          auto invOp = std::make_unique<typename Scheme::LinearInverseOperatorType>
            ( pyParameter( "fem.solver.", parameters, std::make_shared< std::string >() ) );
          invOp->bind(jOp);
          return invOp;
        }, "jOp"_a, "parameters"_a, pybind11::keep_alive<0,2>(), pybind11::keep_alive<0,3>() );
      }
      template< class Scheme, class... options >
      inline static void registerInverseLinearOperator ( pybind11::class_< Scheme, options... > cls, PriorityTag< 0 > )
      {
      }
      template< class Scheme, class... options >
      inline static void registerInverseLinearOperator ( pybind11::class_< Scheme, options... > cls )
      {
        using pybind11::operator""_a;
        cls.def("inverseLinearOperator",[] (Scheme &self) {
          return std::make_unique<typename Scheme::LinearInverseOperatorType>( );
        } );
        cls.def("inverseLinearOperator",[] (Scheme &self, typename Scheme::JacobianOperatorType &jOp ) {
          auto invOp = std::make_unique<typename Scheme::LinearInverseOperatorType>( );
          invOp->bind(jOp);
          return invOp;
        }, "jOp"_a, pybind11::keep_alive<0,2>() );
        registerInverseLinearOperator( cls, PriorityTag<42>() );
      }

      // registerScheme
      // --------------

      template< class Scheme, class... options >
      inline static void registerScheme ( pybind11::module module, pybind11::class_< Scheme, options... > cls )
      {
        typedef typename Scheme::DiscreteFunctionType DiscreteFunction;

        using pybind11::operator""_a;

        registerSchemeConstructor( cls );

        cls.def( "_solve", [] ( Scheme &self, const DiscreteFunction &rhs, DiscreteFunction &solution ) {
            auto info = self.solve( rhs, solution );
            pybind11::dict ret;
            ret["converged"]  = pybind11::cast(info.converged);
            ret["iterations"] = pybind11::cast(info.nonlinearIterations);
            ret["linear_iterations"] = pybind11::cast(info.linearIterations);
            return ret;
          } );
        cls.def( "_solve", [] ( Scheme &self, DiscreteFunction &solution ) {
            auto info = self.solve( solution );
            pybind11::dict ret;
            ret["converged"]  = pybind11::cast(info.converged);
            ret["iterations"] = pybind11::cast(info.nonlinearIterations);
            ret["linear_iterations"] = pybind11::cast(info.linearIterations);
            return ret;
          } );

        cls.def( "setErrorMeasure", &Scheme::setErrorMeasure,
                 pybind11::keep_alive<1,2>() );

        cls.def_property_readonly( "dimRange", [] ( Scheme & ) -> int { return DiscreteFunction::FunctionSpaceType::dimRange; } );
        cls.def_property_readonly( "space", [] ( pybind11::object self ) { return detail::getSpace( self.cast< const Scheme & >(), self ); } );
        cls.def_property_readonly( "domainSpace", [] ( pybind11::object self ) { return detail::getSpace( self.cast< const Scheme & >(), self ); } );
        cls.def_property_readonly( "rangeSpace", [] ( pybind11::object self ) { return detail::getSpace( self.cast< const Scheme & >(), self ); } );

        auto clsInvOp = Dune::Python::insertClass< typename Scheme::LinearInverseOperatorType >
              ( cls, "LinearInverseOperator", Dune::Python::GenerateTypeName(cls,"LinearInverseOperatorType"));
        if( clsInvOp.second )
        {
          Dune::FemPy::detail::registerBasicOperator(clsInvOp.first);
          clsInvOp.first.def("bind",[] (typename Scheme::LinearInverseOperatorType &self,
                                  typename Scheme::JacobianOperatorType &jOp) {
              self.bind(jOp);
          });
          clsInvOp.first.def_property_readonly("iterations",[]( typename Scheme::LinearInverseOperatorType &self) {
              return self.iterations();
          });
        }
        registerInverseLinearOperator( cls );
        Dune::FemPy::registerOperator(module,cls);
      }

    } // namespace detail

    template< class Scheme, class... options >
    inline static void registerScheme ( pybind11::module module, pybind11::class_< Scheme, options... > cls )
    {
      detail::registerScheme( module, cls );
    }

  } // namespace FemPy

} // namespace Dune

#endif // #ifndef DUNE_FEMPY_PY_SCHEME_HH
