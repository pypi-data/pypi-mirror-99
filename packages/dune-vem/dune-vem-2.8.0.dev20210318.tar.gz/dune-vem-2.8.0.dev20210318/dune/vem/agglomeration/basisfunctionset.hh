#ifndef DUNE_VEM_AGGLOMERATION_BASISFUNCTIONSET_HH
#define DUNE_VEM_AGGLOMERATION_BASISFUNCTIONSET_HH

#include <cassert>
#include <cstddef>

#include <type_traits>
#include <utility>

#include <dune/geometry/referenceelements.hh>

#include <dune/fem/quadrature/quadrature.hh>
#include <dune/fem/space/basisfunctionset/functor.hh>
#include <dune/fem/space/shapefunctionset/vectorial.hh>

#include <dune/vem/agglomeration/boundingbox.hh>
#include <dune/vem/agglomeration/functor.hh>
// #include <dune/vem/misc/highorderquadratures.hh>

namespace Dune
{

  namespace Vem
  {

    // BoundingBoxBasisFunctionSet
    // ---------------------------

    template< class GridPart, class ShapeFunctionSet >
    class BoundingBoxBasisFunctionSet
    {
      typedef BoundingBoxBasisFunctionSet< GridPart, ShapeFunctionSet > ThisType;

    public:
      typedef typename GridPart::template Codim<0>::EntityType EntityType;
      typedef BoundingBox<GridPart> BoundingBoxType;

      typedef typename ShapeFunctionSet::FunctionSpaceType FunctionSpaceType;

      typedef typename FunctionSpaceType::DomainFieldType DomainFieldType;
      typedef typename FunctionSpaceType::RangeFieldType RangeFieldType;

      typedef typename FunctionSpaceType::DomainType DomainType;
      typedef typename FunctionSpaceType::RangeType RangeType;
      typedef typename FunctionSpaceType::JacobianRangeType JacobianRangeType;
      typedef typename FunctionSpaceType::HessianRangeType HessianRangeType;

      static constexpr int dimDomain = DomainType::dimension;

      typedef ReferenceElement< typename DomainType::field_type, dimDomain > ReferenceElementType;

    private:
      struct Transformation
      {
        Transformation() {}
        explicit Transformation ( const BoundingBoxType &bbox )
        : bbox_(bbox)
        {}

        JacobianRangeType operator() ( JacobianRangeType jacobian, bool transpose=false ) const
        {
          for( int i = 0; i < RangeType::dimension; ++i )
            applyScalar( jacobian[ i ], transpose );
          return jacobian;
        }

        template< class ScalarJacobian >
        Fem::MakeVectorialExpression< ScalarJacobian, JacobianRangeType > operator() ( Fem::MakeVectorialExpression< ScalarJacobian, JacobianRangeType > jacobian, bool transpose=false ) const
        {
          applyScalar( jacobian.scalar()[ 0 ], transpose );
          return jacobian;
        }

        HessianRangeType operator() ( HessianRangeType hessian, bool transpose=false ) const
        {
          for( int i = 0; i < RangeType::dimension; ++i )
            applyScalar( hessian[ i ], transpose );
          return hessian;
        }

        template< class ScalarHessian >
        Fem::MakeVectorialExpression< ScalarHessian, HessianRangeType > operator() ( Fem::MakeVectorialExpression< ScalarHessian, HessianRangeType > hessian, bool transpose ) const
        {
          applyScalar( hessian.scalar()[ 0 ], transpose );
          return hessian;
        }

        void applyScalar ( FieldVector< RangeFieldType, dimDomain > &jacobian, bool transpose=false ) const
        {
          bbox_.gradientTransform(jacobian,transpose);
        }

        void applyScalar ( FieldMatrix< RangeFieldType, dimDomain, dimDomain > &hessian, bool transpose=false ) const
        {
          bbox_.hessianTransform(hessian,transpose);
        }
        BoundingBoxType bbox_;
      };

