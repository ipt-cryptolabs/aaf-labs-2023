#include "functions.h"
#include "parser.h"
#include <iostream>
#include <string>
#include <sstream>

int main() {
    std::string input;
    SelectionResult result;  
    bool selectMode = false; 
    std::vector<Command> collection;

    while (true) {
        std::cout << "Enter a command (or 'exit' to quit): ";
        std::getline(std::cin, input);

        if (input == "exit") {
            break;
        }

        Command command = parseCommand(input);

        switch (command.type) {
        case CREATE:
            createTable(command, collection);
            break;
        case INSERT:
            insertRecord(command, collection, result);
            break;
        case DELETE:
            deleteAllRecords();
            break;
        case SELECT:
            selectMode = true; 
            std::cout << "Enter the columns to select (comma-separated, or '*' for all columns): ";

            std::getline(std::cin, input);
            if (input == "*") {
                result.columns = command.columns; 

                result.data.clear();

                for (const Command& item : collection) {
                    if (item.table_name == command.table_name) {
                        result.data.push_back(item.values);
                    }
                }
            }
            else {
                std::vector<std::string> columnsToPrint;
                std::istringstream iss(input);
                std::string column;
                while (std::getline(iss, column, ',')) {
                    columnsToPrint.push_back(column);
                }

                result.columns = columnsToPrint;
            }
        case UNKNOWN:
            std::cout << "Unknown command." << std::endl;
            break;
        }
    }

    if (selectMode) {
        printSelectionResult(result);
    }

    return 0;
}
