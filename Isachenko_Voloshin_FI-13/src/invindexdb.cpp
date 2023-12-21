#include "invindexdb.h"

Collection::Collection()
{
	docId = 0;
}

void Collection::buildIndex(const std::string& document)
{
	std::string word;
	size_t wordPos = 0;
	docId++;

	for (std::string::const_iterator i = document.cbegin(); i != document.cend(); i++)
	{
		if (*i == ',') continue;
		if (*i == '.') continue;
		if (*i == '!') continue;
		if (*i == '?') continue;

		if (isspace(*i) && !isspace(*(i - 1)))
		{
			word = toLowerStr(word);
			wordPos++;
			invIndex[word][docId].push_back(wordPos);
			word.erase();
			continue;
		}

		word += *i;
	}
	invIndex[word][docId].push_back(++wordPos);
}

std::string Collection::getDocsByWord(std::string word)
{
	if (invIndex.find(word) == invIndex.end()) return "";
	std::string res = "";
	for (const auto& kv : invIndex[word])
	{
		res.append("d" + std::to_string(kv.first) + ", ");
	}
	return res;
}

std::string Collection::toString()
{
	std::string result;
	for (const auto& kv1 : invIndex)
	{
		result.append(kv1.first);
		result.append(":\n");
		for (const auto& kv2 : kv1.second)
		{
			result.append("\td" + std::to_string(kv2.first));
			result.append(" -> [");
			for (auto pos = kv2.second.begin(); pos != kv2.second.end(); pos++)
			{
				result.append(std::to_string(*pos));
				if (pos + 1 != kv2.second.end())
				{
					result.append(", ");
					continue;
				}
			}
			result.append("]\n");
		}
		result.append("\n");
	}

	return result;
}

InvIndDB::InvIndDB()
{
}

void InvIndDB::addCollection(std::string collectionName)
{
	if (collections.find(collectionName) != collections.end()) return;
	collections[collectionName] = Collection();
}

void InvIndDB::addDocument(std::string collectionName, std::string document)
{
	if (collections.find(collectionName) == collections.end()) return;
	collections[collectionName].buildIndex(document);
}

std::string InvIndDB::getDocsByWord(std::string collectionName, std::string word)
{
	if (collections.find(collectionName) == collections.end()) return "";

	return collections[collectionName].getDocsByWord(word);
}

std::string InvIndDB::getIndex(std::string collectionName)
{
	auto coll_iter = collections.find(collectionName);
	if (coll_iter != collections.end())
	{
		std::string str = coll_iter->second.toString();
		return str;
	}
	return "";
}

