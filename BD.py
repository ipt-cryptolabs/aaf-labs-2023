import re

class Table:
    def __init__(self, name, columns):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
            raise ValueError("Invalid table name")

        self.name = name
        self.columns = []
        self.data = []

        # Check column names for validity
        for col_name, _ in columns:
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', col_name):
                raise ValueError(f"Invalid column name: {col_name}")
            self.columns.append(col_name)

    def insert(self, values):
        if len(values) != len(self.columns):
            print("Number of values doesn't match the number of columns")
            return

        try:
            numeric_values = [int(value) for value in values]
        except ValueError:
            print("All values must be integers")
            return

        self.data.append(numeric_values)
        print(f"1 row has been inserted into {self.name}.")

    def select(self, select_columns, where_condition=None, group_by=None):
        full_columns = self.columns
        filtered_data = []

        for row in self.data:
            if where_condition is None or self.evaluate_condition(where_condition, row):
                filtered_data.append(row)

        if group_by:
            grouped_data = {}
            group_indices = [i for i, col in enumerate(full_columns) if col in group_by]

            for row in filtered_data:
                group_key = tuple(row[i] for i in group_indices)
                if group_key not in grouped_data:
                    grouped_data[group_key] = []
                grouped_data[group_key].append(row)

        result_data = []

        for group_key, group_rows in grouped_data.items():
            agg_values = []
            for agg_func in select_columns:
                if '(' in agg_func and ')' in agg_func:
                    func_name, col_name = agg_func.split('(')[0], agg_func.split('(')[1][:-1]
                    col_index = full_columns.index(col_name)
                    if func_name == 'COUNT':
                        agg_value = len(group_rows)
                    elif func_name == 'MAX':
                        agg_value = max(row[col_index] for row in group_rows)
                    elif func_name == 'AVG':
                        agg_value = sum(row[col_index] for row in group_rows) / len(group_rows)
                    agg_values.append(agg_value)
                else:
                    col_index = full_columns.index(agg_func)
                    agg_values.append(group_key[group_indices.index(col_index)])
            result_data.append(tuple(agg_values))

        if not select_columns:
            select_columns = full_columns

        if not select_columns:
            return []

        formatted_result = [select_columns]
        formatted_result.extend(result_data)
        return formatted_result

    def evaluate_condition(self, condition, row):
        col_name, operator, value = condition.split()
        col_name = col_name.strip()
        col_index = self.columns.index(col_name)

        if operator == "=":
            return row[col_index] == int(value)
        elif operator == "!=":
            return row[col_index] != int(value)
        elif operator == "<":
            return row[col_index] < int(value)
        elif operator == ">":
            return row[col_index] > int(value)
        elif operator == "<=":
            return row[col_index] <= int(value)
        elif operator == ">=":
            return row[col_index] >= int(value)
        else:
            return False

