from myparser import parse_create, parse_insert, parse_select
from database import Database


def parse_command(command):
    tokens = []
    current_token = ''
    in_parentheses = False

    for char in command:
        if char in ('(', ')', ',', ';'):
            if current_token.strip(): 
                tokens.append(current_token.strip())
                current_token = ''
            tokens.append(char)
            if char == '(':
                in_parentheses = True
            elif char == ')':
                in_parentheses = False
        elif char == ' ' and not in_parentheses:
            if current_token.strip():  
                tokens.append(current_token.strip())
                current_token = ''
        else:
            current_token += char

    if current_token.strip(): 
        tokens.append(current_token.strip())

    return tokens

def handle_create(db, full_cmd):
    tokens = parse_command(full_cmd)
    try:
        create_command = parse_create(tokens)
        result = db.create_table(create_command)
        print(result)
    except ValueError as e:
        print(e)

def handle_insert(db, full_cmd):
    tokens = parse_command(full_cmd)
    try:
        insert_command = parse_insert(tokens)
        result = db.insert_into_table(insert_command)
        print(result)
    except ValueError as e:
        print(e)

def handle_select(db, full_cmd):
    tokens = parse_command(full_cmd)
    try:
        select_command = parse_select(tokens)
        result = db.select_from_table(select_command)
        print(result)
    except ValueError as e:
        print(e)

def main():
    db = Database()

    print("Example:")
    print(" > create table (first_column, second_column, ....);")
    print(" > insert table (\"1\", \"data\", ....);")
    print(" > select from table where second_column < \"data\";")
    print("------------------")

    for cmd in iter(input, 'exit'):
        buffer = [cmd]

        if ';' in cmd:
            full_cmd = ' '.join(buffer).strip()
            
            try:
                if full_cmd.lower().startswith("create"):
                    handle_create(db, full_cmd)
                elif full_cmd.lower().startswith("insert"):
                    handle_insert(db, full_cmd)
                elif full_cmd.lower().startswith("select"):
                    handle_select(db, full_cmd)
                else:
                    print("Error: Unknown or incorrect command")
            except ValueError as e:
                print(e)

if __name__ == "__main__":
    main()