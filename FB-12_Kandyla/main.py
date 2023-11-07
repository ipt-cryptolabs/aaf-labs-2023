trees = {}
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.set_of_words = []

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        self.set_of_words.append(word)

    def contains(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def search(self):
         print(self.set_of_words)

    def print_tree(self, node=None, prefix=""):
        if node is None:
            node = self.root
        for char, child in node.children.items():
            if len(node.children) > 1 and not node.is_end_of_word:
                child_prefix = prefix + "│   "
            else:
                child_prefix = prefix + "    "
            print(prefix + "└── " + char)
            self.print_tree(child, child_prefix)

def parse(command:str):
    index_of_end = command.find(";")
    if index_of_end < 0:
        raise 'Add ";" in the end of the command'
    command = command[:index_of_end].split()
    possible_commands = ['CREATE', 'create', 'INSERT', 'insert', 'SEARCH', 'search', 'PRINT_TREE', 'print_tree', 'CONTAINS', 'contains']
    if command[0] not in possible_commands:
        raise "Error! Wrong command. Try again"
    else:
        if command[0] == 'CREATE' or command[0] == 'create':
            if command[1] not in trees:
                new_tree = Trie()
                trees[command[1]] = new_tree
                print(f"Set {command[1]} has been created")
            else:
                raise "The set already exists"
        elif command[0] == 'INSERT' or command[0] == 'insert':
            if command[1] not in trees:
                raise "The set does not exist"
            else:
                tree = trees[command[1]]
                value = command[2].replace('"', '')
                tree.insert(value)
                print(f"{value} has been inserted")
        elif command[0] == 'PRINT_TREE' or command[0] == 'print_tree':
            if command[1] not in trees:
                raise "The set does not exist"
            else:
                tree = trees[command[1]]
                print(command[1])
                tree.print_tree()
        elif command[0] == 'CONTAINS' or command[0] == 'contains':
            if command[1] not in trees:
                raise "The set does not exist"
            else:
                tree = trees[command[1]]
                value = command[2].replace('"', '')
                print(tree.contains(value))
        elif command[0] == 'CONTAINS' or command[0] == 'contains':
            if command[1] not in trees:
                raise "The set does not exist"
            else:
                tree = trees[command[1]]
                print(tree.contains(command[2]))
        elif command[0] == 'SEARCH' or command[0] == 'search':
            if command[1] not in trees:
                raise "The set does not exist"
            else:
                tree = trees[command[1]]
                tree.search()

if __name__ == '__main__':
    print("To exit type 'exit'")
    while(True):
        command = input("Type a command: ")
        if command == 'exit':
            break
        res = parse(command)


