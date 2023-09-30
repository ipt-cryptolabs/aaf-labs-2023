cmake_minimum_required(VERSION 3.12)
project(InvertedIndex)

set(CMAKE_CXX_STANDARD 20)

add_subdirectory(src)

# Build the tests
enable_testing()
add_subdirectory(tests)

# Build the example
add_subdirectory(examples)