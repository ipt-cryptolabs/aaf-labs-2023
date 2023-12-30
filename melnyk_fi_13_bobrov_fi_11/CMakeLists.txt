cmake_minimum_required(VERSION 3.10)

project(AAF)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(SOURCES
    src/Trie.cpp
    src/main.cpp
    src/CommandProcessor.cpp
    src/Parser.cpp
    src/Types.cpp
)

set(HEADERS
    include/Trie.h
    include/Types.h
    include/CommandProcessor.h
    include/Parser.h
)

add_executable(aaf ${SOURCES} ${HEADERS})
