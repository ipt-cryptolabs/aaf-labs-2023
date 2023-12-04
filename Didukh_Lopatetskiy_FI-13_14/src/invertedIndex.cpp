#include "invertedIndex.hpp"

void Collections::parse(const std::string& inputString) {
    parser.lexer(inputString);
    auto tokens = parser.getTokens(); 
    
    if(tokens.size()) {
        std::string collectionName = tokens.at(1);

        if(tokens.at(0) == "INSERT") 
            insertSet(collectionName, getSetFromTokens(tokens));

        if(tokens.at(0) == "CREATE")
            createCollection(collectionName);

        if(tokens.at(0) == "PRINT_INDEX") 
            printCollectionIndex(tokens.at(1));

        if(tokens.at(0) == "SEARCH") 
            searchInCollection(collectionName);

        if(tokens.at(0) == "CONTAINS") 
            containsCollection(collectionName, getSetFromTokens(tokens));
    } else {
        std::cout << "Error: Invalid command syntaxis, try again.\n";
    }

}

void Collections::createCollection(const std::string& collectionName) {
    if (collections.find(collectionName) != collections.end()) {
        std::cout << "Error: Creating collection with existing name '" << collectionName << "'" << std::endl;
    } else {
        collections[collectionName] = Collection();
        std::cout << "Collection '" << collectionName << "' has been created." << std::endl;
    }
}

void Collections::insertSet(const std::string& collecntionName, const std::set<int>& set) {
    collections[collecntionName].insert(set);
    std::cout << "Set has been added to " << collecntionName << std::endl;
}

void Collections::printCollectionIndex(const std::string &collectionName) {
    std::cout << "Printing " << collectionName << "collection...\n";
    collections[collectionName].print_index();
}

std::vector<std::set<int>> Collections::searchInCollection(const std::string& collectionName) {
    std::vector<std::set<int>> resultSets;

    if (collections.find(collectionName) != collections.end()) {
        std::cout << "Collection '" << collectionName << "' exists in collections\n";
        resultSets = collections[collectionName].getSets();
    } else {
        std::cout << "Collection '" << collectionName << "' doesn't exist in collections\n";
    }

    return resultSets;
}

bool Collections::containsCollection(const std::string &collectionName, const std::set<int> &set) {
    if (collections.find(collectionName) == collections.end()) {
        std::cout << "Error: Contains method called in collection that doesn't exist '" << collectionName << "'" << std::endl;
        return false;
    } else {
        Collection& currentCollection = collections[collectionName];

        bool found = false;
        for (const auto& existingSet : currentCollection.getSets()) {
            if (existingSet == set) {
                found = true;
                break;
            }
        }

        if (found) {
            std::cout << "Collection '" << collectionName << "' contains the set." << std::endl;
            return true;
        } else {
            std::cout << "Collection '" << collectionName << "' does not contain the set." << std::endl;
            return false;
        }
    }
}

void Collection::insert(const std::set<int>& set) {
    sets.push_back(set);
    
    for(auto it = set.begin(); it != set.end(); ++it) {
        invertedIndex[*it].push_back("set" + std::to_string(sets.size()));
    }
}

void Collection::print_index() {
    for(const auto& pair : invertedIndex) {
        std::cout << pair.first << ": ";
        
        for(const auto& name : pair.second)
            std::cout << name << " ";
        
        std::cout << std::endl;
    }
}