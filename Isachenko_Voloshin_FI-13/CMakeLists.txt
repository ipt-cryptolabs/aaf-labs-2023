cmake_minimum_required(VERSION 3.5)

project(InvertedIndexesLab)

add_executable(${PROJECT_NAME} 
	src/main.cpp
	src/parser.cpp "src/queries.cpp"
	"src/invindexdb.cpp")