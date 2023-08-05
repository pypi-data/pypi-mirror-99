#ifndef DUNE_VEM_AGGLOMERATION_INDEXSET_HH
#define DUNE_VEM_AGGLOMERATION_INDEXSET_HH

#include <cassert>
#include <cstddef>

#include <algorithm>
#include <numeric>
#include <utility>
#include <vector>

#include <dune/grid/common/rangegenerators.hh>

#include <dune/vem/agglomeration/agglomeration.hh>
#include <dune/vem/agglomeration/boundingbox.hh>

namespace Dune
{

  namespace Vem
  {

    // AgglomerationIndexSet
    // ---------------------

    template< class GridPart, class Allocator = std::allocator< std::size_t > >
    class AgglomerationIndexSet
    {
      typedef AgglomerationIndexSet< GridPart > ThisType;

    public:
      typedef GridPart GridPartType;

      typedef Agglomeration< GridPartType > AgglomerationType;

      typedef typename Allocator::template rebind< std::size_t >::other AllocatorType;

      static const int dimension = GridPartType::dimension;

      typedef FieldVector< typename GridPartType::ctype, GridPartType::dimensionworld > GlobalCoordinate;

      typedef typename GridPartType::template Codim< 0 >::EntityType ElementType;

    private:
      struct Agglomerate;

    public:
      explicit AgglomerationIndexSet ( const AgglomerationType &agglomeration, AllocatorType allocator = AllocatorType() );

      std::size_t index ( const ElementType &element ) const { return agglomeration_.index( element ); }

      std::size_t subIndex ( const ElementType &element, int i, int codim ) const
      {
        assert( ( codim >= 0 ) && ( codim <= dimension ) );
        return ( codim == 0 ? index( element ) : agglomerate( element ).index( i, dimension - codim ));
      }

      std::pair< std::size_t, bool > globalIndex ( const ElementType &element, int i, int codim ) const
      {
        assert( ( codim >= 0 ) && ( codim <= dimension ) );
        if( codim == 0 )
          return std::make_pair( index( element ), true );

        const auto &refElement = ReferenceElements< typename GridPart::ctype, dimension >::general( element.type() );
        const typename GridPartType::IndexSetType& indexSet = agglomeration_.gridPart().indexSet();
        const int globalIndex = globalIndex_[ GlobalGeometryTypeIndex::index( refElement.type( i, codim ) ) ][ indexSet.subIndex( element, i, codim ) ];
        return std::make_pair( static_cast< std::size_t >( globalIndex ), globalIndex != -1 );
      }

      std::pair< std::size_t, bool > globalIndex ( const ElementType &entity ) const
      {
        return std::make_pair( index( entity ), true );
      }

      template< class Entity >
      std::pair< std::size_t, bool > globalIndex ( const Entity &entity ) const
      {
        assert( Entity::codimension > 0 );
        const typename GridPartType::IndexSetType& indexSet = agglomeration_.gridPart().indexSet();
        const int globalIndex = globalIndex_[ GlobalGeometryTypeIndex::index( entity.type() ) ][ indexSet.index( entity ) ];
        return std::make_pair( static_cast< std::size_t >( globalIndex ), globalIndex != -1 );
      }

      int localIndex ( const ElementType &element, int i, int codim ) const
      {
        assert( (codim >= 0) && (codim <= dimension) );
        if( codim == 0 )
          return 0;

        const auto result = globalIndex( element, i, codim );
        if( !result.second )
          return -1;
        auto &localAgg = agglomerate( element );
        for( std::size_t k = 0; k < localAgg.size( dimension-codim ); ++k )
          if( localAgg.index( k, dimension-codim ) == result.first )
            return k;
        assert( false );
        return -1;
      }

      int numPolyVertices ( const ElementType &element, int codim ) const
      {
        assert(( codim > 0 ) && ( codim == dimension ));
        return agglomerate( element ).size( dimension-codim );
      }

      /**
       * obtain number of subagglomerates
       *
       * \param[in]  index  index of the agglomerate
       * \param[in]  codim  codimension of the subagglomerates
       */
      std::size_t subAgglomerates ( std::size_t index, int codim ) const
      {
        assert( ( codim >= 0 ) && ( codim <= dimension ) );
        return ( codim == 0 ? 1u : agglomerate( index ).size( dimension - codim ));
      }

      /**
       * obtain number of subagglomerates
       *
       * \param[in]  element  any element belonging to the agglomerate
       * \param[in]  codim   codimension of the subagglomerates
       */
      std::size_t subAgglomerates ( const ElementType &element, int codim ) const
      {
        return subAgglomerates( index( element ), codim );
      }

