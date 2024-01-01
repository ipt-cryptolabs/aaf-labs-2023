import re


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            return {'key': key, 'value': value, 'left': None, 'right': None}

        if key < node['key']:
            node['left'] = self._insert(node['left'], key, value)
        elif key > node['key']:
            node['right'] = self._insert(node['right'], key, value)
        else:
            pass

        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node['key'] == key:
            return node
        if key < node['key']:
            return self._search(node['left'], key)
        return self._search(node['right'], key)


def parse_create_command(command, create_data, table_data):
    command = command.lower()

    if not command.endswith(";"):
        return "Enter the command correct"

    create_keyword = "create"
    create_index = command.find(create_keyword)

    if create_index != -1:
        open_bracket_index = command.find("(", create_index)
        close_bracket_index = command.find(")", create_index)

        if open_bracket_index != -1 and close_bracket_index != -1:
            table_name = command[create_index + len(create_keyword):open_bracket_index].strip()

            columns_info = [col.strip() for col in command[open_bracket_index + 1:close_bracket_index].split(",")]

            columns = []
            indexed_columns = set()
            for col_info in columns_info:
                col_parts = col_info.split()
                col_name = col_parts[0]
                columns.append(col_name)
                if "indexed" in col_parts:
                    indexed_columns.add(col_name)

            create_data[table_name] = columns

            table_data[table_name] = []

            for col_name in indexed_columns:
                table_data[f"{table_name}_{col_name}_index"] = BinarySearchTree()

            return f"Table '{table_name}' created with columns: {', '.join(columns)}"
        else:
            return "Error: Missing opening or closing parenthesis"
    else:
        return "Error: CREATE keyword not found"


def parse_insert_command(command, create_data, table_data):
    command = command.lower()

    if not command.endswith(";"):
        return "Enter the command correct"

    insert_keyword = "insert"
    insert_index = command.find(insert_keyword)

    if insert_index != -1:
        open_bracket_index = command.find("(", insert_index)
        close_bracket_index = command.find(")", insert_index)

        if open_bracket_index != -1 and close_bracket_index != -1:
            table_name = command[insert_index + len(insert_keyword):open_bracket_index].strip().split()[-1]
            values_str = command[open_bracket_index + 1:close_bracket_index]
            values_str = re.sub(r'(?<=\S)\s+(?=\S)', '', values_str)
            values = re.findall(r'\'([^\']*)\'|\"([^\"]*)\"', values_str)
            values = [val[0] if val[0] else val[1] for val in values]

            create_columns = create_data.get(table_name, [])
            if len(values) == len(create_columns):
                table_data[table_name].append({col: val for col, val in zip(create_columns, values)})
                return f"Inserted records into table {table_name}: ({'; '.join([f'{val}' for val in values])})."
            else:
                return "Error: Number of values does not match the number of columns in the table."
        else:
            return "Error: Missing opening or closing parenthesis"
    else:
        return "Error: INSERT keyword not found"


