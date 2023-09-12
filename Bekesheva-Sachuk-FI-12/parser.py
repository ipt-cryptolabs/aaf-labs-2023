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
        COMMAND = match.group().upper()
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



s = '    CREaTE      jnodfsods;'
c, s = look_for_commands(s)
print(c)
n = re_create(s)
print(n)

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