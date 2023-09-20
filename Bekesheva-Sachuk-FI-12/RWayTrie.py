class Node:
    def __init__(self, key=" ", children={}, value={}):
        self._key = key
        self._children = children # map key - value --{"key": next nodes letters}-- 
        self._value = value # non-None if it's the last letter in word, {}

    def __eq__(self, value: object) -> bool:
        return self._key == value._key and self._children == value._children and self._value == value._value 

    def __repr__(self) -> str: 
        if self._value:
            return f'{self._key}\n{self._value}'
        else:
            return str(self._key)
    
    
class Trie:
    def __init__(self):
        self._root = Node()

    def insert(self, key: str, value: dict):
        x = self._root
        self.__insert__(x, key, value)

    def __insert__(self, x: Node, key: str, value: dict):
        for i in range(len(key)):
            if key[i] not in x._children.keys():
                x._children[key[i]] = Node(key[i], children={})
            x = x._children[key[i]]

        x._value = value

    def search(self, key: str) -> Node:
        x = self._root
        return self.__search__(x, key)

    def __search__(self, x: Node, key: str) -> Node:
        for i in range(len(key)):
            try:
                if x != None and key[i] not in x._children:
                    return None
            except:
                pass
                
            x = x._children[key[i]]

        return x
    
    def delete(self, key: str):
        x = self._root
        self.__delete__(x, key)


    def __delete__(self, x: Node, key: str):
        nodes_stack = []  # To keep track of visited nodes

        # Traverse the trie to find the key
        for i in range(len(key)):
        #for char in key:
            if key[i] not in x._children:
                return  # Key not found, nothing to delete
            x = x._children[key[i]]
            nodes_stack.append(x)

        # Mark the node as deleted
        x._value = None

        # Traverse back and remove deleted nodes with no non-deleted children
        while nodes_stack:
            x = nodes_stack.pop()
            if all(child._value is None for child in x._children.values()):
                if nodes_stack:
                    parent = nodes_stack[-1]
                    del parent._children[x._key]

    def __delete_(self, x: Node, key: str):
        print(key)
        if key == "":
            if x._value != {}:
                x._value = {}

            for i in range(len(x._children)):
                if x._children[x._children.keys()[i]] != {}:
                    return x
                
            return None
        
        if len(key) > 0:
            x._children[key[0]] = self.__delete__(x._children[key[0]], key[1:])


t = Trie()
t.insert("sdsd", {"1": [1, 2]})
print(t.search("sdsd"))
t.delete("sdsd")
t.insert("sdsd", {"1": [1, 2]})
t.insert("sdioesdsd", {"2": [3, 2]})
print(t.search("sdioesdsd"))


