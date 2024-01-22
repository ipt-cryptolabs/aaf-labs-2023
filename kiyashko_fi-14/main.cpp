#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>

struct Point {
    int x, y;

    Point(int _x, int _y) : x(_x), y(_y) {}
};

struct Node {
    std::string treeName;  // Added the name of the tree
    Point point;
    Node* left;
    Node* right;
    Node(const std::string& name, const Point& p) : treeName(name), point(p), left(nullptr), right(nullptr) {}
    Node() = delete;
};

class KDTree {
private:
    Node* root;

    Node* buildTree(std::vector<Point> points, const std::string& treeName, int depth) {
        if (points.empty()) {
            return nullptr;
        }

        int axis = depth % 2;
        int median = points.size() / 2;

        std::nth_element(points.begin(), points.begin() + median, points.end(),
                         [axis](const Point& a, const Point& b) {
                             return axis == 0 ? a.x < b.x : a.y < b.y;
                         });

        Node* node = new Node(treeName, points[median]);
        node->left = buildTree(std::move(std::vector<Point>(points.begin(), points.begin() + median)), treeName, depth + 1);
        node->right = buildTree(std::vector<Point>(points.begin() + median + 1, points.end()), treeName, depth + 1);

        return node;
    }

    

    void printTree() {
        printLeaf(root, "", "");
    }

    void printLeaf(Node* current, std::string prefix, std::string childPrefix) {
        if (current != nullptr) {
            std::cout << prefix << "[" << current->point.x << ", " << current->point.y << "]\n";
            Node* left = current->left;
            if (left == nullptr) {
                printLeaf(current->right, childPrefix + "'---", childPrefix + "    ");
            } else {
                printLeaf(current->right, childPrefix + ">---", childPrefix + "|   ");
                printLeaf(current->left, childPrefix + "'---", childPrefix + "    ");
            }
        }
    }

    bool contains(Node* node, const Point& target, int depth) {
        if (node == nullptr) {
            return false;
        }

        if (node->point.x == target.x && node->point.y == target.y) {
            return true;
        }

        int axis = depth % 2;
        if ((axis == 0 && target.x < node->point.x) || (axis == 1 && target.y < node->point.y)) {
            return contains(node->left, target, depth + 1);
        } else {
            return contains(node->right, target, depth + 1);
        }
    }

    void insert(Node*& node, const std::string& treeName, const Point& point, int depth) {
        if (node == nullptr) {
            node = new Node(treeName, point);
            return;
        }

        int axis = depth % 2;
        if ((axis == 0 && point.x < node->point.x) || (axis == 1 && point.y < node->point.y)) {
            insert(node->left, treeName, point, depth + 1);
        } else {
            insert(node->right, treeName, point, depth + 1);
        }
    }
    
    void check(Node*& node, const std::string& treeName, const Point& point, int depth){
        
    }

    void search(Node* node, const std::string& condition, const std::vector<int>& values, int depth) {
        if (node == nullptr) {
            return;
        }

        int axis = depth % 2;

        if (condition == "CONTAINS" && node->point.x == values[0] && node->point.y == values[1]) {
            std::cout << "(" << node->point.x << ", " << node->point.y << ") ";
        } else if (condition == "INTERSECTS" && node->point.x >= values[0] && node->point.x <= values[1]) {
            std::cout << "(" << node->point.x << ", " << node->point.y << ") ";
        } else if (condition == "LEFT_OF" && node->point.x < values[0]) {
            std::cout << "(" << node->point.x << ", " << node->point.y << ") ";
        }

        if ((axis == 0 && values[axis] < node->point.x) || (axis == 1 && values[axis] < node->point.y)) {
            search(node->left, condition, values, depth + 1);
        }

        if ((axis == 0 && values[axis] >= node->point.x) || (axis == 1 && values[axis] >= node->point.y)) {
            search(node->right, condition, values, depth + 1);
        }
    }
    
    bool treeExists(const std::string& name, Node* node) {
        
        if (node == nullptr) {
            return false;
        }
        if (node->treeName == name) {
            return true;
        }

        return treeExists(name, node->left) || treeExists(name, node->right);
    }

public:
    KDTree() : root(nullptr) {}

    void create(const std::string& name) {
    if (treeExists(name, root)) {
        std::cerr << "A tree with the name " << name << " already exists. Cannot create a new tree." << std::endl;
        return;
    }else{
        root = new Node(name, Point(0,0));  // You can modify the default Point as needed
        std::cout << "Tree created with name: " << name << std::endl;
    }
}

    void insert(const std::string& treeName, const std::vector<int>& values) {
        if (values.size() != 2) {
            std::cerr << "Invalid number of coordinates for insertion." << std::endl;
            return;
        }

        Point point(values[0], values[1]);
        if (root == nullptr) {
            root = new Node(treeName, point);
        } else {
            insert(root, treeName, point, 0);
        }

        std::cout << "Point (" << point.x << ", " << point.y << ") inserted successfully into " << treeName << "." << std::endl;
    }
    
    bool treeExists(const std::string& name) {
        return treeExists(name, root);
    }

    void printTree(const std::string& name) {
        std::cout << "Tree " << name << " contents: " << std::endl;
        printTree();
        std::cout << std::endl;
    }

    bool CONTAINS(const std::string& treeName, const Point& target) {
        return contains(root, target, 0);
    }

    void SEARCH(const std::string& treeName) {
        std::cout << "Searching in " << treeName << ": ";
        printTree();
        std::cout << std::endl;
    }

