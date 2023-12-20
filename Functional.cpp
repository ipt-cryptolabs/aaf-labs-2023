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