      std::size_t maxSubAgglomerates ( int codim ) const
      {
        assert( (codim >= 0) && (codim <= dimension) );
        return maxSubAgglomerates_[ dimension-codim ];
      }

      std::size_t size ( int codim ) const
      {
        assert( (codim >= 0) && (codim <= dimension) );
        return size_[ dimension-codim ];
      }

      const AgglomerationType &agglomeration () const { return agglomeration_; }
      const GridPartType &gridPart () const { return agglomeration().gridPart(); }

      double volume( std::size_t index ) const
      {
        assert(boundingBox(index).volume() == volumes_[index]); return volumes_[index];
      }
      double volume( const ElementType &element ) const
      {
        return volume( index( element ) );
      }
      double elementDiameter( std::size_t index ) const { return boundingBox(index).diameter(); }
      double elementDiameter( const ElementType &element ) const
      {
        return elementDiameter( index( element ) );
      }
      double vertexDiameter( std::size_t index ) const { return vertexDiameters_[index]; }
      double vertexDiameter( const ElementType &element, std::size_t index ) const
      {
        return vertexDiameter( localIndex(element,index,dimension) );
      }
      const BoundingBox<GridPart>& boundingBox( std::size_t index ) const { return boundingBoxes_[index]; }
      const BoundingBox<GridPart>& boundingBox( const ElementType &element ) const
      {
        return boundingBox( index( element ) );
      }
      const std::vector< BoundingBox< GridPart > >& boundingBox() const
      {
        return boundingBoxes_;
      }
      std::vector< BoundingBox< GridPart > >& boundingBox()
      {
        return boundingBoxes_;
      }

      std::pair<double,double> diameters() const { return {minDiameter_,maxDiameter_}; }

    private:
      const Agglomerate &agglomerate ( std::size_t agglomerateIndex ) const { return agglomerates_[ agglomerateIndex ]; }
      const Agglomerate &agglomerate ( const ElementType &element ) const { return agglomerate( index( element ) ); }

      const AgglomerationType &agglomeration_;
      std::vector< BoundingBox< GridPart > > boundingBoxes_;
      AllocatorType allocator_;
      std::vector< Agglomerate > agglomerates_;
      std::array< std::size_t, dimension+1 > size_;
      std::array< std::size_t, dimension+1 > maxSubAgglomerates_;
      std::vector< std::vector< int > > globalIndex_;
      std::vector< double > volumes_;
      std::vector< double > vertexDiameters_;
      double minDiameter_, maxDiameter_;
    };



    // AgglomerationIndexSet::Agglomerate
    // ----------------------------------

    template< class GridPart, class Allocator >
    struct AgglomerationIndexSet< GridPart, Allocator >::Agglomerate
      : private AllocatorType
    {
      Agglomerate( AllocatorType allocator = Allocator() )
        : AllocatorType( std::move( allocator ) )
      {
        connectivity_.fill( nullptr );
      }

      template< class V >
      Agglomerate( const std::array< V, dimension > &connectivity, AllocatorType allocator )
        : AllocatorType( std::move( allocator ) )
      {
        build( connectivity );
      }

      Agglomerate( const Agglomerate & ) = delete;

      Agglomerate( Agglomerate &&other )
        : AllocatorType( std::move( allocator() ) ), connectivity_( other.connectivity_ )
      {
        other.connectivity_.fill( nullptr );
      }

      ~Agglomerate ()
      {
        if( connectivity_[ 0 ] )
        {
          for( auto p = connectivity_[ 0 ]; p != connectivity_[ dimension ]; ++p )
            allocator().destroy( p );
          allocator().deallocate( connectivity_[ 0 ], connectivity_[ dimension ] - connectivity_[ 0 ] );
        }
      }

      Agglomerate &operator= ( const Agglomerate & ) = delete;

      Agglomerate &operator= ( Agglomerate &&other )
      {
        allocator() = std::move( other.allocator() );
        connectivity_ = other.connectivity_;
        other.connectivity_.fill( nullptr );
        return *this;
      }

      std::size_t index ( std::size_t i, int dim ) const
      {
        assert( i < size( dim ) );
        return connectivity_[ dim ][ i ];
      }

      std::size_t size ( int dim ) const { return ( connectivity_[ dim+1 ] - connectivity_[ dim ] ); }

    private:
      AllocatorType &allocator () { return static_cast< AllocatorType & >( *this ); }

      template< class V >
      void build ( const std::array< V, dimension > &connectivity )
      {
        const std::size_t size = std::accumulate( connectivity.begin(), connectivity.end(), std::size_t( 0 ), [] ( std::size_t i, const V &v ) {
            return i + v.size();
          } );
        connectivity_[ 0 ] = allocator().allocate( size );
        for( int dim = 0; dim < dimension; ++dim )
        {
          connectivity_[ dim+1 ] = connectivity_[ dim ];
          for( std::size_t index : connectivity[ dim ] )
            allocator().construct( connectivity_[ dim+1 ]++, index );
        }
      }

      std::array< typename AllocatorType::pointer, dimension+1 > connectivity_;
    };



