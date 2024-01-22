from database import *
from parser import *

if __name__ == '__main__':
    data_manager = DataManager()
    while True:
        text = input("Enter request SQL-like: ")
        if not text:
            continue
        else:
            lexer = Lexer(text)
            interpreter = Interpreter(lexer)
            command_dict = interpreter.expr()
            if command_dict is None:
                print("You have been entered something wrong\n"
                      "Try again")
            else:
                print(command_dict)
                match list(command_dict.keys()):

                    case ['CREATE']:
                        data_manager.create_collection(command_dict['CREATE'])
                        print(f"Collection '{command_dict['CREATE']}' has been created")

                    case ['INSERT', 'VALUE']:
                        collection_name = command_dict['INSERT']
                        document = " ".join(command_dict['VALUE'])
                        document_id = f'd{len(data_manager.get_collection(collection_name)) + 1}'
                        data_manager.insert_into_collection(collection_name, document, document_id)
                        print(f"Document '{command_dict['VALUE']}' has been added to '{command_dict['INSERT']}'")

                    case ['PRINT_INDEX']:
                        collection_name = command_dict['PRINT_INDEX']
                        data_manager.print_inverted_index(collection_name)

                    case ['SEARCH']:
                        collection_name = command_dict['SEARCH']
                        try:
                            documents = data_manager.get_all_documents(collection_name)
                            for doc_id, document in documents.items():
                                print(f"{doc_id}: {document}")
                        except Exception as e:
                            print(f"Error: {e}")

                    case ['SEARCH', 'WHERE']:
                        print(f"Searching in '{command_dict['SEARCH']}' for '{command_dict['WHERE']}'")
                        collection_name = command_dict['SEARCH']
                        condition = command_dict['WHERE']
                        try:
                            results = data_manager.search_with_condition(collection_name, condition)
                            if isinstance(results, str):
                                print(results)
                            else:
                                for doc_id, document in results:
                                    print(f"{doc_id}: {document}")
                        except Exception as e:
                            print(f"Error: {e}")
