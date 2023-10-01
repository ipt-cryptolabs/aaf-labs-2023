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

        command_handled = False

        if full_cmd.upper().startswith("CREATE"):
            parsed_command = parse_create(full_cmd)
            if parsed_command["success"]:
                handle_create(parsed_command)
                command_handled = True

        elif full_cmd.upper().startswith("INSERT"):
            parsed_command = parse_insert(full_cmd)
            if parsed_command["success"]:
                handle_insert(parsed_command)
                command_handled = True

        elif full_cmd.upper().startswith("SELECT"):
            parsed_command = parse_select(full_cmd)
            if parsed_command["success"]:
                handle_select(parsed_command)
                command_handled = True

        if not command_handled:
            print("Error: Unknown or incorrect command")

        buffer = []
