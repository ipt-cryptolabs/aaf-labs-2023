import re


class DB_Handler:
    def __init__(self):
        self.tables = {}

    def create(self, table_name: str, columns: list):
        self.tables[table_name] = {column: [] for column in columns}
        print(f'Table {table_name} has been created.')

    def insert(self, table_name: str, values: list):
        if table_name in self.tables:
            for n, v in enumerate(self.tables[table_name].values()):
                v.append(values[n])
            print(f'1 row has been inserted into {table_name}.')
        else:
            print(f"Table '{table_name}' does not exist.")

    def select(self, table_name: str, left_join_table=None, join_condition=None, where_condition=None):
        if table_name in self.tables:
            if not left_join_table:
                if where_condition:
                    where_column, where_value = where_condition.split(' < ')
                    column_values = self.tables[table_name][where_column]
                    filtered_indices = [idx for idx, val in enumerate(column_values) if val < where_value]
                    selected_values = [[self.tables[table_name][col][idx] for col in self.tables[table_name]] for idx in
                                       filtered_indices]

                    keys = list(self.tables[table_name].keys())
                    print(' '.join(keys))
                    for row in selected_values:
                        print(' '.join(str(val) for val in row))
                else:
                    selected_values = [list(row) for row in zip(*self.tables[table_name].values())]

                    keys = list(self.tables[table_name].keys())
                    print(' '.join(keys))
                    for row in selected_values:
                        print(' '.join(str(val) for val in row))

            elif left_join_table and join_condition:
                table_1, table_2 = table_name, left_join_table
                t1_column, t2_column = join_condition.split(' = ')
                t1_values, t2_values = self.tables[table_1][t1_column+' INDEXED'], self.tables[table_2][t2_column+' INDEXED']
                result_table = []

                for t1_idx, t1_val in enumerate(t1_values):
                    matched_indices = [t2_idx for t2_idx, t2_val in enumerate(t2_values) if t1_val == t2_val]
                    if matched_indices:
                        for t2_idx in matched_indices:
                            row = [self.tables[table_1][col][t1_idx] for col in self.tables[table_1]]
                            row.extend([self.tables[table_2][col][t2_idx] for col in self.tables[table_2]])
                            result_table.append(row)
                    else:
                        row = [self.tables[table_1][col][t1_idx] for col in self.tables[table_1]]
                        row.extend(['' for _ in self.tables[table_2]])
                        result_table.append(row)

                keys = list(self.tables[table_1].keys()) + list(self.tables[table_2].keys())
                print(', '.join(keys))
                for row in result_table:
                    print(' '.join(str(val) for val in row))


            else:
                print("Invalid SELECT command.")
        else:
            print(f"Table '{table_name}' does not exist.")

    def parse_command(self, command):

        create_match = re.match(r'CREATE (\w+) \((.*)\);', command)
        if create_match:
            table_name = create_match.group(1)
            columns = [col.strip() for col in create_match.group(2).split(',')]
            self.create(table_name, columns)
            return

        insert_match = re.match(r'INSERT INTO (\w+)\((.*)\);', command)
        if insert_match:
            table_name = insert_match.group(1)
            values = [val.strip() for val in insert_match.group(2).split(',')]
            self.insert(table_name, values)
            return

        insert_match = re.match(r'INSERT (\w+) \((.*)\);', command)
        if insert_match:
            table_name = insert_match.group(1)
            values = [val.strip() for val in insert_match.group(2).split(',')]
            self.insert(table_name, values)
            return

        select_match = re.match(r'SELECT FROM (\w+);', command)
        if select_match:
            table_name = select_match.group(1)
            self.select(table_name)
            return

        select_where_match = re.match(r'SELECT FROM (\w+) WHERE (\w+) INDEXED < “(.*?)”;', command)
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

        select_join_match = re.match(r'SELECT FROM (\w+)\s+LEFT_JOIN (\w+)\s+ON (\w+) INDEXED\s*=\s*(\w+) INDEXED;', command)
        if select_join_match:
            table_name = select_join_match.group(1)
            join_table = select_join_match.group(2)
            join_condition = f"{select_join_match.group(3)} = {select_join_match.group(4)}"
            self.select(table_name, left_join_table=join_table, join_condition=join_condition)
            return

        print("Invalid command.")
