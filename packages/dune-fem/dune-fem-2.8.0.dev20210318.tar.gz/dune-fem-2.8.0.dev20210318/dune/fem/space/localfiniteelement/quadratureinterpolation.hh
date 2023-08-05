#ifndef DUNE_LOBATTOBASIS_HH
#define DUNE_LOBATTOBASIS_HH

#include <fstream>

#include <dune/geometry/type.hh>
#include <dune/geometry/topologyfactory.hh>
#include <dune/geometry/quadraturerules.hh>
#include <dune/geometry/referenceelements.hh>

#include <dune/fem/common/forloop.hh>

#if HAVE_DUNE_LOCALFUNCTIONS
#include <dune/localfunctions/utility/field.hh>
#include <dune/localfunctions/lagrange/lagrangecoefficients.hh>
#include <dune/localfunctions/lagrange/emptypoints.hh>
#include <dune/localfunctions/lagrange/equidistantpoints.hh>


namespace Dune
{
  namespace Impl
  {
    template <class Field>
    struct Builder
    {
      template <class Points1DType>
      static int size(GeometryType gt, const Points1DType &points1D)
      {
        if (gt.dim()==0) return 1;
        else if (Impl::isTopology(Impl::prismConstruction,gt.id(),gt.dim()))
        {
          GeometryType baseGt(Impl::baseTopologyId(gt.id(),gt.dim()),gt.dim()-1);
          return Builder<Field>::size(baseGt,points1D)*points1D.size(); // (order-1);
        }
        else
        {
          std::cout << "Not implemented for pyramid geometries still missing!\n";
          std::abort();
        }
      }
      template <unsigned int dim, class Points1DType>
      static void setup(GeometryType gt, const Points1DType &points1D,
                        LagrangePoint< Field, dim > *points )
      {
        if (dim==0)
        {
          points->weight_ = 1.;
          return;
        }
        if (gt.dim()==0)
        {
          points->point_[0] = Zero<Field>();
          points->weight_ = 1.;
        }
        else if (Impl::isTopology(Impl::prismConstruction,gt.id(),gt.dim()))
        {
          GeometryType baseGt(Impl::baseTopologyId(gt.id(),gt.dim()),gt.dim()-1);
          assert(dim>=gt.dim());
          Builder<Field>::template setup<dim>(baseGt,points1D,points);
          const unsigned int baseSize = Builder::size(baseGt,points1D);
          for (unsigned int i=0;i<baseSize;++i)
          {
            Field weight = points[i].weight_;
            for (unsigned int q=0;q<points1D.size();q++)
            {
              const unsigned int pos = q*baseSize+i;
              for (unsigned int d=0;d<gt.dim()-1;++d)
                points[pos].point_[d] = points[i].point_[d];
              points[pos].point_[gt.dim()-1]=points1D[q].first;
              points[pos].weight_ = weight*points1D[q].second;
            }
          }
        }
        else
        {
          std::cout << "Not implemented for pyramid geometries still missing!\n";
          std::abort();
        }
      }
    };
  } // namespace Impl

  template< class F, unsigned int dim >
  struct PointSetFromQuadrature : public EmptyPointSet<F,dim>
  {
    static const unsigned int dimension = dim;
    typedef F Field;
    typedef EmptyPointSet<F,dim> Base;
    typedef typename Base::LagrangePoint Point;
    typedef std::vector<std::pair<Field,Field>> Points1DType;
    PointSetFromQuadrature(unsigned int order)
      : Base(order), quadOrder_(-1)
    {}

