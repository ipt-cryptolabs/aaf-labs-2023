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
    pattern = '(?i)^([a-zA-Z]*[a-zA-Z0-9_]*)\s*(?:WHERE\s*\"(.*)\"(\*)?\s*)?\s*;'  # search for collection name, nvm spaces, group keyword if present
    match = re.search(pattern, string)
    if match:   
        if match.group(1):
            collection_name = match.group(1)
            if match.group(2):
                keyword = match.group(2)
                if match.group(3):
                    prefix = True
                else:
                    prefix = False
                pattern = '(.*)\"\s*-\s*\"(.*)|(.*)\"\s*<(\d)>\s*\"(.*)|\"(.*)'
                match = re.search(pattern, keyword)
                if match:
                    if match.group(1) and match.group(2):
                        keyword1, keyword2 = match.group(1), match.group(2)
                        return collection_name, keyword1, None, keyword2, False
                    elif match.group(3) and match.group(4) and match.group(5):
                        keyword1, N, keyword2 = match.group(3), match.group(4), match.group(5)
                        return collection_name, keyword1, N, keyword2, False
                    elif match.group(6):
                        return None, None, None, None, False
                return collection_name, keyword, None, None, prefix
            else:
                return collection_name, None, None, None, False
        else:
            return None, None, None, None, False
    else:
        return None, None, None, None, False




