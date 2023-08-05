// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef DUNE_DGLOCALCOEFFICIENTS_HH
#define DUNE_DGLOCALCOEFFICIENTS_HH

#include <cassert>
#include <vector>

#include <dune/localfunctions/common/localkey.hh>

namespace Dune
{

  // DGLocalCoefficients
  // -------------------

  /**
   * @brief A class providing local coefficients for dg spaces
   **/
  class DGLocalCoefficients
  {
    typedef DGLocalCoefficients This;

  public:
    //! construct local keys for n basis functions
    DGLocalCoefficients ( const unsigned int n )
      : localKey_( n )
    {
      for( unsigned i = 0; i < n; ++i )
        localKey_[ i ] = LocalKey( 0, 0, i );
    }

    const LocalKey &localKey ( const unsigned int i ) const
    {
      assert( i < size() );
      return localKey_[ i ];
    }

    unsigned int size () const
    {
      return localKey_.size();
    }

  private:
    std::vector< LocalKey > localKey_;
  };



  // DGLocalCoefficientsFactory
  // --------------------------
  /**
   * @brief A factory class for the dg local coefficients.
   **/
  template< class BasisFactory >
  struct DGLocalCoefficientsFactory
  {
    static const unsigned int dimension = BasisFactory::dimension;
    typedef typename BasisFactory::Key Key;
    typedef const DGLocalCoefficients Object;

    template< class Topology >
    static Object *create ( const Key &key )
    {
      const typename BasisFactory::Object *basis
        = BasisFactory::template create< Topology >( key );
      Object *coefficients = new Object( basis->size() );
      BasisFactory::release( basis );
      return coefficients;
    }
    static void release( Object *object ) { delete object; }
  };

}

#endif // #ifndef DUNE_DGLOCALCOEFFICIENTS_HH