    // Implementation of AgglomerationIndexSet
    // ---------------------------------------

    template< class GridPart, class Allocator >
    inline AgglomerationIndexSet< GridPart, Allocator >::AgglomerationIndexSet ( const AgglomerationType &agglomeration, AllocatorType allocator )
      : agglomeration_( agglomeration )
      , boundingBoxes_( boundingBoxes( agglomeration ) )
      , allocator_( std::move( allocator ) )
    {
      const typename GridPartType::IndexSetType& indexSet = agglomeration_.gridPart().indexSet();
      std::vector< std::vector< typename GridPartType::IndexSetType::IndexType > > subAgglomerates( GlobalGeometryTypeIndex::size( dimension-1 ) );

      // find subagglomerates
      //
      // insert the index of each subentity belonging to more than one agglomerate into the
      // subAgglomerates vector for the corresponding geometry type

      for( const auto element : elements( static_cast< typename GridPart::GridViewType >( agglomeration_.gridPart() ), Partitions::interiorBorder ) )
      {
        const std::size_t agIndex = index( element );
        const auto &refElement = ReferenceElements< typename GridPart::ctype, dimension >::general( element.type() );
        for( const auto intersection : intersections( static_cast< typename GridPart::GridViewType >( agglomeration_.gridPart() ), element ) )
        {
          assert( intersection.conforming() );
          if( !intersection.neighbor() || ( index( intersection.outside() ) != agIndex ) )
          {
            const int face = intersection.indexInInside();
            for( int codim = 1; codim <= dimension; ++codim )
            {
              const int numSubEntities = refElement.size( face, 1, codim );
              for( int i = 0; i < numSubEntities; ++i )
              {
                const int k = refElement.subEntity( face, 1, i, codim );
                const std::size_t typeIndex = GlobalGeometryTypeIndex::index( refElement.type( k, codim ) );
                subAgglomerates[ typeIndex ].push_back( indexSet.subIndex( element, k, codim ) );
              }
            }
          }
        }
      }

      // make subagglomerates unique
      //
      // The position of a subentity's index in the subAgglometates vector will then give its subagglomerate index.

      for( auto &list : subAgglomerates )
      {
        std::sort( list.begin(), list.end() );
        list.erase( std::unique( list.begin(), list.end() ), list.end() );
      }

      // compute offsets

      std::vector< std::size_t > offset( GlobalGeometryTypeIndex::size( dimension ) );
      for( int dim = 0; dim < dimension; ++dim )
      {
        maxSubAgglomerates_[ dim ] = 0;
        size_[ dim ] = 0;
        for( std::size_t typeIndex = GlobalGeometryTypeIndex::offset( dim ); typeIndex < GlobalGeometryTypeIndex::offset( dim+1 ); ++typeIndex )
        {
          offset[ typeIndex ] = size_[ dim ];
          const std::size_t numSubAgglomerates = subAgglomerates[ typeIndex ].size();
          size_[ dim ] += numSubAgglomerates;
          maxSubAgglomerates_[ dim ] = std::max( maxSubAgglomerates_[ dim ], numSubAgglomerates );
        }
      }

      // build connectivity

      maxSubAgglomerates_[ dimension ] = 1;
      size_[ dimension ] = agglomeration.size();
      std::vector< std::array< std::vector< std::size_t >, dimension > > connectivity( size_[ dimension ] );
      volumes_.resize( agglomeration.size() );
      std::fill(volumes_.begin(), volumes_.end(), 0.);

      for( const auto element : elements( static_cast< typename GridPart::GridViewType >( agglomeration_.gridPart() ), Partitions::interiorBorder ) )
      {
        const std::size_t agIndex = agglomeration.index( element );
        const auto &refElement = ReferenceElements< typename GridPart::ctype, dimension >::general( element.type() );
        //for( const auto intersection : intersections( agglomeration_.gridPart(), element ) )
        for( const auto intersection : intersections( static_cast< typename GridPart::GridViewType >( agglomeration_.gridPart() ), element ))
        {
          assert( intersection.conforming() );
          if( !intersection.neighbor() || ( agglomeration.index( intersection.outside() ) != agIndex ) )
          {
            const int face = intersection.indexInInside();
            for( int codim = 1; codim <= dimension; ++codim )
            {
              std::vector< std::size_t > &list = connectivity[ agIndex ][ dimension - codim ];
              const int numSubEntities = refElement.size( face, 1, codim );
              for( int i = 0; i < numSubEntities; ++i )
              {
                const int k = refElement.subEntity( face, 1, i, codim );
                const std::size_t typeIndex = GlobalGeometryTypeIndex::index( refElement.type( k, codim ) );
                const auto &subAgs = subAgglomerates[ typeIndex ];
                const auto pos = std::lower_bound( subAgs.begin(), subAgs.end(), indexSet.subIndex( element, k, codim ) );
                assert( ( pos != subAgs.end()) && ( *pos == indexSet.subIndex( element, k, codim )) );
                list.push_back( offset[ typeIndex ] + static_cast< std::size_t >( pos - subAgs.begin() ) );
              }
            }
          }
        }
        volumes_[agIndex] += element.geometry().volume();
      }

      // compress connectivity

      agglomerates_.reserve( size_[ dimension ] );
      for( auto &c : connectivity )
      {
        for( int dim = 0; dim < dimension; ++dim )
        {
          std::sort( c[ dim ].begin(), c[ dim ].end() );
          c[ dim ].erase( std::unique( c[ dim ].begin(), c[ dim ].end() ), c[ dim ].end() );
        }
        agglomerates_.emplace_back( c, allocator_ );
      }

      // copy subentities

      globalIndex_.resize( GlobalGeometryTypeIndex::size( dimension-1 ) );
      for( int codim = 1; codim <= dimension; ++codim )
      {
        for( const GeometryType type : indexSet.types( codim ) )
          globalIndex_[ GlobalGeometryTypeIndex::index( type ) ].resize( indexSet.size( type ), -1 );
      }

      for( const auto element : elements( static_cast< typename GridPart::GridViewType >( agglomeration_.gridPart() ), Partitions::interiorBorder ) )
      {
        const auto &refElement = ReferenceElements< typename GridPart::ctype, dimension >::general( element.type() );

        for( int codim = 1; codim <= dimension; ++codim )
        {
          const int numSubEntities = refElement.size( codim );
          for( int i = 0; i < numSubEntities; ++i )
          {
            const std::size_t typeIndex = GlobalGeometryTypeIndex::index( refElement.type( i, codim ) );
            const auto &subAgs = subAgglomerates[ typeIndex ];
            const auto index = indexSet.subIndex( element, i, codim );
            const auto pos = std::lower_bound( subAgs.begin(), subAgs.end(), index );
            if( ( pos != subAgs.end()) && ( *pos == index ) )
              globalIndex_[ typeIndex ][ index ] = offset[ typeIndex ] + static_cast< std::size_t >( pos - subAgs.begin() );
          }
        }
      }

      vertexDiameters_.resize( size(dimension), 0.);
      std::vector<std::size_t> vertexCount( size(dimension), 0);
      for( const auto element : elements( static_cast< typename GridPart::GridViewType >( agglomeration_.gridPart() ), Partitions::interiorBorder ) )
      {
        auto &localAgg = agglomerate( element );
        assert( localAgg.size( 0 ) == 3 );
        for( std::size_t k = 0; k < localAgg.size( 0 ); ++k )
        {
          auto idx = localAgg.index( k, 0 );
          assert( idx < vertexDiameters_.size() );
          vertexDiameters_[idx] += elementDiameter(element);
          vertexCount[idx] += 1;
        }
      }
      for ( std::size_t k = 0; k < vertexCount.size(); ++k)
        vertexDiameters_[k] /= double(vertexCount[k]);

      maxDiameter_ = *std::max_element(vertexDiameters_.begin(),vertexDiameters_.end());
      minDiameter_ = *std::min_element(vertexDiameters_.begin(),vertexDiameters_.end());

      std::cout << "maximal vertex diameter: "
                << *std::max_element(vertexDiameters_.begin(),vertexDiameters_.end())
                << std::endl;
    }
  } // namespace Vem

} // namespace Dune

#endif // #ifndef DUNE_VEM_AGGLOMERATION_INDEXSET_HH
