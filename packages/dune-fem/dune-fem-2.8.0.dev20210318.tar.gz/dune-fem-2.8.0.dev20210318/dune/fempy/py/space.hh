#ifndef DUNE_FEMPY_PY_SPACE_HH
#define DUNE_FEMPY_PY_SPACE_HH

#include <dune/common/hybridutilities.hh>

#include <dune/fem/space/basisfunctionset/codegen.hh>

#include <dune/python/common/dynmatrix.hh>
#include <dune/python/common/dynvector.hh>
#include <dune/python/common/fmatrix.hh>
#include <dune/python/common/fvector.hh>

#include <dune/fempy/pybind11/pybind11.hh>
#include <dune/fempy/py/grid/gridpart.hh>

namespace Dune
{

  namespace FemPy
  {

    namespace detail
    {

      // registerSpaceConstructor
      // -------------------------
      template< class Space, class... options >
      void registerSpaceConstructor ( pybind11::class_< Space, options... > cls, std::false_type )
      {}
      template< class Space, class... options >
      void registerSpaceConstructor ( pybind11::class_< Space, options... > cls, std::true_type )
      {
        using pybind11::operator""_a;

        typedef typename Space::GridPartType GridPart;
        typedef typename GridPart::GridViewType GridView;

        cls.def( pybind11::init( [] ( const GridView &gridView ) {
            return new Space( gridPart< GridView >( gridView ) );
          } ), pybind11::keep_alive< 1, 2 >(), "gridView"_a );
      }
      template< class Space, class... options >
      void registerSpaceConstructorWithOrder ( pybind11::class_< Space, options... > cls, std::false_type )
      {}
      template< class Space, class... options >
      void registerSpaceConstructorWithOrder ( pybind11::class_< Space, options... > cls, std::true_type )
      {
        using pybind11::operator""_a;

        typedef typename Space::GridPartType GridPart;
        typedef typename GridPart::GridViewType GridView;

        cls.def( pybind11::init( [] ( const GridView &gridView, int order ) {
            return new Space( gridPart< GridView >( gridView ), order );
          } ), pybind11::keep_alive< 1, 2 >(), "gridView"_a, "order"_a );
      }
      template< class Space, class... options >
      void registerSpaceConstructor ( pybind11::class_< Space, options... > cls )
      {
        typedef typename Space::GridPartType GridPart;
        registerSpaceConstructor( cls, std::is_constructible< Space, GridPart& >() );
        registerSpaceConstructorWithOrder( cls, std::is_constructible< Space, GridPart&, int >() );
      }

      template< class Space, class... options >
      inline static auto registerSubSpace ( pybind11::class_< Space, options... > cls, PriorityTag< 1 > )
        -> std::enable_if_t< std::is_same< const typename Space::template SubDiscreteFunctionSpace< 0 >::Type&, decltype( std::declval< Space & >().template subDiscreteFunctionSpace< 0 >() ) >::value >
      {
        cls.def_property_readonly( "components", [] ( pybind11::object self ) -> pybind11::tuple {
            Space &space = pybind11::cast< Space & >( self );
            pybind11::tuple components( Space::Sequence::size() );
            Hybrid::forEach( typename Space::Sequence(), [ self, &space, &components ] ( auto i ) {
                assert( pybind11::already_registered< typename Space::template SubDiscreteFunctionSpace< i.value >::Type > );
                pybind11::object subSpace = pybind11::cast( &space.template subDiscreteFunctionSpace< i.value >(), pybind11::return_value_policy::reference_internal, self );
                if( subSpace )
                  components[ i.value ] = subSpace;
                else
                  throw pybind11::error_already_set();
              } );
            return components;
          } );
      }
      template< class Space, class... options >
      inline static void registerSubSpace ( pybind11::class_< Space, options... > cls, PriorityTag< 0 > )
      {}

