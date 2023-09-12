class Database:
    def __init__(self):
        self.db = {} #collection_name : collection

    def create_collection(self, collection_name):
        if collection_name in self.db.keys():
            raise Exception(f"Database Error: collection '{collection_name}' has been already added in database")

        self.db[collection_name] = Collection(collection_name)
        print(f"Collection {collection_name} has been added successfully")

    def insert_in_collection(self, collection_name, document):
        if collection_name not in self.db.keys():
            raise Exception(f"Database Error: there is no collection with name '{collection_name}'")

        self.db[collection_name].add_document(document)
        print(f"Collection '{collection_name}' has been updated")

    def print_collection_index(self, collection_name):
        if collection_name not in self.db.keys():
            raise Exception(f"Database Error: there is no collection with name '{collection_name}'")
        self.db[collection_name].print_indexes()

    def search_in_collection(self, collection_name):
        if collection_name not in self.db.keys():
            raise Exception(f"Database Error: there is no collection with name '{collection_name}'")

        self.db[collection_name].search()

    def search_by_keyword(self,collection_name, keyword):
        if collection_name not in self.db.keys():
            raise Exception(f"Database Error: there is no collection with name '{collection_name}'")
        self.db[collection_name].search_by_keyword(keyword.lower())

    def search_by_range(self, collection_name, key1,key2):
        if collection_name not in self.db.keys():
            raise Exception(f"Database Error: there is no collection with name '{collection_name}'")
        self.db[collection_name].search_by_range(key1.lower(),key2.lower())

    def search_by_keys(self, collection_name, key1, n, key2):
        if collection_name not in self.db.keys():
            raise Exception(f"Database Error: there is no collection with name '{collection_name}'")
        self.db[collection_name].search_by_keys(key1.lower(), int(n), key2.lower())


class Collection:
    def __init__(self, name):
        self.name = name
        self.documents = []
        self.indexes = {} # word: {document_index: [word_index]}

    def print_indexes(self):
        for key, value in self.indexes.items():
            print(key, ": ")
            for idx, word_idx_list in value.items():
                print(f"    Document {idx}: {word_idx_list}")

    def add_document(self, document):
        document_index = len(self.documents)
        self.documents.append(document)

        for idx, word in enumerate(document.lower().split()):
            if word in self.indexes.keys():
                if document_index in self.indexes[word].keys():
                    self.indexes[word][document_index].append(idx)
                else:
                    self.indexes[word][document_index] = [idx]
            else:
                self.indexes[word] = {}
                self.indexes[word][document_index] = [idx]

    def search(self):
        for idx, document in enumerate(self.documents):
            print(f"DOCUMENT {idx}:\n   {document}")

    def search_by_keyword(self, key):
        if key in self.indexes.keys():
            for idx in self.indexes[key].keys():
                print(f"DOCUMENT:\n    {self.documents[idx]}\n")

    def search_by_range(self, key1, key2):
        for_print = set()
        for key in self.indexes.keys():
            if key1 <= key <= key2:
                for idx in self.indexes[key].keys():
                    for_print.add(idx)

        for i in for_print:
            print(f"DOCUMENT:\n{self.documents[i]}\n")

    def search_by_keys(self, key1, n, key2):
        key1_results = set()
        if key1 in self.indexes.keys() and key2 in self.indexes.keys():
            for idx in self.indexes[key1].keys():
                key1_results.add(idx)

            for idx in key1_results:
                if self.indexes[key2][idx]:
                    for position in self.indexes[key2][idx]:
                        if (position - int(n) - 1) in self.indexes[key1][idx]:
                            print(f"DOCUMENT:\n{self.documents[idx]}\n")