    public:
      BoundingBoxBasisFunctionSet ()
      : entity_(nullptr) , useOnb_(false)
      { }

      BoundingBoxBasisFunctionSet ( const EntityType &entity, const BoundingBoxType &bbox,
                                    bool useOnb,
                                    ShapeFunctionSet shapeFunctionSet = ShapeFunctionSet() )
        : entity_( &entity ), shapeFunctionSet_( std::move( shapeFunctionSet ) ), bbox_( std::move( bbox ) ),
          transformation_(bbox_),
          vals_(shapeFunctionSet_.size()),
          jacs_(shapeFunctionSet_.size()),
          hess_(shapeFunctionSet_.size()),
          useOnb_(useOnb)
      {
      }

      int order () const { return shapeFunctionSet_.order(); }

      std::size_t size () const { return shapeFunctionSet_.size(); }

      const EntityType &entity () const { assert( entity_ ); return *entity_; }

      const ReferenceElementType &referenceElement () const
      {
        return referenceElement( entity().type() );
      }

      template< class Quadrature, class Vector, class DofVector >
      void axpy ( const Quadrature &quadrature, const Vector &values, DofVector &dofs ) const
      {
        const std::size_t nop = quadrature.nop();
        for( std::size_t qp = 0; qp < nop; ++qp )
          axpy( quadrature[ qp ], values[ qp ], dofs );
      }

      template< class Quadrature, class VectorA, class VectorB, class DofVector >
      void axpy ( const Quadrature &quadrature, const VectorA &valuesA, const VectorB &valuesB, DofVector &dofs ) const
      {
        const std::size_t nop = quadrature.nop();
        for( std::size_t qp = 0; qp < nop; ++qp )
        {
          axpy( quadrature[ qp ], valuesA[ qp ], dofs );
          axpy( quadrature[ qp ], valuesB[ qp ], dofs );
        }
      }

      template< class Point, class DofVector >
      void axpy ( const Point &x, const RangeType &valueFactor, DofVector &dofs ) const
      {
        // onb
        sfEvaluateAll(x,vals_);
        Fem::FunctionalAxpyFunctor< RangeType, DofVector > f( valueFactor, dofs );
        for (std::size_t beta=0;beta<size();++beta)
          f(beta,vals_[beta]);
      }

      template< class Point, class DofVector >
      void axpy ( const Point &x, const JacobianRangeType &jacobianFactor, DofVector &dofs ) const
      {
        // onb
        sfEvaluateAll(x,jacs_);
        const JacobianRangeType transformedFactor = transformation_( jacobianFactor,true );
        Fem::FunctionalAxpyFunctor< JacobianRangeType, DofVector > f( transformedFactor, dofs );
        for (std::size_t beta=0;beta<size();++beta)
          f(beta,jacs_[beta]);
      }

      template< class Point, class DofVector >
      void axpy ( const Point &x, const RangeType &valueFactor, const JacobianRangeType &jacobianFactor, DofVector &dofs ) const
      {
        axpy( x, valueFactor, dofs );
        axpy( x, jacobianFactor, dofs );
      }

      template< class Quadrature, class DofVector, class Values >
      void evaluateAll ( const Quadrature &quadrature, const DofVector &dofs, Values &values ) const
      {
        const std::size_t nop = quadrature.nop();
        for( std::size_t qp = 0; qp < nop; ++qp )
          evaluateAll( quadrature[ qp ], dofs, values[ qp ] );
      }

      template< class Point, class DofVector >
      void evaluateAll ( const Point &x, const DofVector &dofs, RangeType &value ) const
      {
        // onb
        sfEvaluateAll(x,vals_);
        value = RangeType( 0 );
        Fem::AxpyFunctor< DofVector, RangeType > f( dofs, value );
        for (std::size_t beta=0;beta<size();++beta)
          f(beta,vals_[beta]);
      }

