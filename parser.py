import re
from colorama import Fore, Style

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
    
    
def create(collection_name):
    print(Fore.GREEN + f'Collection {collection_name} has been created')
    print(Style.RESET_ALL, end='')

def insert(collection_name, param):
    print(Fore.GREEN + f'Document has been added to {collection_name}')
    print(Style.RESET_ALL, end='')

def print_index(collection_name):
    print(Fore.GREEN + f'Print_index function')
    print(Style.RESET_ALL, end='')

def search(collection_name, param):
    print(Fore.GREEN + f'Search function')
    print(Style.RESET_ALL, end='')

def invalid_syntax():
    print(Fore.RED + 'Invalid syntax')
    print(Style.RESET_ALL, end='')


if __name__ == "__main__":
    while True:
        command, coll_name, param = read()
        
        match command:
            case 'exit':
                break
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
                    invalid_syntax()
            case _:
                print(Fore.RED + f'{command}')
                print(Style.RESET_ALL, end='')