#include <iostream>
#include <iomanip>
#include <sstream>
#include "functions.h"
#include <algorithm>


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
           // printSelectionResult(result); 
            return;
        }
    }

    std::cout << "Table " << command.table_name << " not found." << std::endl;
}

/*void performSelect(const Command& command, const std::vector<Command>& collection, SelectionResult& result) {
    // Only clear if you want to start with an empty result
    // result.columns.clear();
    // result.data.clear();

    for (const Command& item : collection) {
        if (item.table_name == command.table_name) {
            // Store the columns only once (if they are not already stored)
            if (result.columns.empty()) {
                result.columns = item.columns;
            }

            // Check for the WHERE condition
            if (!command.condition.empty()) {
                std::string column1, column2_or_value, operation;
                std::stringstream cond_stream(command.condition);
                cond_stream >> column1 >> operation >> column2_or_value;

                if (operation == ">" && column1 == item.columns[0]) {
                    // Assuming the first column is the one we are comparing
                    for (const std::vector<std::string>& row : result.data) {
                        if (column2_or_value[0] == '"' && column2_or_value[column2_or_value.size() - 1] == '"') {
                            // Compare with a string value
                            std::string value = column2_or_value.substr(1, column2_or_value.size() - 2);
                            if (row[0] > value) {
                                result.data.push_back(row);
                            }
                        }
                        else {
                            // Compare with another column
                            int col2_idx = -1;
                            for (int i = 0; i < item.columns.size(); i++) {
                                if (item.columns[i] == column2_or_value) {
                                    col2_idx = i;
                                    break;
                                }
                            }
                            if (col2_idx != -1 && row.size() > col2_idx && row[0] > row[col2_idx]) {
                                result.data.push_back(row);
                            }
                        }
                    }
                }
            }
            else {
                // Append all data to result.data
                //result.data.push_back(item.values);
            }
        }
    }
}*/

/*void performSelect(const Command& command, const std::vector<Command>& collection, SelectionResult& result) {
   // result.columns.clear();
   // result.data.clear();
    

    for (const Command& item : collection) {
        if (item.table_name == command.table_name) {
            if (result.columns.empty()) {
                result.columns = item.columns;
            }

            if (!command.condition.empty()) {
                std::string column1, operation, column2_or_value;
                std::stringstream cond_stream(command.condition);
                cond_stream >> column1 >> operation >> column2_or_value;

                for (const std::vector<std::string>& row : item.data) {
                    int col1_idx = -1;
                    int col2_idx = -1;

                    for (int i = 0; i < item.columns.size(); i++) {
                        if (item.columns[i] == column1) {
                            col1_idx = i;
                        }

                        if (column2_or_value[0] != '"' && item.columns[i] == column2_or_value) {
                            col2_idx = i;
                        }
                    }

                    if (col1_idx != -1) {
                        int col1_value = std::stoi(row[col1_idx]);

                        if (operation == ">" && col1_value > std::stoi(column2_or_value)) {
                            result.data.push_back(row);
                        }
                        else if (operation == "=" && col1_value == std::stoi(column2_or_value)) {
                            result.data.push_back(row);
                        }
                    }
                    else if (col2_idx != -1) {
                        if (operation == "=" && row[col2_idx] == column2_or_value) {
                            result.data.push_back(row);
                        }
                    }
                }
            }
            else {
                result.data.insert(result.data.end(), item.data.begin(), item.data.end());
            }
        }
    }
}*/

