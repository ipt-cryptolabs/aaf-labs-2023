#include "invertedIndex.hpp"


void Parser::processCommand(const std::smatch& match, const std::string& commandName) {
    std::string collectionName = match[1];

    if (std::regex_match(collectionName, identifierPattern)) {
        tokens.push_back(commandName);
        tokens.push_back(collectionName);
    } else {
        std::cout << "Error: Invalid collection name." << std::endl << std::endl;
    }
}

void Parser::processCreateCommand(const std::smatch& match) {
    processCommand(match, "CREATE");
}

void Parser::processPrintIndexCommand(const std::smatch& match) {
    processCommand(match, "PRINT_INDEX");
}

void Parser::processSearchCommand(const std::smatch& match) {
    processCommand(match, "SEARCH");
}

void Parser::processIntersectsCommand(const std::smatch& match) {
    processCommandWithValues(match, "SEARCH_INTERSECTS");
}

void Parser::processContainsSetCommand(const std::smatch& match) {
    processCommandWithValues(match, "SEARCH_CONTAINS");
}

void Parser::processContainedByCommand(const std::smatch& match) {
    processCommandWithValues(match, "SEARCH_CONTAINED_BY");
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

void Parser::processContainsCommand(const std::smatch& match) {
    processCommandWithValues(match, "CONTAINS");
}

void Parser::lexer(std::string inputString) {
    clearTokens();
    std::smatch match;

    if(std::regex_match(inputString, match, createPattern))
        processCreateCommand(match);

    if(std::regex_match(inputString, match, searchPattern))
        processSearchCommand(match);
    
    if (std::regex_match(inputString, match, insertPattern)) 
        processInsertCommand(match);

    if (std::regex_match(inputString, match, printIndexPattern))
        processPrintIndexCommand(match);

    if (std::regex_match(inputString, match, containsPattern))
        processContainsCommand(match);

    if(std::regex_match(inputString, match, intersectsPattern))
        processIntersectsCommand(match);

    if(std::regex_match(inputString, match, containsSetPattern))
        processContainsSetCommand(match);

    if(std::regex_match(inputString, match, containedByPattern))
        processContainedByCommand(match);
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
