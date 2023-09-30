find_package(GTest REQUIRED)

add_executable(tests
    tests.cpp
)

target_link_libraries(tests
    InvertedIndex
    GTest::GTest 
    GTest::Main   
)

include(GoogleTest)
gtest_discover_tests(tests)  