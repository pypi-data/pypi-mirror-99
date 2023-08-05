// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef DUNE_CLASSNAME_HH
#define DUNE_CLASSNAME_HH

/** \file
 * \brief A free function to provide the demangled class name
 *        of a given object or type as a string
 */

#include <cstdlib>
#include <memory>
#include <string>
#include <typeinfo>
#include <type_traits>

#if HAVE_CXA_DEMANGLE
#include <cxxabi.h>
#endif // #if HAVE_CXA_DEMANGLE

namespace Dune {

  namespace Impl {

    inline std::string demangle(std::string name)
    {
#if HAVE_CXA_DEMANGLE
      int status;
      std::unique_ptr<char, void(*)(void*)>
        demangled(abi::__cxa_demangle(name.c_str(), nullptr, nullptr, &status),
                  std::free);
      if( demangled )
        name = demangled.get();
#endif // #if HAVE_CXA_DEMANGLE
      return name;
    }
  }

  /** \brief Provide the demangled class name of a type T as a string */
  /*
   * \ingroup CxxUtilities
   */
  template <class T>
  std::string className ()
  {
    typedef typename std::remove_reference<T>::type TR;
    std::string className = Impl::demangle( typeid( TR ).name() );
    if (std::is_const<TR>::value)
        className += " const";
    if (std::is_volatile<TR>::value)
        className += " volatile";
    if (std::is_lvalue_reference<T>::value)
        className += "&";
    else if (std::is_rvalue_reference<T>::value)
        className += "&&";
    return className;
  }

  /** \brief Provide the demangled class name of a given object as a string */
  /*
   * \ingroup CxxUtilities
   */
  template <class T>
  std::string className ( T&& v)
  {
    typedef typename std::remove_reference<T>::type TR;
    std::string className = Impl::demangle( typeid(v).name() );
    if (std::is_const<TR>::value)
        className += " const";
    if (std::is_volatile<TR>::value)
        className += " volatile";
    return className;
  }
} // namespace Dune

#endif  // DUNE_CLASSNAME_HH
