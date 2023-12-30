from bintrees import FastRBTree
from collections import defaultdict
import re

def print_table_by_columns(arrays, column_names):
    if len(arrays)==0:
        print("No data in columns")
        arrays = [[" "] for _ in column_names ]
    elif len(arrays[0])==0:
        print("No data in columns")
        arrays = [[" "] for _ in column_names ]
        
        
    num_columns = len(arrays)
    max_lengths = [max(len(elem) for elem in array) for array in arrays]

    headers = column_names

    for i in range(num_columns):
        max_lengths[i] = max(max_lengths[i], len(headers[i]))

    print("+" + "+".join("-" * (length + 2) for length in max_lengths) + "+")

    header_row = "| " + " | ".join(f"{headers[i]:<{max_lengths[i]}}" for i in range(num_columns)) + " |"
    print(header_row)

    print("+" + "+".join("-" * (length + 2) for length in max_lengths) + "+")

    num_rows = max(len(array) for array in arrays)

    for j in range(num_rows):
        row = "| " + " | ".join(f"{arrays[i][j]:<{max_lengths[i]}}" if j < len(arrays[i]) else " " * max_lengths[i] for i in range(num_columns)) + " |"
        print(row)
        print("+" + "+".join("-" * (length + 2) for length in max_lengths) + "+")


class Column:
    def __init__(self, name, indexed=False):
        self.name = name
        self.indexed = indexed


class Table:
    def __init__(self, table_name):
        self.table_name = table_name
        self.columns = {}
        self.data = {column_name: [] for column_name in self.columns}
        self.indexes = {column_name: {} for column_name in self.columns}
        self.bst_indexes = defaultdict(FastRBTree)

    def add_column(self, column_name, indexed=False):
        if column_name not in self.columns:
            self.columns[column_name] = Column(column_name, indexed)
            self.data[column_name] = []

            if indexed:
                self.indexes[column_name] = {}
        else:
            print(f"Column '{column_name}' already exists in table '{self.table_name}'")

    def add_value(self, column_name, value):
        # print(f"trying to add value {value} to table {self.table_name} in column {column_name}")
        value = str(value)
        if column_name in self.columns:
            if self.columns[column_name].indexed:
                if value in self.indexes[column_name]:
                    print(f"Value '{value}' already exists in column '{column_name}' (indexed)")
                    return False  # Abort insertion due to duplicate value in indexed column
                indexed_i = len(self.data[column_name])
                self.indexes[column_name][value] = indexed_i
                self.bst_indexes[column_name][value] = indexed_i
                
            self.data[column_name].append(value)
        else:
            print(f"Column '{column_name}' does not exist in table '{self.table_name}'")

        return True  # Successful insertion
    
    def add_row(self, values):
        if len(values) != len(self.columns):
            print("Number of values does not match the number of columns.")
            return False

        for i, col_name in enumerate(self.columns):
            self.add_value(col_name, values[i])

        return True
    
    def select_rows_where_equal_by_value(self, column_name, value):
        value = str(value)
        if column_name not in self.columns:
            print(f"Column '{column_name}' does not exist in table '{self.table_name}'")
            return []

        if self.columns[column_name].indexed :
            if value in self.indexes[column_name]:
                row_index = self.indexes[column_name][value]
                selected_row = self._get_row_by_index(row_index)
                return [selected_row]
            else:
                return []
        else:
            # Perform linear search if column is not indexed or value not found in index
            return self._select_rows_where_equal_linear_by_value(column_name, value)

    def _select_rows_where_equal_linear_by_value(self, column_name, value):
        selected_rows = []
        column_data = self.data[column_name]
        for i, val in enumerate(column_data):
            if val == value:
                selected_rows.append(self._get_row_by_index(i))
        return selected_rows

    def _get_row_by_index(self, index):
        row = [self.data[col][index] for col in self.columns]
        return row

    def select_rows_where_equal_by_column(self, column_name1, column_name2):
        if column_name1 not in self.columns or column_name2 not in self.columns:
            print("One or more columns do not exist in the table.")
            return []
        
        selected_rows = []
        for i in range(len(self.data[column_name1])):
            if self.data[column_name1][i] == self.data[column_name2][i]:
                selected_rows.append(self._get_row_by_index(i))

        return selected_rows

    def select_rows_where_greater_by_value(self, column_name, value):
        value = str(value)
        if column_name not in self.columns:
            print(f"Column '{column_name}' does not exist in table '{self.table_name}'")
            return []

        if self.columns[column_name].indexed:
            ceiling_item_key, _ = self.bst_indexes[column_name].ceiling_item(value)
            
            greater_indices = [value for _, value in self.bst_indexes[column_name].iter_items(ceiling_item_key)]


            if value in self.indexes[column_name]:
                greater_indices.remove(self.indexes[column_name][value])
            return [self._get_row_by_index(idx) for idx in greater_indices]
        else:
            # Perform linear search if column is not indexed
            return self._select_rows_where_greater_linear_by_value(column_name, value)

    def _select_rows_where_greater_linear_by_value(self, column_name, value):
        selected_rows = []
        column_data = self.data[column_name]
        for i, val in enumerate(column_data):
            if val > value:
                selected_rows.append(self._get_row_by_index(i))
        return selected_rows

    def select_rows_where_greater_by_column(self, column_name1, column_name2):
        if column_name1 not in self.columns or column_name2 not in self.columns:
            print("One or more columns do not exist in the table.")
            return []
        
        selected_rows = []
        for i in range(len(self.data[column_name1])):
            if self.data[column_name1][i] > self.data[column_name2][i]:
                selected_rows.append(self._get_row_by_index(i))

        return selected_rows

    def get_column(self, column_name):
        return self.columns.get(column_name, None)

    def display_columns(self):
        print(f"Columns in table '{self.table_name}':")
        column_names = ["Column Name","Indexed"]
        first_column = []
        second_column = []
        for column_name, column_obj in self.columns.items():
            first_column.append(column_name)
            second_column.append(str(column_obj.indexed))
        print_table_by_columns([first_column,second_column],column_names)

    def display_table(self):
        print(f"Table: '{self.table_name}'")
        column_names = []
        column_values = []
        for column_name, values in self.data.items():
            column_names.append(column_name)
            column_values.append(values)
        print_table_by_columns(column_values,column_names)

    @staticmethod
    def join_tables(table1, table2, table1_column=None, table2_column=None):
        rows = []

        if table1_column and table2_column:
            if table1.data.get(table1_column) is None or table2.data.get(table2_column) is None:
                print("Specified columns not found in tables.")
                return rows

            if table2.columns[table2_column].indexed:
                for i in range(len(table1.data[table1_column])):
                    value = table1.data[table1_column][i]
                    if value in table2.indexes[table2_column]:
                        index_in_table2 = table2.indexes[table2_column][value]
                        rows.extend([
                            table1._get_row_by_index(i) + table2._get_row_by_index(index_in_table2)
                        ])
            else:
                for i in range(len(table1.data[table1_column])):
                    for j in range(len(table2.data[table2_column])):
                        if table1.data[table1_column][i] == table2.data[table2_column][j]:
                            row1 = table1._get_row_by_index(i)
                            row2 = table2._get_row_by_index(j)
                            rows.append(row1 + row2)
        else:
            for i in range(len(table1.data[next(iter(table1.data))])):
                for j in range(len(table2.data[next(iter(table2.data))])):
                    row1 = table1._get_row_by_index(i)
                    row2 = table2._get_row_by_index(j)
                    rows.append(row1 + row2)

        return rows


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.tables = {}

    def add_table(self, table_name):
        if table_name not in self.tables:
            self.tables[table_name] = Table(table_name)
        else:
            print(f"Table '{table_name}' already exists in database '{self.db_name}'")

    def get_table(self, table_name):
        return self.tables.get(table_name, None)

    def display_tables(self):
        print(f"Tables in database '{self.db_name}':",", ".join(self.tables))
        print()

