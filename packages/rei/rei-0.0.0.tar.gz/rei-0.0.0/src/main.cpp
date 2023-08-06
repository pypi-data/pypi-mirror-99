#include <pybind11/pybind11.h>

namespace py = pybind11;

#define MODULE_NAME _rei
#define C_STR_HELPER(a) #a
#define C_STR(a) C_STR_HELPER(a)
#ifndef VERSION_INFO
#define VERSION_INFO "dev"
#endif

PYBIND11_MODULE(MODULE_NAME, m) {
  m.doc() = R"pbdoc(Python port of `re2` C++ library.)pbdoc";
  m.attr("__version__") = C_STR(VERSION_INFO);
}
