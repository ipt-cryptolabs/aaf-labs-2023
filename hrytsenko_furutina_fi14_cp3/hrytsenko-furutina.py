import re


class Table:
    def __init__(self, columns):
        self.columns = columns
        self.data = []

    def insert(self, row):
        if len(row) != len(self.columns):
            raise ValueError("Row must have the same number of elements as columns")

        if all(isinstance(value, int) for value in row):
            self.data.append(row)
        else:
            raise ValueError("All elements in the row must be integers")

    def get_column_count(self):
        return len(self.columns)

    def get_row_count(self):
        return len(self.data)


class Database:
    def __init__(self):
        self.tables = {}

    def create(self, table_name, columns):
        if table_name in self.tables:
            raise ValueError(f"Table {table_name} already exists")
        self.tables[table_name] = Table(columns)

    def insert(self, table_name, row):
        if table_name not in self.tables:
            raise ValueError(f"Table {table_name} does not exist")
        # Convert string values to integers before inserting
        row = [int(value) for value in row]
        self.tables[table_name].insert(row)

    def select(self, table_name):
        if table_name not in self.tables:
            raise ValueError(f"Table {table_name} does not exist")

        table = self.tables[table_name]
        print(f"Table: {table_name}")
        print("Columns:", ", ".join(table.columns))
        print("Data:")
        for row in table.data:
            print(row)

    def execute_sql_command(self, command):
        # Remove leading and trailing whitespace and newlines
        command = command.strip()
        # Normalize whitespace to single spaces
        command = re.sub(r'\s+', ' ', command)
        # Ensure the command ends with a semicolon
        if not command.endswith(';'):
            print("Command must end with a semicolon (;)")
            return
        command = command[:-1]  # Remove the trailing semicolon

        # Split the command into the operation and the rest of the command
        operation, rest = command.split(' ', 1)
        allowed_operators = {'CREATE', 'INSERT', 'SELECT'}
        if operation not in allowed_operators:
            print(f"Invalid operation: {operation}. Allowed operations are {', '.join(allowed_operators)}")
            return

        if operation == 'CREATE':
            # Regular expression for validating table and column names
            table_pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
            match = re.match(r'(\w+)\s*\((.*)\)', rest)
            if match:
                table_name = match.group(1)
                column_names = [col.strip() for col in match.group(2).split(',')]
                # Validate table name and column names using the regular expression
                if re.match(table_pattern, table_name) and all(re.match(table_pattern, col) for col in column_names):
                    self.create(table_name, column_names)
                    print(f"Table {table_name} created with columns: {', '.join(column_names)}")
                else:
                    print(
                        "Invalid table name or column names.")
            else:
                print("Invalid CREATE command format. Please use: CREATE table_name (column1, column2, ...);")
        elif operation == 'INSERT':
            match = re.match(r'(?:INTO)?\s*(\w+)\s*\((.*)\)', rest)
            if match:
                table_name = match.group(1)
                values = [value.strip() for value in match.group(2).split(',')]
                if table_name in self.tables:
                    try:
                        self.insert(table_name, values)
                        print(f"Inserted {values} into table {table_name}")
                    except ValueError as e:
                        print(str(e))
                else:
                    print(f"Table {table_name} does not exist")
            else:
                print("Invalid INSERT command format. Please use: INSERT [INTO] table_name (value1, value2, ...);")
        elif operation == 'SELECT':
            match = re.match(r'(\w+)', rest)
            if match:
                table_name = match.group(1)
                try:
                    self.select(table_name)
                except ValueError as e:
                    print(str(e))
            else:
                print("Invalid SELECT command format. Please use: SELECT table_name;")
        else:
            print("Unknown command. Available commands: CREATE, INSERT")

    def run_console(self):
        while True:
            command = input("Enter a command (or 'exit' to quit): ")
            if command.lower() == 'exit':
                break
            self.execute_sql_command(command)


if __name__ == "__main__":
    db = Database()
    db.run_console()

