#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <string>
#include <map>
#include <regex>

namespace {
    std::regex insertPattern("^\\s*INSERT\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s+\\{(.+?)\\};\\s*$", std::regex::icase);

//     std::regex insertRegex("INSERT", std::regex_constants::icase);
//     std::regex createRegex("CREATE", std::regex_constants::icase);
//     std::regex printIndexRegex("PRINT_INDEX", std::regex_constants::icase);
//     std::regex containsRegex("CONTAINS", std::regex_constants::icase);
//     std::regex searchRegex("SEARCH", std::regex_constants::icase);
}

class Parser {
private:
    // mb should add some enum or kinda
    std::vector<std::string> tokens;

private:
    std::string mergeTokens();

public:
    // add method to get string from user 
    
    std::string lexer(std::string inputString);
    std::vector<std::string> getTokens();
};


class InvertedIndex {
private: 
    std::map<int, std::vector<int>> invertedIndex;
    Parser parser;

public: 
    // type are definitely wrong)
    void insert();
    void create();
    void print_index();
    void contains();
    void search();

    void activateParser(std::string inputString);
};