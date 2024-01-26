import re
from collections import namedtuple

# Define a token as a named tuple
Token = namedtuple('Token', ['type', 'value'])

# Define regex patterns for different types of tokens
token_patterns = {
    'KEYWORD': r'(CREATE|INSERT|INTO|SELECT|FROM|WHERE|GROUP_BY|INDEXED)',
    'AGG_FUNCTION': r'(COUNT|MAX|LONGEST)',
    'IDENTIFIER': r'([a-zA-Z][a-zA-Z0-9_]*)',
    'STRING': r'(".*?")',
    'SYMBOL': r'([(),;])',
    'COMPARISON_OPERATOR': r'(<)',
    'WHITESPACE': r'(\s+)',
    'UNKNOWN': r'(.+?)'
}

# Combine all patterns into one regex pattern
combined_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns.items())

# Compile the combined regex pattern
token_re = re.compile(combined_pattern, re.IGNORECASE)


def tokenize(text):
    tokens = []
    for match in token_re.finditer(text):
        for name, value in match.groupdict().items():
            if value is not None:
                if name != 'WHITESPACE':
                    tokens.append(Token(name, value))
                if value == ';':
                    return tokens
    return tokens


CreateTable = namedtuple('CreateTable', ['table_name', 'columns']) 
InsertInto = namedtuple('InsertInto', ['table_name', 'values'])  
Select = namedtuple('Select', ['agg_functions', 'table_name', 'where_condition', 'group_by_columns'])  

def parse_create(tokens):
    assert tokens[0].value.upper() == 'CREATE'
    
    # Get table name
    table_name_token = tokens[1]
    if table_name_token.type != 'IDENTIFIER':
        raise ValueError(f"Expected IDENTIFIER, got {table_name_token.type}")
    table_name = table_name_token.value
    
    # Check for opening parenthesis
    if tokens[2].value != '(':
        raise ValueError(f"Expected '(', got {tokens[2].value}")
    
    # Parse columns
    columns = []
    i = 3
    while i < len(tokens):
        token = tokens[i]
        if token.type == 'IDENTIFIER':
            column_name = token.value
            is_indexed = False
            # Check for optional INDEXED keyword
            if i + 1 < len(tokens) and tokens[i + 1].value.upper() == 'INDEXED':
                is_indexed = True
                i += 1  # Skip INDEXED token
            columns.append((column_name, is_indexed))
            
            # Look ahead for comma or closing parenthesis
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token.value == ',':
                    i += 1  # Skip comma
                elif next_token.value == ')':
                    i += 1  # Move to ')'
                    break
                else:
                    raise ValueError(f"Expected ',' or ')', got {next_token.value}")
        i += 1
        
    if i >= len(tokens) or tokens[i].value != ')':
        raise ValueError("Expected ')' at the end of CREATE command")
    
    # Ensure there is a ';' after ')'
    if i + 1 >= len(tokens) or tokens[i + 1].value != ';':
        raise ValueError("Expected ';' after ')' in CREATE command")
    
    return CreateTable(table_name, columns)

def parse_insert(tokens):
    assert tokens[0].value.upper() == 'INSERT'
    
    # Check for optional 'INTO' keyword
    i = 1
    if i < len(tokens) and tokens[i].value.upper() == 'INTO':
        i += 1
    
    # Get table name
    table_name_token = tokens[i]
    if table_name_token.type != 'IDENTIFIER':
        raise ValueError(f"Expected IDENTIFIER, got {table_name_token.type}")
    table_name = table_name_token.value
    
    # Check for opening parenthesis
    i += 1
    if tokens[i].value != '(':
        raise ValueError(f"Expected '(', got {tokens[i].value}")
    
    # Parse values
    i += 1
    values = []
    while i < len(tokens):
        token = tokens[i]
        if token.type == 'STRING':
            values.append(token.value.strip('"'))
            
            # Look ahead for comma or closing parenthesis
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token.value == ',':
                    i += 1  # Skip comma
                elif next_token.value == ')':
                    i += 1  # Move to ')'
                    break
                else:
                    raise ValueError(f"Expected ',' or ')', got {next_token.value}")
        i += 1
        
    if i >= len(tokens) or tokens[i].value != ')':
        raise ValueError("Expected ')' at the end of INSERT command")
    
    # Ensure there is a ';' after ')'
    if i + 1 >= len(tokens) or tokens[i + 1].value != ';':
        raise ValueError("Expected ';' after ')' in INSERT command")
    
    return InsertInto(table_name, values)

def parse_select(tokens):
    assert tokens[0].value.upper() == 'SELECT'
    
    i = 1  # Start parsing after 'SELECT'

    # Ensure 'FROM' is present
    if tokens[i].value.upper() != 'FROM':
        raise ValueError(f"Expected 'FROM', got {tokens[i].value}")
    
    # Parse table name
    i += 1
    if tokens[i].type != 'IDENTIFIER':
        raise ValueError(f"Expected IDENTIFIER, got {tokens[i].type}")
    table_name = tokens[i].value

    i += 1  # Move to the next token

    where_condition = None
    order_by_clause = []

    # Check for WHERE or ORDER_BY
    while i < len(tokens):
        if tokens[i].value.upper() == 'WHERE':
            # Parse WHERE condition
            i += 1  # Move to column name
            column_name = tokens[i].value

            i += 1  # Move to operator
            if tokens[i].value != '>':
                raise ValueError(f"Expected '>', got {tokens[i].value}")

            i += 1  # Move to value
            value = tokens[i].value
            where_condition = (column_name, '>', value)
            i += 1  # Move to next token or end

        elif tokens[i].value.upper() == 'ORDER_BY':
            # Parse ORDER_BY clause
            i += 1  # Move to first column name
            while i < len(tokens) and tokens[i].type == 'IDENTIFIER':
                column_name = tokens[i].value
                i += 1  # Move to ASC|DESC

                if tokens[i].value.upper() not in ('ASC', 'DESC'):
                    raise ValueError(f"Expected 'ASC' or 'DESC', got {tokens[i].value}")

                order_direction = tokens[i].value.upper()
                order_by_clause.append((column_name, order_direction))

                i += 1  # Move to comma or next part
                if i < len(tokens) and tokens[i].value == ',':
                    i += 1  # Skip comma
        else:
            break  # Exit loop if neither WHERE nor ORDER_BY is found

    # Ensure there is a ';' at the end
    if tokens[-1].value != ';':
        raise ValueError("Expected ';' at the end of SELECT command")
    
    return Select(table_name=table_name, where_condition=where_condition, order_by_clause=order_by_clause)

# The Select namedtuple needs to be updated to match the new structure
Select = namedtuple('Select', ['table_name', 'where_condition', 'order_by_clause'])  

