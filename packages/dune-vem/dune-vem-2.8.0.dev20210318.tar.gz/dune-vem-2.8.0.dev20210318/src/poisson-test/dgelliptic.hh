/**************************************************************************

  The dune-fem module is a module of DUNE (see www.dune-project.org).
  It is based on the dune-grid interface library
  extending the grid interface by a number of discretization algorithms
  for solving non-linear systems of partial differential equations.

  Copyright (C) 2003 - 2014 Robert Kloefkorn
  Copyright (C) 2003 - 2010 Mario Ohlberger
  Copyright (C) 2004 - 2014 Andreas Dedner
  Copyright (C) 2005        Adrian Burri
  Copyright (C) 2005 - 2014 Mirko Kraenkel
  Copyright (C) 2006 - 2014 Christoph Gersbacher
  Copyright (C) 2006 - 2014 Martin Nolte
  Copyright (C) 2011 - 2014 Tobias Malkmus
  Copyright (C) 2012 - 2014 Stefan Girke
  Copyright (C) 2013 - 2014 Claus-Justus Heine
  Copyright (C) 2013 - 2014 Janick Gerstenberger
  Copyright (C) 2013        Sven Kaulman
  Copyright (C) 2013        Tom Ranner


  The dune-fem module is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License as
  published by the Free Software Foundation; either version 2 of
  the License, or (at your option) any later version.

  The dune-fem module is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

 **************************************************************************/
#ifndef DGELLIPTIC_HH
#define DGELLIPTIC_HH

#include <dune/common/fmatrix.hh>

#include <dune/fem/quadrature/cachingquadrature.hh>
#include <dune/fem/operator/common/operator.hh>

#include <dune/fem/operator/common/differentiableoperator.hh>
#include <dune/fem/operator/common/stencil.hh>

// EllipticOperator
// ----------------

template< class DiscreteFunction, class Model >
struct DGEllipticOperator
    : public virtual Dune::Fem::Operator< DiscreteFunction >
{
  typedef DiscreteFunction DiscreteFunctionType;
  typedef Model            ModelType;

protected:
  typedef typename DiscreteFunctionType::DiscreteFunctionSpaceType DiscreteFunctionSpaceType;
  typedef typename DiscreteFunctionType::LocalFunctionType LocalFunctionType;
  typedef typename LocalFunctionType::RangeType RangeType;
  typedef typename LocalFunctionType::JacobianRangeType JacobianRangeType;

  typedef typename DiscreteFunctionSpaceType::IteratorType IteratorType;
  typedef typename IteratorType::Entity       EntityType;
  typedef typename EntityType::Geometry       GeometryType;

  typedef typename DiscreteFunctionSpaceType::DomainType DomainType;

  typedef typename DiscreteFunctionSpaceType::GridPartType  GridPartType;
  typedef typename GridPartType::IntersectionIteratorType IntersectionIteratorType;
  typedef typename IntersectionIteratorType::Intersection IntersectionType;
  typedef typename IntersectionType::Geometry  IntersectionGeometryType;

  typedef Dune::Fem::ElementQuadrature< GridPartType, 1 > FaceQuadratureType;
  typedef Dune::Fem::CachingQuadrature< GridPartType, 0 > QuadratureType;

  static const int dimDomain = LocalFunctionType::dimDomain;
  static const int dimRange = LocalFunctionType::dimRange;

public:
  //! contructor
  DGEllipticOperator ( const ModelType &model, const DiscreteFunctionSpaceType &space)
: model_( model )
{}

  // prepare the solution vector
  template <class Function>
  void prepare( const Function &func, DiscreteFunctionType &u )
  {
  }

  //! application operator
  virtual void
  operator() ( const DiscreteFunctionType &u, DiscreteFunctionType &w ) const;

protected:
  const ModelType &model () const { return model_; }
  double penalty() const { return model_.penalty(); }

private:
  ModelType model_;
};



// DifferentiableDGEllipticOperator
// --------------------------------

