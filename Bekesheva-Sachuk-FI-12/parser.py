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
   string = re.sub(r'^\s+', '', string)
   pattern = r'(?i)(' + '|'.join(COMMANDS) + r')\b'  # (?i) - case-insensitivity, | - pipe for commands
   match = re.match(pattern, string) 
   
   if match:
       return match.group().upper()  # goup() - for extracting values
   else:
       return None  

print(look_for_commands('CREATE jnodfsods;'))

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