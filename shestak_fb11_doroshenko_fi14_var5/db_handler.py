import json


class DB_Handler:
    def __init__(self, file_path):
        self.path = file_path

    def create(self, table_name: str, columns: list):
        new_table = {table_name: {column: [] for column in columns}}
        with open(self.path, 'r', encoding='UTF-8') as f:
            table = dict(json.load(f))
            table.update(new_table)
        with open(self.path, 'w', encoding='UTF-8') as f:
            json.dump(table, f)
        print(f'Table {table_name} has been created.')

    def insert(self, table_name: str, values: list):
        with open(self.path, 'r', encoding='UTF-8') as f:
            table = dict(json.load(f))
            for n, v in enumerate(table[table_name].values()):
                v.append(values[n])
        with open(self.path, 'w', encoding='UTF-8') as f:
            json.dump(table, f)
        print(f'1 row has been inserted into {table_name}.')

    def select(self, table_name: str, column=None, cond=None, value=None):
        pass
