# cond = True
# while cond:
#     command = input('Enter command: ')
#     if command == 'exit':
#         break
#     elif command == 'hi':
#         continue
#     else:
#         out = 5 + int(command)
#         print(f'Command: {str(out)}')


import db_handler

handler = db_handler.DB_Handler('db.json')
handler.create('Students', ['name', 'age'])
handler.create('Cats', ['name', 'age'])
handler.insert('Students', ['Yura', 19])
handler.insert('Students', ['Max', 19])
# handler.insert('1', [])

