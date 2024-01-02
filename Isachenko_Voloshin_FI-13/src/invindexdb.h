#ifndef INVERTED_INDEX_DATABASE_H
#define INVERTED_INDEX_DATABASE_H

// There will be inverted indexes database

#include <string>
#include <vector>
#include <sstream>
#include <map>
#include <set>
#include <list>
#include <algorithm>

#include "utils.h"

class InvIndDB;

enum class DBStatus : char
{
	Ok,
	WordNotExists,
	DocumentNotFound,
	DocumentExists,
	CollectionExists,
	CollectionNotExists
};

class Collection
{
private:
	size_t docId;
	std::vector<std::string> docs;
	std::map<std::string, std::map<size_t, std::vector<size_t>>> invIndex;
public:
	Collection();
	void buildIndex(const std::string& document, DBStatus& status);
	std::string getDocsByWord(const std::string& word, DBStatus& status);
	std::string getDocsByWordDistance(const std::string& word1, const std::string& word2, unsigned int distance, DBStatus& status);
	std::string toString(DBStatus& status);
};

class InvIndDB
{
private:
	std::map<std::string, Collection> collections;
public:
	InvIndDB();
	void addCollection(std::string collectionName, DBStatus& status);
	void addDocument(std::string collectionName, std::string document, DBStatus& status);
	std::string getDocsByWord(std::string collectionName, std::string word, DBStatus& status);
	std::string getDocsByWordDistance(std::string collectionName, const std::string& word1, const std::string& word2, unsigned int distance, DBStatus& status);
	std::string getIndex(std::string collectionName, DBStatus& status);
};

#endif