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
    """
    Tokenizes the given SQL-like text into a list of tokens.
    """
    tokens = []
    for match in token_re.finditer(text):
        for name, value in match.groupdict().items():
            if value is not None:
                if name != 'WHITESPACE':
                    tokens.append(Token(name, value))
                if value == ';':
                    return tokens
    return tokens


CreateTable = namedtuple('CreateTable', ['table_name', 'columns'])  # columns is a list of (column_name, is_indexed)
InsertInto = namedtuple('InsertInto', ['table_name', 'values'])  # values is a list of strings
Select = namedtuple('Select', ['agg_functions', 'table_name', 'where_condition', 'group_by_columns'])  # agg_functions is a list of (function, column)

def parse_create(tokens):
    """
    Parses a CREATE table command from the list of tokens.
    Assumes that the first token is 'CREATE'.
    """
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
    """
    Parses an INSERT INTO table command from the list of tokens.
    Assumes that the first token is 'INSERT'.
    """
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
    """
    Parses a SELECT command from the list of tokens.
    Assumes that the first token is 'SELECT'.
    """
    assert tokens[0].value.upper() == 'SELECT'
    
    i = 1  # Start parsing after 'SELECT'
    agg_functions = []
    
    # Parse aggregate functions if any
    while i < len(tokens) and tokens[i].value.upper() != 'FROM':
        token = tokens[i]
        if token.type == 'AGG_FUNCTION':
            agg_function = token.value.upper()
            
            i += 1  # Move to '('
            if tokens[i].value != '(':
                raise ValueError(f"Expected '(', got {tokens[i].value}")
            
            i += 1  # Move to column name
            if tokens[i].type != 'IDENTIFIER':
                raise ValueError(f"Expected IDENTIFIER, got {tokens[i].type}")
            agg_column = tokens[i].value  # e.g., name, age
            
            i += 1  # Move to ')'
            if tokens[i].value != ')':
                raise ValueError(f"Expected ')', got {tokens[i].value}")
            
            agg_functions.append((agg_function, agg_column))
            
            # Look ahead for comma
            if i + 1 < len(tokens) and tokens[i + 1].value == ',':
                i += 1  # Skip comma
        else:
            raise ValueError(f"Unexpected token {token.value}. Expected aggregate function or 'FROM'.")        
        i += 1

    # Parse table name after 'FROM'
    if i >= len(tokens) or tokens[i].value.upper() != 'FROM':
        raise ValueError(f"Expected 'FROM', got {tokens[i].value}" if i < len(tokens) else "Unexpected end of command, expected 'FROM'.")
    
    i += 1  # Move to table name
    if tokens[i].type != 'IDENTIFIER':
        raise ValueError(f"Expected IDENTIFIER, got {tokens[i].type}")
    table_name = tokens[i].value


    # If the next token is not WHERE, GROUP_BY, or the end of command (;), it's an error
    i += 1  
    if i < len(tokens) and tokens[i].value.upper() not in ('WHERE', 'GROUP_BY') and tokens[i].value != ';':
        raise ValueError(f"Unexpected text after table name: {tokens[i].value}")
    
    # Initialize optional parts
    where_condition = None
    group_by_columns = []
    
    # Look ahead for 'WHERE' or 'GROUP_BY'
    where, group_by = False, False
    WhereCondition = namedtuple('WhereCondition', ['left_column', 'operator', 'right_operand'])  # right_operand can be a column name or a value

    while i < len(tokens):  
        if tokens[i].value.upper() == 'WHERE' and not where:
            where = True
            # Parse WHERE condition
            i += 1  # Move to left column
            left_column = tokens[i].value
            
            i += 1  # Move to operator
            if tokens[i].value != '<':
                raise ValueError(f"Expected '<', got {tokens[i].value}")
            
            i += 1  # Move to right operand (either column name or value)
            right_operand = tokens[i].value
            
            where_condition = WhereCondition(left_column, '<', right_operand)       
            i += 1  # Move to next part or end

        elif tokens[i].value.upper() == 'GROUP_BY' and not group_by:
            group_by = True
            # Parse GROUP_BY columns
            i += 1  # Move to first column
            while i < len(tokens) and tokens[i].type == 'IDENTIFIER':
                group_by_columns.append(tokens[i].value)
                
                # Look ahead for comma
                if i + 1 < len(tokens) and tokens[i + 1].value == ',':
                    i += 1  # Skip comma
                i += 1
        else:
            i += 1  # Move to next part or end
    
    # Ensure there is a ';' at the end
    if tokens[-1].value != ';':
        raise ValueError("Expected ';' at the end of SELECT command")
    
    return Select(agg_functions, table_name, where_condition, group_by_columns)