#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <iterator>
#include <set>

#include "parser.hpp"

class Collection {
private: 
    std::map<int, std::set<int>> invertedIndex;
    std::vector<std::set<int>> sets;

public:
    void insert(const std::set<int> &set);
    bool contains(const std::set<int> &set);
    void print_index();
    std::vector<std::set<int>> getSets() { return sets; }

    std::vector<std::set<int>> containsSearch(const std::set<int> &set) const;
    std::vector<std::set<int>> containedBySearch(const std::set<int> &set) const;
    std::vector<std::set<int>> intersectsSearch(const std::set<int> &set) const;
};

class Collections {
private:
    std::map<std::string, Collection> collections;
    Parser parser;

private:    
    std::set<int> getSetFromTokens(const std::vector<std::string> &tokens);
    void printsSets(const std::vector<std::set<int>> &sets);

public:
    void parse(const std::string &inputString);

    void createCollection(const std::string &collecntionName);
    void insertSet(const std::string &collecntionName, const std::set<int> &set);
    void printCollectionIndex(const std::string &collectionName);
    bool containsCollection(const std::string &collectionName, const std::set<int> &set);
   
    std::vector<std::set<int>> searchInCollection(const std::string &collectionName);
    std::vector<std::set<int>> intersectsSearch(const std::string &collecntionName, const std::set<int> &set);
    std::vector<std::set<int>> containsSearch(const std::string &collecntionName, const std::set<int> &set);
    std::vector<std::set<int>> containedBySearch(const std::string &collecntionName, const std::set<int> &set);
};