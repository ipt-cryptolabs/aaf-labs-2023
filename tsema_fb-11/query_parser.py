EOF = 'EOF'


CMD_LIST = ['CREATE', 'INSERT', 'PRINT_TREE', 'SEARCH', 'CONTAINS']
KEY_PHR = ['CONTAINS', 'WHERE', 'CONTAINED_BY', 'INTERSECTS']

SPACE_CHARS = ['\n', '\r', '\t', ' ']


import re
from cmds import *


class TOKEN:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return 'TOKEN({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self) -> str:
        return self.__str__()
    
    
class Parser:
    def __init__(self) -> None:
        self.query = None
        self.pos = 0
        self.current_token = None
        self.current_char =  None


    def get_query(self, query: str) -> None:
        self.query = query
        self.pos = 0
        self.current_token = None
        self.current_char = self.query[self.pos]
        
        if not self.is_balanced():
            raise Exception("There is no matching opening parenthesis in query")


    def is_balanced(self) -> None:
        stack = []
        
        for char in self.query:

            if char in '{':
                stack.append(char)
            elif char in '}':
                if not stack:
                    return False
                
                top = stack.pop()
                if char == '}' and top != '{':
                    return False
        
        if stack:
            return False     
        return True


    def advance(self) -> None:
        self.pos += 1
        if self.pos > len(self.query) - 1:
            self.current_char = None
        else:
            self.current_char = self.query[self.pos]


    def return_int(self) -> int:
        result_int = ""

        while self.current_char.isnumeric() or self.current_char == '-':
            result_int += self.current_char
            self.advance()

        return int(result_int)
    
    
    def get_command_token(self) -> TOKEN:
        result_cmd = ""

        while self.current_char.isalpha() or self.current_char == "_":
            result_cmd += self.current_char
            self.advance()

        if result_cmd.upper() not in CMD_LIST:
            raise Exception("An unknown command in the query")

        return TOKEN("CMD", result_cmd.upper())
    

    def get_key_phrase_token(self) -> TOKEN:
        result_key = ""

        while self.current_char.isalpha() or self.current_char == '_':
            result_key += self.current_char
            self.advance()

        if result_key.upper() not in KEY_PHR:
            raise Exception("An unknown key phrase in the query")
        
        return TOKEN("KEYPHR", result_key.upper())
    

    def get_id_token(self) -> TOKEN:
        result_ind = ""

        while self.current_char not in SPACE_CHARS and self.current_char != ";":
            result_ind += self.current_char
            self.advance()

        if not re.match("[a-zA-Z][a-zA-Z0-9_]*", result_ind):
            raise Exception("Incorrect identifier format")
        
        if result_ind.upper() in CMD_LIST:
            raise Exception(f"This identifier name is not available ({result_ind})")

        return TOKEN("IDENT", result_ind)


    def get_set_token(self) -> TOKEN:
        result_set = set()

        while self.current_char != "}":
            if self.current_char.isdigit() or self.current_char == '-':
                int_t = self.return_int()
                result_set.add(int_t)

            else:
                self.advance()

        self.advance()
        return TOKEN("SET", result_set)
    

    def get_condition_q(self) -> TOKEN:
        condition_q_tokens = []

        while self.current_char != ";":
            if self.current_char in SPACE_CHARS:
                self.advance()

            if self.current_char == "{":
                condition_q_tokens.append(self.get_set_token())
            else:
                condition_q_tokens.append(self.get_key_phrase_token())

        return TOKEN("CONDITION", condition_q_tokens)
    
    
    def get_next_token(self) -> TOKEN:
        while self.current_char != ";":

            if self.current_char in SPACE_CHARS:
                self.advance()

                if self.current_char == ";":
                    return TOKEN(EOF, None)

            if self.current_char == "{":
                return self.get_set_token()
            
            if self.current_token == None:
                return self.get_command_token()
            
            elif self.current_token.type == "IDENT":
                return self.get_key_phrase_token()
            
            elif self.current_token.type == "KEYPHR":
                return self.get_condition_q()
            
            else:
                if self.current_char in SPACE_CHARS:
                    self.advance()
                    continue

                return self.get_id_token()

        return TOKEN(EOF, None)
    

    def exec(self) -> None:
        CMD_DICT = {
            'CREATE': create,
            'INSERT': insert,
            'SEARCH': search,
            'PRINT_TREE': print_tree,
            'CONTAINS': contains
        }

        RIGHT_TOKEN_ORDER = "CMD", "IDENT", "KEYPHR", "CONDITION"

        self.current_token = self.get_next_token()
        if self.current_token.type != "CMD":
            raise Exception("Invalid syntax")

        cmd = self.current_token.value
        stack = []

        current_token_pos = 0
        while current_token_pos < len(RIGHT_TOKEN_ORDER):

            self.current_token = self.get_next_token()
            current_token_pos += 1

            if self.current_token.type == EOF:
                break

            if current_token_pos == 2 and self.current_token.type == "SET":
                stack.append(self.current_token.value)
                break

            if self.current_token.type != RIGHT_TOKEN_ORDER[current_token_pos]:
                raise Exception("Invalid syntax")
            
            stack.append(self.current_token.value)

        success = CMD_DICT[cmd](stack)

        return success
