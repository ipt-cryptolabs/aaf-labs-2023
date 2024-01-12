import re
from tabulate import tabulate

CREATE, INSERT, SELECT, WHERE = (
    'CREATE',
    'INSERT',
    'SELECT',
    'WHERE'
)

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self):
        self.tables = {}
        self.data = {}

    def create_table(self, table_name, columns):
        self.tables[table_name] = columns
        self.data[table_name] = []

        print(f'Table "{table_name}" has been created')

    def insert_data(self, table_name, values):
        if table_name not in self.tables:
            print(f'Table "{table_name}" does not exist')
            return

        expected_columns = self.tables[table_name]
        if len(expected_columns) != len(values):
            print('Incorrect data: Number of values does not match the number of columns')
            return

        row_data = dict(zip(expected_columns, values))
        self.data[table_name].append(row_data)

        print(f'Processing...')
        print(f'Data: {{{", ".join(f"{key}: {value}" for key, value in row_data.items())}}}')

    def select_data(self, table_name, condition=None):
        if table_name not in self.tables:
            print(f'Table "{table_name}" does not exist')
            return

        columns = self.tables[table_name]

        selected_data = self.data[table_name]

        if not selected_data:
            print(f'Table "{table_name}" is empty')
            return

        if condition:
            column, operator, value = self.parse_condition(condition)
            selected_data = [row for row in selected_data if self.check_condition(row, column, operator, value)]

        print(tabulate(selected_data, headers="keys", tablefmt="grid", showindex=False))

    def parse_condition(self, condition):
        match = re.match(r'(.*?)\s*([=<>])\s*(.*)', condition)
        if match:
            column, operator, value = match.groups()
            return column, operator, value
        else:
            print('Incorrect condition syntax')
            return None

    def check_condition(self, row, column, operator, value):
        if column not in row:
            print(f'Column "{column}" does not exist in the table')
            return False

        if operator == '=':
            return row[column] == value
        else:
            print(f'Unsupported operator "{operator}"')
            return False

    def interpret(self, command):
        tokens = command.split()
        if tokens[0] == CREATE:
            match = re.match(r'CREATE (\w+) \((.*?)\)', command)
            if match:
                table_name = match.group(1)
                columns = [col.strip() for col in match.group(2).split(',')]
                self.create_table(table_name, columns)
            else:
                print('Incorrect CREATE command syntax')
        elif tokens[0] == INSERT:
            table_name = tokens[1]
            values_str = re.findall(r'\((.*?)\)', command)
            if values_str:
                values = [value.strip('"') for value in values_str[0].split(',')]
                self.insert_data(table_name, values)
            else:
                print('Incorrect data: No values provided for insertion')
        elif tokens[0].lower() == SELECT.lower():
            table_name = tokens[1].rstrip(';')
            condition = None

            if WHERE.lower() in [token.lower() for token in tokens]:
                where_index = [token.lower() for token in tokens].index(WHERE.lower())
                condition = ' '.join(tokens[where_index + 1:])

            self.select_data(table_name, condition)


if __name__ == '__main__':
    interpreter = Interpreter()
    while True:
        try:
            command = input('Enter SQL request: ')
        except EOFError:
            break
        if not command:
            continue
        interpreter.interpret(command)

