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
handler.create('Cats', ['name', 'age', 'type'])

handler.insert('Students', ['Yura', 19])
handler.insert('Students', ['Max', 19])
handler.insert('Students', ['Bob', 24])

handler.insert('Cats', ['A', 1, 9])
handler.insert('Cats', ['B', 2, 8])
handler.insert('Cats', ['C', 3, 7])
handler.insert('Cats', ['D', 4, 6])

# handler.select('Students')
# handler.select('Cats')

handler.select('Cats', column='name', cond='=', value='D')
