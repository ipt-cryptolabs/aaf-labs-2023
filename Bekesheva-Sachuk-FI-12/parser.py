# TODO: CREATE, INSERT, PRINT_INDEX, SEARCH 

'''     
        Importing relevant modules
'''
import re
from DataBase import *


COMMANDS = ["CREATE", "INSERT", "PRINT_INDEX", "SEARCH"] # we'll be using uppercase to distinguish querry commands
KEYWORDS = ["WHERE"]
STOP = ";"
READ = True

def look_for_commands(string):
   string = re.sub(r'^\s*', '', string)
   pattern = r'(?i)(' + '|'.join(COMMANDS) + r')\s*'  # (?i) - case-insensitivity, | - pipe for commands
   match = re.match(pattern, string) 

   if match:
        COMMAND = match.group(1).upper()
        string = re.sub(f'(?i){COMMAND}' + r'\s*', '', string)
        return COMMAND, string  
   else:
       return None, None  
   

def re_create(string):
    pattern = '^[a-zA-Z]*[a-zA-Z0-9_]*\s*;'  # search for collection name, nvm spaces
    match = re.search(pattern, string)
    if match:
        string = re.sub(';', '', match.group())
        return string
    else:
        return None

def re_insert(string):
    pattern = '^([a-zA-Z]*[a-zA-Z0-9_]*)\s*"(.*)"\s*;'  # search for collection name, nvm spaces, search for value (must be in " ")
    match = re.match(pattern, string) 
    if match:
        collection_name = match.group(1)
        value = match.group(2)
        print(collection_name, value)
        return collection_name, value
    else:
        return None, None

def re_print(string):
    pattern = '^[a-zA-Z]*[a-zA-Z0-9_]*\s*;'  # search for collection name, nvm spaces
    match = re.search(pattern, string)
    if match:
        string = re.sub(';', '', match.group())
        return string
    else:
        return None
    
def re_search(string):
    print(stringSE)
    pattern = '^([a-zA-Z]*[a-zA-Z0-9_]*)\s*|(?i:WHERE\s*"(.*)"\s*-\s*"(.*))"\s*|\s*(?i:WHERE\s*"(.*)"\s*<(\d)>\s*"(.*))"\s*|\s*(?i:WHERE\s*"(.*)"\s*);'  # search for collection name, nvm spaces, group keyword if present
    match = re.search(pattern, string)
    if match:
        collection_name = match.group(1)
        if match.group(1):
            keyword = match.group(2)
            return collection_name, keyword
        else:
            return collection_name, None
    else:
        return None, None
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
        collection_name, keyword = re_search(STRING)
        if collection_name:
            if keyword:
                print(f'searching collection \'{collection_name} with keyword \'{keyword}\'...')
                db.SEARCH_WHERE(collection_name, keyword)
            else:
                print(f'searching collection \'{collection_name}\'...')
                db.SEARCH(collection_name)
        else:
            print("incorrect collection_name or no keyword provided")
    else:
        print("incorrect input, plese try again")