      template< class Space, class... options >
      inline static void registerSubSpace ( pybind11::class_< Space, options... > cls )
      {
        registerSubSpace( cls, PriorityTag< 42 >() );
      }
      // registerSpace
      // -------------

      template< class Space, class... options >
      void registerFunctionSpace ( pybind11::handle module, pybind11::class_< Space, options... > cls )
      {
        typedef typename Space::GridPartType GridPart;
        typedef typename GridPart::GridViewType GridView;
        cls.def_property_readonly( "dimRange", [] ( Space & ) -> int { return Space::dimRange; } );
        cls.def_property_readonly( "dimDomain", [] ( Space & ) -> int { return Space::FunctionSpaceType::dimDomain; } );
        cls.def_property_readonly( "grid", [] ( Space &self ) -> GridView { return static_cast< GridView >( self.gridPart() ); } );
        cls.def_property_readonly( "order", [] ( Space &self ) -> int { return self.order(); } );
      }

      template< class Space, class... options >
      void registerSpace ( pybind11::handle module, pybind11::class_< Space, options... > cls )
      {
        registerFunctionSpace(module,cls);
        cls.def_property_readonly( "size", [] ( Space &self ) -> int { return self.size(); } );
        cls.def_property_readonly( "localBlockSize", [] ( Space &spc ) -> unsigned int { return spc.localBlockSize; } );
        cls.def("localOrder", [] ( Space &self, typename Space::EntityType &e) -> int { return self.order(e); } );
        cls.def("map", [] ( Space &spc, typename Space::EntityType &e) -> std::vector<unsigned int>
            { std::vector<unsigned int> idx(spc.blockMapper().numDofs(e));
              spc.blockMapper().mapEach(e, Fem::AssignFunctor< std::vector< unsigned int > >( idx ) );
              return idx;
            } );

        registerSpaceConstructor( cls );
        registerSubSpace( cls );

        cls.def( "as_ufl", [] ( pybind11::object &self ) -> pybind11::handle {
              pybind11::tuple args( 1 );
              args[ 0 ] = self;
              pybind11::handle res = PyObject_Call( Dune::FemPy::getSpaceWrapper().ptr(), args.ptr(), nullptr );
              return res;
            },  pybind11::keep_alive< 0, 1 >() );

        cls.def( "_generateQuadratureCode", []( Space &self,
                 const std::vector<unsigned int> &interiorOrders,
                 const std::vector<unsigned int> &skeletonOrders,
                 const std::string &path,
                 const std::string &filename)
            {
              std::cout << "Generate code to " << filename << std::endl;
              Dune::Fem::generateCode(self, interiorOrders, skeletonOrders, path, filename);
            } );
      }



      // getSpace
      // --------

      template< class T, class Space >
      pybind11::object getSpaceObject ( const T &obj, pybind11::handle parent, const Space &space )
      {
        pybind11::object pySpace = pybind11::reinterpret_borrow< pybind11::object >( pybind11::detail::get_object_handle( &space, pybind11::detail::get_type_info( typeid( Space ) ) ) );
        if( !pySpace )
        {
          if( !parent )
            parent = pybind11::detail::get_object_handle( &obj, pybind11::detail::get_type_info( typeid( T ) ) );
          pySpace = pybind11::cast( space, pybind11::return_value_policy::reference_internal, parent );
        }
        return pySpace;
      }
      template< class T >
      pybind11::object getSpace ( const T &obj, pybind11::handle parent = pybind11::handle() )
      {
        typedef std::decay_t< decltype( std::declval< const T & >().space() ) > Space;
        const Space &space = obj.space();
        return getSpaceObject(obj, parent, space);
      }

    } // namespace detail



    // registerSpace
    // -------------

    template< class Space, class... options >
    void registerSpace ( pybind11::handle module, pybind11::class_< Space, options... > cls )
    {
      detail::registerSpace( module, cls );
    }
  } // namespace FemPy

} // namespace Dune

#endif // #ifndef DUNE_FEMPY_PY_SPACE_HH
