from database import *
import myparser

def search_table(tables_dict: dict, name: str) -> int:
    return tables_dict.get(name, -1)

def handle_create_command(tables_dict, table_name, column_names):
    if table_name not in tables_dict:
        tables_dict[table_name] = table(table_name, column_names, [])
        print(f"Таблицю успішно створено \"{table_name}\"")
    else:
        print("Таблиця з такою назвою вже існує")

def handle_insert_command(tables_dict, table_name, data):
    table_obj = search_table(tables_dict, table_name)
    if table_obj == -1:
        print("Такої таблички не існує")
    else:
        if len(table_obj.columns) == len(data):
            table_obj.new_row(data)
            print(f"Успішно додано в \'{table_name}\'")
        else:
            print(f"\'{table_name}\' має {len(table_obj.columns)} колонок, але ви мені надали {len(data)} аргумента")

def handle_select_from_command(tables_dict, table_name, data):
    table_obj = search_table(tables_dict, table_name)
    if table_obj == -1:
        print("Такої таблички не існує")
    else:
        select(table_obj, data[0], data[1]).print_table()

def handle_select_all_from_command(tables_dict, table_name):
    table_obj = search_table(tables_dict, table_name)
    if table_obj == -1:
        print("Такої таблички не існує")
    else:
        table_obj.print_table()

if __name__ == "__main__":
    tables_dict = {}
    
    print("Приклади команд:")
    print(" > create some_table (first_column, second_column);")
    print(" > insert into some_table (\"1\", \"data\");")
    print(" > select from some_table where second_column < \"data\";")
    print("------------------")
    
    while True:
        query = str(input("> "))
        try:
            result = myparser.parse(query)
            command = result[0]
            
            if command == "exit":
                break
            
            table_name = result[1]
            
            if command == "create":
                column_names = result[2:]
                handle_create_command(tables_dict, table_name, column_names)
                
            elif command == "insert into":
                data = result[2:]
                handle_insert_command(tables_dict, table_name, data)
            
            elif command == "insert":
                data = result[2:]
                handle_insert_command(tables_dict, table_name, data)

            elif command == "insert into":
                data = result[2:]
                handle_insert_command(tables_dict, table_name, data)
                
            elif command == "select from":
                data = result[2:]
                handle_select_from_command(tables_dict, table_name, data)
                
            else:
                print("Невідома команда")
                
        except Exception as e:
            print(str(e))