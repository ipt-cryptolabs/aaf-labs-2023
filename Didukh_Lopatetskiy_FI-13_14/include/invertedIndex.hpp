#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <string>
#include <map>
#include <regex>

namespace {
    std::regex insertPattern("^\\s*INSERT\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s+\\{(.+?)\\};\\s*$", std::regex::icase);
    std::regex createPattern("^\\s*CREATE\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s+\\;\\s*$", std::regex::icase);
    
    std::regex identifierPattern("[a-zA-Z][a-zA-Z0-9_]*");
    std::regex numberPattern("\\s*([^,]+)\\s*,?");
    // std::regex createPattern("^\\s*CREATE\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s*;\\s*$", std::regex::icase);

    // std::regex insertPattern("^\\s*INSERT\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s+\\{(.+?)\\};\\s*$", std::regex::icase);

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

public:
    // add method to get string from user 
    
    void lexer(std::string inputString);
    std::vector<std::string> getTokens();
    void clearTokens();
};

class InvertedIndex {
private: 
    std::map<std::string, std::vector<int>> invertedIndex;
    Parser parser;

public: 
    void insert(const std::string& collectionName, const std::vector<int>& collection);
    void create(const std::string& collectionName);
    void print_index();

    // for Mykhailo)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))0
    void contains();
    void search();

    void parse(std::string inputString);
};