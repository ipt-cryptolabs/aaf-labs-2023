#include "parser.h"
#include <iostream>
#include <sstream>

Command parseCommand(std::string input) {
    Command command;
    std::stringstream ss(input);
    std::string token;

    ss >> token;

    if (token == "CREATE") {
        command.type = CREATE;
        ss.ignore(); // Ignore the table name
        ss >> command.table_name;
        ss.ignore(); // Ignore the '(' character
        std::string column;
        while (ss >> column) {
            if (column == ")") break;
            command.columns.push_back(column);
        }
    }
    else if (token == "INSERT") {
        command.type = INSERT;
        ss >> command.table_name; // Read the table name directly
        std::string value;
        while (ss >> value) {
            if (value == ")") break;
            command.values.push_back(value);
        }
    }
    else if (token == "SELECT") {
        command.type = SELECT;
        ss.ignore(); // Ignore the "FROM" keyword
        ss >> command.table_name;
    }
    else if (token == "DELETE") {
        command.type = DELETE;
    }
    else {
        command.type = UNKNOWN;
    }

    return command;
}

