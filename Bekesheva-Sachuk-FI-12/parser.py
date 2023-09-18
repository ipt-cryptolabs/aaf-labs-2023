# TODO: CREATE, INSERT, PRINT_INDEX, SEARCH 

'''     
        Importing relevant modules
'''
import re


COMMANDS = ["CREATE", "INSERT", "PRINT_INDEX", "SEARCH"] # we'll be using uppercase to distinguish querry commands
KEYWORDS = ["WHERE"]
STOP = ";"
READ = True

def look_for_commands(string):
   string = re.sub(r'^\s*', '', string)
   pattern = r'(?i)(' + '|'.join(COMMANDS) + r')\b'  # (?i) - case-insensitivity, | - pipe for commands
   match = re.match(pattern, string) 

   if match:
        COMMAND = match.group(1).upper()
        string = re.sub(f'(?i){COMMAND}' + r'\s+', '', string)
        return COMMAND, string  # goup() - for extracting values
   else:
       return None, None  
   

def re_create(string):
    pattern = '^[a-zA-Z]*[a-zA-Z0-9_]*\s*;'
    match = re.search(pattern, string)
    if match:
        string = re.sub(';', '', match.group())
        return string
    else:
        return None

def re_insert(string):
    pattern = '^([a-zA-Z]*[a-zA-Z0-9_]*)\s*"([a-zA-Z]*\s*[a-zA-Z0-9_]*)"\s*;' # я оце пишу ці регулярки, а хто потім згадає як ця хуйня мені в голову прийшла
    match = re.match(pattern, string) 
    if match:
        collection_name = match.group(1)
        value = match.group(2)
        return collection_name, value
    else:
        return None, None

def re_print(string):
    pattern = '^[a-zA-Z]*[a-zA-Z0-9_]*\s*;'
    match = re.search(pattern, string)
    if match:
        string = re.sub(';', '', match.group())
        return string
    else:
        return None
    
def re_search(string):
    pattern = '^([a-zA-Z]*[a-zA-Z0-9_]*)\s*(?i:WHERE\s*"([a-zA-Z]*\s*[a-zA-Z0-9_]*)"\s*)?\s*;'
    match = re.search(pattern, string)
    if match:
        collection_name = match.group(1)
        print(collection_name)
        if match.group(1):
            keyword = match.group(1)
            return collection_name, keyword
    else:
        return None

s = '\tCREaTE      jnodfs ;'
c, s = look_for_commands(s)
n = re_create(s)
re_insert(s)
re_search(s)
'''
while True: # read user input
    while READ:
        user_input = input()
        COMMAND = look_for_commands(user_input)
        if COMMAND == "CREATE":
            #collection_name = re_create()
        else:
            print("Incorrect input, plese try again")
'''
