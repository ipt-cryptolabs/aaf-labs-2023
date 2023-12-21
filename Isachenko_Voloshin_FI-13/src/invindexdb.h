#ifndef INVERTED_INDEX_DATABASE_H
#define INVERTED_INDEX_DATABASE_H

// There will be inverted indexes database

#include <string>
#include <vector>
#include <sstream>
#include <map>
#include <set>
#include <list>

#include "utils.h"

class InvIndDB;

class Collection
{
private:
	size_t docId;
	std::map<std::string, std::map<size_t, std::vector<size_t>>> invIndex;
public:
	Collection();
	void buildIndex(const std::string& document);
	std::string getDocsByWord(std::string word);
	std::string toString();
};

class InvIndDB
{
private:
	std::map<std::string, Collection> collections;
public:
	InvIndDB();
	void addCollection(std::string collectionName);
	void addDocument(std::string collectionName, std::string document);
	std::string getDocsByWord(std::string collectionName, std::string word);
	std::string getIndex(std::string collectionName);
};

#endif