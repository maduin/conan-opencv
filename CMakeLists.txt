cmake_minimum_required(VERSION 2.8.12)
project(conan-opencv)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(MINGW)
    add_definitions(-DSTRSAFE_NO_DEPRECATE)
endif()

include(CMakeListsOriginal.txt)