template< class JacobianOperator, class Model >
struct DifferentiableDGEllipticOperator
    : public DGEllipticOperator< typename JacobianOperator::DomainFunctionType, Model >,
      public Dune::Fem::DifferentiableOperator< JacobianOperator >
{
  typedef DGEllipticOperator< typename JacobianOperator::DomainFunctionType, Model > BaseType;

  typedef JacobianOperator JacobianOperatorType;

  typedef typename BaseType::DiscreteFunctionType DiscreteFunctionType;
  typedef typename BaseType::ModelType ModelType;

protected:
  typedef typename DiscreteFunctionType::DiscreteFunctionSpaceType DiscreteFunctionSpaceType;
  typedef typename DiscreteFunctionType::LocalFunctionType LocalFunctionType;
  typedef typename LocalFunctionType::RangeType RangeType;
  typedef typename LocalFunctionType::RangeFieldType RangeFieldType;
  typedef typename LocalFunctionType::JacobianRangeType JacobianRangeType;

  typedef typename DiscreteFunctionSpaceType::IteratorType IteratorType;
  typedef typename IteratorType::Entity       EntityType;
  typedef typename EntityType::Geometry       GeometryType;

  typedef typename DiscreteFunctionSpaceType::DomainType DomainType;

  typedef typename DiscreteFunctionSpaceType::GridPartType  GridPartType;
  typedef typename GridPartType::IntersectionIteratorType IntersectionIteratorType;
  typedef typename IntersectionIteratorType::Intersection IntersectionType;
  typedef typename IntersectionType::Geometry  IntersectionGeometryType;

  typedef typename DiscreteFunctionSpaceType::BlockMapperType BlockMapperType;
  typedef typename BlockMapperType::AgglomerationType AgglomerationType;
//  typedef typename



  typedef Dune::Fem::ElementQuadrature< GridPartType, 1 > FaceQuadratureType;
  typedef Dune::Fem::CachingQuadrature< GridPartType, 0 > QuadratureType;

  static const int dimDomain = LocalFunctionType::dimDomain;
  static const int dimRange = LocalFunctionType::dimRange;

public:
  //! contructor
  DifferentiableDGEllipticOperator ( const ModelType &model, const DiscreteFunctionSpaceType &space )
: BaseType( model, space ), stencil_(space,space)
{}

  //! method to setup the jacobian of the operator for storage in a matrix
  void jacobian ( const DiscreteFunctionType &u, JacobianOperatorType &jOp ) const;

protected:
  using BaseType::model;
  using BaseType::penalty;
  Dune::Fem::DiagonalAndNeighborStencil<DiscreteFunctionSpaceType,DiscreteFunctionSpaceType> stencil_;
};



// Implementation of DGEllipticOperator
// ------------------------------------

