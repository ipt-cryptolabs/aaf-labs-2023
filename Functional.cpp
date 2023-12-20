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

    std::vector<std::vector<int>> select(const std::vector<std::string>& select_columns, const std::string& where_condition, const std::vector<std::string>& group_by) {

        std::vector<std::pair<std::string, bool>> full_columns = this->columns;
        bool selected_manually = true;
        std::vector<std::vector<int>> filtered_data;

        if (!where_condition.empty()) {
            std::istringstream iss(where_condition);
            std::string col_name, operator_str, value_str;
            iss >> col_name >> operator_str >> value_str;

            col_name = col_name.erase(std::remove_if(col_name.begin(), col_name.end(), ::isspace), col_name.end());
            int col_index = -1;

            // Check for index existence and use it for searching
            if (indexed_columns.find(col_name) != indexed_columns.end() && indexed_columns[col_name]) {
                // Find the index of the column in self.columns
                auto iter = std::find_if(columns.begin(), columns.end(), [col_name](const auto& col) {
                    return col.first == col_name;
                    });

                if (iter != columns.end()) {
                    col_index = std::distance(columns.begin(), iter);
                }

                if (col_index != -1) {
                    if (operator_str == "=") {
                        // Use index for exact match
                        auto rows_to_select = indexed_columns[col_name].search(std::stoi(value_str));
                        for (const auto& row : rows_to_select) {
                            if (row < data.size()) {
                                filtered_data.push_back(data[row]);
                            }
                        }
                    }
                    else if (operator_str == "<" || operator_str == ">") {
                        // Use index for range search
                        auto int_value = std::stoi(value_str);
                        auto rows_to_select = (operator_str == "<") ? indexed_columns[col_name].range_search(nullptr, int_value) : indexed_columns[col_name].range_search(int_value, nullptr);
                        for (const auto& row : rows_to_select) {
                            if (row < data.size()) {
                                filtered_data.push_back(data[row]);
                            }
                        }
                    }
                }
            }
        }

        if (filtered_data.empty()) {
            // If indices cannot be used, manually filter the data
            for (const auto& row : data) {
                // If the WHERE condition is empty or evaluates to true, add the row to filtered_data
                if (where_condition.empty() || evaluate_condition(where_condition, row)) {
                    filtered_data.push_back(row);
                }
            }
        }

        if (!grouped_data.empty()) {
            // If grouping is required
            std::unordered_map<std::tuple<int, int>, std::vector<int>> grouped_data;

            // Obtaining indices for grouping
            std::vector<int> group_indices;
            for (int i = 0; i < full_columns.size(); ++i) {
                const auto& [col, _] = full_columns[i];
                if (std::find(group_by.begin(), group_by.end(), col) != group_by.end()) {
                    group_indices.push_back(i);
                }
            }

            // Filling grouped_data
            for (const auto& row : filtered_data) {
                std::tuple<int, int> group_key;
                for (int i : group_indices) {
                    group_key += std::make_tuple(row[i]);
                }

                if (grouped_data.find(group_key) == grouped_data.end()) {
                    grouped_data[group_key] = std::vector<int>();
                }

                grouped_data[group_key].push_back(row);
            }

            std::vector<std::vector<int>> result_data;

            if (!grouped_data.empty()) {
                // If there are grouped data
                for (const auto& [group_key, group_rows] : grouped_data) {
                    std::vector<int> agg_values;

                    // Processing each aggregation function
                    for (const auto& agg_func : select_columns) {
                        if (agg_func.find('(') != std::string::npos && agg_func.find(')') != std::string::npos) {
                            std::string func_name = agg_func.substr(0, agg_func.find('('));
                            std::string col_name = agg_func.substr(agg_func.find('(') + 1, agg_func.find(')') - agg_func.find('(') - 1);

                            int col_index = -1;

                            for (int i = 0; i < full_columns.size(); ++i) {
                                const auto& [col, _] = full_columns[i];
                                if (col == col_name) {
                                    col_index = i;
                                    break;
                                }
                            }

                            if (col_index != -1) {
                                // Performing aggregation based on the function
                                if (func_name == "COUNT") {
                                    agg_values.push_back(group_rows.size());
                                }
                                else if (func_name == "MAX") {
                                    int max_value = *std::max_element(group_rows.begin(), group_rows.end(),
                                        [col_index](const auto& row1, const auto& row2) {
                                            return row1[col_index] < row2[col_index];
                                        });
                                    agg_values.push_back(max_value);
                                }
                                else if (func_name == "AVG") {
                                    int sum = 0;
                                    for (const auto& row : group_rows) {
                                        sum += row[col_index];
                                    }
                                    agg_values.push_back(sum / group_rows.size());
                                }
                            }
                        }
                        else {
                            int col_index = -1;

                            for (int i = 0; i < full_columns.size(); ++i) {
                                const auto& [col, _] = full_columns[i];
                                if (col == agg_func) {
                                    col_index = i;
                                    break;
                                }
                            }

                            if (col_index != -1) {
                                // Adding the grouped value for non-aggregate columns
                                agg_values.push_back(group_key[group_indices.index(col_index)]);
                            }
                        }
                    }

                    result_data.push_back(agg_values);
                }
            }
            else {
                // If there is no grouped data, use filtered data directly
                result_data = filtered_data;
            }

            if (select_columns.empty()) {
                // If no specific columns are selected, use all columns
                select_columns = full_columns;
                selected_manually = false;
            }

            if (select_columns.empty()) {
                // If still no columns are specified, return an empty vector
                return {};
            }

            if (!selected_manually) {
                // If columns were not manually selected, use only the first element of each column pair
                select_columns = { col.first for col in select_columns };
            }

            std::vector<std::vector<int>> formatted_result;
            formatted_result.push_back(select_columns);

            for (const auto& row : result_data) {
                formatted_result.push_back(row);
            }

            return formatted_result;

            // Evaluate condition method checks if a given condition is satisfied for a row
            bool evaluateCondition(const std::string & condition, const std::vector<int>&row) {
                std::istringstream iss(condition);
                std::string col_name, op, val;
                iss >> col_name >> op >> val;

                col_name = trim(col_name); // Function trim removes leading and trailing spaces from a string
                int col_index = -1;

                for (int i = 0; i < columns.size(); ++i) {
                    if (col_name == columns[i]) {
                        col_index = i;
                        break;
                    }
                }

                if (col_index == -1) {
                    // Column not found
                    return false;
                }

                int value = std::stoi(val);

                if (op == "=") {
                    return row[col_index] == value;
                }
                else if (op == "!=") {
                    return row[col_index] != value;
                }
                else if (op == "<") {
                    return row[col_index] < value;
                }
                else if (op == ">") {
                    return row[col_index] > value;
                }
                else if (op == "<=") {
                    return row[col_index] <= value;
                }
                else if (op == ">=") {
                    return row[col_index] >= value;
                }
                else {
                    return false;
                }
            }
        }

    }
}

class Database {
private:
    std::unordered_map<std::string, Table> tables;

public:
    Database() {}
    void create_table(const std::string& name, const std::vector<std::pair<std::string, bool>>& columns);


};
