#include "invertedIndex.hpp"

void Parser::lexer(std::string inputString) {
    clearTokens();
    std::smatch match;

    if(std::regex_match(inputString, match, createPattern)) {
        std::string commandName = "CREATE";
        std::string collectionName = match[1];

        if (std::regex_match(collectionName, identifierPattern)) {
            tokens.push_back(commandName);
            tokens.push_back(collectionName);
        } else {
            std::cout << "Invalid collection name." << std::endl << std::endl;
        }
    }

    if (std::regex_match(inputString, match, insertPattern)) {
        std::string commandName = "INSERT";
        std::string collectionName = match[1];
        std::string values = match[2];

        if (std::regex_match(collectionName, identifierPattern)) {
            tokens.push_back(commandName);
            tokens.push_back(collectionName);
        
            std::sregex_iterator it(values.begin(), values.end(), numberPattern);
            std::sregex_iterator end;
            
            while (it != end) {
                std::smatch match = *it;
                std::string numberToken = match[1];
                tokens.push_back(numberToken);
                ++it;
            }
        } else {
            std::cout << "Invalid collection name." << std::endl << std::endl;
        }
    }

    if (std::regex_match(inputString, match, printIndexPattern)) {
        std::string commandName = "PRINT_INDEX";
        std::string collectionName = match[1];

        if (std::regex_match(collectionName, identifierPattern)) {
            tokens.push_back(commandName);
            tokens.push_back(collectionName);
        } else {
            std::cout << "Invalid collection name." << std::endl << std::endl;
        }
    }

    if (std::regex_match(inputString, match, searchPattern)) {
        std::string commandName = "SEARCH";
        std::string collectionName = match[1];
        std::string values = match[2];

        if (std::regex_match(collectionName, identifierPattern)) {
            tokens.push_back(commandName);
            tokens.push_back(collectionName);
        
            std::sregex_iterator it(values.begin(), values.end(), numberPattern);
            std::sregex_iterator end;
            
            while (it != end) {
                std::smatch match = *it;
                std::string numberToken = match[1];
                tokens.push_back(numberToken);
                ++it;
            }
        } else {
            std::cout << "Invalid collection name." << std::endl << std::endl;
        }
    }

    if (std::regex_match(inputString, match, containsPattern)) {
        std::string commandName = "CONTAINS";
        std::string collectionName = match[1];
        std::string values = match[2];

        if (std::regex_match(collectionName, identifierPattern)) {
            tokens.push_back(commandName);
            tokens.push_back(collectionName);
        
            std::sregex_iterator it(values.begin(), values.end(), numberPattern);
            std::sregex_iterator end;
            
            while (it != end) {
                std::smatch match = *it;
                std::string numberToken = match[1];
                tokens.push_back(numberToken);
                ++it;
            }
        } else {
            std::cout << "Invalid collection name." << std::endl << std::endl;
        }
    }
}

std::vector<std::string> Parser::getTokens() {
    return tokens;
}

void Parser::clearTokens() {
    tokens.clear();
}


void Collections::parse(const std::string& inputString) {
    parser.lexer(inputString);
    auto tokens = parser.getTokens(); 

    for(int i = 0; i < tokens.size(); i++) {
        int collectionNamePosition = 0;

        if(tokens.at(i) == "INSERT") {
            std::string collectionName = tokens.at(i + 1);
            std::set<int> setToInsert;

            for(int j = collectionNamePosition + 1; j < tokens.size(); j++) {
                try{
                    setToInsert.emplace(std::stoi(tokens.at(j)));
                } catch(const std::invalid_argument& e) {
                
                }
            } 
            insertSet(collectionName, setToInsert);
            break;
        }

        if(tokens.at(i) == "CREATE") {
            createCollection(tokens.at(i + 1));
            break;
        }

        if(tokens.at(i) == "PRINT_INDEX") {
            printCollectionIndex(tokens.at(i + 1));
            break;
        }

        if(tokens.at(i) == "SEARCH") {
            std::string collectionName = tokens.at(i + 1);
            std::set<int> setToInsert;

            for(int j = collectionNamePosition + 1; j < tokens.size(); j++) {
                try{
                    setToInsert.emplace(std::stoi(tokens.at(j)));
                } catch(const std::invalid_argument& e) {
                
                }
            } 
            searchInCollection(collectionName, setToInsert);
            break;
        }

        if(tokens.at(i) == "CONTAINS") {
            std::string collectionName = tokens.at(i + 1);
            std::set<int> setToInsert;

            for(int j = collectionNamePosition + 1; j < tokens.size(); j++) {
                try{
                    setToInsert.emplace(std::stoi(tokens.at(j)));
                } catch(const std::invalid_argument& e) {
                
                }
            }
            containsCollection(collectionName, setToInsert);
            break;
        }
    }

}


void Collections::createCollection(const std::string& collectionName) {
    collections[collectionName] = Collection();
    std::cout << "Collection " << collectionName << " has been created." << std::endl;
}

void Collections::insertSet(const std::string& collecntionName, const std::set<int>& set) {
    collections[collecntionName].insert(set);
}

void Collections::printCollectionIndex(const std::string &collectionName) {
    collections[collectionName].print_index();
}

void Collection::insert(const std::set<int>& set) {
    sets.push_back(set);
    
    for(auto it = set.begin(); it != set.end(); ++it) {
        invertedIndex[*it].push_back("set" + std::to_string(sets.size()));
    }
}

void Collections::searchInCollection(const std::string& collectionName, const std::set<int>& set) {
    std::cout << "search in collection will be executed with this input: " << collectionName << ", ";
    
    for(const auto& num : set)
        std::cout << num << " ";
    
    std::cout << std::endl;
}

void Collections::containsCollection(const std::string &collectionName, const std::set<int> &set) {
    std::cout << "contains will be executed with this input: " << collectionName << ", ";
    
    for(const auto& num : set)
        std::cout << num << " ";
    
    std::cout << std::endl;
}

void Collection::print_index() {
    for(const auto& pair : invertedIndex) {
        std::cout << pair.first << ": ";
        
        for(const auto& name : pair.second)
            std::cout << name << " ";
        
        std::cout << std::endl;
    }
}