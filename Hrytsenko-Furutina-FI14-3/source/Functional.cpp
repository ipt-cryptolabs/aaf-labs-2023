#include <iostream>
#include <vector>
#include <unordered_map>
#include "Parser.cpp"
#include <string>
#include <regex>
#include <map>
using namespace std;

class Node {
public:
    int key;
    int value;
    Node* left;
    Node* right;

    Node(int k, int v) : key(k), value(v), left(nullptr), right(nullptr) {}
};

class Index {
private:
    Node* root;

    Node* _insert_recursive(Node* node, int key, int value) {
        if (node == nullptr) {
            return new Node(key, value);
        }

        if (key < node->key) {
            node->left = _insert_recursive(node->left, key, value);
        }
        else if (key > node->key) {
            node->right = _insert_recursive(node->right, key, value);
        }

        return node;
    }

    int _search_recursive(Node* node, int key) {
        if (node == nullptr) {
            return -1; 
        }

        if (node->key == key) {
            return node->value;
        }

        if (key < node->key) {
            return _search_recursive(node->left, key);
        }

        return _search_recursive(node->right, key);
    }

    void _range_search_recursive(Node* node, int low, int high, std::vector<int>& result) {
        if (node == nullptr) {
            return;
        }

        if (low < node->key) {
            _range_search_recursive(node->left, low, high, result);
        }

        if (low <= node->key && node->key <= high) {
            result.push_back(node->value);
        }

        if (high > node->key) {
            _range_search_recursive(node->right, low, high, result);
        }
    }

public:
    Index() : root(nullptr) {}

    void insert(int key, int value) {
        root = _insert_recursive(root, key, value);
    }

    int search(int key) {
        return _search_recursive(root, key);
    }

    vector<int> range_search(int low, int high) {
        vector<int> result;
        _range_search_recursive(root, low, high, result);
        return result;
    }
};

class Table {
private:
    std::string name;
    std::vector<std::pair<std::string, int>> columns;
    std::vector<std::vector<int>> data;
    std::map<std::string, Index> indexed_columns;

    bool validateName(const std::string& name) {
        std::regex name_regex(R"(^[a-zA-Z][a-zA-Z0-9_]*$)");
        return std::regex_match(name, name_regex);
    }

public:
   
    Table(const std::string& name, const std::vector<std::pair<std::string, int>>& columns)
        : name(name), columns(columns) {
        if (!validateName(name)) {
            std::cout << "Invalid table name" << std::endl;
            return;
        }

        for (const auto& col : columns) {
            if (!validateName(col.first)) {
                std::cout << "Invalid column name: " << col.first << std::endl;
                return;
            }
        }
    }

    void create_index(const std::string& column_name) {
       
        if (!std::regex_match(column_name, std::regex("^[a-zA-Z][a-zA-Z0-9_]*$"))) {
            std::cout << "Invalid column name" << std::endl;
            return;
        }

        // Check for the existence of a column
        auto col_it = std::find_if(columns.begin(), columns.end(), [column_name](const auto& col) {
            return col.first == column_name;
            });

        if (col_it != columns.end()) {
            // Check if the column is indexed
            if (indexed_columns.find(column_name) == indexed_columns.end()) {
                indexed_columns[column_name] = Index(); 
                std::cout << "Index created for column " << column_name << std::endl;
            }
            else {
                std::cout << "Index already exists for column " << column_name << std::endl;
            }
        }
        else {
            std::cout << "Column does not exist in the table" << std::endl;
        }
    }

    void insert(const std::vector<std::string>& values) {
        // Check if the number of values matches the number of columns
        if (values.size() != columns.size()) {
            std::cout << "Number of values doesn't match the number of columns" << std::endl;
            return;
        }

        try {
            // Convert string values to integers
            std::vector<int> numeric_values;
            for (const auto& value : values) {
                numeric_values.push_back(std::stoi(value));
            }

            // Add the row of numeric values to the data of the table
            data.push_back(numeric_values);
            std::cout << "1 row has been inserted into " << name << "." << std::endl;

            // Update the indexes for indexed columns
            for (const auto& indexed_column : indexed_columns) {
                const auto& col_name = indexed_column.first;
                const auto& indexed = indexed_column.second; // This should be a boolean value

                // Check if the column is indexed
                if (indexed_columns.find(col_name) != indexed_columns.end()) {
                    auto col_index = std::find(columns.begin(), columns.end(), col_name) - columns.begin();
                    auto col_value = std::stoi(values[col_index]);

                    // Insert the value into the index
                    indexed_columns[col_name].insert(col_value, data.size() - 1);
                }
            }
        }
        catch (const std::invalid_argument& e) {
            std::cout << "All values must be integers" << std::endl;
        }
    }