/*void performSelect(const Command& command, const std::vector<Command>& collection, SelectionResult& result) {
    for (const Command& item : collection) {
        if (item.table_name == command.table_name) {
            if (result.columns.empty()) {
                result.columns = item.columns;
            }

            if (!command.condition.empty()) {
                std::string column1, operation, column2_or_value;
                std::stringstream cond_stream(command.condition);
                cond_stream >> column1 >> operation >> column2_or_value;

                int col1_idx = -1;
                int col2_idx = -1;

                for (int i = 0; i < item.columns.size(); i++) {
                    if (item.columns[i] == column1) {
                        col1_idx = i;
                    }

                    if (column2_or_value[0] != '"' && item.columns[i] == column2_or_value) {
                        col2_idx = i;
                    }
                }

                if (col1_idx != -1) {
                    for (const std::vector<std::string>& row : item.data) {
                        int col1_value = std::stoi(row[col1_idx]);
                        bool conditionSatisfied = false;

                        if (operation == ">" && (col2_idx != -1 ? col1_value > std::stoi(row[col2_idx]) : col1_value > std::stoi(column2_or_value))) {
                            conditionSatisfied = true;
                        }

                        if (conditionSatisfied) {
                            result.data.push_back(row);
                        }
                    }
                }
            }
            else {
                result.data.insert(result.data.end(), item.data.begin(), item.data.end());
            }
        }
    }
}*/

void performSelect(const Command& command, const std::vector<Command>& collection, SelectionResult& result) {
    for (const Command& item : collection) {
        if (item.table_name == command.table_name) {
            if (result.columns.empty()) {
                result.columns = item.columns;
            }

            // Apply WHERE condition
            // (Existing code for WHERE condition)

            // No WHERE condition, include all rows
            result.data.insert(result.data.end(), item.data.begin(), item.data.end());

            // Sort the result data if ORDER BY is specified
            if (!command.order_by_column.empty()) {
                std::vector<std::string> order_by_columns;  // Store the columns to sort by
                std::vector<bool> is_descending;  // Store the sorting order for each column

                std::stringstream order_by_ss(command.order_by_column);
                std::string column;
                while (getline(order_by_ss, column, ',')) {
                    size_t pos = column.find_last_not_of(" \t\n\r\f\v");
                    if (pos != std::string::npos) {
                        column.erase(pos + 1);
                    }
                    size_t space_pos = column.find_last_of(" \t\n\r\f\v");
                    if (space_pos != std::string::npos) {
                        std::string order = column.substr(space_pos + 1);
                        if (order == "ASC") {
                            is_descending.push_back(false);
                        }
                        else if (order == "DESC") {
                            is_descending.push_back(true);
                        }
                        else {
                            // Default to ASC if no explicit order is specified
                            is_descending.push_back(false);
                            column += " " + order;  // Append "ASC" for consistent parsing
                        }
                        column.erase(space_pos);
                    }
                    else {
                        // Default to ASC if no explicit order is specified
                        is_descending.push_back(false);
                    }

                    order_by_columns.push_back(column);
                }

                std::sort(result.data.begin(), result.data.end(), [&](const std::vector<std::string>& a, const std::vector<std::string>& b) {
                    for (size_t i = 0; i < order_by_columns.size(); ++i) {
                        size_t column_index = std::find(result.columns.begin(), result.columns.end(), order_by_columns[i]) - result.columns.begin();
                        if (column_index < result.columns.size()) {
                            if (a[column_index] != b[column_index]) {
                                if (is_descending[i]) {
                                    return a[column_index] > b[column_index];
                                }
                                else {
                                    return a[column_index] < b[column_index];
                                }
                            }
                        }
                    }
                return false;  // Rows are considered equal if all columns are equal
                    });
            }
        }
    }
}




void deleteAllRecords() {
    collection.clear(); // Clear the collection

    std::cout << "All records deleted from the collection." << std::endl;
}

void printSelectionResult(const SelectionResult& result) {
    if (result.columns.empty() || result.data.empty()) {
        std::cout << "No data to print." << std::endl;
        return;
    }

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

    for (const std::vector<std::string>& row : result.data) {
        std::cout << "|";
        for (size_t i = 0; i < row.size(); ++i) {
            if (i < result.columns.size()) {
                std::cout << " " << std::setw(result.columns[i].length()) << row[i] << " |";
            }
        }
        std::cout << std::endl;

        std::cout << "+";
        for (const std::string& column : result.columns) {
            for (size_t j = 0; j < column.length() + 2; ++j) std::cout << "-";
            std::cout << "+";
        }
        std::cout << std::endl;
    }
}

