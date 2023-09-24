class Node:
    def __init__(self, key=" ", children={}, value=[]):
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
    def __init__(self) -> None:
        self._root = Node(key="", children={}, value=[]) # root is always empty

    def insert(self, key: str, value: dict) -> None:
        self.__insert__(self._root, key, value)

    def __insert__(self, x: Node, key: str, value: dict) -> None:
        for i in range(len(key)):
            if key[i] not in x._children.keys():
                x._children[key[i]] = Node(key[i], children={},  value = [])
            x = x._children[key[i]]

        x._value.append(value)

    def search(self, key: str) -> list:
        return self.__search__(self._root, key)

    def __search__(self, x: Node, key: str) -> list:
        for i in range(len(key)):
            if key[i].lower() not in x._children:
                return None
            
            x = x._children[key[i]]

        return x
    
    def delete(self, key: str) -> None:
        self.__delete__(self._root, key)


    def __delete__(self, x: Node, key: str) -> None:
        nodes_stack = [] 

        for i in range(len(key)):
            if key[i] not in x._children:
                return  # key not found, nothing to delete
            x = x._children[key[i]]
            nodes_stack.append(x)


       # Mark the node as deleted only if it has no children
        if all(child._value is None for child in x._children.values()):
            x._value = None
        else:
            x._value = []

        while nodes_stack:
            x = nodes_stack.pop()
            if all(child._value is None for child in x._children.values()): # check if there are no children
                if nodes_stack:
                    parent = nodes_stack[-1]
                    del parent._children[x._key]

    def __repr__(self) -> str:
        return self.__display__()

    def __display__(self) -> str:
        res = ""
        stack = [(self._root, "")]
        while stack:
            x, prefix = stack.pop()
            if x._value:
                res += f"{prefix} - {x._value}\n"
            for child in x._children.values():
                stack.append((child, prefix + child._key))
        return res
    
    def get_all_values(self) -> list:
        return self.__get_all_values__(self._root)
    
    def __get_all_values__(self, x: Node):
        values = []
        nodes_stack = [x]
    
        while nodes_stack:
            x = nodes_stack.pop()
            if x._value != [] and x._value != None:
                values.append(x._value)
            for child in x._children.values():
                nodes_stack.append(child)
        return values

t = Trie()
t.insert("sdsd", {"1": [1, 2]})
t.insert("sdsdss", {"2": [1, 5]})
print(t.search("sdsd"))
t.delete("sdsd")
print(t.search("sdsd"))
t.insert("sdsd", {"1": [1, 2]})
print(t.search("sdsd"))

print(t.get_all_values())

 