# Importing string for checking ascii letters
import string
# import regex
import re
# import shlex for split a text
import shlex

# Defining token types
CREATE, INSERT, PRINT_INDEX, SEARCH, WHERE, EOF, VALUES = (
    'CREATE',
    'INSERT',
    'PRINT_INDEX',
    'SEARCH',
    'WHERE',
    'EOF',
    'VALUES'
)

# Regex patterns for identifying command types in the text
pattern_create = re.compile(r'create', re.I)
pattern_insert = re.compile(r'insert', re.I)
pattern_print_index = re.compile(r'print_index', re.I)
pattern_search = re.compile(r'search', re.I)
pattern_where = re.compile(r'where', re.I)

# Token class to represent the different elements of the input
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type = self.type,
            value = repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

# Lexer class to tokenize the input text
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position]

    # Method for handling errors
    def error(self):
        raise Exception("Invalid input")

    # Method for handling errors related to collection names
    def error_coll(self):
        raise Exception("Invalid name of collection")

    # Method to advance to the next character in the input
    def advance(self):
        self.position += 1
        if self.position > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.position]

    # Method to skip whitespace in the input
    def whitespace_SKIP(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Method to process the main SQL-like request
    def request(self):
        result = ''
        if self.current_char is not None:
            if self.current_char.isspace():
                self.whitespace_SKIP()
        while self.current_char is not None and (
                self.current_char in string.ascii_letters or self.current_char == "_"
                or self.current_char == '"' or self.current_char == ';'):
            if self.current_char == '"':
                self.advance()
                while self.position != len(self.text):
                    result += self.current_char
                    self.advance()
                    if self.current_char == '"':
                        self.advance()
                    if self.current_char == ';':
                        self.current_char = None
                        break
            else:
                if self.current_char == ';':
                    self.current_char = None
                    break
                result += self.current_char
                self.advance()

        # Identifying token types based on patterns
        if pattern_create.search(result):
            result = "CREATE"
            return str(result)
        elif pattern_insert.search(result):
            result = "INSERT"
            return str(result)
        elif pattern_search.search(result):
            result = "SEARCH"
            return str(result)
        elif pattern_where.search(result):
            result = "WHERE"
            return str(result)
        elif pattern_print_index.search(result):
            result = "PRINT_INDEX"
            return str(result)
        else:
            return result

    # Method to process collection names
    def coll_name(self):
        res = ""
        while self.current_char is not None and not self.current_char.isspace():
            if self.current_char == ';':
                self.current_char = None
                break
            res += self.current_char
            self.advance()

        # Validating the format of collection names
        if re.compile(r'^[a-zA-z][a-zA-Z0-9_]*$').match((res)):
            return str(res)
        else:
            self.error_coll()
        return str(res)

    # Method to process search values
    def search_value(self):
        result = ''
        while True:
            if self.current_char.isspace():
                self.advance()
            else:
                break
        while True:
            if self.current_char == "\"":
                self.advance()
            if self.current_char == ";":
                break
            if self.current_char is None:
                break
            result += self.current_char
            self.advance()

        return result

    # Method to process insert values
    def insert_value(self):
        result = ''
        if self.current_char.isspace():
            self.advance()
        if self.current_char == "\"":
            self.advance()
            while True:
                result += self.current_char
                self.advance()
                if self.current_char == "\"":
                    break
                if self.current_char == ";":
                    break
        return result

    # Method to get the next token from the input
    def get_next_token(self):
        type = self.request()
        while self.current_char is not None:
            if self.current_char.isspace():
                self.whitespace_SKIP()
                continue
            if type == "CREATE":
                return Token(CREATE, self.coll_name())
            if type == "INSERT":
                return Token(INSERT, self.coll_name())
            if type == "PRINT_INDEX":
                return Token(PRINT_INDEX, self.coll_name())
            if type == "SEARCH":
                return Token(SEARCH, self.coll_name())
            if type == "WHERE":
                return Token(WHERE, self.search_value())
            else:
                self.error()
        return Token(VALUES, type)

# Interpreter class to interpret the tokens and generate command dictionaries
class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    # Method to handle syntax errors
    def error(self):
        raise Exception('Invalid syntax')

    # Method to interpret the input and generate command dictionaries
    def expr(self):
        while self.current_token.type in (CREATE, INSERT, PRINT_INDEX, SEARCH, WHERE):
            token = self.current_token
            if token.type == CREATE:
                # Handling CREATE command
                dictionary = {}
                dictionary[token.type] = token.value
                return dictionary
            elif token.type == INSERT:
                # Handling INSERT command
                dictionary = {token.type: token.value, 'VALUE': []}
                insert = self.lexer.insert_value()
                final_values = shlex.split(insert)
                dictionary["VALUE"] = final_values
                return dictionary
            elif token.type == PRINT_INDEX:
                # Handling PRINT_INDEX command
                dict_print = {}
                dict_print[token.type] = token.value
                return dict_print
            elif token.type == SEARCH:
                # Handling SEARCH command
                dict_s = {}
                dict_s[token.type] = token.value
                self.current_token = self.lexer.get_next_token()
                if self.current_token.type == WHERE:
                    dict_sw = {}
                    dict_sw[token.type] = token.value
                    dict_sw[self.current_token.type] = self.current_token.value
                    return dict_sw
                return dict_s

# Main block for user input and execution
if __name__ == '__main__':
    while True:
        text = input("Enter SQL-like request: ")
        if not text:
            break
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        command_dict = interpreter.expr()
        print(command_dict)
        # Matching command types to print appropriate messages
        match list(command_dict.keys()):
            case ['CREATE']:
                print(f"Collection '{command_dict['CREATE']}' has been created")
            case ['INSERT', 'VALUE']:
                print(f"Document '{command_dict['VALUE']}' has been added to '{command_dict['INSERT']}'")
            case ['PRINT_INDEX']:
                print("There are indexes")
            case ['SEARCH']:
                print(f"Searching in '{command_dict['SEARCH']}'")
            case ['SEARCH', 'WHERE']:
                print(f"Searching in '{command_dict['SEARCH']}' for '{command_dict['WHERE']}'")
