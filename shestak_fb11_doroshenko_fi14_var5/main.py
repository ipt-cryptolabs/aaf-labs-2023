import new_handler


db = new_handler.DB_Handler()

while True:
    command = input()
    if command == 'exit':
        break
    db.parse_command(command)
