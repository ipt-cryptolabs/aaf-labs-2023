import re
from RWayTrie import *

def tokenize(value) -> list:

    pattern = r'\w+|\S+'
    return re.findall(pattern, value)

class DB:
    def __init__(self) -> None:
        self._collections = {}

    def CREATE(self, collection_name: str) -> None:
        self._collections[collection_name] = Collection(collection_name)

    def INSERT(self, collection_name: str, value: str) -> None:
        if collection_name in self._collections:
            self._collections[collection_name].insert(value)
        else:
            print(f"No collection named f{collection_name}")

    def PRINT_INDEX(self, collection_name: str) -> None:
        if collection_name in self._collections:
            self._collections[collection_name].print_index()
        else:
            print(f"No collection named f{collection_name}")

    def SEARCH(self, collection_name: str) -> list:
        if collection_name in self._collections:
            self._collections[collection_name].search()
        else:
            print(f"No collection named f{collection_name}")
        
    def SEARCH_WHERE(self, collection_name: str, keyword: str) -> list:
        if collection_name in self._collections:
            return self._collections[collection_name].search_where(keyword)
        else:
            print(f"No collection named f{collection_name}")



class Collection:
    def __init__(self, name: str) -> None:
        self._trie = Trie()
        self._name = name
        self._size = 0


    def insert(self, value: str) -> None:
        self._size += 1
        tokens = tokenize(value)

        for token in list(dict.fromkeys(tokens)):
            indices = [i for i in range(len(tokens)) if tokens[i] == token]
            self._trie.insert(token, {f"DOC{self._size}": indices})

    def print_index(self) -> None:
        print(self._trie)

    def search(self) -> list:
        #idk
        return

    def search_where(self, keyword: str) -> list:
        res = self._trie.search(keyword)
        res_docs = []

        for i in res._value:
            res_docs.append(list(i.keys()))

        
        res_docs = sum(res_docs, [])
        return list(set(res_docs))


db = DB()

db.CREATE("col")
db.INSERT("col", "There is no place for blalbal, also non= is - no, dsd , sd.")
db.INSERT("col", " is no place for blalbal, nxfgns")
db.PRINT_INDEX("col")
print(db.SEARCH_WHERE("col", "no"))



    