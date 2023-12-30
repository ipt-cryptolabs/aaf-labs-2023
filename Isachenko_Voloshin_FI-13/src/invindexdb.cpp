#include "invindexdb.h"

Collection::Collection()
{
	docId = 0;
}

void Collection::buildIndex(const std::string& document, DBStatus& status)
{
	if (std::find(docs.begin(), docs.end(), document) != docs.end())
	{
		status = DBStatus::DocumentExists;
		return;
	}
	std::string word;
	size_t wordPos = 0;
	docId++;
	docs.push_back(document);

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
	status = DBStatus::Ok;
}

std::string Collection::getDocsByWord(const std::string& word, DBStatus& status)
{
	if (invIndex.find(word) == invIndex.end())
	{
		status = DBStatus::WordNotExists;
		return "";
	}
	std::string res = "";
	for (const auto& kv : invIndex[word])
	{
		res.append("d" + std::to_string(kv.first) + ":\n\t" + docs[kv.first - 1] + "\n");
	}
	status = DBStatus::Ok;
	return res;
}

std::string Collection::getDocsByWordDistance(const std::string& word1, const std::string& word2, unsigned int distance, DBStatus& status)
{
	if (invIndex.find(word1) == invIndex.end() || invIndex.find(word2) == invIndex.end())
	{
		status = DBStatus::WordNotExists;
		return "";
	}

	std::set<std::size_t> crossingSet;
	std::vector<std::size_t> matchingVec;
	std::string res;

	for (auto& const kv : invIndex[word1])
	{
		crossingSet.insert(kv.first);
	}

	for (auto& const kv : invIndex[word2])
	{
		crossingSet.insert(kv.first);
	}

	for (auto& const d : crossingSet)
	{
		auto &docVec1 = invIndex[word1][d];
		auto &docVec2 = invIndex[word2][d];
		for (int i = 0; i < docVec1.size(); i++)
		{
			for (int j = 0; j < docVec2.size(); j++)
			{
				if ((docVec1[i] > docVec2[j]) && (docVec1[i] - docVec2[j] == distance))
				{
					matchingVec.push_back(d);
					continue;
				}
				if ((docVec1[i] < docVec2[j]) && (docVec2[j] - docVec1[i] == distance))
				{
					matchingVec.push_back(d);
					continue;
				}

			}
		}
	}

	for (std::size_t d : matchingVec) {
		res += "d" + std::to_string(d) + ":\n\n ";
		res += docs[d - 1] + '\n';
	}

	if (!matchingVec.empty()) {
		status = DBStatus::Ok;
	}
	else {
		status = DBStatus::DocumentNotFound;
	}

	return res;

}

std::string Collection::toString(DBStatus& status)
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
	status = DBStatus::Ok;
	return result;
}

InvIndDB::InvIndDB()
{
}

void InvIndDB::addCollection(std::string collectionName, DBStatus& status)
{
	if (collections.find(collectionName) != collections.end())
	{
		status = DBStatus::CollectionExists;
		return;
	}
	collections[collectionName] = Collection();
	status = DBStatus::Ok;
}

void InvIndDB::addDocument(std::string collectionName, std::string document, DBStatus& status)
{
	if (collections.find(collectionName) == collections.end())
	{
		status = DBStatus::CollectionNotExists;
		return;
	}
	collections[collectionName].buildIndex(document, status);
}

std::string InvIndDB::getDocsByWord(std::string collectionName, std::string word, DBStatus& status)
{
	if (collections.find(collectionName) == collections.end())
	{
		status = DBStatus::CollectionNotExists;
		return "";
	}

	return collections[collectionName].getDocsByWord(word, status);
}

std::string InvIndDB::getDocsByWordDistance(std::string collectionName, const std::string& word1, const std::string& word2, unsigned int distance, DBStatus& status)
{
	if (collections.find(collectionName) == collections.end())
	{
		status = DBStatus::CollectionNotExists;
		return "";
	}

	return collections[collectionName].getDocsByWordDistance(word1, word2, distance, status);

}

std::string InvIndDB::getIndex(std::string collectionName, DBStatus& status)
{
	auto coll_iter = collections.find(collectionName);
	if (coll_iter != collections.end())
	{
		std::string str = coll_iter->second.toString(status);
		return str;
	}
	status = DBStatus::CollectionNotExists;
	return "";
}

