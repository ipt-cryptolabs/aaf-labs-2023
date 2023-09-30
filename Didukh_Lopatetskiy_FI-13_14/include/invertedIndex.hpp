#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <regex>

namespace {
    std::regex insertPattern(R"(^\s*INSERT\s+([a-zA-Z][a-zA-Z0-9_]*)\s+\{((?:\s*[-+]?[0-9]+\s*,\s*)*[-+]?[0-9]+)\s*};)", std::regex::icase);

    std::regex createPattern("^\\s*CREATE\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s*;\\s*$", std::regex::icase);
    std::regex printIndexPattern("^\\s*PRINT_INDEX\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s*;\\s*$", std::regex::icase);
    std::regex containsPattern(R"(^\s*CONTAINS\s+([a-zA-Z][a-zA-Z0-9_]*)\s+\{((?:\s*[-+]?[0-9]+\s*,\s*)*[-+]?[0-9]+)\s*};)", std::regex::icase);
    std::regex searchPattern(R"(^\s*SEARCH\s+([a-zA-Z][a-zA-Z0-9_]*)\s+\{((?:\s*[-+]?[0-9]+\s*,\s*)*[-+]?[0-9]+)\s*};)", std::regex::icase);

    std::regex identifierPattern("[a-zA-Z][a-zA-Z0-9_]*");
    std::regex numberPattern("\\s*([^,]+)\\s*,?");
}

class Parser {
private:
    std::vector<std::string> tokens;

private:
    // processes commands with this pattern: <command_name> <collection_name>;
    void processCommand(const std::smatch& match, const std::string& commandName);
    // processes commands with this pattern: <command_name> <collection_name> {val1, val2, ... };
    void processCommandWithValues(const std::smatch& match, const std::string& commandName);
   
    void processCreateCommand(const std::smatch& match);
    void processInsertCommand(const std::smatch& match);
    void processPrintIndexCommand(const std::smatch& match);
    void processSearchCommand(const std::smatch& match);
    void processContainsCommand(const std::smatch& match);
public:
    // add method to get string from user 
    void lexer(std::string inputString);
    std::vector<std::string> getTokens();
    void clearTokens();
};

class Collection {
private: 
    std::map<int, std::vector<std::string>> invertedIndex;
    std::vector<std::set<int>> sets;
public:
    void insert(const std::set<int>& set);
    void print_index();
};

class Collections {
private:
    std::map<std::string, Collection> collections;
    Parser parser;
    
    std::set<int> getSetFromTokens(const std::vector<std::string>& tokens);
public:
    void createCollection(const std::string& collecntionName);
    void insertSet(const std::string& collecntionName, const std::set<int>& set);
    void printCollectionIndex(const std::string& collectionName);
    void parse(const std::string& inputString);

    // for Mykhailo  
    void searchInCollection(const std::string& collectionName, const std::set<int>& set);
    // mb u should change the name because it not that clear what that mean
    void containsCollection(const std::string& collectionName, const std::set<int>& set);
};