      template< class Point, class Values > const
      void evaluateAll ( const Point &x, Values &values ) const
      {
        // onb
        sfEvaluateAll(x,vals_);
        assert( values.size() >= size() );
        Fem::AssignFunctor< Values > f( values );
        for (std::size_t beta=0;beta<size();++beta)
          f(beta,vals_[beta]);
      }

      template< class Quadrature, class DofVector, class Jacobians >
      void jacobianAll ( const Quadrature &quadrature, const DofVector &dofs, Jacobians &jacobians ) const
      {
        const std::size_t nop = quadrature.nop();
        for( std::size_t qp = 0; qp < nop; ++qp )
          jacobianAll( quadrature[ qp ], dofs, jacobians[ qp ] );
      }

      template< class Point, class DofVector >
      void jacobianAll ( const Point &x, const DofVector &dofs, JacobianRangeType &jacobian ) const
      {
        // onb
        sfEvaluateAll(x,jacs_);
        jacobian = JacobianRangeType( 0 );
        Fem::AxpyFunctor< DofVector, JacobianRangeType > f( dofs, jacobian );
        for (std::size_t beta=0;beta<size();++beta)
          f(beta,jacs_[beta]);
        jacobian = transformation_( jacobian );
      }

      template< class Point, class Jacobians > const
      void jacobianAll ( const Point &x, Jacobians &jacobians ) const
      {
        // onb
        sfEvaluateAll(x,jacs_);
        assert( jacobians.size() >= size() );
        Fem::AssignFunctor< Jacobians, TransformedAssign< Transformation > > f( jacobians, transformation_ );
        for (std::size_t beta=0;beta<size();++beta)
          f(beta,jacs_[beta]);
      }

      template< class Quadrature, class DofVector, class Hessians >
      void hessianAll ( const Quadrature &quadrature, const DofVector &dofs, Hessians &hessians ) const
      {
        const std::size_t nop = quadrature.nop();
        for( std::size_t qp = 0; qp < nop; ++qp )
          hessianAll( quadrature[ qp ], dofs, hessians[ qp ] );
      }

      template< class Point, class DofVector >
      void hessianAll ( const Point &x, const DofVector &dofs, HessianRangeType &hessian ) const
      {
        // onb
        sfEvaluateAll(x,hess_);
        hessian = HessianRangeType( RangeFieldType( 0 ) );
        Fem::AxpyFunctor< DofVector, HessianRangeType > f( dofs, hessian );
        for (std::size_t beta=0;beta<size();++beta)
          f(beta,hess_[beta]);
        hessian = transformation_( hessian );
      }

      template< class Point, class Hessians > const
      void hessianAll ( const Point &x, Hessians &hessians ) const
      {
        // onb
        sfEvaluateAll(x,hess_);
        assert( hessians.size() >= size() );
        Fem::AssignFunctor< Hessians, TransformedAssign< Transformation > > f( hessians, transformation_ );
        for (std::size_t beta=0;beta<size();++beta)
          f(beta,hess_[beta]);
      }

      template< class Point, class Functor >
      void evaluateEach ( const Point &x, Functor functor ) const
      {
        //! onb
        sfEvaluateAll(x,vals_);
        for (std::size_t beta=0;beta<size();++beta)
          functor(beta,vals_[beta]);
      }

      template< class Point, class Functor >
      void jacobianEach ( const Point &x, Functor functor ) const
      {
        //! onb
        sfEvaluateAll(x,jacs_);
        for (std::size_t beta=0;beta<size();++beta)
          functor(beta,transformation_( jacs_[beta] ));
      }

      template< class Point, class Functor >
      void hessianEach ( const Point &x, Functor functor ) const
      {
        sfEvaluateAll(x,hess_);
        for (std::size_t beta=0;beta<size();++beta)
          functor(beta,transformation_( hess_[beta] ));
      }

