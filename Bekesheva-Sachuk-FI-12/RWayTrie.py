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
                if x != None and key[i] not in x._children.keys():
                    return None
            except:
                return None
                
            x = x._children[key[i]]

        return x
    
    def delete(self, key: str):
        x = self._root
        self.__delete__(x, key)

    def __delete__(self, x: Node, key: str):
        print(key)
        if key == " ":
            if x._value != {}:
                x._value == {}

            for i in range(len(x._children)):
                if x._children != {}:
                    return x
                
            return None
        
        if len(key) > 0:
            x._children[key[0]] = self.__delete__(x._children[key[0]], key[1:])




t = Trie()
t.insert("sdsd", {"1": [1, 2]})
print(t.search("sdsd"))
t.delete("sdsd")
print(t.search("sdsd"))
