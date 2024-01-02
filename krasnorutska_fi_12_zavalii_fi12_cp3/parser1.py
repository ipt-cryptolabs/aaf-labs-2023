import re
from colorama import Fore, Style
from functions import *

commands = ['create', 'insert', 'print_index', 'search']

def read():
    read_command = []

    while True:
        try:
            line = ' '.join(re.split(r'\s+', input().strip()))
        except EOFError:
            return EOFError, None, None

        if ';' in line:
            read_command.append(line + ' ')
            break
        else:
            read_command.append(line) 

        if 'exit' in line:
            return 'exit', None, None
        if 'clear' in line:
            return 'clear', None, None
        if 'show' in line:
            return 'show', None, None
    
    pattern = r'(\w+)\s+(\w+)\s*([^;]*)'
    match = re.match(pattern, ''.join(read_command))

    try:
        command = match.group(1)  
        coll_name = match.group(2) 
        param = match.group(3).strip() if match.group(3) is not None else None
    except AttributeError: 
        return 'Invalid syntax', None, None  
    except Exception as e:
        return str(e), None, None

    return command.lower() if command.lower() in commands else f'Command "{command}" is not defined', coll_name, param
    
def invalid_syntax():
    print(Fore.RED + 'Invalid syntax')
    print(Style.RESET_ALL, end='')


if __name__ == "__main__":
    while True:
        command, coll_name, param = read()
        
        match command:
            case 'exit':
                break
            case 'clear':
                print('\033c')
            case 'show':
                show()
            case 'create':
                if param == '':
                    create(coll_name)
                else:
                    invalid_syntax()
            case 'insert':
                if param != '':
                    insert(coll_name, param)
                else:
                    invalid_syntax()
            case 'print_index':
                if param == '':
                    print_index(coll_name)
                else:
                    invalid_syntax()
            case 'search':
                if param != '':
                    search(coll_name, param)
                else:
                    search_lite(coll_name)
            case _:
                print(Fore.RED + f'{command}')
                print(Style.RESET_ALL, end='')