    private:
      template< class Point >
      DomainType position ( const Point &x ) const
      {
        return bbox_.transform( entity().geometry().global( Fem::coordinate( x ) ) );
      }
      // make basis orthogonal
      // k = 0
      // for i < N
      //   for j < i; ++k
      //     b_i -= r_k b_j {Remove the projection of b_i onto b_j
      //   b_i /= r_k
      template <class Vector>
      void onb(Vector &values) const
      {
        if (!useOnb_)
          return;
        std::size_t k = 0;
        for (std::size_t i=0;i<values.size();++i,++k)
        {
          for (std::size_t j=0;j<i;++j,++k)
            values[i].axpy(-bbox_.r(k), values[j]);
          values[i] /= bbox_.r(k);
        }
      }
      template< class Point>
      void sfEvaluateAll(const Point &x, std::vector<RangeType> &values) const
      {
        Fem::AssignFunctor< decltype(values) > f( values );
        auto y = position(x);
        for (std::size_t beta=0;beta<size();++beta)
          shapeFunctionSet_.evaluateEach( y, f);
        onb( values );
      }
      template< class Point>
      void sfEvaluateAll(const Point &x, std::vector<JacobianRangeType> &values) const
      {
        Fem::AssignFunctor< decltype(values) > f( values );
        auto y = position(x);
        for (std::size_t beta=0;beta<size();++beta)
          shapeFunctionSet_.jacobianEach( y, f);
        onb( values );
      }
      template< class Point>
      void sfEvaluateAll(const Point &x, std::vector<HessianRangeType> &values) const
      {
        Fem::AssignFunctor< decltype(values) > f( values );
        auto y = position(x);
        for (std::size_t beta=0;beta<size();++beta)
          shapeFunctionSet_.hessianEach( y, f);
        // onb( values ); // Note: failing axpy on FV<FM> due to missing // double*FM
        std::size_t k = 0;
        for (std::size_t i=0;i<values.size();++i,++k)
        {
          for (std::size_t j=0;j<i;++j,++k)
            for (std::size_t r=0;r<values[i].size();++r)
              values[i][r].axpy(-bbox_.r(k), values[j][r]);
          values[i] /= bbox_.r(k);
        }
      }

      const EntityType *entity_ = nullptr;
      ShapeFunctionSet shapeFunctionSet_;
      BoundingBoxType bbox_;
      Transformation transformation_;
      mutable std::vector< RangeType > vals_;
      mutable std::vector< JacobianRangeType > jacs_;
      mutable std::vector< HessianRangeType > hess_;
      bool useOnb_ = false;
    };

