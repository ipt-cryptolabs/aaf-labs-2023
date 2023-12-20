#include <iostream>
#include <vector>
#include <unordered_map>
#include <Parser.cpp>
using namespace std;

class TreeNode {
public:
    int key;
    int value;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int k, int v) : key(k), value(v), left(nullptr), right(nullptr) {}
};

class Index {
private:
    TreeNode* root;

    TreeNode* _insert_recursive(TreeNode* node, int key, int value) {
        if (node == nullptr) {
            return new TreeNode(key, value);
        }

        if (key < node->key) {
            node->left = _insert_recursive(node->left, key, value);
        }
        else if (key > node->key) {
            node->right = _insert_recursive(node->right, key, value);
        }

        return node;
    }

    int _search_recursive(TreeNode* node, int key) {
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

    void _range_search_recursive(TreeNode* node, int low, int high, std::vector<int>& result) {
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
    std::vector<std::string> columns;
    std::vector<std::vector<int>> data;
    std::unordered_map<std::string, Index> indexed_columns;

public:

    Table(const std::string& name, const std::vector<std::string>& columns) {     // Class constructor Table

        // Use the isValidTableName function to check the correctness of the table name from the parser

        if (Parser::isValidTableName(name)) {

            this->name = name;
            this->columns = columns;
            std::vector<int> data;
            std::unordered_map<int, int> indexed_columns;

        }
        else {
            cout << "Invalid table name !" << endl;
        }
    }

    // Verify the correctness of column names. We use the isValidColumnName function from the parser.

    void checkColumnNamesValidity() {
        for (const auto& col : columns) {
            const std::string& col_name = col.first;
            if (!(Parser::isValidColumnName(col_name))) {
                std::cout << "Invalid column name: " << col_name << std::endl;
                return;
            }
        }
    }

    void create_index(const std::string& column_name) {
       
        if (!(Parser::isValidColumnName(column_name))) {
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
                const auto& indexed = indexed_column.second;

                // Check if the column is indexed
                if (indexed) {
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










}