class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
            print("Invalid table name")
            return

        if name in self.tables:
            print("Table already exists")
            return

        # Check column names for validity
        for col_name, _ in columns:
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', col_name):
                print(f"Invalid column name: {col_name}")
                return

        self.tables[name] = Table(name, columns)

        print(f"Table {name} has been created")

    def execute_query(self, command):

        command = command.strip().split(';')[0] + ';'

        parts = list(filter(None, command.split()))

        if not parts:
            return
        command_type = parts[0].upper()
        if command_type == "CREATE":
            self.handle_create_command(command)
        elif command_type == "INSERT":
            self.handle_insert_command(command)
        elif command_type == "SELECT":
            self.handle_select_command(command)
        else:
            print("Invalid command")

    def handle_create_command(self, command):
        parts = command.split()
        if len(parts) < 3:
            print("Invalid CREATE command")
            return

        table_name = parts[1]
        column_definition = " ".join(parts[2:])

        if (not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', table_name)) or (not column_definition.startswith("(")) or (
        not column_definition.endswith(");")):
            print("Invalid CREATE command format")
            return

        column_definition = column_definition[1:-2]
        column_definitions = [col.strip() for col in column_definition.split(",")]

        columns = []
        for definition in column_definitions:
            column_parts = definition.split()
            if len(column_parts) != 2 or not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', column_parts[0]):
                print("Invalid column definition format")
                return
            column_name, column_type = column_parts
            columns.append((column_name, column_type))

        self.create_table(table_name, columns)

    def handle_insert_command(self, command):
        parts = command.split()
        if len(parts) < 3:
            print("Invalid INSERT command")
            return
        if parts[1].upper() == "INTO":
            del parts[1]

        table_name = parts[1]
        values = " ".join(parts[2:])

        if "(" in values and ")" in values:
            values = values.replace(")", "")
            values = values.replace("(", "")
            values = values.replace(";", "")
            values = values.split(",")
            try:
                numeric_values = [int(value.strip()) for value in values]
            except ValueError:
                print("All values must be integers")
                return

            # Insert data into the table
            self.insert_into_table(table_name, numeric_values)

        elif parts[1].endswith("("):
            values = values[:-1]
            values = values.split(",")
            try:
                numeric_values = [int(value.strip()) for value in values]
            except ValueError:
                print("All values must be integers")
                return

            self.insert_into_table(table_name, numeric_values)
        else:
            print("Invalid INSERT command format")

    def handle_select_command(self, command):
        parts = command.split()

        from_index = next((i for i, part in enumerate(parts) if part.upper() == "FROM"), None)
        where_index = next((i for i, part in enumerate(parts) if part.upper() == "WHERE"), None)
        group_by_index = next((i for i, part in enumerate(parts) if part.upper() == "GROUP_BY"), None)

        select_columns = list(
            filter(None, [col.rstrip(',') for col in parts[1:from_index]])) if from_index is not None else []
        table_name = parts[from_index + 1] if from_index is not None else None
        where_condition = " ".join(
            filter(None, parts[where_index + 1:group_by_index])) if where_index is not None else None
        group_by_columns = list(filter(None, [col.rstrip(',;') for col in
                                              parts[group_by_index + 1:]])) if group_by_index is not None else None

        if where_condition and where_condition.endswith(";"):
            where_condition = where_condition[:-1]

        if table_name and table_name.endswith(";"):
            table_name = table_name[:-1]

        aggregate_functions = []
        non_aggregate_columns = []

        for col in select_columns:
            if ('MAX(' in col or 'AVG(' in col or 'COUNT(' in col) and ')' in col:
                aggregate_functions.append(col)
            else:
                non_aggregate_columns.append(col)

        if group_by_columns:
            for col in non_aggregate_columns:
                if col not in group_by_columns:
                    print("Error: Non-aggregate columns in SELECT must be in GROUP BY as well.")
                    return

        if aggregate_functions:
            if table_name not in self.tables:
                print(f"Error: Table {table_name} does not exist.")
                return

            table_columns = [col[0] for col in self.tables[table_name].columns]
            for func in aggregate_functions:
                col_name = func.split('(')[1].split(')')[0]
                if col_name not in table_columns:
                    print(f"Error: Column {col_name} used in aggregate function does not exist in the table.")
                    return

        if table_name in self.tables:
            result = self.select_from_table(table_name, select_columns, where_condition, group_by_columns)
            self.display_result(result)
        else:
            print(f"Table {table_name} does not exist")

    def display_result(self, result):
        if not result or not result[1:]:
            print("No results to display")
            return

        column_names = result[0]
        data = result[1:]

        column_widths = [max(len(str(column_names[i])), max(len(str(row[i])) for row in data)) for i in
                         range(len(column_names))]

        format_string = "+"
        for width in column_widths:
            format_string += "-" * (width) + "+"

        print(format_string)

        table_header = "|".join(f"{column_names[i]:^{column_widths[i]}}" for i in range(len(column_names)))

        print(f"|{table_header}|")

        print(format_string)

        for row in data:
            row_str = "|".join(f"{str(row[i]):^{column_widths[i]}}" for i in range(len(column_names)))
            print(f"|{row_str}|")

        print(format_string)

    def insert_into_table(self, table_name, values):
        if table_name in self.tables:
            table = self.tables[table_name]
            table.insert(values)
        else:
            print(f"Table {table_name} does not exist")

    def select_from_table(self, table_name, select_columns, where_condition, group_by_columns):
        if table_name in self.tables:
            table = self.tables[table_name]

            result = table.select(select_columns, where_condition, group_by_columns)
            return result
        else:
            print(f"Table {table_name} does not exist")
            return None

# Main
db = Database()
current_command = ""
while True:
    line = input("Enter an SQL-like command: ").strip()
    current_command += " " + line
    if ';' in line:
        db.execute_query(current_command)
        current_command = ""









