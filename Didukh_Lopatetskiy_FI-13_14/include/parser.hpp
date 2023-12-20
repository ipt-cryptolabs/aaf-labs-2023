#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <regex>

namespace {
    std::regex insertPattern(R"(^\s*INSERT\s+([a-zA-Z][a-zA-Z0-9_]*)\s+\{((?:\s*[-+]?[0-9]+(?:\s*,\s*[-+]?[0-9]+)*)?)\s*};)", std::regex::icase);
    std::regex createPattern("^\\s*CREATE\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s*;\\s*$", std::regex::icase);
    std::regex printIndexPattern("^\\s*PRINT_INDEX\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s*;\\s*$", std::regex::icase);
    std::regex containsPattern(R"(^\s*CONTAINS\s+([a-zA-Z][a-zA-Z0-9_]*)\s+\{((?:\s*[-+]?[0-9]+(?:\s*,\s*[-+]?[0-9]+)*)?)\s*};)", std::regex::icase);

    std::regex searchPattern("^\\s*SEARCH\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s*;\\s*$", std::regex::icase);
    std::regex intersectsPattern("^\\s*SEARCH\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s+WHERE\\s+INTERSECTS\\s+\\{((?:\\s*[-+]?[0-9]+(?:\\s*,\\s*[-+]?[0-9]+)*)?)\\s*\\};", std::regex::icase);
    std::regex containsSetPattern("^\\s*SEARCH\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s+WHERE\\s+CONTAINS\\s+\\{((?:\\s*[-+]?[0-9]+(?:\\s*,\\s*[-+]?[0-9]+)*)?)\\s*\\};", std::regex::icase);
    std::regex containedByPattern("^\\s*SEARCH\\s+([a-zA-Z][a-zA-Z0-9_]*)\\s+WHERE\\s+CONTAINED_BY\\s+\\{((?:\\s*[-+]?[0-9]+(?:\\s*,\\s*[-+]?[0-9]+)*)?)\\s*\\};", std::regex::icase);


    std::regex identifierPattern("[a-zA-Z][a-zA-Z0-9_]*");
    std::regex numberPattern("\\s*([^,]+)\\s*,?");
}

class Parser {
private:
    std::vector<std::string> tokens;

private:
    // processes commands with this pattern: <command_name> <collection_name>;
    void processCommand(const std::smatch& match, const std::string& commandName);
    // processes commands with this pattern: <command_name> <collection_name> {val1, val2, ... };
    void processCommandWithValues(const std::smatch& match, const std::string& commandName);
   
    void processCreateCommand(const std::smatch& match);
    void processInsertCommand(const std::smatch& match);
    void processPrintIndexCommand(const std::smatch& match);
    void processContainsCommand(const std::smatch& match);
    void processSearchCommand(const std::smatch& match);
    void processIntersectsCommand(const std::smatch& match);
    void processContainsSetCommand(const std::smatch& match);
    void processContainedByCommand(const std::smatch& match);

public:
    void lexer(std::string inputString);
    std::vector<std::string> getTokens();
    void clearTokens();
};