    void SEARCH(const std::string& treeName, const std::string& condition, const std::vector<int>& values) {
        std::cout << "Searching in " << treeName << " where ";
        if (condition == "CONTAINS") {
            std::cout << condition << " [" << values[0] << ", " << values[1] << "]: ";
        } else if (condition == "INTERSECTS") {
            std::cout << condition << " [" << values[0] << ", " << values[1] << "]: ";
        } else if (condition == "LEFT_OF") {
            std::cout << condition << " " << values[0] << ": ";
        }
        
        search(root, condition, values, 0);
        std::cout << std::endl;
    }
};



void collectWords(const std::string& text, std::vector<std::string>& collectedWords) {
    std::istringstream iss(text);
    std::string word;
    while (iss >> word) {
        // Remove punctuation (replace with your logic if needed)
        word.erase(std::remove_if(word.begin(), word.end(), ::ispunct), word.end());
        collectedWords.push_back(word);
    }
}

void parseCommand(const std::vector<std::string>& words, std::string& command, std::string& name, std::vector<std::string>& additionalData) {
    if (!words.empty()) {
        command = words[0];
    }
    if (words.size() > 1) {
        name = words[1];
    }
    additionalData.clear();
    additionalData.insert(additionalData.end(), words.begin() + 2, words.end());
}

int main() {
    KDTree kdTree;

    std::cout << "Пишіть текст\n";
    bool is_closed = false;

    while (!is_closed) {
        try {
            std::string text = "";
            std::string line = "";
            std::vector<std::string> collectedWords;

            std::cout << ">>>";

            while (line.find(';') == std::string::npos) {
                getline(std::cin, line);
                size_t semicolonPos = line.find(';');
                if (semicolonPos != std::string::npos) {
                    text += (" " + line.substr(0, semicolonPos));
                } else {
                    text += (" " + line);
                }
            }

            collectWords(text, collectedWords);

            std::string command;
            std::string name;
            std::vector<std::string> additionalData;
            parseCommand(collectedWords, command, name, additionalData);

            if (command == "CREATE") {
                if (kdTree.treeExists(name)) {
                    std::cerr << "Tree with name " << name << " already exists." << std::endl;
                } else {
                    kdTree.create(name);
                }
            } else if (command == "INSERT") {
                if (!name.empty() && kdTree.treeExists(name)) {
                    if (!name.empty() && additionalData.size() == 2) {
                        int x = std::stoi(additionalData[0]);
                        int y = std::stoi(additionalData[1]);
                        kdTree.insert(name, {x, y});
                    } else {
                        std::cerr << "Invalid command parameters for INSERT. Try (INSERT <name> 5 10)" << std::endl;
                    }
                } else {
                    std::cerr << "Tree with name " << name << " does not exist." << std::endl;
                }

            } else if (command == "PRINT") {
                if (!name.empty() && kdTree.treeExists(name)) {
                    kdTree.printTree(name);
                } else {
                    std::cerr << "Tree with name " << name << " does not exist." << std::endl;
                }
            } else if (command == "CONTAINS") {
                if (!name.empty() && additionalData.size() == 2 && kdTree.treeExists(name)) {
                    int x = std::stoi(additionalData[0]);
                    int y = std::stoi(additionalData[1]);
                    bool contains = kdTree.CONTAINS(name, {x, y});
                    std::cout << "Contains: " << (contains ? "true" : "false") << std::endl;
                } else {
                    std::cerr << "Invalid command parameters for CONTAINS." << std::endl;
                }
            } else if (command == "SEARCH") {
                if (!name.empty() && additionalData.size() >= 1) {
                    if (additionalData[0] == "WHERE" && additionalData.size() >= 4) {
                        std::string condition = additionalData[1];
                        int x = std::stoi(additionalData[2]);
                        int y = std::stoi(additionalData[3]);
                        kdTree.SEARCH(name, condition, {x, y});
                    } else if (additionalData.size() == 1) {
                        kdTree.SEARCH(name); // SEARCH <treeName>;
                    } else if (additionalData.size() >= 3
                               && additionalData[0] == "WHERE" && additionalData[1] == "CONTAINS") {
                        int x = std::stoi(additionalData[2]);
                        int y = std::stoi(additionalData[3]);
                        kdTree.SEARCH(name, "CONTAINS", {x, y}); // SEARCH <treeName> WHERE CONTAINS [10, 12];
                    } else if (additionalData.size() >= 4
                               && additionalData[0] == "WHERE" && additionalData[1] == "INTERSECTS") {
                        int x1 = std::stoi(additionalData[2]);
                        int x2 = std::stoi(additionalData[3]);
                        kdTree.SEARCH(name, "INTERSECTS", {x1, x2}); // SEARCH <treeName> WHERE INTERSECTS [5, 20];
                    } else if (additionalData.size() >= 3
                               && additionalData[0] == "WHERE" && additionalData[1] == "LEFT_OF") {
                        int x = std::stoi(additionalData[2]);
                        kdTree.SEARCH(name, "LEFT_OF", {x}); // SEARCH <treeName> WHERE LEFT_OF 15;
                    } else {
                        std::cerr << "Invalid SEARCH command format." << std::endl;
                    }
                } else {
                    std::cerr << "Invalid command parameters for SEARCH." << std::endl;
                }
            } else {
                std::cerr << "Unknown command: " << command << std::endl;
            }
        } catch (const std::exception& e) {
            std::cerr << "Error: " << e.what() << '\n';
        }
    }

    return 0;
}