def parse_select_command(command, table_data):
    command = command.lower()

    if not command.endswith(";"):
        return "Enter the command correct"

    command = command[:-1]

    select_keyword = "select"
    select_index = command.find(select_keyword)

    if select_index != -1:
        from_index = command.find("from", select_index)

        if from_index != -1:
            table_name_start = from_index + len("from")
            where_index = command.find("where", from_index)
            order_by_index = command.find("order_by", from_index)

            if where_index != -1 and order_by_index != -1:
                table_name = command[table_name_start:where_index].strip()
                condition_str = command[where_index + len("where"):order_by_index].strip()
            elif where_index != -1:
                table_name = command[table_name_start:where_index].strip()
                condition_str = command[where_index + len("where"):].strip()
            elif order_by_index != -1:
                table_name = command[table_name_start:order_by_index].strip()
                condition_str = None
            else:
                table_name = command[table_name_start:].strip()
                condition_str = None

            condition = None
            if condition_str:
                condition_match = re.match(r'\s*([a-zA-Z_]\w*)\s*([><=]=?|<>|like)\s*(([a-zA-Z_]\w*)|(\"[^\"]+\")|(\'[^\']+\'))\s*', condition_str)
                if condition_match:
                    column_name_1 = condition_match.group(1)
                    operator = condition_match.group(2)
                    column_name_2_or_value = condition_match.group(3)
                    condition = (column_name_1, operator, column_name_2_or_value)
                else:
                    return "Error: Invalid WHERE condition"

            order_by_columns = []
            if order_by_index != -1:
                order_by_str = command[order_by_index + len("order_by"):].strip()
                order_by_parts = order_by_str.split(',')
                for part in order_by_parts:
                    order_by_parts = part.split()
                    if len(order_by_parts) == 1:
                        order_by_column = order_by_parts[0]
                        order_by_direction = "asc"
                        order_by_columns.append((order_by_column, order_by_direction))
                    elif len(order_by_parts) == 2:
                        order_by_column = order_by_parts[0]
                        order_by_direction = order_by_parts[1]
                        order_by_columns.append((order_by_column, order_by_direction))

            if table_name in table_data:
                table_rows = table_data[table_name]

                if table_rows:
                    indexed_columns_used = set()
                    if condition:
                        for col_name in [condition[0], condition[2]]:
                            if f"{table_name}_{col_name}_index" in table_data:
                                indexed_columns_used.add(col_name)

                    if indexed_columns_used:
                        for col_name in indexed_columns_used:
                            print(f"Using index for column {col_name}")

                    if condition:
                        comparison_func = get_comparison_function(condition[1])
                        table_rows = [row for row in table_rows if comparison_func(row[condition[0]], get_value(condition[2], row))]

                    if order_by_columns:
                        for column, direction in reversed(order_by_columns):
                            table_rows = sorted(table_rows, key=lambda x: x[column], reverse=(direction == "desc"))

                    return display_table(table_name, table_rows)
                else:
                    return f"Table {table_name} is empty."
            else:
                return f"Error: Table {table_name} not found in the database."
        else:
            return "Error: FROM keyword not found in the SELECT command."
    else:
        return "Error: SELECT keyword not found in the command."


def get_value(value_str, row):
    if value_str[0] in ["'", '"']:
        return value_str[1:-1]
    else:
        return row[value_str]


def get_comparison_function(operator):
    if operator == '>':
        return lambda x, y: x > y
    elif operator == '<':
        return lambda x, y: x < y
    elif operator == '>=':
        return lambda x, y: x >= y
    elif operator == '<=':
        return lambda x, y: x <= y
    elif operator == '=' or operator == '==':
        return lambda x, y: x == y
    elif operator == '<>':
        return lambda x, y: x != y

    return lambda x, y: x == y


def display_table(table_name, table_rows):
    if not table_rows:
        return f"Table {table_name} is empty."

    columns = list(table_rows[0].keys())
    header_row = "+--+" + "+".join(["--" * (len(col)) for col in columns]) + "+"
    column_names_row = "|" + "|".join([f" {col} " for col in columns]) + "|"
    data_rows = [f"|" + "|".join([f" {row[col]} " for col in columns]) + "|" for row in table_rows]

    res = "\n".join([header_row, column_names_row, header_row] + data_rows + [header_row])

    return res


create_info = {}
table_info = {}

while True:
    user_input = input("Enter the SQL-command (or 'exit' for quit): ")
    user_input = user_input.lower()

    if user_input.lower() == 'exit':
        break

    if "create" in user_input:
        result = parse_create_command(user_input, create_info, table_info)
    elif "insert" in user_input:
        result = parse_insert_command(user_input, create_info, table_info)
    elif "select" in user_input:
        result = parse_select_command(user_input, table_info)
    else:
        result = "Error: Unsupported SQL command"

    print(result)
