from collections import namedtuple

CreateTable = namedtuple('CreateTable', ['table_name', 'columns'])
InsertInto = namedtuple('InsertInto', ['table_name', 'values'])
Select = namedtuple('Select', ['agg_functions', 'table_name', 'where_condition', 'group_by_columns'])

def parse_create(tokens):
    print(f"Tokens: {tokens}")

    assert tokens and tokens[0].lower() == 'create', "Invalid create command"

    table_name = None
    columns = []

    i = 1
    if tokens[i].isidentifier():
        table_name = tokens[i]
        i += 1

        if i < len(tokens) and tokens[i] == '(':
            i += 1

            while i < len(tokens) and tokens[i].isidentifier():
                column_name = tokens[i]
                is_indexed = False

                i += 1
                print(f"Current token: {tokens[i]}")
                if i < len(tokens) and tokens[i].lower() == 'indexed':
                    is_indexed = True
                    i += 1

                columns.append((column_name, is_indexed))

                if i < len(tokens) and tokens[i] == ',':
                    i += 1
                elif i < len(tokens) and tokens[i] == ')':
                    i += 1
                    break
                else:
                    raise ValueError(f"Expected ',' or ')', got {tokens[i]}")

    if i >= len(tokens) or tokens[i] != ';':
        raise ValueError("Expected ';' after ')' in create command")

    print(f"Table name: {table_name}, Columns: {columns}")
    return CreateTable(table_name, columns)

def parse_insert(tokens):
    assert tokens[0].lower() == 'insert', f"Invalid command: {tokens[0].lower()}"

    table_name = None
    values = []

    i = 1
    if i < len(tokens) and tokens[i].isidentifier():
        table_name = tokens[i]
        i += 1

        if i < len(tokens) and tokens[i] == '(':
            i += 1

            while i < len(tokens):
                if tokens[i].startswith('"') and tokens[i].endswith('"'):
                    values.append(tokens[i].strip('"'))

                    i += 1
                    if i < len(tokens) and tokens[i] == ',':
                        i += 1
                    elif i < len(tokens) and tokens[i] == ')':
                        i += 1
                        break
                    else:
                        raise ValueError(f"Expected ',' or ')', got {tokens[i]}")
                else:
                    raise ValueError(f"Expected STRING, got {tokens[i]}")

    if i >= len(tokens) or tokens[i] != ';':
        raise ValueError("Expected ';' after ')' in insert command")

    return InsertInto(table_name, values)


def parse_select(tokens):
    assert tokens[0].lower() == 'select', f"Invalid command: {tokens[0].lower()}"

    agg_functions = []
    table_name = None
    where_condition = None
    group_by_columns = []

    i = 1
    while i < len(tokens) and tokens[i].lower() not in ('from', 'where', 'group_by', ';'):
        raise ValueError(f"Unexpected token {tokens[i]}. Expected aggregate function or keyword.")

    if 'from' in tokens:
        from_index = tokens.index('from')
        if from_index + 1 < len(tokens) and tokens[from_index + 1].isidentifier():
            table_name = tokens[from_index + 1]
        else:
            raise ValueError(f"Expected identifier after 'from'.")

    if 'where' in tokens:
        where_index = tokens.index('where')
        if where_index + 3 < len(tokens) and tokens[where_index + 1].isidentifier() and tokens[where_index + 2] == '<':
            left_column = tokens[where_index + 1]
            right_operand = tokens[where_index + 3]

            where_condition = (left_column, '<', right_operand)
        else:
            raise ValueError("Incorrect 'where' condition format.")

    if 'group_by' in tokens:
        group_by_index = tokens.index('group_by')
        i = group_by_index + 1
        while i < len(tokens) and tokens[i] != ';':
            if tokens[i].isidentifier():
                group_by_columns.append(tokens[i])

                i += 1
                if i < len(tokens) and tokens[i] == ',':
                    i += 1
            else:
                raise ValueError(f"Unexpected token after 'group_by': {tokens[i]}")

    if ';' not in tokens:
        raise ValueError("Expected ';' at the end of select command")

    if agg_functions and not group_by_columns:
        raise ValueError("Aggregate functions require a group by clause")

    return Select(agg_functions, table_name, where_condition, group_by_columns)