import re
from RWayTrie import *

def tokenize(value) -> list:

    pattern = r'\w+|\S+'
    return re.findall(pattern, value)

class DB:
    def __init__(self) -> None:
        self._collections = {}

    def CREATE(self, collection_name: str) -> None: 
        if collection_name in self._collections:
            print(f"Collection {collection_name} already exists")
            return
        self._collections.update({collection_name : Collection(collection_name)})

    def INSERT(self, collection_name: str, value: str) -> None:
        if collection_name in self._collections: 
            self._collections[collection_name].insert(value.lower())
        else:
            print(f"No collection named f{collection_name}")

    def PRINT_INDEX(self, collection_name: str) -> None:
        if collection_name in self._collections:
            self._collections[collection_name].print_index()
        else:
            print(f"No collection named f{collection_name}")

    def SEARCH(self, collection_name: str) -> list:
        if collection_name in self._collections:
            return self._collections[collection_name].search()
        else:
            print(f"No collection named '{collection_name}")
        
    def SEARCH_WHERE(self, collection_name: str, keyword: str, prefix) -> list:
        if collection_name in self._collections:
            values = self._collections[collection_name].search_where(keyword.lower(), prefix)
            unique_keys = set()

            for dictionary in values:
                print(dictionary)
                unique_keys.update(dictionary.keys())

            return list(unique_keys)
        else:
            print(f"No collection named '{collection_name}")

    def SEARCH_WHERE_WORD(self, collection_name: str, keyword1: str, keyword2: str) -> list:
        if collection_name in self._collections:
            docs = []
            values = self._collections[collection_name]._trie.get_words()
            for doc, words in values.items():
                for word in words:
                    if word >=keyword1 and word <= keyword2:
                        if doc not in docs:
                            docs.append(doc)
                        pass


            return docs
        else:
            print(f"No collection named '{collection_name}")

    def SEARCH_WHERE_WORD_N(self, collection_name: str, keyword1: str, keyword2: str, N:int) -> list:
        if collection_name in self._collections:
            word1 = self._collections[collection_name].search_where(keyword1, False)
            word2 = self._collections[collection_name].search_where(keyword2, False)

            docs_res = []

            #sorry(((
            for dic1 in word1:
                for dic2 in word2:
                    for docs1 in list(dic1.keys()):
                        for docs2 in list(dic2.keys()):
                            if docs1 != docs2:
                                pass
                            else:
                                ind1 = dic1[docs1]
                                ind2 = dic2[docs1]
                                for i1 in ind1:
                                    for i2 in ind2:
                                        if abs(i1-i2) == N:
                                            if docs1 not in docs_res:
                                                docs_res.append(docs1)
                                                pass
                                
            return docs_res


        else:
            print(f"No collection named '{collection_name}")






class Collection:
    def __init__(self, name: str) -> None:
        self._trie = Trie()
        self._name = name
        self._size = 0

    def get_values(self):
        values = self._trie.get_all_values()
        print(values)        
        words = []

        for i in values:
            for j in i:
                for k in j.keys():
                    words.append(k)

        return list(set(words))
    

    def insert(self, value: str) -> None:
        self._size += 1
        tokens = tokenize(value)

        for token in list(dict.fromkeys(tokens)):
            indices = [i for i in range(len(tokens)) if tokens[i] == token]
            self._trie.insert(token, {f"DOC{self._size}": indices})

    def print_index(self) -> None:
        print(self._trie)

    def search(self) -> list:
        values = self._trie.get_all_values()
        unique_keys = set()

        for sublist in values:
            for dictionary in sublist:
                unique_keys.update(dictionary.keys())

        return list(unique_keys)

    def search_where(self, keyword: str, prefix) -> list:
        if prefix == False:
            res = self._trie.search(keyword)
            if res:
                values = res._value

            else:
                return None
        else:
            res = self._trie.search(keyword, True)
            if res == []:
                return None
            res_docs = []
            for i in res:
                res_docs.append(i._value)
            values = [item for sublist in res_docs for item in sublist]

        return values
    
        

    