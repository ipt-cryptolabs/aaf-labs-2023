cmake_minimum_required(VERSION 3.10)


project(DB_OAA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(SOURCES
        DB_OAA.cpp
        Database.hpp
        Table.hpp
)

add_executable(aaf ${SOURCES})