    std::vector<std::vector<int>> select(const std::vector<std::string>& select_columns, const std::string& where_condition, const std::vector<std::string>& group_by) {

        std::vector<std::pair<std::string, bool>> full_columns ;
        for (const auto& col : this->columns) {
            full_columns.emplace_back(col.first, false); 
        }
        bool selected_manually = true;
        std::vector<std::vector<int>> filtered_data;



    }
};

class Database {
private:
    std::unordered_map<std::string, Table> tables;

public:
    Database() {}
    void create_table(const std::string& name, const std::vector<std::pair<std::string, bool>>& columns);

    void create_table(const std::string& name, const std::vector<std::pair<std::string, bool>>& columns) {
        // Validate the table name using a regular expression
        if (!std::regex_match(name, std::regex("^[a-zA-Z][a-zA-Z0-9_]*$"))) {
            std::cout << "Invalid table name" << std::endl;
            return;
        }

        // Check if the table already exists
        if (tables.find(name) != tables.end()) {
            std::cout << "Table already exists" << std::endl;
            return;
        }

        // Check column names for validity using a regular expression
        for (const auto& [col_name, _] : columns) {
            if (!std::regex_match(col_name, std::regex("^[a-zA-Z][a-zA-Z0-9_]*$"))) {
                std::cout << "Invalid column name: " << col_name << std::endl;
                return;
            }
        }

        // Create a new table with the specified name and columns
        tables[name] = Table(name, columns);

        std::cout << "Table " << name << " has been created" << std::endl;

        // Check if there are INDEXED flags for columns and create corresponding indexes
        for (const auto& [column_name, indexed] : columns) {
            if (indexed) {
                tables[name].create_index(column_name);
            }
        }
    }

    // Display the result of the query
    void display_result(const std::vector<std::string>& column_names, const std::vector<std::vector<std::string>>& data) {
        if (data.empty() || data[0].empty()) {
            std::cout << "No results to display" << std::endl;
            return;
        }

        // Calculate column widths based on the length of the column names and data
        std::vector<std::size_t> column_widths(column_names.size());
        for (std::size_t i = 0; i < column_names.size(); ++i) {
            column_widths[i] = std::max(column_names[i].size(),
                static_cast<std::size_t>(std::max_element(data.begin(), data.end(),
                    [i](const auto& row1, const auto& row2) {
                        return row1[i].size() < row2[i].size();
                    })->at(i).size()));
        }

        // Create a format string for formatting the table
        std::string format_string = "+";
        for (std::size_t width : column_widths) {
            format_string += std::string(width, '-') + "+";
        }

        // Display the frame line
        std::cout << format_string << std::endl;

        // Display the table header
        std::string table_header;
        for (std::size_t i = 0; i < column_names.size(); ++i) {
            table_header += "|" + std::string((column_widths[i] - column_names[i].size()) / 2, ' ')
                + column_names[i] + std::string((column_widths[i] - column_names[i].size() + 1) / 2, ' ');
        }
        std::cout << "|" << table_header << "|" << std::endl;

        // Display the frame line
        std::cout << format_string << std::endl;

        // Display the data rows
        for (const auto& row : data) {
            std::string row_str;
            for (std::size_t i = 0; i < column_names.size(); ++i) {
                row_str += "|" + std::string((column_widths[i] - row[i].size()) / 2, ' ')
                    + row[i] + std::string((column_widths[i] - row[i].size() + 1) / 2, ' ');
            }
            std::cout << "|" << row_str << "|" << std::endl;
        }

        // Display the frame line
        std::cout << format_string << std::endl;
    }

    void create_index(const std::string& table_name, const std::string& column_name) {
        if (tables.find(table_name) != tables.end()) {
            Table& table = tables[table_name];
            table.create_index(column_name);
        }
        else {
            std::cout << "Table " << table_name << " does not exist" << std::endl;
        }
    }

    void insert_into_table(const std::string& table_name, const std::vector<std::string>& values) {
        if (tables.find(table_name) != tables.end()) {
            Table& table = tables[table_name];
            table.insert(values);
        }
        else {
            std::cout << "Table " << table_name << " does not exist" << std::endl;
        }
    }

    std::vector<std::vector<int>> select_from_table(const std::string& table_name, const std::vector<std::string>& select_columns, const std::string& where_condition, const std::vector<std::string>& group_by_columns) {
        if (tables.find(table_name) != tables.end()) {
            Table& table = tables[table_name];
            return table.select(select_columns, where_condition, group_by_columns);
        }
        else {
            std::cout << "Table " << table_name << " does not exist" << std::endl;
            return std::vector<std::vector<int>>(); // Return an empty vector as a placeholder for the non-existent table
        }
    }


};
