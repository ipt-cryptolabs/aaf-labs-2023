from Parser import parse_create, parse_insert, parse_select, tokenize
from DataBase import Database

def main():
    db = Database()

    buffer = []
    while True:
        prompt = '...  ' if buffer else '> '
        cmd = input(prompt)  
              
        if cmd.strip().lower() == 'exit':
            break

        buffer.append(cmd)

        if ';' in cmd:
            full_cmd = ' '.join(buffer).strip()
            tokens = tokenize(full_cmd)
            
            try:
                if tokens[0].value.upper() == "CREATE":
                    create_command = parse_create(tokens)
                    result = db.create_table(create_command)
                    print(result)

                elif tokens[0].value.upper() == "INSERT":
                    insert_command = parse_insert(tokens)
                    result = db.insert_into_table(insert_command)
                    print(result)

                elif tokens[0].value.upper() == "SELECT":
                    select_command = parse_select(tokens)
                    result = db.select_from_table(select_command)
                    print(result)
                else:
                    print("Error: Unknown or incorrect command")
            except ValueError as e:
                print(e)

            buffer = []

if __name__ == "__main__":
    main()
