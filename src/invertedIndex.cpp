#include "invertedIndex.hpp"

void Parser::processCommand(const std::smatch& match, const std::string& commandName) {
    std::string collectionName = match[1];

    if (std::regex_match(collectionName, identifierPattern)) {
        tokens.push_back(commandName);
        tokens.push_back(collectionName);
    } else {
        std::cout << "Invalid collection name." << std::endl << std::endl;
    }
}

void Parser::processCreateCommand(const std::smatch& match) {
    processCommand(match, "CREATE");
}

void Parser::processPrintIndexCommand(const std::smatch& match) {
    processCommand(match, "PRINT_INDEX");
}

void Parser::processCommandWithValues(const std::smatch& match, const std::string& commandName) {
    std::string collectionName = match[1];
    std::string values = match[2];

    if (std::regex_match(collectionName, identifierPattern)) {
        tokens.push_back(commandName);
        tokens.push_back(collectionName);

        std::sregex_iterator it(values.begin(), values.end(), numberPattern);
        std::sregex_iterator end;

        while (it != end) {
            std::smatch numberMatch = *it;
            std::string numberToken = numberMatch[1];
            tokens.push_back(numberToken);
            ++it;
        }
    } else {
        std::cout << "Invalid collection name." << std::endl << std::endl;
    }
}

void Parser::processInsertCommand(const std::smatch& match) {
    processCommandWithValues(match, "INSERT");
}

void Parser::processSearchCommand(const std::smatch& match) {
    processCommandWithValues(match, "SEARCH");
}

void Parser::processContainsCommand(const std::smatch& match) {
    processCommandWithValues(match, "CONTAINS");
}

void Parser::lexer(std::string inputString) {
    clearTokens();
    std::smatch match;

    if(std::regex_match(inputString, match, createPattern))
        processCreateCommand(match);

    if (std::regex_match(inputString, match, insertPattern)) 
        processInsertCommand(match);

    if (std::regex_match(inputString, match, printIndexPattern))
        processPrintIndexCommand(match);

    if (std::regex_match(inputString, match, searchPattern))
        processSearchCommand(match);

    if (std::regex_match(inputString, match, containsPattern))
        processContainsCommand(match);
}

std::vector<std::string> Parser::getTokens() {
    return tokens;
}

void Parser::clearTokens() {
    if(tokens.size())
        tokens.clear();
}

std::set<int> Collections::getSetFromTokens(const std::vector<std::string>& tokens) {
    std::set<int> setToInsert;
    for(int j = 2; j < tokens.size(); j++) {
        try{
            setToInsert.emplace(std::stoi(tokens.at(j)));
        } catch(const std::invalid_argument& e) {
        
        }
    } 

    return setToInsert;
}

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
            searchInCollection(collectionName, getSetFromTokens(tokens));

        if(tokens.at(0) == "CONTAINS") 
            containsCollection(collectionName, getSetFromTokens(tokens));
    } else {
        std::cout << "Invalid command, try again.\n";
    }

}

void Collections::createCollection(const std::string& collectionName) {
    collections[collectionName] = Collection();
    std::cout << "Collection " << collectionName << " has been created." << std::endl;
}

void Collections::insertSet(const std::string& collecntionName, const std::set<int>& set) {
    collections[collecntionName].insert(set);
    std::cout << "Set has been added to " << collecntionName << std::endl;
}

void Collections::printCollectionIndex(const std::string &collectionName) {
    std::cout << "Printing " << collectionName << "collection...\n";
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