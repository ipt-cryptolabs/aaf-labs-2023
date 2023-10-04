from Parser import parse_create, parse_insert, parse_select
from CommandHandler import handle_create, handle_insert, handle_select


buffer = []
while True:
    cmd = input()       
    if cmd.strip().lower() == 'exit':
        break

    buffer.append(cmd)

    if ';' in cmd:
        full_cmd = ' '.join(buffer).strip()

        if full_cmd.upper().startswith("CREATE"):
            parsed_command = parse_create(full_cmd)
            if parsed_command["success"]:
                handle_create(parsed_command)
            else:
                print("Incorrect syntax for CREATE. Correct syntax is CREATE table_name (column_name [INDEXED] [, ...]);")

        elif full_cmd.upper().startswith("INSERT"):
            parsed_command = parse_insert(full_cmd)
            if parsed_command["success"]:
                handle_insert(parsed_command)
            else:
                print("Incorrect syntax for INSERT. Correct syntax is INSERT [INTO] table_name (“value” [, ...]);")

        elif full_cmd.upper().startswith("SELECT"):
            parsed_command = parse_select(full_cmd)
            if parsed_command["success"]:
                handle_select(parsed_command)
            else:
                print("""Incorrect syntax for SELECT. Correct syntax is 
                    SELECT [agg_function(agg_column) [, ... ]]
                     FROM table_name
                     [WHERE condition]
                     [GROUP_BY column_name [, ...] ];""")
        else:
            print("Error: Unknown or incorrect command")

        buffer = []

