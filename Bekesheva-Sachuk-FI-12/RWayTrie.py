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
        self._root = Node() # root is always empty

    def insert(self, key: str, value: dict) -> None:
        x = self._root
        self.__insert__(x, key, value)

    def __insert__(self, x: Node, key: str, value: dict) -> None:
        for i in range(len(key)):
            if key[i] not in x._children.keys():
                x._children[key[i]] = Node(key[i], children={},  value = [])
            x = x._children[key[i]]

        x._value.append(value)

    def search(self, key: str) -> Node:
        x = self._root
        return self.__search__(x, key)

    def __search__(self, x: Node, key: str) -> Node:
        for i in range(len(key)):
            try:  # x might exist but have None values, thus the overloaded = won't work and it's probably cheaper to use try/catch rather than check if values exist in Node and then compare 
                if x != None and key[i] not in x._children:
                    return None
            except:
                pass
                
            x = x._children[key[i]]

        return x
    
    def delete(self, key: str) -> None:
        x = self._root
        self.__delete__(x, key)


    def __delete__(self, x: Node, key: str) -> None:
        nodes_stack = [] 

        for i in range(len(key)):
            if key[i] not in x._children:
                return  # key not found, nothing to delete
            x = x._children[key[i]]
            nodes_stack.append(x)


        x._value = None  # mark the node as deleted

        while nodes_stack:
            x = nodes_stack.pop()
            if all(child._value is None for child in x._children.values()): # check if there are no children
                if nodes_stack:
                    parent = nodes_stack[-1]
                    del parent._children[x._key]

    def __repr__(self) -> str:
        level = 0
        key = {}
        x = self._root
        return self.__display__(x, key, level)
    
    def __display__(self, x: Node, key: dict, level: int) -> str:
        res = ""
        nodes_stack = [(x, key, level)]
    
        while nodes_stack:
            x, x_key, x_level = nodes_stack.pop()
            if len(x._children) == 0:
                x_key[x_level] = f' - {x._value}\n'
                res += "".join(x_key.values())
            else:
                for child in x._children.values():
                    child_key = x_key.copy()
                    child_key[x_level] = child._key
                    nodes_stack.append((child, child_key, x_level + 1))

        return res

 