template< class DiscreteFunction, class Model >
void DGEllipticOperator< DiscreteFunction, Model >
::operator() ( const DiscreteFunctionType &u, DiscreteFunctionType &w ) const
{
  // clear destination
  w.clear();

  // get discrete function space
  const DiscreteFunctionSpaceType &dfSpace = w.space();

  // iterate over grid
  const IteratorType end = dfSpace.end();
  for( IteratorType it = dfSpace.begin(); it != end; ++it )
  {
    // get entity (here element)
    const EntityType &entity = *it;
    model().init(entity);
    // get elements geometry
    const GeometryType &geometry = entity.geometry();

    // get local representation of the discrete functions
    const LocalFunctionType uLocal = u.localFunction( entity );
    LocalFunctionType wLocal = w.localFunction( entity );

    // obtain quadrature order
    const int quadOrder = uLocal.order() + wLocal.order();

    { // element integral
      QuadratureType quadrature( entity, quadOrder );
      const size_t numQuadraturePoints = quadrature.nop();
      for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
      {
        const typename QuadratureType::CoordinateType &x = quadrature.point( pt );
        const double weight = quadrature.weight( pt ) * geometry.integrationElement( x );

        RangeType vu;
        uLocal.evaluate( quadrature[ pt ], vu );
        JacobianRangeType du;
        uLocal.jacobian( quadrature[ pt ], du );

        // compute mass contribution (studying linear case so linearizing around zero)
        RangeType avu( 0 );
        model().source( quadrature[ pt ], vu, avu );
        avu *= weight;
        // add to local functional wLocal.axpy( quadrature[ pt ], avu );

        JacobianRangeType adu( 0 );
        // apply diffusive flux
        model().diffusiveFlux( quadrature[ pt ], vu, du, adu );
        adu *= weight;

        // add to local function
        wLocal.axpy( quadrature[ pt ], avu, adu );
      }
    }
    if ( ! dfSpace.continuous() )
    {
      const double area = entity.geometry().volume();
      const IntersectionIteratorType iitend = dfSpace.gridPart().iend( entity );
      for( IntersectionIteratorType iit = dfSpace.gridPart().ibegin( entity ); iit != iitend; ++iit ) // looping over intersections
      {
        //! [Compute skeleton terms: iterate over intersections]
        const IntersectionType &intersection = *iit;
        if ( intersection.neighbor() )
        {
          const EntityType &outside = intersection.outside(); // pointer to outside element.

          typedef typename IntersectionType::Geometry  IntersectionGeometryType;
          const IntersectionGeometryType &intersectionGeometry = intersection.geometry();

          // compute penalty factor
          const double intersectionArea = intersectionGeometry.volume();
          const double beta = penalty() * intersectionArea / std::min( area, outside.geometry().volume() );
          //          std::cout << "???" << std::endl;
          LocalFunctionType uOutLocal = u.localFunction( outside ); // local u on outisde element

          FaceQuadratureType quadInside( dfSpace.gridPart(), intersection, quadOrder, FaceQuadratureType::INSIDE );
          FaceQuadratureType quadOutside( dfSpace.gridPart(), intersection, quadOrder, FaceQuadratureType::OUTSIDE );
          const size_t numQuadraturePoints = quadInside.nop();
          //! [Compute skeleton terms: iterate over intersections]

          for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
          {
            //! [Compute skeleton terms: obtain required values on the intersection]
            // get coordinate of quadrature point on the reference element of the intersection
            const typename FaceQuadratureType::LocalCoordinateType &x = quadInside.localPoint( pt );
            const DomainType normal = intersection.integrationOuterNormal( x );
            const double weight = quadInside.weight( pt );

            RangeType value;
            JacobianRangeType dvalue,advalue;

            RangeType vuIn,vuOut,jump;
            JacobianRangeType duIn, aduIn, duOut, aduOut;
            uLocal.evaluate( quadInside[ pt ], vuIn );
            uLocal.jacobian( quadInside[ pt ], duIn );
            model().diffusiveFlux( quadInside[ pt ], vuIn, duIn, aduIn );
            uOutLocal.evaluate( quadOutside[ pt ], vuOut );
            uOutLocal.jacobian( quadOutside[ pt ], duOut );
            model_.diffusiveFlux( quadInside[ pt ], jump, dvalue, advalue );
            model().init(outside);
            model_.diffusiveFlux( quadOutside[ pt ], vuOut, duOut, aduOut );
            model().init(entity);
            //! [Compute skeleton terms: obtain required values on the intersection]



            //! [Compute skeleton terms: compute factors for axpy method]
            jump = vuIn - vuOut;
            // penalty term : beta [u] [phi] = beta (u+ - u-)(phi+ - phi-)=beta (u+ - u-)phi+
            value = jump;
            value *= beta * intersectionGeometry.integrationElement( x );
            // {A grad u}.[phi] = {A grad u}.phi+ n_+ = 0.5*(grad u+ + grad u-).n_+ phi+
            aduIn += aduOut;
            aduIn *= -0.5;

            aduIn.umv(normal,value);
            //  [ u ] * { grad phi_en } = -normal(u+ - u-) * 0.5 grad phi_en
            // here we need a diadic product of u x n
            for (int r=0;r<dimRange;++r)
              for (int d=0;d<dimDomain;++d)
                dvalue[r][d] = -0.5 * normal[d] * jump[r];

            value *= weight;
            advalue *= weight;
            wLocal.axpy( quadInside[ pt ], value, advalue );
            //! [Compute skeleton terms: compute factors for axpy method]
          }
        }
        else if( intersection.boundary() )
        {
          Dune::FieldVector<int,RangeType::dimension> components(1);
          if ( ! model().isDirichletIntersection( intersection, components ) )
            continue;

          typedef typename IntersectionType::Geometry  IntersectionGeometryType;
          const IntersectionGeometryType &intersectionGeometry = intersection.geometry();

          // compute penalty factor
          const double intersectionArea = intersectionGeometry.volume();
          const double beta = penalty() * intersectionArea / area;

          FaceQuadratureType quadInside( dfSpace.gridPart(), intersection, quadOrder, FaceQuadratureType::INSIDE );
          const size_t numQuadraturePoints = quadInside.nop();

          for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
          {
            const typename FaceQuadratureType::LocalCoordinateType &x = quadInside.localPoint( pt );
            const DomainType normal = intersection.integrationOuterNormal( x );
            const double weight = quadInside.weight( pt );

            RangeType value;
            JacobianRangeType dvalue,advalue;

            RangeType vuIn,jump;
            JacobianRangeType duIn, aduIn;
            uLocal.evaluate( quadInside[ pt ], vuIn );
            uLocal.jacobian( quadInside[ pt ], duIn );
            model_.diffusiveFlux( quadInside[ pt ], vuIn, duIn, aduIn );

            jump = vuIn;

            // penalty term : beta [u] [phi] = beta (u+ - u-)(phi+ - phi-)=beta (u+ - u-)phi+
            value = jump;
            value *= beta * intersectionGeometry.integrationElement( x );
            // {A grad u}.[phi] = {A grad u}.phi+ n_+ = 0.5*(grad u+ + grad u-).n_+ phi+
            aduIn.umv(normal,value);


            //  [ u ] * { grad phi_en } = -normal(u+ - u-) * 0.5 grad phi_en
            // here we need a diadic product of u x n
            for (int r=0;r<dimRange;++r)
              for (int d=0;d<dimDomain;++d)
                dvalue[r][d] = -0.5 * normal[d] * jump[r];

            model_.diffusiveFlux( quadInside[ pt ], jump, dvalue, advalue );

            value *= weight;
            advalue *= weight;
            wLocal.axpy( quadInside[ pt ], value, advalue );
          }
        }
      }
    }

  }

  // communicate data (in parallel runs)
  w.communicate();
}

