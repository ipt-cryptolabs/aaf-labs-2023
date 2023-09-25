#include "invertedIndex.hpp"

// std::string Parser::mergeTokens(const std::vector<std::string>& tokens) {
//     std::string res;

//     for(const auto& token : tokens)
//         res += token + " ";

//     return res;
// }

std::string Parser::lexer(std::string inputString) {
    std::regex insertPattern("^\\s*INSERT\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s+\\{(.+?)\\};\\s*$", std::regex::icase);
    std::smatch match;

    if (std::regex_match(inputString, match, insertPattern)) {
        std::string collectionName = match[1];
        std::string values = match[2];
        
        std::regex identifierPattern("[a-zA-Z][a-zA-Z0-9_]*");
        if (std::regex_match(collectionName, identifierPattern)) {
            std::cout << "Collection Name: " << collectionName << std::endl;
            std::cout << "Values: " << values << std::endl << std::endl;
        } else {
            std::cout << "Invalid collection name." << std::endl << std::endl;
        }
    } else {
        std::cout << "Invalid command." << std::endl << std::endl;
    }

    return inputString;
}

















































































void InvertedIndex::insert() {
    std::cout << "InvertedIndex::insert() called\n";
}

void InvertedIndex::create() {
    std::cout << "InvertedIndex::create() called\n";
    
}

void InvertedIndex::print_index() {
    std::cout << "InvertedIndex::print_index() called\n";
    
}

void InvertedIndex::contains() {
    std::cout << "InvertedIndex::contains() called\n";
    
}

void InvertedIndex::search() {
    std::cout << "InvertedIndex::search() called\n";
    
}