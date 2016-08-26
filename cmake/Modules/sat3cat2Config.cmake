INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SAT3CAT2 sat3cat2)

FIND_PATH(
    SAT3CAT2_INCLUDE_DIRS
    NAMES sat3cat2/api.h
    HINTS $ENV{SAT3CAT2_DIR}/include
        ${PC_SAT3CAT2_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SAT3CAT2_LIBRARIES
    NAMES gnuradio-sat3cat2
    HINTS $ENV{SAT3CAT2_DIR}/lib
        ${PC_SAT3CAT2_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SAT3CAT2 DEFAULT_MSG SAT3CAT2_LIBRARIES SAT3CAT2_INCLUDE_DIRS)
MARK_AS_ADVANCED(SAT3CAT2_LIBRARIES SAT3CAT2_INCLUDE_DIRS)

