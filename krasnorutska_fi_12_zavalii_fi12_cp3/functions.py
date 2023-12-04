import re
from colorama import Fore, Style

mycollections = {}
inverted_indexes = {}

def build_inverted_index(collection_name, doc): 
    inverted_index = {} if collection_name not in inverted_indexes else inverted_indexes[collection_name]
    pattern = r'[^a-zA-Z0-9_ ]'
    doc = re.sub(pattern, '', doc)
    unique_words = sorted( (set(doc.lower().split())) )
    
    doc_index = len(mycollections[collection_name])

    for word in unique_words:
        if word in inverted_index:
            inverted_index[word].append((doc_index, [index+1 for index, value in enumerate(doc.split()) if value.lower() == word]))
        else:
            inverted_index[word] = [(doc_index, [index+1 for index, value in enumerate(doc.split()) if value.lower() == word])]
        
    inverted_indexes[collection_name] = inverted_index

def create(collection_name):
    if collection_name not in mycollections:
        mycollections[collection_name] = []
        print(Fore.GREEN + f'Collection "{collection_name}" has been created')
        print(Fore.GREEN + f'Number of collections: {len(mycollections)}\n')
    else:
        print(Fore.YELLOW + 'A collection with the same name already exists. \n')
    print(Style.RESET_ALL, end='')

def insert(collection_name, doc):
    if collection_name in mycollections:
        table = mycollections.get(collection_name)
        table.append(doc)
        build_inverted_index(collection_name, doc)
        print(Fore.GREEN + f'Document has been added to "{collection_name}" collection.\n')
    else:
        print(Fore.YELLOW + f'Collection "{collection_name}" not found. \n')
    print(Style.RESET_ALL, end='')

def print_index(collection_name):
    if collection_name in mycollections:
        print(Fore.GREEN + f'Inverted Index for collection "{collection_name}":')
        for word, indexes in inverted_indexes[collection_name].items():
                print(f'"{word}":')
                for elem in indexes:
                    print(f'd{elem[0]} -> {elem[1]}')
        print()
    else:
        print(Fore.YELLOW + f'Collection "{collection_name}" not found.')
    print(Style.RESET_ALL, end='')

def search_lite(collection_name):
    if collection_name in mycollections:
        print('List of available documents:')
        for index, data in enumerate(mycollections[collection_name]):
            print(f'd{index+1}: "{data}"')
        print()
    else:
        print(Fore.YELLOW + f'Collection "{collection_name}" not found.\n')
    print(Style.RESET_ALL, end='')

def search_keyword(collection_name, query):
    keyword = query.split()[1]
    result = []
    if collection_name in inverted_indexes:
        if keyword.lower() in inverted_indexes[collection_name]:
            for item in inverted_indexes[collection_name][keyword.lower()]:
                result.append(f'd{item[0]}')
        
        print('Search result:')
        print(*sorted(set(result)))
        print()
    else:
        print(Fore.YELLOW + f'Collection "{collection_name}" not found or empty.\n')
    print(Style.RESET_ALL, end='')

def search_prefix(collection_name, query):
    prefix = query.split()[-1][:-1]
    result = []
    if collection_name not in mycollections:
        print(Fore.YELLOW + f'Collection "{collection_name}" not found or empty.\n')
        print(Style.RESET_ALL, end='')
        return  
    for keys, data in inverted_indexes[collection_name].items():
        if prefix.lower() == keys[:len(prefix)].lower():
            for item in data:
                result.append(f'd{item[0]}')
    print('Search result:')
    print(*sorted(set(result)))
    print()

def search_by_num(collection_name, query):
    pattern = re.compile(r'where (\w+) <(\d+)> (\w+)')
    match = pattern.match(query)
    result = []

    if match:
        values = [match.group(1).lower(), int(match.group(2)), match.group(3).lower()]
    else:
        print(Fore.YELLOW + 'SyntaxError\n')
    
    if values[0] and values[2] in inverted_indexes[collection_name]:
        word_1_list = inverted_indexes[collection_name][values[0]]
        word_2_list = inverted_indexes[collection_name][values[2]]
        for i in word_1_list:
            for j in word_2_list:
                if i[0] == j[0]:
                    for a in i[1]:
                        for b in j[1]:
                            if abs(a-b) == values[1]:
                                result.append(f'd{i[0]}')
        print('Search result:')
        print(*list(set(result)))
        print()
    else:
        print(Fore.YELLOW + "Can't find words in documents.\n")
    print(Style.RESET_ALL, end='')

def search(collection_name, query):
    pattern = re.compile(r'\bwhere\s(\w+$|\w+\*$|(\w+)\s<(\d+)>\s(\w+)$)', re.IGNORECASE)
    match = re.match(pattern, query)
    if match:
        temp = query.split()
        if len(temp) > 2:
            search_by_num(collection_name, query)
        elif temp[-1][-1] == '*':
            search_prefix(collection_name, query)
        else:
            search_keyword(collection_name, query)
    else:
        print(Fore.YELLOW + 'SyntaxError\n')
    print(Style.RESET_ALL, end='')

def show():
    for keys, items in mycollections.items():
        print(f'Collection "{keys}":')
        for i, d in enumerate(items):
            print(f'd{i+1}: "{d}"')
    print()