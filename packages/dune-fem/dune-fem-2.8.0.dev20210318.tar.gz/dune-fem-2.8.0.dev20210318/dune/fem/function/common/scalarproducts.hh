#ifndef DUNE_FEM_SCALARPRODURCTS_HH
#define DUNE_FEM_SCALARPRODURCTS_HH

#include <iostream>
#include <memory>
#include <set>
#include <map>
#include <limits>
#include <algorithm>

#include <dune/common/exceptions.hh>
#include <dune/common/genericiterator.hh>
#include <dune/common/ftraits.hh>
#include <dune/common/version.hh>

#include <dune/grid/common/gridenums.hh>
#include <dune/grid/common/datahandleif.hh>

#if HAVE_DUNE_ISTL
#include <dune/istl/scalarproducts.hh>
#endif

#include <dune/fem/common/hybrid.hh>
#include <dune/fem/storage/singletonlist.hh>
#include <dune/fem/misc/mpimanager.hh>
#include <dune/fem/space/common/auxiliarydofs.hh>
#include <dune/fem/space/common/commindexmap.hh>
#include <dune/fem/function/blockvectorfunction/declaration.hh>
#include <dune/fem/function/blockvectors/defaultblockvectors.hh>

namespace Dune
{

  namespace Fem
  {

  /** @addtogroup Communication Communication
      @{
  **/

#if HAVE_DUNE_ISTL
    template <class DofVector>
    struct ISTLScalarProductSelector
    {
      typedef Dune::FieldVector< typename DofVector::FieldType, DofVector::blockSize > Block;
      typedef Dune::BlockVector< Block > type;
    };

    template <class Block>
    struct ISTLScalarProductSelector< Dune::Fem::ISTLBlockVector< Block > >
      : public Dune::ScalarProduct< typename Dune::Fem::ISTLBlockVector< Block > :: DofContainerType >
    {
#if ! DUNE_VERSION_NEWER(DUNE_ISTL, 2, 6)
      //! define the category
      enum { category=Dune::SolverCategory::sequential };
#endif // #if !DUNE_VERSION_NEWER(DUNE_ISTL, 2, 6)

      typedef typename ISTLBlockVector< Block > :: DofContainerType type;

#if DUNE_VERSION_NEWER(DUNE_ISTL, 2, 6)
      Dune::SolverCategory::Category category () const override { return SolverCategory::sequential; }
#endif // #if DUNE_VERSION_NEWER(DUNE_ISTL, 2, 6)
    };
#endif

    //! Proxy class to evaluate ScalarProduct
    //! holding AuxiliaryDofs which is singleton per space and mapper
    template< class DiscreteFunction >
    class ParallelScalarProduct
#if HAVE_DUNE_ISTL
      : public ISTLScalarProductSelector< typename DiscreteFunction :: DofVectorType >
#endif
    {
    public:
      typedef DiscreteFunction DiscreteFunctionType;

      //! type of the discrete function space
      typedef typename DiscreteFunctionType :: DiscreteFunctionSpaceType
        DiscreteFunctionSpaceType;

    private:
      typedef ParallelScalarProduct< DiscreteFunctionType > ThisType;

    public:
      //! type of range field
      typedef typename DiscreteFunctionSpaceType :: RangeFieldType  RangeFieldType;

      //! type of used mapper
      typedef typename DiscreteFunctionSpaceType :: BlockMapperType MapperType;

      // type of communication manager object which does communication
      typedef AuxiliaryDofs< typename DiscreteFunctionSpaceType::GridPartType, MapperType > AuxiliaryDofsType;

      typedef RangeFieldType  field_type;
      typedef typename Dune::FieldTraits< RangeFieldType >::real_type real_type;

      //! constructor taking space
      ParallelScalarProduct ( const DiscreteFunctionSpaceType &space )
      : space_( space )
      {}

      const DiscreteFunctionSpaceType &space() const
      {
        return space_;
      }

      //! evaluate scalar product and omit auxiliary nodes
      template < class OtherDiscreteFunctionType >
      RangeFieldType scalarProductDofs ( const DiscreteFunctionType &x, const OtherDiscreteFunctionType &y ) const
      {
        assert(x.space() == y.space());
        assert(x.space() == space());
        return dotProduct( x.dofVector(), y.dofVector() );
      }

      const AuxiliaryDofsType &auxiliaryDofs() const
      {
        return space().auxiliaryDofs();
      }

    protected:
      //! evaluate scalar product on dofVector and omit auxiliary nodes
      template < class DofVector, class OtherDofVector >
      RangeFieldType dotProduct ( const DofVector &x, const OtherDofVector &y ) const
      {
        typedef typename DiscreteFunctionSpaceType::LocalBlockIndices LocalBlockIndices;

        RangeFieldType scp = 0;
        for( const auto i : primaryDofs( space().auxiliaryDofs() ) )
          Hybrid::forEach( LocalBlockIndices(), [ &x, &y, &scp, i ] ( auto &&j ) { scp += x[ i ][ j ] * y[ i ][ j ]; } );
        return space().gridPart().comm().sum( scp );
      }

#if HAVE_DUNE_ISTL
    protected:
      typedef typename ISTLScalarProductSelector< typename DiscreteFunction :: DofVectorType > :: type BlockVectorType;

    public:
      //! dot product for ISTL solvers
      virtual field_type dot (const BlockVectorType& x,
                              const BlockVectorType& y) const
      {
        return dotProduct( x, y );
      }

      //! norm for ISTL solvers
      virtual real_type norm( const BlockVectorType& x ) const
      {
        return std::abs( std::sqrt( dotProduct( x, x ) ) );
      }

      //! delete auxiliary values (for debugging)
      void deleteNonInterior( BlockVectorType& x) const
      {
#if HAVE_MPI
        // case of ALUGrid and DGSpace or FVSpace
        // BUG: We should not use the leafGridView to detect whether the grid has overlap!
        const bool deleteGhostEntries = (space().gridPart().grid().leafGridView().overlapSize( 0 ) == 0) && !space().continuous();

        // only delete ghost entries
        if( deleteGhostEntries )
        {
          const auto &auxiliaryDofs = space().auxiliaryDofs();

          // don't delete the last since this is the overall Size
          const int auxiliarySize = auxiliaryDofs.size() - 1;
          for(int auxiliary = 0; auxiliary<auxiliarySize; ++auxiliary)
            x[ auxiliaryDofs[auxiliary] ] = 0;
        }
#endif // #if HAVE_MPI
      }
#endif // #if HAVE_DUNE_ISTL
      const DiscreteFunctionSpaceType &space_;
    };

  //@}

  } // end namespace Fem

} // end namespace Dune
#endif // #ifndef DUNE_FEM_SCALARPRODURCTS_HH
