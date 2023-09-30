add_library(InvertedIndex
    invertedIndex.cpp
)

target_include_directories(InvertedIndex
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../include
)