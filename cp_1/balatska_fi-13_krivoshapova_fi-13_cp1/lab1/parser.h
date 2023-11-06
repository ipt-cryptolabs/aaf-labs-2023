#pragma once
#include <string>
#include <vector>

enum CommandType {
    CREATE,
    INSERT,
    SELECT,
    DELETE,
    UNKNOWN
};

struct Command {
    CommandType type = UNKNOWN;
    std::string table_name;
    std::vector<std::string> columns;
    std::vector<std::string> values;
    std::string condition;
    std::string order_by;
    std::string order;
    std::string select_all;
    std::vector<std::vector<std::string>> data;
    std::string operation;
};

struct SelectionResult {
    std::vector<std::string> columns;
    std::vector<std::vector<std::string>> data;
};


Command parseCommand(std::string input);
