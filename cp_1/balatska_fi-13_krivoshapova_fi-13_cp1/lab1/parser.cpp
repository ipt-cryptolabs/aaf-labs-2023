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
        std::string value;
        ss >> token;
        if (token == "INTO") {
            // If "INTO" was find, read the name of table
            ss >> command.table_name;
            while (ss >> value) {
                if (value == ")") break;
                command.values.push_back(value);
            }
        }
        else {
            // If "INTO" wasn't find, token = name of table
            command.table_name = token;
            while (ss >> value) {
                if (value == ")") break;
                command.values.push_back(value);
            }
        }
       
    }
    else if (token == "SELECT") {
        command.type = SELECT;
        ss >> token;
        if (token == "FROM") {
            // If "FROM" was find, read the name of table
            ss >> command.table_name;
            ss >> token;
            if (token == "WHERE") {
                //std::getline(ss, command.condition);
                ss >> command.condition;
            }
        }
        else {
            // If "FROM" wasn't find, token = name of table
            command.table_name = token;
            ss >> token;
            if (token == "WHERE") {
                //std::getline(ss, command.condition);
                ss >> command.condition;
            }
        }
    }
    else if (token == "DELETE") {
        command.type = DELETE;
    }
    else {
        command.type = UNKNOWN;
    }

    return command;
}

