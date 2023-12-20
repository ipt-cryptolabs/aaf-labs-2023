from Parser import *
from DataBase import *

db = DB()

while READ:
    user_input = input()
    COMMAND, STRING = look_for_commands(user_input)
    if user_input == "--s":
        READ = False
    elif COMMAND == "CREATE":
        collection_name = re_create(STRING)
        if collection_name:
            print(f'creating collection \'{collection_name}\'...')
            db.CREATE(collection_name)

        else:
            print("incorrect collection_name")
    elif COMMAND == "INSERT":
        collection_name, value = re_insert(STRING)
        if collection_name and value:
            print(f'inserting \'{value}\' into collection \'{collection_name}\'...')
            db.INSERT(collection_name, value)
        else:
            print("incorrect collection_name or value")
    elif COMMAND == "PRINT_INDEX":
        collection_name = re_print(STRING)
        if collection_name:
            print(f'printing collection \'{collection_name}\' as index...')
            db.PRINT_INDEX(collection_name)
        else:
            print("incorrect collection_name")
    elif COMMAND == "SEARCH":
        collection_name, keyword1, N, keyword2, prefix = re_search(STRING)
        if collection_name:
            if keyword1:
                if keyword2:
                    if N:
                        print(f'searching collection \'{collection_name} with keywords \'{keyword1}\', \'{keyword2}\' separated by {N} words...')
                        #print(db.SEARCH_WHERE_WORD(collection_name, keyword1, keyword2))
                    else:
                        print(f'searching collection \'{collection_name} with keywords \'{keyword1}\', \'{keyword2}\'...')
                else:
                    print(f'searching collection \'{collection_name} with keyword \'{keyword1}\'...')
                    print(db.SEARCH_WHERE(collection_name, keyword1, prefix))
            else:
                print(f'searching collection \'{collection_name}\'...')
                print(db.SEARCH(collection_name))
        else:
            print("incorrect collection_name or no keyword provided")
    else:
        print("incorrect input, plese try again")