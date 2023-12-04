#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>

#include "parser.hpp"

class Collection {
private: 
    std::map<int, std::vector<std::string>> invertedIndex;
    std::vector<std::set<int>> sets;

public:
    void insert(const std::set<int>& set);
    void print_index();
    std::vector<std::set<int>> getSets() { return sets; }
};

class Collections {
private:
    std::map<std::string, Collection> collections;
    Parser parser;

private:    
    std::set<int> getSetFromTokens(const std::vector<std::string>& tokens);
public:
    void insertSet(const std::string& collecntionName, const std::set<int>& set);
    bool containsCollection(const std::string& collectionName, const std::set<int>& set);
    void createCollection(const std::string& collecntionName);
    bool searchInCollection(const std::string& collectionName);
    void printCollectionIndex(const std::string& collectionName);

    void parse(const std::string& inputString);
};