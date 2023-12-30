import re

helper = '''
Available commands:
              CREATE collection_name;
              INSERT collection_name 'document';
              PRINT_INDEX collection_name;
              SEARCH collection_name [WHERE 'query'];
              HELP;
              EXIT;
'''

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.documents = []
        
    def add_document(self, doc_id, text):
        self.documents.append(text)
        words = self._tokenize(text)
        for idx, word in enumerate(words):
            if word in self.index:
                if doc_id in self.index[word]:
                    self.index[word][doc_id].append(idx+1)
                else:
                    self.index[word][doc_id] = [idx+1]
            else:
                self.index[word] = {doc_id: [idx+1]}

    def search(self, query):
        result = set()
        words = self._tokenize(query)

        for idx, word in enumerate(words):
            if "*" in query:
                prefix = word.rstrip("*")
                for i in self.index.keys():
                    if i.startswith(prefix):
                        result.update(self.index[i])
            elif word in self.index and "<" not in query:
                result.update(self.index[word])
            elif "<" in word and ">" in word:
                word1, distance, word2 = words[idx - 1], int(word[1:-1]), words[idx + 1]
                if word1 in self.index and word2 in self.index:
                    for doc_id1 in self.index[word1].keys():
                        if doc_id1 in self.index[word2].keys():
                            positions1 = self.index[word1][doc_id1]
                            positions2 = self.index[word2][doc_id1]
                            for pos1 in positions1:
                                for pos2 in positions2:
                                    if abs(pos1 - pos2) == distance:
                                        result.add(doc_id1)
        return result
    
    def _tokenize(self, text):
        return [word.strip('.,?!') for word in text.split()]

class CollectionManager:
    def __init__(self):
        self.collections = {}

    def create_collection(self, collection_name):
        self.i = 1
        if collection_name in self.collections:
            return f"Collection {collection_name} already exists."
        self.collections[collection_name] = InvertedIndex()
        return f"Collection {collection_name} has been created."

    def insert_document(self, collection_name, text):
        if collection_name not in self.collections:
            return f"Collection {collection_name} does not exist."
        doc_id = f'd{self.i}'
        self.i += 1
        self.collections[collection_name].add_document(doc_id, text)
        return f"Document '{text}' has been added to {collection_name}."

    def print_index(self, collection_name):
        if collection_name not in self.collections:
            print(f"Collection {collection_name} does not exist.")
            return 0
        index = self.collections[collection_name].index
        for word, postings in index.items():
            print(f'"{word}":')
            for doc_id, positions in postings.items():
                print(f'  {doc_id} -> {positions}')

    def search_documents(self, collection_name, query=None):
        if collection_name not in self.collections:
            return f"Collection {collection_name} does not exist."
        if query:
            results = list(self.collections[collection_name].search(query))
            documents = []
            for i in results:
                documents.append(self.collections[collection_name].documents[int(i[1:])-1])
            return documents
        else:
            documents = self.collections[collection_name].documents
            return documents

collections = CollectionManager()
while True:
    command = input("Your command: ").strip().lower()
    if not command:
        print(helper)
    else:
        parts = command.split()

        if parts[0] == "create":
            if len(parts) == 2 and re.match(r'[a-zA-Z][a-zA-Z0-9_]*;', parts[1]):
                collection_name = re.sub(";","",parts[1])
                print(collections.create_collection(collection_name))
            elif len(parts) < 2:
                print("Format: CREATE collection_name;")
            else:
                print("Your collection name is incorrect or you missed ';' at the end")

        elif parts[0] == "insert":
            if len(parts) >= 3 and parts[2][0] == "'" and  parts[-1][-1] == ";":
                collection_name = parts[1]
                document = re.sub("'",""," ".join(parts[2:])[:-1])
                print(collections.insert_document(collection_name, document))
            else:
                print("Format: INSERT collection_name 'document';")

        elif parts[0] == "print_index":
            if len(parts) == 2 and parts[-1][-1] == ";":
                collection_name = re.sub(";","",parts[1])
                collections.print_index(collection_name)
            else:
                print("Format: PRINT_INDEX collection_name;")

        elif parts[0] == "search":
            if len(parts) >= 2 and parts[-1][-1] == ";":
                if len(parts) > 2:
                    collection_name = parts[1]
                    query = re.sub("'",""," ".join(parts[3:])[:-1])
                    if parts[2] == 'where' and re.match(r'[a-zA-Z0-9_]*', re.sub("'","",parts[3][:-1])):
                        print(collections.search_documents(collection_name, query))
                    else:
                        print("Your query is incorrect")
                else:
                    collection_name = re.sub(";","",parts[1])
                    print(collections.search_documents(collection_name))
            else:
                print("Format: SEARCH collection_name [WHERE 'query'];")
        elif re.sub(";","",parts[0]) == "help":
            print(helper)
        elif re.sub(";","",parts[0]) == "exit":
            break
        else:
            print(helper)