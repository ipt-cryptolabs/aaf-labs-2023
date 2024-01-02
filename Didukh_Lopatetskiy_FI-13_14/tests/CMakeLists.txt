find_package(GTest REQUIRED)

add_executable(runTests
    invertedIndexTests.cpp
    parserTests.cpp
    runTests.cpp
)

target_link_libraries(runTests
    InvertedIndex
    GTest::GTest 
    GTest::Main   
)

include(GoogleTest)
gtest_discover_tests(runTests)  