my_db = Database("MyDatabase")

def StringParser(input, database = my_db):
    end_index = input.find(";")
    if end_index == -1:
        print('Incorrect syntax. Command must end with a semicolon')
        return

    command = input[:end_index + 1]
    command = re.sub(r'[\n\t\r]', ' ', command)
    command = re.sub(r'  +', ' ', command)

    # Now checking for special words or arguments
    if command.startswith("CREATE TABLE"):
        pattern = r'CREATE TABLE (\w+) \((.*?)\);'
        match = re.match(pattern, command)
        if match:
            table_name = match.group(1)
            arguments_string = match.group(2)
            arguments = re.findall(r'(\w+\s*(?:INDEXED)?)', arguments_string)
            ARGUMENTS_tokens = {arg.replace('INDEXED', '').strip(): 'INDEXED' in arg for arg in arguments}
            database.add_table(table_name)
            table = database.get_table(table_name)
            for arg, indexed in ARGUMENTS_tokens.items():
                table.add_column(arg, indexed)
        else:
            print('Incorrect syntax for CREATE TABLE')
            return

    elif command.startswith("INSERT"):
        pattern = r'INSERT (\w+) \((.*?)\);'
        match = re.match(pattern, command)
        if match:
            table_name = match.group(1)
            ARGUMENTS_token = re.findall(r"'([^']*)'", match.group(2))
            table = database.get_table(table_name)
            if table:
                table.add_row(ARGUMENTS_token)
            else:
                print(f"Table '{table_name}' not found.")
        else:
            print('Incorrect syntax for INSERT')
            return

    elif command.startswith("SELECT FROM"):
        pattern = r"SELECT FROM\s+(\w+)(?:\s+JOIN\s+(\w+)(?:\s+ON\s+(\w+)\.(\w+)\s*=\s*(\w+)\.(\w+))?)?(?:\s+WHERE\s+(\w+)\s*(>|=)\s*('([^']*)'|\w+))?\s*;"
        match = re.match(pattern, command)
        if match:
            TABLE_token = match.group(1)
            JOIN_token = match.group(2)
            ON_token = ( match.group(3),match.group(4),match.group(5),match.group(6) ) 
            WHERE_token = match.group(7),match.group(8),match.group(9)
            # print("TABLE_token:", TABLE_token)
            # print("JOIN_token:", JOIN_token)
            # print("ON_token:", ON_token)
            # print("WHERE_token:", WHERE_token)
            SelectFromTableFunc(database, TABLE_token, JOIN_token, ON_token, WHERE_token)
            # Implement the SELECT FROM functionality using database methods
            # For example: database.select_from(TABLE_token, JOIN_token, ON_token, WHERE_token)
        else:
            print('Incorrect syntax for SELECT FROM')
            return

    else:
        print(f"Unknown command '{command[:12]}...'")


