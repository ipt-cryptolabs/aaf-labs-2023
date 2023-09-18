class Node:
    # fucking python with it's dynamic type-designs, I can't write this shit, it doesn't make any sense AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    def __init__(self, next=None, value=None, is_terminal=None):
        self._next = next # this is supposed to be an dict with links to next (aka children) nodes
        self._value = value 
        self._is_terminal = is_terminal
        # this oop is cringe

    def __repr__(self): # overload output (kinda)
        return str(self.value)
    

class Trie:

    def __init__(self):
        self._root = Node()

    def __insert__(self, key, value):
        x = self._root
        for i in range(0, len(key)):
            if x._next[key[i]] == None:
                x._next[key[i]] = Node()
            x = x._next[key[i]]
            

        self._root._value = value
        self._root._is_terminal = True
    

node = Node(value={"d1":[3, 5]})
print(node)