// Implementation of DifferentiableDGEllipticOperator
// ------------------------------------------------

template< class JacobianOperator, class Model >
void DifferentiableDGEllipticOperator< JacobianOperator, Model >
::jacobian ( const DiscreteFunctionType &u, JacobianOperator &jOp ) const
 {
  typedef typename JacobianOperator::LocalMatrixType LocalMatrixType;
  typedef typename DiscreteFunctionSpaceType::BasisFunctionSetType BasisFunctionSetType;

  jOp.reserve(stencil_);
  jOp.clear();
  std::ofstream flhs ("lhs-agglo.dat");

  // gcd3 added 20-Nov-15
  const DiscreteFunctionSpaceType &dfSpace = u.space();
  const GridPartType& gridPart = dfSpace.gridPart();
  const BlockMapperType& blockmapper = dfSpace.blockMapper();
  const AgglomerationType& agglomeration = blockmapper.agglomeration();


  const unsigned int numDofs = dfSpace.blockMapper().maxNumDofs() *
      DiscreteFunctionSpaceType :: localBlockSize ;

  const std::size_t maxNumLocalDofs = DiscreteFunctionSpaceType::localBlockSize * u.space().blockMapper().maxNumDofs();


  std::vector< RangeType > phi( numDofs );
  std::vector< JacobianRangeType > dphi( numDofs );

  std::vector< RangeType > phiNb( numDofs );
  std::vector< JacobianRangeType > dphiNb( numDofs );

  const IteratorType end = dfSpace.end();
  int myElem = 0;

  // gcd3 added 20-Nov-15
  // this gets the global element numbers if needed
  typedef typename GridPartType::IndexSetType LeafIndexSet;
  const LeafIndexSet& set = gridPart.indexSet();



  for( IteratorType it = dfSpace.begin(); it != end; ++it )
  {
    const EntityType &entity = *it;
    model().init(entity);

    // gcd3 added 15-Nov-15
    typedef typename GridPartType::IndexSetType LeafIndexSet;
    const LeafIndexSet& lset = gridPart.indexSet();
    Dune::GeometryType gt = it->type();
    auto& ref = Dune::ReferenceElements<double,dimDomain>::general(gt);
    const int LeafElementIndex = lset.index(entity); // Global element number of the current element
    const int currentPolygon = agglomeration.index(*it); // the polygon we are integrating
    myElem++;



    const GeometryType geometry = entity.geometry();
    const LocalFunctionType uLocal = u.localFunction( entity );
    LocalMatrixType jLocal = jOp.localMatrix( entity, entity );

    const BasisFunctionSetType &baseSet = jLocal.domainBasisFunctionSet();
    const unsigned int numBaseFunctions = baseSet.size();

    QuadratureType quadrature( entity, 2*dfSpace.order() );
    const size_t numQuadraturePoints = quadrature.nop();
    for( size_t pt = 0; pt < numQuadraturePoints; ++pt )
    {
      const typename QuadratureType::CoordinateType &x = quadrature.point( pt );
      //      std::cout << "gp = " << x[0] << " " << x[1] << std::endl;
      const double weight = quadrature.weight( pt ) * geometry.integrationElement( x );

      // evaluate all basis functions at given quadrature point
      baseSet.evaluateAll( quadrature[ pt ], phi );


      // evaluate jacobians of all basis functions at given quadrature point
      baseSet.jacobianAll( quadrature[ pt ], dphi );

      //      std::cout << "phi: " << std::endl;
      //      for (auto i = phi.begin(); i != phi.end(); ++i)
      //        std::cout << *i << ' ';
      //      std::cout << "dphi: " << std::endl;
      //      for (auto j = dphi.begin(); j != dphi.end(); ++j)
      //        std::cout << *j << ' ';


      // get value for linearization
      RangeType u0;
      JacobianRangeType jacU0;
      uLocal.evaluate( quadrature[ pt ], u0 );
      uLocal.jacobian( quadrature[ pt ], jacU0 );

      RangeType aphi( 0 );
      JacobianRangeType adphi( 0 );
      for( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
      {
        // if mass terms or right hand side is present
        model().linSource( u0, quadrature[ pt ], phi[ localCol ], aphi );

        // if gradient term is present
        model().linDiffusiveFlux( u0, jacU0, quadrature[ pt ], phi[ localCol ], dphi[ localCol ], adphi );

        // get column object and call axpy method
        jLocal.column( localCol ).axpy( phi, dphi, aphi, adphi, weight );
      }
    }
    if ( dfSpace.continuous() )
      continue;

    double area = geometry.volume();
    const IntersectionIteratorType endiit = gridPart.iend( entity );
    for ( IntersectionIteratorType iit = gridPart.ibegin( entity );
        iit != endiit ; ++ iit )
    {
      const IntersectionType& intersection = *iit ;

      //       skip internal edges

      if( intersection.neighbor()  )
      {
        const EntityType& neighbor = intersection.outside();
        const int neighborPolygon = agglomeration.index(neighbor);
        typedef typename IntersectionType::Geometry  IntersectionGeometryType;
        const IntersectionGeometryType &intersectionGeometry = intersection.geometry();

        if (currentPolygon!=neighborPolygon)
        {
//          std::cout << intersectionGeometry.center() << std::endl;

          //! [Assemble skeleton terms: get contributions on off diagonal block]
          // get local matrix for face entries
          LocalMatrixType localOpNb = jOp.localMatrix( neighbor, entity );
          // get neighbor's base function set
          const BasisFunctionSetType &baseSetNb = localOpNb.domainBasisFunctionSet();
          //! [Assemble skeleton terms: get contributions on off diagonal block]

          // compute penalty factor
          const double intersectionArea = intersectionGeometry.volume();
          const double beta = penalty() * intersectionArea / std::min( area, neighbor.geometry().volume() );

//          std::cout << intersectionArea <<" " << penalty() <<" " <<   area <<" " <<  neighbor.geometry().volume()  <<" " << beta << std::endl;

          // here we assume that the intersection is conforming
          FaceQuadratureType faceQuadInside(gridPart, intersection, 2*dfSpace.order() + 1,
              FaceQuadratureType::INSIDE);
          FaceQuadratureType faceQuadOutside(gridPart, intersection, 2*dfSpace.order() + 1,
              FaceQuadratureType::OUTSIDE);
          //        std::cout << "???" << std::endl;
          const size_t numFaceQuadPoints = faceQuadInside.nop();
          for( size_t pt = 0; pt < numFaceQuadPoints; ++pt )
          {
            const typename FaceQuadratureType::LocalCoordinateType &x = faceQuadInside.localPoint( pt );
            DomainType normal = intersection.integrationOuterNormal( x );
            double faceVol = normal.two_norm();
            normal /= faceVol; // make it into a unit normal
            //          std::cout << "inside elliptic: " << geometry.center() << std::endl;

            const double quadWeight = faceQuadInside.weight( pt );
            const double weight = quadWeight * faceVol;

            //! [Assemble skeleton terms: obtain values om quadrature point]
            RangeType u0En;
            JacobianRangeType u0EnJac;
            uLocal.evaluate( faceQuadInside[ pt ], u0En );
            uLocal.jacobian( faceQuadInside[ pt ], u0EnJac );

            /////////////////////////////////////////////////////////////
            // evaluate basis function of face inside E^- (entity)
            /////////////////////////////////////////////////////////////

            // evaluate all basis functions for quadrature point pt
            baseSet.evaluateAll( faceQuadInside[ pt ], phi );

            // evaluate the jacobians of all basis functions
            baseSet.jacobianAll( faceQuadInside[ pt ], dphi );

            /////////////////////////////////////////////////////////////
            // evaluate basis function of face inside E^+ (neighbor)
            /////////////////////////////////////////////////////////////

            // evaluate all basis functions for quadrature point pt on neighbor
            baseSetNb.evaluateAll( faceQuadOutside[ pt ], phiNb );

            // evaluate the jacobians of all basis functions on neighbor
            baseSetNb.jacobianAll( faceQuadOutside[ pt ], dphiNb );

            for( unsigned int i = 0; i < numBaseFunctions; ++i )
            {
              JacobianRangeType adphiEn = dphi[ i ];
              JacobianRangeType adphiNb = dphiNb[ i ];
              model().linDiffusiveFlux( u0En, u0EnJac, faceQuadInside[ pt ], phi[i], adphiEn, dphi[ i ] );
              model().init(neighbor);
              model().linDiffusiveFlux( u0En, u0EnJac, faceQuadOutside[ pt ], phiNb[i], adphiNb, dphiNb[ i ] );
              model().init(entity);
            }
            //! [Assemble skeleton terms: obtain values om quadrature point]

            //! [Assemble skeleton terms: compute factors for axpy method]
            for( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
            {
              RangeType valueEn(0), valueNb(0);
              JacobianRangeType dvalueEn(0), dvalueNb(0);

              //  -{ A grad u } * [ phi_en ]
              dphi[localCol].usmv( -0.5, normal, valueEn );

              //  -{ A grad u } * [ phi_en ]
              dphiNb[localCol].usmv( -0.5, normal, valueNb );

              //  [ u ] * [ phi_en ] = u^- * phi_en^-
              valueEn.axpy( beta, phi[ localCol ] );

              valueNb.axpy(-beta, phiNb[ localCol ] );
              // here we need a diadic product of u x n
              for ( int r=0; r< dimRange; ++r )
                for ( int d=0; d< dimDomain; ++d )
                {
                  //  [ u ] * { grad phi_en }
                  dvalueEn[r][d] = - 0.5 * normal[d] * phi[localCol][r];

                  //  [ u ] * { grad phi_en }
                  dvalueNb[r][d] = 0.5 * normal[d] * phiNb[localCol][r];
                }

              jLocal.column( localCol ).axpy( phi, dphi, valueEn, dvalueEn, weight );
              localOpNb.column( localCol ).axpy( phi, dphi, valueNb, dvalueNb, weight );
            }
            //! [Assemble skeleton terms: compute factors for axpy method]
          }
        }
      }
      else if( intersection.boundary() )
      {
        Dune::FieldVector<int,RangeType::dimension> components(1);
        if ( ! model().isDirichletIntersection( intersection, components ) )
          continue;

        typedef typename IntersectionType::Geometry  IntersectionGeometryType;
        const IntersectionGeometryType &intersectionGeometry = intersection.geometry();

        // compute penalty factor
//        std::cout << intersectionGeometry.center() << std::endl;
        const double intersectionArea = intersectionGeometry.volume();

        const double beta = penalty() * intersectionArea / area;

        // here we assume that the intersection is conforming
        FaceQuadratureType faceQuadInside(gridPart, intersection, 2*dfSpace.order() + 1,
            FaceQuadratureType::INSIDE);

        const size_t numFaceQuadPoints = faceQuadInside.nop();
        for( size_t pt = 0; pt < numFaceQuadPoints; ++pt )
        {
          const typename FaceQuadratureType::LocalCoordinateType &x = faceQuadInside.localPoint( pt );
          DomainType normal = intersection.integrationOuterNormal( x );
          double faceVol = normal.two_norm();
          normal /= faceVol; // make it into a unit normal

          const double quadWeight = faceQuadInside.weight( pt );
          const double weight = quadWeight * faceVol;

          RangeType u0En;
          JacobianRangeType u0EnJac;
          uLocal.evaluate( faceQuadInside[ pt ], u0En );
          uLocal.jacobian( faceQuadInside[ pt ], u0EnJac );

          /////////////////////////////////////////////////////////////
          // evaluate basis function of face inside E^- (entity)
          /////////////////////////////////////////////////////////////

          // evaluate all basis functions for quadrature point pt
          baseSet.evaluateAll( faceQuadInside[ pt ], phi );

          // evaluate the jacobians of all basis functions
          baseSet.jacobianAll( faceQuadInside[ pt ], dphi );

          for( unsigned int i = 0; i < numBaseFunctions; ++i )
          {
            JacobianRangeType adphiEn = dphi[ i ];
            model().linDiffusiveFlux( u0En, u0EnJac, faceQuadInside[ pt ], phi[i], adphiEn, dphi[ i ] );
          }

          for( unsigned int localCol = 0; localCol < numBaseFunctions; ++localCol )
          {
            RangeType valueEn(0);
            JacobianRangeType dvalueEn(0);

            //  -{ A grad u } * [ phi_en ]
            dphi[localCol].usmv( -0.5, normal, valueEn );

            //  [ u ] * [ phi_en ] = u^- * phi_en^-
            valueEn.axpy( beta, phi[ localCol ] );

            // here we need a diadic product of u x n
            for ( int r=0; r< dimRange; ++r )
              for ( int d=0; d< dimDomain; ++d )
              {
                //  [ u ] * { grad phi_en }
                dvalueEn[r][d] = - 0.5 * normal[d] * phi[localCol][r];
              }

            jLocal.column( localCol ).axpy( phi, dphi, valueEn, dvalueEn, weight );
          }
        }
      }
    } // for ( IntersectionIteratorType iit = gridPart.ibegin( entity );
  } // end grid traversal

  // jOp.matrix().print(flhs);

  jOp.communicate();
 }

#endif // ELLIPTIC_HH
