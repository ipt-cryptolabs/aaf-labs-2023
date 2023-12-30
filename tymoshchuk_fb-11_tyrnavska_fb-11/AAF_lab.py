import re

class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class Index:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        self.root = self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node, key, value):
        if node is None:
            return TreeNode(key, value)

        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)

        return node

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None:
            return None 

        if node.key == key:
            return node.value

        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def range_search(self, low, high):
        result = []
        self._range_search_recursive(self.root, low, high, result)
        return result

    def _range_search_recursive(self, node, low, high, result):
        if node is None:
            return

        if low < node.key:
            self._range_search_recursive(node.left, low, high, result)

        if low <= node.key <= high:
            result.append(node.value)

        if high > node.key:
            self._range_search_recursive(node.right, low, high, result)

class Table:
    def __init__(self, name, columns):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
            print("Invalid table name")
            return

        self.name = name
        self.columns = columns
        self.data = []
        self.indexed_columns = {}  # Dictionary of indexes

        # Check column names for validity
        for col_name, _ in self.columns:
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', col_name):
                print(f"Invalid column name: {col_name}")
                return

    def create_index(self, column_name):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', column_name):
            print("Invalid column name")
            return

        # Check if the column with the given name exists in self.columns
        if any(col[0] == column_name for col in self.columns):
            if column_name not in self.indexed_columns:
                self.indexed_columns[column_name] = Index()
                print(f"Index created for column {column_name}")
            else:
                print(f"Index already exists for column {column_name}")
        else:
            print("Column does not exist in the table")

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

        # Update indexes for indexed columns
        for col_name, indexed in self.indexed_columns.items():
            if indexed:
                col_index = self.columns.index((col_name, True))
                col_value = values[col_index]
                self.indexed_columns[col_name].insert(col_value, len(self.data) - 1)

    def select(self, select_columns, where_condition=None, group_by=None):
        full_columns = self.columns
        selected_manually = True
        filtered_data = []

        # Check for the presence of an index and use it for searching
        if where_condition:
            col_name, operator, value = where_condition.split()
            col_name = col_name.strip()
            col_index = None

            if col_name in self.indexed_columns and self.indexed_columns[col_name]:
                col_index = next((i for i, (name, _) in enumerate(self.columns) if name == col_name), None)

                if operator == "=":
                    # Use the index for exact search
                    rows_to_select = self.indexed_columns[col_name].search(int(value))
                    if rows_to_select and any(i < len(self.data) for i in [rows_to_select]):
                        filtered_data = [self.data[i] for i in [rows_to_select]]
                    else:
                        filtered_data = []
                elif operator == "<" or operator == ">":
                    # Use the index for range search
                    if operator == "<":
                        rows_to_select = self.indexed_columns[col_name].range_search(None, int(value))
                    else:
                        rows_to_select = self.indexed_columns[col_name].range_search(int(value), None)
                    filtered_data = [self.data[i] for i in rows_to_select]

        if not filtered_data:
            # If unable to use indexes, filter the data manually
            for row in self.data:
                if where_condition is None or self.evaluate_condition(where_condition, row):
                    filtered_data.append(row)

        if group_by:
            grouped_data = {}
            group_indices = [i for i, (col, _) in enumerate(full_columns) if col in group_by]

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
                        col_index = None
                        for i, (col, _) in enumerate(full_columns):
                            if col == col_name:
                                col_index = i
                                break
                        if col_index is not None:
                            if func_name == 'COUNT':
                                agg_value = len(group_rows)
                            elif func_name == 'MAX':
                                agg_value = max(row[col_index] for row in group_rows)
                            elif func_name == 'AVG':
                                agg_value = sum(row[col_index] for row in group_rows) / len(group_rows)
                            agg_values.append(agg_value)
                    else:
                        col_index = None
                        for i, (col, _) in enumerate(full_columns):
                            if col == agg_func:
                                col_index = i
                                break
                        if col_index is not None:
                            agg_values.append(group_key[group_indices.index(col_index)])
                result_data.append(tuple(agg_values))
        else:
            result_data = filtered_data

        if not select_columns:
            select_columns = full_columns
            selected_manually = False

        if not select_columns:
            return []

        if not selected_manually:
            select_columns = [col[0] for col in select_columns]

        formatted_result = [select_columns]
        formatted_result.extend(result_data)
        return formatted_result

    def evaluate_condition(self, condition, row):
        col_name, operator, value = condition.split()
        col_name = col_name.strip()
        col_index = None

        for i, (column_name, _) in enumerate(self.columns):
            if col_name == column_name:
                col_index = i
                break
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

        # Check if there are INDEXED flags for columns and create corresponding indexes
        for column_name, indexed in columns:
            if indexed:
                self.create_index(name, column_name)

    def execute_query(self, command):
        # Remove leading and trailing whitespace and ignore characters after ';'
        command = command.strip().split(';')[0] + ';'

        # Split the command into parts, removing empty strings from the split result
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

        if (not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', table_name)) or (not column_definition.startswith("(")) or (not column_definition.endswith(");")):
            print("Invalid CREATE command format")
            return

        column_definition = column_definition[1:-2]
        column_names = [col.strip() for col in column_definition.split(",")]
        columns = []

        for column_name in column_names:
            indexed = False
            if column_name.upper().endswith(" INDEXED"):
                column_name = column_name[:-8].strip()
                indexed = True
            columns.append((column_name, indexed))

        # Now create the table with the specified columns
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

            # Insert data into the table
            self.insert_into_table(table_name, numeric_values)
        else:
            print("Invalid INSERT command format")

    def handle_select_command(self, command):
        parts = command.split()

        # Find the indexes of all keywords
        from_index = next((i for i, part in enumerate(parts) if part.upper() == "FROM"), None)
        where_index = next((i for i, part in enumerate(parts) if part.upper() == "WHERE"), None)
        group_by_index = next((i for i, part in enumerate(parts) if part.upper() == "GROUP_BY"), None)

        # Determine the ends of different parts of the command
        select_columns = list(filter(None, [col.rstrip(',') for col in parts[1:from_index]])) if from_index is not None else []
        table_name = parts[from_index + 1] if from_index is not None else None
        where_condition = " ".join(filter(None, parts[where_index + 1:group_by_index])) if where_index is not None else None
        group_by_columns = list(filter(None, [col.rstrip(',;') for col in parts[group_by_index + 1:]])) if group_by_index is not None else None
        # Remove semicolon from where_condition if present
        if where_condition and where_condition.endswith(";"):
            where_condition = where_condition[:-1]

        if table_name and table_name.endswith(";"):
            table_name = table_name[:-1]
        # Identify and extract aggregate functions from SELECT
        aggregate_functions = []
        non_aggregate_columns = []

        for col in select_columns:
            if ('MAX(' in col or 'AVG(' in col or 'COUNT(' in col) and ')' in col:
                aggregate_functions.append(col)
            else:
                non_aggregate_columns.append(col)

        # Check if non-aggregate columns are in SELECT and not in GROUP BY
        if group_by_columns:
            for col in non_aggregate_columns:
                if col not in group_by_columns:
                    print("Error: Non-aggregate columns in SELECT must be in GROUP BY as well.")
                    return
        # Check if all columns used in aggregate functions exist in the table
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

        # Call the method to process the SELECT query
        if table_name in self.tables:
            result = self.select_from_table(table_name, select_columns, where_condition, group_by_columns)
            self.display_result(result)
        else:
            print(f"Table {table_name} does not exist")

        #Display the result of the query

    def display_result(self, result):
        if not result or not result[1:]:
            print("No results to display")
            return

        column_names = result[0]
        data = result[1:]

        # Calculate column widths based on the length of the column names and data
        column_widths = [max(len(str(column_names[i])), max(len(str(row[i])) for row in data)) for i in range(len(column_names))]

        # Create a format string for formatting the table
        format_string = "+"
        for width in column_widths:
            format_string += "-" * (width) + "+"

        # Display the frame line
        print(format_string)

        # Display the table header
        table_header = "|".join(f"{column_names[i]:^{column_widths[i]}}" for i in range(len(column_names)))

        print(f"|{table_header}|")

        # Display the frame line
        print(format_string)

        # Display the data rows
        for row in data:
            row_str = "|".join(f"{str(row[i]):^{column_widths[i]}}" for i in range(len(column_names)))
            print(f"|{row_str}|")

        # Display the frame line
        print(format_string)

    def create_index(self, table_name, column_name):
        if table_name in self.tables:
            table = self.tables[table_name]
            table.create_index(column_name)
        else:
            print(f"Table {table_name} does not exist")

    def insert_into_table(self, table_name, values):
        if table_name in self.tables:
            table = self.tables[table_name]
            table.insert(values)
        else:
            print(f"Table {table_name} does not exist")

    def select_from_table(self, table_name, select_columns, where_condition, group_by_columns):
        if table_name in self.tables:
            table = self.tables[table_name]
            # Call the select method of the table to get the result
            result = table.select(select_columns, where_condition, group_by_columns)
            return result
        else:
            print(f"Table {table_name} does not exist")
            return None

# Main program loop
db = Database()
current_command = ""
while True:
    line = input("Enter an SQL-like command: ").strip()
    current_command += " " + line

    # If the line ends with a ';', execute the command and reset current_command
    if ';' in line:
        db.execute_query(current_command)
        current_command = ""
