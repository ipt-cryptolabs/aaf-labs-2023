#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <string>
#include <map>
#include <regex>

// namespace {
//     std::regex insertPattern("^INSERT\\s+([a-zA-Z_][a-zA-Z0-9_]*)\\s+\\{(.+?)\\};$");
//     std::regex insertRegex("INSERT", std::regex_constants::icase);
//     std::regex createRegex("CREATE", std::regex_constants::icase);
//     std::regex printIndexRegex("PRINT_INDEX", std::regex_constants::icase);
//     std::regex containsRegex("CONTAINS", std::regex_constants::icase);
//     std::regex searchRegex("SEARCH", std::regex_constants::icase);
// }

class Parser {
private:
    std::vector<std::string> tokens;

private:
    std::string mergeTokens(const std::vector<std::string>& tokens);

public:
    std::string lexer(std::string inputString);

};


class InvertedIndex {
private: 
    std::map<int, std::vector<int>> invertedIndex;
public: 
    // type are definitely wrong)
    void insert();
    void create();
    void print_index();
    void contains();
    void search();
};