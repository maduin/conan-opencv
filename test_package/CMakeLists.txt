cmake_minimum_required(VERSION 2.8.12)
project(OpenCVPackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(DisplayImage display_image.cpp)
target_link_libraries(DisplayImage ${CONAN_LIBS})

enable_testing()

add_test(NAME OpenCVPackageTest
    COMMAND DisplayImage
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