    template< class GridPart, class ShapeFunctionSet >
    inline static void onbBasis( const Agglomeration< GridPart > &agglomeration,
        const ShapeFunctionSet &shapeFunctionSet,
        std::vector< BoundingBox< GridPart > > &boundingBoxes )
    {
      typedef typename GridPart::template Codim< 0 >::EntityType ElementType;
      typedef typename GridPart::template Codim< 0 >::EntitySeedType ElementSeedType;
      typedef BoundingBoxBasisFunctionSet< GridPart, ShapeFunctionSet > BBBasisFunctionSetType;
      typedef typename BBBasisFunctionSetType::RangeType RangeType;
      typedef typename BBBasisFunctionSetType::DomainFieldType DomainFieldType;

#if 1 // FemQuads
      typedef Dune::Fem::ElementQuadrature<GridPart,0> Quadrature0Type;
#else
      typedef Dune::Fem::ElementQuadrature<GridPart,0,Dune::Fem::HighOrderQuadratureTraits> Quadrature0Type;
#endif

      const int polOrder = shapeFunctionSet.order();
      const auto &gridPart = agglomeration.gridPart();

      // start off with R=I
      for (std::size_t b=0;b<boundingBoxes.size();++b)
      {
        auto &bbox = boundingBoxes[b];
        bbox.resizeR( shapeFunctionSet.size() );
        std::size_t k = 0;
        for (std::size_t i=0;i<shapeFunctionSet.size();++i,++k)
        {
          for (std::size_t j=0;j<i;++j,++k)
            bbox.r(k) = 0;
          bbox.r(k) = 1;
        }
      }

      // return; // no ONB

      std::vector<RangeType> val;
      std::vector< std::vector<RangeType> > values;
      std::vector<DomainFieldType> weights;
      values.resize( shapeFunctionSet.size() );
      val.resize( shapeFunctionSet.size() );

      // compute onb factors
      // want to iterate over each polygon separately - so collect all
      // triangles from a given polygon
      std::vector< std::vector< ElementSeedType > > entitySeeds( agglomeration.size() );
      for( const ElementType &element : elements( static_cast< typename GridPart::GridViewType >( gridPart ), Partitions::interiorBorder ) )
        entitySeeds[ agglomeration.index( element ) ].push_back( element.seed() );

      // start iteration over all polygons
      for( std::size_t agglomerate = 0; agglomerate < agglomeration.size(); ++agglomerate )
      {
        auto &bbox = boundingBoxes[agglomerate];
        const ElementType &element = gridPart.entity( entitySeeds[agglomerate][0] );

        // first collect all weights and basis function evaluation needed
        // to compute mass matrix over this polygon
        Quadrature0Type quadrature( element , 2*polOrder );
        const std::size_t nop = quadrature.nop();
        for (std::size_t i=0;i<values.size(); ++i)
          values[i].resize( nop * entitySeeds[agglomerate].size() );
        weights.resize( nop * entitySeeds[agglomerate].size() );
        std::size_t e = 0;
        for( const ElementSeedType &entitySeed : entitySeeds[ agglomerate ] )
        {
          const ElementType &element = gridPart.entity( entitySeed );
          const auto geometry = element.geometry();
          BBBasisFunctionSetType basisFunctionSet( element, bbox, false, shapeFunctionSet );
          Quadrature0Type quadrature( element, 2*polOrder );
          for( std::size_t qp = 0; qp < nop; ++qp, ++e )
          {
            weights[e] = geometry.integrationElement( quadrature.point( qp ) ) * quadrature.weight( qp );
            basisFunctionSet.evaluateAll(quadrature[qp], val);
            for (unsigned int i=0;i<val.size();++i)
              values[i][e] = val[i];
          }
        }

        // now compute ONB coefficients
        // k = 0
        // for i < N
        //   for j < i; ++k
        //     r_k = ( b_i, b_j )
        //     b_i -= r_k b_j {Remove the projection of b_i onto b_j
        //   r_k = ( b_i, b_i )
        //   b_i /= r_k
        auto l2Integral = [&](std::size_t i, std::size_t j) -> double {
          double ret = 0;
          for (std::size_t l = 0; l<weights.size(); ++l)
            ret += values[i][l]*values[j][l]*weights[l];
          return ret / bbox.volume();
        };
        std::size_t k = 0;
        for (std::size_t i=0;i<values.size();++i,++k)
        {
          auto &bi = values[i];
          for (std::size_t j=0;j<i;++j,++k)
          {
            bbox.r(k) = l2Integral(i,j);
            assert( bbox.r(k) == bbox.r(k) );
            for (std::size_t l = 0; l<values[i].size(); ++l)
              bi[l].axpy(-bbox.r(k), values[j][l]);
            // std::cout << i << " " << j << " = " << bbox.r(k) << "   ";
          }
          bbox.r(k) = std::sqrt( l2Integral(i,i) );
          assert( bbox.r(k) == bbox.r(k) );
          // std::cout << i << " " << i << " = " << bbox.r(k) << std::endl;
          for (std::size_t l = 0; l<values[i].size(); ++l)
            bi[l] /= bbox.r(k);
        }
      }
    }

  } // namespace Vem

} // namespace Dune

#endif // #ifndef DUNE_VEM_AGGLOMERATION_BASISFUNCTIONSET_HH
