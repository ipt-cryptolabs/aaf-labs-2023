add_library(InvertedIndex
    invertedIndex.cpp
    parser.cpp
)

target_include_directories(InvertedIndex
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../include
)