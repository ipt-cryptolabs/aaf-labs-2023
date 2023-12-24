#include "parser.h"
#include <iostream>
#include <sstream>
#include <cctype>  
#include <stdexcept> 
#include <algorithm> 

std::string trim(const std::string& str) {
    
    size_t first = str.find_first_not_of(' ');
    size_t last = str.find_last_not_of(' ');
    return str.substr(first, (last - first + 1));
}

Command parseCommand(std::string input) {


    Command command;
    std::stringstream ss(input);
    std::string token;

    ss >> token;


    if (token == "CREATE" || token == "create") {
        command.type = CREATE;
        // Read the table name (even if there's no space)
        //ss.ignore(); // Ignore the '(' or space
        std::getline(ss, command.table_name, '(');

        // Trim leading and trailing spaces from the table name
        command.table_name = trim(command.table_name);

        // Read the columns
        std::string column;
        while (ss >> column) {
            if (column.back() == ',')
            {
                column.pop_back();
            }
            if (column.back() == ';')
            {
                column.pop_back();
            }
            if (column.back() == ')')
            {
                column.pop_back();
            }

            size_t Comma = column.find(",");
            if (Comma != std::string::npos) {
                std::string substring = column.substr(Comma);
                ss << 256;
                continue;
            }

            command.columns.push_back(column);
        }
    }

    else if (token == "INSERT" || token == "insert") {
        command.type = INSERT;
        ss >> token;
        if (token == "INTO" || token == "into") {
            // If "INTO" was found, read the name of the table
            ss >> command.table_name;

            // Ignore everything until an opening parenthesis "(" is found
            ss.ignore(std::numeric_limits<std::streamsize>::max(), '(');

            // Read values inside parentheses
            std::string value;
            while (ss >> value) {
                // Remove trailing comma or semicolon if present
                if (value.size() >= 2 && (value[value.size() - 1] == ',' || value[value.size() - 1] == ';' || value[value.size() - 2] == ',' || value[value.size() - 2] == ';')) {
                    value.pop_back();
                    value.pop_back();
                }

                // Remove double quotes from the value
                value.erase(std::remove(value.begin(), value.end(), '"'), value.end());

                // Add the value to the command
                command.values.push_back(value);

                // Check if the last character is the closing parenthesis ")"
                if (value.find(')') != std::string::npos) {
                    break;
                }
            }
        }
        else {
            // If "INTO" wasn't found, token = name of the table
            command.table_name = token;

            // Ignore everything until an opening parenthesis "(" is found
            ss.ignore(std::numeric_limits<std::streamsize>::max(), '(');

            // Read values inside parentheses
            std::string value;
            while (ss >> value) {
                // Remove trailing comma or semicolon if present
                if (value.size() >= 2 && (value[value.size() - 1] == ',' || value[value.size() - 1] == ';' || value[value.size() - 2] == ',' || value[value.size() - 2] == ';')) {
                    value.pop_back();
                    value.pop_back();
                }

                // Remove double quotes from the value
                value.erase(std::remove(value.begin(), value.end(), '"'), value.end());

                // Add the value to the command
                command.values.push_back(value);

                // Check if the last character is the closing parenthesis ")"
                if (value.find(')') != std::string::npos) {
                    break;
                }
            }
        }
    }



    else if (token == "SELECT" || token == "select") {
        command.type = SELECT;
        ss >> token;
        if (token == "FROM" || token == "from") {
            // If "FROM" was found, read the name of the table
            ss >> command.table_name;
            ss >> token;
            if (token == "WHERE" || token == "where") {
                ss.ignore(); // Ignore the space after WHERE
                std::getline(ss, command.condition); // Read the entire condition line
            }
            if (token == "ORDER_BY" || token == "order_by") {
                std::string order_by_column;
                std::string order;
                while (ss >> order_by_column) {
                    // Check for ASC or DESC
                    if (order_by_column == "ASC" || order_by_column == "asc" || order_by_column == "DESC" || order_by_column == "desc") {
                        order = order_by_column;
                        break;
                    }
                    // If not ASC or DESC, it's a column name
                    command.order_by_column = order_by_column;
                    // Check for the next token after the column name
                    ss >> order_by_column;
                    if (order_by_column == "ASC" || order_by_column == "asc" || order_by_column == "DESC" || order_by_column == "desc") {
                        order = order_by_column;
                        break;
                    }
                }
                command.order = order;
            }
        }
    }
    else if (token == "DELETE" || token == "delete") {
        command.type = DELETE;
    }
    else {
        command.type = UNKNOWN;
    }
    if (input.back() != ';') {
        command.type = UNKNOWN;
        std::cerr << "Error: Missing semicolon at the end of the command.\n";
        return command;
    }

    return command;
}

