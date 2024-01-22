import re


class DB_Handler:
    def __init__(self):
        self.tables = {}
        self.indexed_columns = {}

    def create(self, table_name: str, column_definitions: list):
        columns = {}
        for column_def in column_definitions:
            if 'INDEXED' in column_def:
                column_name, _ = column_def.split(' INDEXED')
                self.indexed_columns[f'{table_name}.{column_name}'] = True
            else:
                column_name = column_def
            columns[column_name] = []

        self.tables[table_name] = columns
        print(f'Table {table_name} has been created.')

    def insert(self, table_name: str, values: list):
        if table_name in self.tables:
            columns = self.tables[table_name]
            if len(values) != len(columns):
                print(f"Error: The number of values does not match the number of columns in {table_name}.")
                return

            for (column, value), column_name in zip(zip(columns.values(), values), columns.keys()):
                column.append(value)
            print(f'1 row has been inserted into {table_name}.')
        else:
            print(f"Table '{table_name}' does not exist.")

    def select(self, table_name: str, left_join_table=None, join_condition=None, where_condition=None):
        if table_name not in self.tables:
            print(f"Table '{table_name}' does not exist.")
            return

        result_keys = list(self.tables[table_name].keys())
        result_table = [list(row) for row in zip(*self.tables[table_name].values())]

        if left_join_table:
            if left_join_table not in self.tables:
                print(f"Table '{left_join_table}' does not exist.")
                return

            join_table_columns = list(self.tables[left_join_table].keys())
            # print(join_table_columns)
            result_keys.extend(join_table_columns)
            # print(result_keys)

            if join_condition:
                t1_column, t2_column = join_condition.split(' = ')
                t1_index = result_keys.index(t1_column)
                t2_index = result_keys.index(t2_column) - len(self.tables[table_name])

                joined_table = []
                for row in result_table:
                    join_matched = False
                    for join_row in zip(*self.tables[left_join_table].values()):
                        if row[t1_index] == join_row[t2_index]:
                            joined_table.append(row + list(join_row))
                            join_matched = True
                            break
                    if not join_matched:
                        joined_table.append(row + [None] * len(join_table_columns))
                result_table = joined_table

        if where_condition:
            where_column, where_value = where_condition.split(' < ')
            where_value = where_value.strip('"')
            if where_column in result_keys:
                where_index = result_keys.index(where_column)
                # print(type(where_index))
                # print(result_table)
                result_table = [row for row in result_table if str(row[where_index]) < where_value]
            else:
                print(f"Column '{where_column}' not found in the table.")
                return

        print(', '.join(result_keys))
        for row in result_table:
            print(' '.join(str(val) if val is not None else '' for val in row))

    def parse_command(self, command):

        create_match = re.match(r'(?i)CREATE (\w+) \((.*)\);', command)
        if create_match:
            table_name = create_match.group(1)
            column_definitions = [col.strip() for col in create_match.group(2).split(',')]
            self.create(table_name, column_definitions)
            return

        insert_match = re.match(r'(?i)INSERT INTO (\w+)\((.*)\);', command)
        if insert_match:
            table_name = insert_match.group(1)
            matches = re.findall(r'"([^"]*)"', insert_match.group(2))

            # values = [val.strip() for val in insert_match.group(2).replace('"', '').split(',')]
            self.insert(table_name, matches)
            return

        insert_match = re.match(r'(?i)INSERT (\w+) \((.*)\);', command)
        if insert_match:
            table_name = insert_match.group(1)
            matches = re.findall(r'"([^"]*)"', insert_match.group(2))

            # values = [val.strip() for val in insert_match.group(2).replace('"', '').split(',')]
            self.insert(table_name, matches)
            return

        select_match = re.match(r'(?i)SELECT FROM (\w+);', command)
        if select_match:
            table_name = select_match.group(1)
            self.select(table_name)
            return

        select_where_match = re.match(r'(?i)SELECT FROM (\w+) WHERE (\w+) < "(.*?)";', command)
        if select_where_match:
            table_name = select_where_match.group(1)
            where_column = select_where_match.group(2)
            # print(where_column)
            where_value = select_where_match.group(3)
            try:
                if self.tables[table_name][where_column]:
                    where_condition = f"{where_column} < {where_value}"
                    self.select(table_name, where_condition=where_condition)
                    return
            except KeyError:
                where_column += ' INDEXED'
                where_condition = f"{where_column} < {where_value}"
                self.select(table_name, where_condition=where_condition)
                return

        select_where_match = re.match(r'(?i)SELECT FROM (\w+) WHERE (\w+) < (\w+);', command)
        if select_where_match:
            table_name = select_where_match.group(1)
            where_column = select_where_match.group(2)
            # print(where_column)
            where_value = select_where_match.group(3)
            try:
                if self.tables[table_name][where_column]:
                    where_condition = f"{where_column} < {where_value}"
                    self.select(table_name, where_condition=where_condition)
                    return
            except KeyError:
                where_column += ' INDEXED'
                where_condition = f"{where_column} < {where_value}"
                self.select(table_name, where_condition=where_condition)
                return

        select_join_match = re.match(r'(?i)SELECT FROM (\w+) LEFT_JOIN (\w+) ON (\w+) = (\w+);', command)
        if select_join_match:
            table_name = select_join_match.group(1)
            join_table = select_join_match.group(2)
            join_condition = f"{select_join_match.group(3)} = {select_join_match.group(4)}"
            self.select(table_name, left_join_table=join_table, join_condition=join_condition)
            return

        select_join_where_match = re.match(r'(?i)SELECT FROM (\w+) LEFT_JOIN (\w+) ON (\w+) = (\w+) WHERE (\w+) < "(.*?)";', command)
        if select_join_where_match:
            table_name = select_join_where_match.group(1)
            join_table = select_join_where_match.group(2)
            join_condition = f"{select_join_where_match.group(3)} = {select_join_where_match.group(4)}"
            where_column = select_join_where_match.group(5)
            where_value = select_join_where_match.group(6)
            where_condition = f"{where_column} < {where_value}"

            self.select(table_name, left_join_table=join_table, join_condition=join_condition, where_condition=where_condition)
            return

        print("Invalid command.")
