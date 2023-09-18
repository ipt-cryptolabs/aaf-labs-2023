#include <iostream>
#include <iomanip>
#include "functions.h"

// Global colectiond for saving elements
std::vector<Command> collection;

void createTable(const Command& command, std::vector<Command>& collection) {
    // Check if the table exist
    for (const Command& item : collection) {
        if (item.table_name == command.table_name) {
            std::cout << "Table " << command.table_name << " already exists." << std::endl;
            return;
        }
    }

    // Create new table and add to collection
    Command newTable;
    newTable.type = CREATE;
    newTable.table_name = command.table_name;

    // Add column to table
    for (const std::string& column : command.columns) {
        newTable.columns.push_back(column);
    }

    // Add new table to collection
    collection.push_back(newTable);

    std::cout << "Table '" << command.table_name << "' created with columns: ";
    for (size_t i = 0; i < command.columns.size(); ++i) {
        std::cout << command.columns[i];
        if (i < command.columns.size() - 1) {
            std::cout << ", ";
        }
    }
    std::cout << std::endl;
}


void insertRecord(const Command& command, std::vector<Command>& collection, SelectionResult& result) {
    // Searched table
    for (Command& item : collection) {
        if (item.table_name == command.table_name) {
            //Add a new line
            item.values = command.values;

            std::cout << "Inserted record into table " << command.table_name << ": (";
            for (size_t i = 0; i < command.values.size(); ++i) {
                std::cout << command.values[i];
                if (i < command.values.size() - 1) {
                    std::cout << ", ";
                }
            }
            std::cout << ")" << std::endl;

            // Update the data in result.data
            result.columns = item.columns;
            result.data.push_back(item.values); // Add new row to result.data

            // Diaplay the update table
            printSelectionResult(result); 
            return;
        }
    }

    std::cout << "Table " << command.table_name << " not found." << std::endl;
}




void deleteAllRecords() {
    collection.clear(); // Clear the collection

    std::cout << "All records deleted from the collection." << std::endl;
}

void printSelectionResult(const SelectionResult& result) {
    // Виводьте заголовок таблиці, як робили раніше
    std::cout << "+";
    for (const std::string& column : result.columns) {
        for (size_t j = 0; j < column.length() + 2; ++j) std::cout << "-";
        std::cout << "+";
    }
    std::cout << std::endl;

    std::cout << "|";
    for (const std::string& column : result.columns) {
        std::cout << " " << std::left << std::setw(column.length()) << column << " |";
    }
    std::cout << std::endl;

    std::cout << "+";
    for (const std::string& column : result.columns) {
        for (size_t j = 0; j < column.length() + 2; ++j) std::cout << "-";
        std::cout << "+";
    }
    std::cout << std::endl;

    // Виводьте дані результату вибірки
    for (const std::vector<std::string>& row : result.data) {
        std::cout << "|";
        for (size_t i = 0; i < row.size(); ++i) {
            std::cout << " " << std::setw(result.columns[i].length()) << row[i] << " |";
        }
        std::cout << std::endl;

        // Виводьте роздільник між записами
        std::cout << "+";
        for (const std::string& column : result.columns) {
            for (size_t j = 0; j < column.length() + 2; ++j) std::cout << "-";
            std::cout << "+";
        }
        std::cout << std::endl;
    }
}