def SelectFromTableFunc(database, TABLE_token, JOIN_token, ON_token, WHERE_token):
    table_name = TABLE_token
    join_table_name = JOIN_token
    on_table1, on_column1, on_table2, on_column2 = ON_token
    where_first, condition, where_second = WHERE_token
    table = database.get_table(table_name)
    # print whole table
    if table_name and not join_table_name and not where_first:
        table.display_table()
    # print table with where cond 
    elif table_name and not join_table_name and where_first:
        WhereFilter(table,condition,where_first,where_second)
    # print joined table
    elif table_name and join_table_name:
        join_table = database.get_table(join_table_name)
        temp_table = Table(f"{table_name}_{table_name}")
        for column_name in table.columns:
            temp_table.add_column(column_name)
        for column_name in join_table.columns:
            temp_table.add_column(column_name)
        if on_column1:
            joined_table_rows = Table.join_tables(table, join_table, on_column1, on_column2)
        else: 
            joined_table_rows = Table.join_tables(table, join_table)
        for row in joined_table_rows:
            temp_table.add_row(row)
        if where_first:
            # print joined table with where cond
            WhereFilter(temp_table,condition,where_first,where_second)
        else:
            temp_table.display_table()
    
    

def WhereFilter(table, condition, first_column ,value_or_column:str):
    if value_or_column.startswith("'"):
        is_column = False
        value_or_column = value_or_column[1:-1]
    elif value_or_column in table.columns:
        is_column = True
    else:
        print("Bad WHERE second_column name")
        return
    if first_column not in table.columns:
        print("Bad WHERE first_column name")
        return
    
    if condition == "=":
        if is_column:
            rows = table.select_rows_where_equal_by_column(first_column, value_or_column)
        else:
            rows = table.select_rows_where_equal_by_value(first_column, value_or_column)
    else:
        if is_column:
            rows = table.select_rows_where_greater_by_column(first_column, value_or_column)
        else:
            rows = table.select_rows_where_greater_by_value(first_column, value_or_column)
    columns = transpose_array(rows)
    print_table_by_columns(columns, list(table.columns))

def transpose_array(arr):
    return list(map(list, zip(*arr)))




InputString = list()
InputString.append("CREATE  TABLE Table1   (Column1 INDEXED, Column2, Column3, Column4); abrakadabra")
InputString.append("CREATE  TABLE Table2   (Col1, Col2, Col3, Col4); abrakadabra")
InputString.append("INSERT Table1 ('a','num2212112','num3121121211','num4'); awdawdwa")
InputString.append("INSERT Table1 ('b','num2212112','num3121121211','num4'); awdawdwa")
InputString.append("INSERT Table1 ('c','num2212112','num3121121211','num4'); awdawdwa")

InputString.append("INSERT Table2 ('num1','a','num3121121211','num4'); awdawdwa")
InputString.append("INSERT Table2 ('num','b','num3121121211','b'); awdawdwa")
# InputString.append("SELECT FROM Table1 ;")
# InputString.append("SELECT FROM Table2 ;")
# InputString.append("SELECT FROM Table1 JOIN Table2 ON Table1.Column1=Table2.Col1 ;")
InputString.append("SELECT FROM Table1  WHERE Column1 > 'a' ;")
# InputString.append("SELECT FROM Table1 JOIN Table2 ON Table1.Column1=Table2.Col1 WHERE Col2 > 'a';")
# InputString.append("SELECT FROM Table2 WHERE Col2 > 'a';")

for i in InputString:
    print(i)
    StringParser(i)



