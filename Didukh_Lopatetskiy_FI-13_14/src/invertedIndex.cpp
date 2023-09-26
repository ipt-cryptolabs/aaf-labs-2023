#include "invertedIndex.hpp"

void Parser::lexer(std::string inputString) {
    clearTokens();
    std::smatch match;

    if(std::regex_match(inputString, match, createPattern)) {
        std::string commandName = "CREATE";
        std::string collectionName = match[1];

        tokens.push_back(commandName);
        tokens.push_back(collectionName);

        if (std::regex_match(collectionName, identifierPattern)) {
            std::cout << "Collection Name: " << collectionName << std::endl;
            tokens.push_back(collectionName);
        } else {
            std::cout << "Invalid collection name." << std::endl << std::endl;
        }
    }

    if (std::regex_match(inputString, match, insertPattern)) {
        std::string commandName = "INSERT";
        tokens.push_back(commandName);
        std::string collectionName = match[1];
        std::string values = match[2];

        if (std::regex_match(collectionName, identifierPattern)) {
            tokens.push_back(collectionName);
        
            // Tokenize and store individual numbers
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
    } else {
        std::cout << "Invalid command." << std::endl << std::endl;
    }
}

std::vector<std::string> Parser::getTokens() {
    return tokens;
}

void Parser::clearTokens() {
    tokens.clear();
}

void InvertedIndex::parse(std::string inputString) {
    parser.lexer(inputString);
    auto tokens = parser.getTokens(); 
    
    std::cout << std::endl << std::endl;
    for(auto el : tokens)
        std::cout << el << " ";
    std::cout << std::endl << std::endl;

    for(int i = 0; i < tokens.size(); i++) {
        int collectionNamePosition = 0;

        // mb refactor into different functions? like switch or smth
        if(tokens.at(i) == "INSERT") {
            std::string collectionName = tokens.at(i + 1);
            std::vector<int> collectionToInsert;

            for(int j = collectionNamePosition + 1; j < tokens.size(); j++) {
                try{
                    collectionToInsert.push_back(stoi(tokens.at(j)));
                } catch(const std::invalid_argument& e) {
                    
                }
            } 
            
            insert(collectionName, collectionToInsert);
            break;
        }

    }

}

void InvertedIndex::insert(const std::string& collectionName, const std::vector<int>& collection) {
    for(const auto& num : collection)
        invertedIndex[collectionName].push_back(num);
}

void InvertedIndex::create(const std::string& collectionName) {
    std::vector<int> collection;
    invertedIndex.emplace(std::pair(collectionName, collection));
}

void InvertedIndex::print_index() {
    for(const auto& elem : invertedIndex) {
        std::cout << elem.first << ": ";

        for(const auto& num : elem.second) {
            std::cout << num << " ";
        }

        std::cout << std::endl;
    }
}

void InvertedIndex::contains() {
    std::cout << "InvertedIndex::contains() called\n";
    
}

void InvertedIndex::search() {
    std::cout << "InvertedIndex::search() called\n";
    
}