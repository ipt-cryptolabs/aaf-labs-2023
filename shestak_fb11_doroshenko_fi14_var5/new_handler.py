import re
import sortedcontainers


class DB_Handler:
    def __init__(self):
        self.tables = {}
        self.indexed = []

    def create(self, table_name: str, column_definitions: list):
        columns = {}
        for column_def in column_definitions:
            if 'INDEXED' in column_def:
                column_name = column_def.replace(' INDEXED', '')
                columns[column_name] = sortedcontainers.SortedDict()
                self.indexed.append(column_name)
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

            # row_id = len(next(iter(columns.values())))
            max_value = -1
            # print(columns.values())

            for i in list(columns.values()):
                if len(i) == 0:
                    row_id = 0
                elif type(i) != type([]):
                    max_value = max([max(x) if type(x) == type([]) else x for x in i.values()])
            row_id = max_value+1

            for (column, value), column_name in zip(zip(columns.values(), values), columns.keys()):
                if type(column) == type([]):
                    column.append(value)
                    # print(1)
                else:
                    if value in column:
                        column[value] = [column[value]] + [row_id]
                    else:
                        column.setdefault(value, row_id)
                    # print(2)

            print(f'1 row has been inserted into {table_name}.')
        else:
            print(f"Table '{table_name}' does not exist.")

    def select(self, table_name: str, left_join_table=None, join_condition=None, where_condition=None):
        if table_name not in self.tables:
            print(f"Table '{table_name}' does not exist.")
            return

        result_keys = list(self.tables[table_name].keys())

        fin_list = []
        for i in list(self.tables[table_name].values()):
            if type(i) == type([]):
                fin_list.append(i)
            else:
                pairs = []
                for k, v in i.items():
                    if isinstance(v, list):
                        for vv in v:
                            pairs.append((k, vv))
                    else:
                        pairs.append((k, v))

                sorted_pairs = sorted(pairs, key=lambda x: x[1])

                sorted_keys = [k for k, v in sorted_pairs]
                fin_list.append(sorted_keys)
                # print(sorted_keys)

        # print(fin_list)

        result_table = [row for row in zip(*fin_list)]


        if left_join_table:
            if left_join_table not in self.tables:
                print(f"Table '{left_join_table}' does not exist.")
                return

            join_table_columns = list(self.tables[left_join_table].keys())
            result_keys.extend(join_table_columns)

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

        # тут реалізована індексація, у випадку коли колонка має її
        if where_condition:
            where_column, where_value = where_condition.split(' < ')
            where_value = where_value.strip('"')

            if where_column in self.indexed:
                column_data = self.tables[table_name][where_column]
                filtered_keys = list(column_data.irange(maximum=where_value, inclusive=(True, False)))

                filtered_rows = []

                for i in filtered_keys:
                    if type(column_data[i]) != type([]):
                        filtered_rows.append(result_table[column_data[i]])
                    else:
                        for v in column_data[i]:
                            filtered_rows.append(result_table[v])

                result_table = filtered_rows

            else:
                column_data = self.tables[table_name][where_column]
                column_index = list(self.tables[table_name].keys()).index(where_column)

                filtered_rows = []

                for row in zip(*self.tables[table_name].values()):
                    value_to_check = row[column_index].split('$')[0]
                    if value_to_check < where_value:
                        filtered_rows.append(list(map(lambda x: x.split('$')[0], row)))

                result_table = filtered_rows

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

        select_join_where_match = re.match(
            r'(?i)SELECT FROM (\w+) LEFT_JOIN (\w+) ON (\w+) = (\w+) WHERE (\w+) < "(.*?)";', command)
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