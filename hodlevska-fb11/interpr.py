import re
from kdtree import KDTree


collections = dict()


class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f"Token<{self.type}, {self.value}>"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    
class Parser:
    def __init__(self) -> None:
        self.query = None
        self.pos = 0
        self.curr_token = None
        self.curr =  None


    def adv(self):
        self.pos += 1
        if self.pos > len(self.query) - 1:
            self.curr = None
        else:
            self.curr = self.query[self.pos]
    

    @staticmethod
    def _create(ident):
        if ident in collections.keys():
            raise Exception(f"This collection already exists (\"{ident}\")")
        
        collections.update({ident: KDTree()})
        return f"Collection \"{ident}\" has been created"


    @staticmethod
    def _insert(col, point):
        if col not in collections.keys():
            raise Exception(f"This collection doesn't exist (\"{col}\")")
        
        collections[col].insert(tuple(point))
        return f"Insert point \"{str(point)}\" in \"{col}\""


    @staticmethod
    def _search(col, cond=None):
        if col not in collections.keys():
            raise Exception(f"This collection doesn't exist (\"{col}\")")
        
        if collections[col].root == None:
            raise Exception(f"This collection is empty")
        
        if cond:
            if len(cond) <= 1:
                raise Exception("Invalid parameters")
            
            if cond[0] == "INSIDE":
                if len(cond[1]) != 2:
                    raise Exception("Invalid parameters")
                
                p_bottom, p_top = cond[1]

                if len(p_bottom) != 2 or len(p_top) != 2:
                    raise Exception("Invalid parameters")
                
                return f"Points inside rectangle {cond[1][0]} {cond[1][1]}: " + str(collections[col].points_inside_rectangle(*p_bottom, *p_top))
            elif cond[0] == "ABOVE_TO":
                return f"Point(s) above y={cond[1][0]}: " + str(collections[col].above_to(cond[1][0]))
            elif cond[0] == "NN":
                return f"Nearest neighbour(s) for target point {cond[1][0]} is: " + str(collections[col].nn(*cond[1][0]))
        else:
            return f"Points in \"{col}\": " + ", ".join([str(p) for p in collections[col]])

    
    @staticmethod
    def _print_tree(col):
        if col not in collections.keys():
            raise Exception(f"This collection doesn't exist (\"{col}\")")
        
        print(f"KDTree {col}")
        collections[col].print_tree()


    @staticmethod
    def _contains(col, target):
        if col not in collections.keys():
            raise Exception(f"This collection doesn't exist (\"{col}\")")
        
        if collections[col].contains(target, collections[col].root):
            return f"Point {target} exists in collection {col}"
        return f"Point {target} doesn't exist in collection {col}"


    def recvQuerry(self, query):
        s = []

        self.query = query
        self.pos = 0
        self.curr_token = None
        self.curr = self.query[self.pos]

        for char in self.query:
            if char in '(':
                s.append(char)
            elif char in ')':
                if not s:
                    raise Exception("There is no matching opening parenthesis in query")
                
                top = s.pop()
                if char == ')' and top != '(':
                    raise Exception("There is no matching opening parenthesis in query")


    def _retInt(self):
        result_int = ""

        while self.curr.isnumeric() or self.curr == '-':
            result_int += self.curr
            self.adv()

        return int(result_int)
    

    def _getPointT(self):
        point = []

        while self.curr != ")":
            if self.curr.isdigit() or self.curr == '-':
                point.append(self._retInt())
            else:
                self.adv()

        self.adv()
        if len(point) != 2:
            raise Exception(f"Wrong point format (x, y)")
        
        return Token("POINT", point)
    
    
    def _getCmdT(self):
        cmd = ""

        while self.curr.isalpha() or self.curr == "_":
            cmd += self.curr
            self.adv()

        if cmd.upper() not in ['CREATE', 'INSERT', 'PRINT_TREE', 'SEARCH', 'CONTAINS']:
            raise Exception("An unknown command in the query")

        return Token("CMD", cmd.upper())
    

    def _getCondT(self):
        cond_phrase = ""

        while self.curr.isalpha() or self.curr == '_':
            cond_phrase += self.curr
            self.adv()

        if cond_phrase.upper() not in ['WHERE', 'INSIDE', 'ABOVE_TO', 'NN']:
            raise Exception("An unknown condition in the query")
        
        return Token("COND_PHRASE", cond_phrase.upper())
    

    def _getIdentT(self):
        ID = ""

        while self.curr not in ['\n', '\r', '\t', ' '] and self.curr != ";":
            ID += self.curr
            self.adv()

        if not re.match("[a-zA-Z][a-zA-Z0-9_]*", ID):
            raise Exception("Incorrect identifier format")
        
        if ID.upper() in ['CREATE', 'INSERT', 'PRINT_TREE', 'SEARCH', 'CONTAINS']:
            raise Exception(f"This identifier name is not available ({ID})")

        return Token("ID", ID)
    
    
    def _getIntT(self):
        return Token("INT", self._retInt())


    def _getCondQuerry(self):
        cond_querry = []

        while self.curr != ";":
            if self.curr in ['\n', '\r', '\t', ' ']:
                self.adv()

            if self.curr == "(" or self.curr == ",":
                cond_querry.append(self._getPointT())
            elif self.curr.isdigit() or self.curr == '-':
                cond_querry.append(self._retInt)
            else:
                cond_querry.append(self._getCondT())

        return Token("COND", cond_querry)
    
    
    def _next(self):
        while self.curr != ";":

            if self.curr in ['\n', '\r', '\t', ' ']:
                self.adv()

                if self.curr == ";":
                    return Token("EOF", None)

            if self.curr == "(":
                return self._getPointT()
            
            if self.curr.isnumeric() or self.curr == "-":
                return self._getIntT()
            
            if self.curr_token == None:
                return self._getCmdT()
            
            elif self.curr_token.type == "ID":
                return self._getCondT()
            
            elif self.curr_token.type == "COND_PHRASE":
                return self._getCondQuerry()
            
            else:
                if self.curr in ['\n', '\r', '\t', ' ']:
                    self.adv()
                    continue

                return self._getIdentT()

        return Token("EOF", None)
    

    def exec(self):
        RIGHT_ORD = "CMD", "ID", "COND_PHRASE", "COND"

        self.curr_token = self._next()
        if self.curr_token.type != "CMD":
            raise Exception("Invalid syntax")

        cmd = self.curr_token.value
        stack = []

        current_token_pos = 0
        while current_token_pos < len(RIGHT_ORD):

            self.curr_token = self._next()
            current_token_pos += 1

            if self.curr_token.type == "EOF":
                break

            if current_token_pos == 2 and self.curr_token.type == "POINT":
                stack.append(self.curr_token.value)
                break

            if self.curr_token.type != RIGHT_ORD[current_token_pos]:
                raise Exception("Invalid syntax")
            
            stack.append(self.curr_token.value)

        if cmd == "CREATE":
            print(self._create(stack.pop(0)))

        elif cmd == "INSERT":
            print(self._insert(stack.pop(0), stack.pop(0)))

        elif cmd == "SEARCH":
            col = stack.pop(0)
            if stack:
                stack.pop(0)
                c = stack.pop(0)
                cond = [c.pop(0).value, [t.value for t in c]]
            else:
                cond = None
            print(self._search(col, cond))

        elif cmd == "PRINT_TREE":
            self._print_tree(stack.pop(0))

        elif cmd == "CONTAINS":
            print(self._contains(stack.pop(0), stack.pop(0)))
