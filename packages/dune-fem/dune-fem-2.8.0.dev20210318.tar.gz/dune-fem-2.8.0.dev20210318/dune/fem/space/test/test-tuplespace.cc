#include <config.h>

#include <sstream>
#include <string>

#include <dune/grid/io/file/dgfparser/dgfparser.hh>

#include <dune/fem/function/adaptivefunction.hh>
#include <dune/fem/function/common/gridfunctionadapter.hh>
#include <dune/fem/gridpart/leafgridpart.hh>
#include <dune/fem/io/file/vtkio.hh>
#include <dune/fem/misc/mpimanager.hh>
#include <dune/fem/space/lagrange.hh>
#include <dune/fem/space/discontinuousgalerkin.hh>
#include <dune/fem/space/combinedspace.hh>
#include <dune/fem/space/common/interpolate.hh>
#include <dune/fem/test/exactsolution.hh>


// dgfUnitCube
// -----------

inline static std::string dgfUnitCube ( int dimWorld, int cells )
{
  std::string dgf = "DGF\nINTERVAL\n";
  for( int i = 0; i < dimWorld; ++i )
    dgf += " 0";
  dgf += "\n";
  for( int i = 0; i < dimWorld; ++i )
    dgf += " 1";
  dgf += "\n";
  for( int i = 0; i < dimWorld; ++i )
    dgf += (" " + std::to_string( cells ));
  dgf += "\n#\n";
  return dgf;
}



// FunctionSpace
// -------------

template< class GridPart, int dimRange >
using FunctionSpace = Dune::Fem::FunctionSpace< typename GridPart::ctype, double, GridPart::dimensionworld, dimRange >;



// main
// ----

int main ( int argc, char **argv )
{
  Dune::Fem::MPIManager::initialize( argc, argv );

  // construct unit cube
  typedef typename Dune::GridSelector::GridType GridType;
  std::istringstream dgf( dgfUnitCube( GridType::dimensionworld, 4 ) );
  Dune::GridPtr< GridType > grid( dgf );

  // create leaf grid part
  typedef Dune::Fem::LeafGridPart< GridType > GridPartType;
  GridPartType gridPart( *grid );

  using FunctionSpaceType = FunctionSpace< GridPartType, 1 > ;

  // construct FE-DG space
  typedef Dune::Fem::LagrangeDiscreteFunctionSpace< FunctionSpaceType, GridPartType, 1 > ContinuousSpaceType;
  typedef Dune::Fem::DiscontinuousGalerkinSpace< FunctionSpaceType, GridPartType, 0 > DGSpaceType;
  typedef Dune::Fem::EnrichedDiscreteFunctionSpace< DGSpaceType, ContinuousSpaceType > DiscreteFunctionSpaceType;
  DiscreteFunctionSpaceType dfSpace( gridPart );

  // interpolate a function
  Dune::Fem::ExactSolution< FunctionSpaceType > uExact;
  const auto uGridExact = gridFunctionAdapter( "exact solution", uExact, gridPart, 3 );
  Dune::Fem::AdaptiveDiscreteFunction< DiscreteFunctionSpaceType > u( "solution", dfSpace );

  std::cout << "Grid elements " << grid->size( 0 ) << std::endl;
  std::cout << "Grid vertices " << grid->size( GridPartType::dimension ) << std::endl;
  std::cout << "DOFs          " << dfSpace.size() << std::endl;
  interpolate( uGridExact, u );

  Dune::Fem::GlobalRefine::apply( *grid, 2 );

  // output analytical function and interolation to vtk file
  Dune::Fem::VTKIO< GridPartType > vtkIO( gridPart, Dune::VTK::nonconforming );
  vtkIO.addVertexData( uGridExact );
  vtkIO.addVertexData( u );
  vtkIO.write( "test-tuplespace" );

  return 0;
}