    template <class Topology, class Quad>
    bool build (const Quad& quadFactory)
    {
      unsigned int order = Base::order();
      const auto &quad = quadFactory(order);
      quadOrder_ = quad.order();
      assert( quad.size() == order+1 );
      bool withEndPoints = false;
      Points1DType points1D;
      Field vertexWeight = 1;
      for (unsigned int i=0;i<=order;++i)
      {
        // remove corner points if part of the quadrature - are added in by
        // topology construction of points
        Field p = field_cast<Field>(quad[i].position());
        Field q = p-1.;
        if (std::abs(p)<1e-12 || std::abs(q)<1e-12)
        {
          withEndPoints = true;
          vertexWeight = quad[i].weight(); // assuming weight is identical for both end points
        }
        else
          points1D.push_back(std::make_pair(p,quad[i].weight()));
      }
      if (withEndPoints)
        Dune::Fem::ForLoop<Setup<Topology>::template InitCodim,0,dimension>::
          apply(GeometryType(Topology()),order,points1D,vertexWeight,points_);
      else
        Setup<Topology>::template InitCodim<dimension>::
          apply(GeometryType(Topology()),order,points1D,vertexWeight,points_);
      return true;
    }
    static bool supports ( GeometryType gt, int order )
    {
      return gt.isCube();
    }
    template <class Topology>
    static bool supports (int order)
    {
      return supports( GeometryType(Topology()), order );
    }
    unsigned int quadOrder() const
    {
      return quadOrder_;
    }
    protected:
    using Base::points_;
    unsigned int quadOrder_;
    private:
    template <class Topology>
    struct Setup
    {
      template <int pdim>
      struct InitCodim
      {
        static const unsigned int codim = dimension-pdim;
        static void apply(GeometryType gt, const unsigned int order,
                          const Points1DType &points1D,
                          const Field &vertexWeight,
                          std::vector<Point> &points)
        {
          const unsigned int subEntities = Dune::Geo::Impl::size(gt.id(),gt.dim(),codim);
          for (unsigned int subEntity=0;subEntity<subEntities;++subEntity)
          {
            GeometryType subGt(Impl::baseTopologyId(gt.id(),gt.dim(),codim),gt.dim()-codim);
            unsigned int oldSize = points.size();
            unsigned int size = Impl::Builder<Field>::size(subGt,points1D);
            if (size==0) continue;
            points.resize(oldSize+size);
            std::vector< LagrangePoint<Field,dimension-codim> > subPoints(size);
            Impl::Builder<Field>::template setup<dimension-codim>( subGt, points1D, &(subPoints[0]) );

            const GeometryType geoType( Topology::id, dimension );
            const auto &refElement = referenceElement<Field,dimension>(gt);
            const auto &mapping = refElement.template geometry< codim >( subEntity );

            LagrangePoint<Field,dimension> *p = &(points[oldSize]);
            for ( unsigned int nr = 0; nr<size; ++nr, ++p)
            {
              p->point_    = mapping.global( subPoints[nr].point_ );
              p->weight_   = subPoints[nr].weight_ * std::pow(vertexWeight,codim)*refElement.volume();
              p->localKey_ = LocalKey( subEntity, codim, nr );
            }
          }
        }
      };
    };
  };

  ///////////////////////////////////////////////////////
  // Some pointsets from dune-geometry
  ///////////////////////////////////////////////////////

  template< class F, unsigned int dim >
  struct GaussLobattoPointSet : public PointSetFromQuadrature<F,dim>
  {
    static const unsigned int dimension = dim;
    typedef F Field;
    typedef PointSetFromQuadrature<F,dim> Base;
    typedef typename Base::LagrangePoint Point;

    // enum identifier from dune-geometry QuadratureRules
    static const int pointSetId = Dune::QuadratureType::GaussLobatto;

    GaussLobattoPointSet(unsigned int order)
      : Base(order)
    {}
    template <class Topology>
    bool build ()
    {
      // get LobattoQuad with order+1 points
      auto quadFactory = [](int order)
      { return Dune::QuadratureRules<Field,1>::rule(
          Dune::GeometryTypes::line, pol2QuadOrder(order),
                    Dune::QuadratureType::GaussLobatto);
      };
      return Base::template build<Topology>(quadFactory);
    }
    static unsigned int pol2QuadOrder(int order)
    {
      return (order>0)? 2*order-1 : 0;
    }
    static unsigned int quad2PolOrder(int order)
    {
      return order/2 + 1;
    }

    static auto buildCubeQuadrature(unsigned int quadOrder)
    {
      using namespace Impl;
      GaussLobattoPointSet ps(quad2PolOrder(quadOrder));
      ps.template build< typename CubeTopology< dim >::type > ();
      return ps;
    }
  };


  template< class F, unsigned int dim >
  struct GaussLegendrePointSet : public PointSetFromQuadrature<F,dim>
  {
    static const unsigned int dimension = dim;
    typedef F Field;
    typedef PointSetFromQuadrature<F,dim> Base;
    typedef typename Base::LagrangePoint Point;

    // enum identifier from dune-geometry QuadratureRules
    static const int pointSetId = Dune::QuadratureType::GaussLegendre;

    GaussLegendrePointSet(unsigned int order)
      : Base(order)
    {}
    template <class Topology>
    bool build ()
    {
      // get LobattoQuad with order+1 points
      auto quadFactory = [](int order)
      { return Dune::QuadratureRules<Field,1>::rule(
          Dune::GeometryTypes::line, pol2QuadOrder(order), Dune::QuadratureType::GaussLegendre);
      };
      return Base::template build<Topology>(quadFactory);
    }

    static unsigned int pol2QuadOrder(int order)
    {
      return 2*order+1;
    }
    static unsigned int quad2PolOrder(int order)
    {
      return order/2;
    }

    static auto buildCubeQuadrature(unsigned int quadOrder)
    {
      using namespace Impl;
      GaussLegendrePointSet ps(quad2PolOrder(quadOrder));
      ps.template build< typename CubeTopology< dim >::type > ();
      return ps;
    }

  };
}  // namespace DUNE

#endif // HAVE_DUNE_LOCALFUNCTIONS

#endif // DUNE_LOBATTOBASIS_HH
