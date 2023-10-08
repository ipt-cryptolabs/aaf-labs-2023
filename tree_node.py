class TreeNode:
    def __init__(self, key, value):
        self.left = None
        self.right = None
        self.key = key
        self.value = value

class Tree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = TreeNode(key, value)
        else:
            self.__insert(self.root, key, value)

    def __insert(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, value)
            else:
                self.__insert(node.left, key, value)
        else:
            if node.right is None:
                node.right = TreeNode(key, value)
            else:
                self.__insert(node.right, key, value)

    def root_item(self):
        if self.root is not None:
            return self.root.key, self.root.value
        return None

    def __show_tree(self, node):
        if node is None:
            print("Binary tree is empty")
            return
        v = [('r:', node)]
        while v:
            vn = []
            for x in v:
                print(x[0], x[1].key, x[1].value, end='   ')
                if x[1].left:
                    vn += [(f"L,{x[1].key}:", x[1].left)]
                if x[1].right:
                    vn += [(f"R,{x[1].key}:", x[1].right)]
            v = vn
            print()

    def display(self):
        self.__show_tree(self.root)
        print()

    def delete(self, key):
        if self.root is None:
            return None
        else:
            self.root = self.__delete(self.root, key)

    def __delete(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self.__delete(node.left, key)
        elif key > node.key:
            node.right = self.__delete(node.right, key)
        else:
            if node.left is None and node.right is None:
                node = None
            elif node.left is None:
                node = node.right
            elif node.right is None:
                node = node.left
            else:
                min_right = self.__find_min(node.right)
                node.key, node.value = min_right.key, min_right.value
                node.right = self.__delete(node.right, min_right.key)
        return node

    def __find_min(self, node):
        if node.left is None:
            return node
        else:
            return self.__find_min(node.left)

    def same_letters(self, node):
        if node is None:
            print("Binary tree is empty")
            return
        letters = {}
        for key, value in node.items():
            for i in set(value):
                if value.count(i) > 1:
                    letters[key] = value.count(i) - 1
        print(letters, end='\n\n')
        for key, value in letters.items():
            for _ in range(value):
                self.delete(key)

    @classmethod
    def build_binary_tree_from_dict(self, data_dict):
        tree = Tree()
        for key, value in data_dict.items():
            tree.insert(key, value)
        return tree