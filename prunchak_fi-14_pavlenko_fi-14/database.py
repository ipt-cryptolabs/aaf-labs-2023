from parser import *
class DataManager:
    def __init__(self):
        self.collections = {}
        self.indexes = {}

    def create_collection(self, name):
        if name in self.collections:
            raise Exception(f"Collection '{name}' already exists.")
        self.collections[name] = {}
        self.indexes[name] = {}

    def insert_into_collection(self, name, document, document_id):
        if name not in self.collections:
            raise Exception(f"Collection '{name}' does not exist.")
        self.collections[name][document_id] = document  # Вставка за допомогою document_id як ключа
        self._update_inverted_index(name, document, document_id)

    def _update_inverted_index(self, collection_name, document, document_id):
        words = document.split()
        for position, word in enumerate(words):
            if word not in self.indexes[collection_name]:
                self.indexes[collection_name][word] = {}
            if document_id not in self.indexes[collection_name][word]:
                self.indexes[collection_name][word][document_id] = []
            self.indexes[collection_name][word][document_id].append(position + 1)

    def print_inverted_index(self, collection_name):
        if collection_name not in self.indexes:
            print(f"No index found for '{collection_name}'.")
            return
        for word, doc_positions in self.indexes[collection_name].items():
            print(f'"{word}":')
            for doc_id, positions in doc_positions.items():
                print(f"  {doc_id} -> {positions}")

    def get_collection(self, name):
        return self.collections.get(name, [])

    def search(self, collection_name, query):
        if collection_name not in self.collections:
            raise Exception(f"Collection '{collection_name}' does not exist.")

        results = []
        for doc_id, document in self.collections[collection_name].items():
            if query.lower() in document.lower():
                results.append((doc_id, document))

        if not results:
            return "No documents matching the query were found."
        return results

    def search_with_condition(self, collection_name, condition):
        if collection_name not in self.collections:
            raise Exception(f"Collection '{collection_name}' does not exist.")

        # Оптимізований пошук з використанням інвертованих індексів
        if '-' in condition or '<' in condition:
            # Для складних умов (діапазон, відстань) використовуємо повне сканування
            results = [(doc_id, document) for doc_id, document in self.collections[collection_name].items() if
                       self._matches_condition(collection_name, document, condition)]
        else:
            # Для простого пошуку одного слова
            condition_word = condition.lower()
            if condition_word in self.indexes[collection_name]:
                document_ids = self.indexes[collection_name][condition_word]
                results = [(doc_id, self.collections[collection_name][doc_id]) for doc_id in document_ids]
            else:
                results = []

        if not results:
            return "No documents matching the condition were found."
        return results


    def _matches_condition(self, collection_name, document, condition):
        print(f"Debug: Searching in document '{document}' for condition '{condition}'")
        # Перевірка на діапазон слов
        if '-' in condition:
            return self._matches_range_condition(document, condition)
        # Перевірка на відстань між словами
        elif '<' in condition:
            return self._matches_distance_condition(document, condition)
        # Пошук фрази
        else:
            return condition.lower() in document.lower()

    def _matches_range_condition(self, document, condition):
        range_start, range_end = condition.split('-')
        range_start = range_start.lower().strip()
        range_end = range_end.lower().strip()

        # Додано сортування діапазону для випадків, коли початкове слово більше за кінцеве
        if range_start > range_end:
            range_start, range_end = range_end, range_start

        words = re.findall(r'\b\w+\b', document.lower())
        for word in words:
            if range_start <= word <= range_end:
                return True
        return False

    def get_all_documents(self, collection_name):
        if collection_name not in self.collections:
            raise Exception(f"Collection '{collection_name}' does not exist.")

        return self.collections[collection_name]

    def _matches_distance_condition(self, document, condition):
        # Реалізація логіки для перевірки відстані між словами
        # Наприклад: "word1" <3> "word2"
        word1, distance, word2 = re.split(r' <(\d+)> ', condition)
        distance = int(distance)
        words = re.findall(r'\b\w+\b', document.lower())

        # Отримання позицій кожного слова
        positions_word1 = [i for i, word in enumerate(words) if word == word1.lower()]
        positions_word2 = [i for i, word in enumerate(words) if word == word2.lower()]

        # Перевірка, чи існують позиції, що задовольняють умову про відстань
        for pos1 in positions_word1:
            for pos2 in positions_word2:
                if abs(pos1 - pos2) == distance:
                    return True
        return False


