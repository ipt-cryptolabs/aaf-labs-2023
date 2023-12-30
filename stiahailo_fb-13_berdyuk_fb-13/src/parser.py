import re
from src.db import Database


class Interpreter:

    def __init__(self):
        self.db = Database()
        self.COMMANDS = {
            "help": help,
            "quit": quit,
            "create": self.__parse_create,
            "insert": self.__parse_insert,
            "print_index": self.__parse_print_index,
            "search": self.__parse_search
        }
        self.SPACE = r"[\n\r\t\s]*"
        self.STRICT_SPACE = r"[\n\r\t\s]+"
        self.TOKEN = r"[a-zA-Z0-9_]+"
        self.COLLECTION = r"[a-zA-Z][a-zA-Z0-9_]*"
        self.TEXT = r"[a-zA-Z0-9_\s]*"

    def parse(self, commands):
        c = commands.split(";")[:-1]
        if not c:
            raise Exception("Interpreter Error: enter command with ';' ended")
        for command in c:
            tokens = self.__get_tokens(command)

            if not tokens:
                raise Exception("Interpreter Error: empty command")

            if tokens[0].lower() in self.COMMANDS.keys():
                self.COMMANDS[tokens[0].lower()](command)
            else:
                raise Exception(f"Interpreter Error: unknown command '{tokens[0]}'")

    def __get_tokens(self, command):
        return re.findall(rf'{self.TOKEN}', command)

    def __parse_create(self, command):
        m = re.match(rf'{self.SPACE}[cC][rR][eE][aA][tT][eE]{self.STRICT_SPACE}({self.COLLECTION}){self.SPACE}$', command)
        if not m:
            raise Exception("Interpreter Error: command CREATE unknown syntax\n    CREATE <collection_name>")

        self.db.create_collection(m.group(1))

    def __parse_insert(self, command):
        m = re.match(rf'{self.SPACE}[iI][nN][sS][eE][rR][tT]{self.STRICT_SPACE}({self.COLLECTION}){self.STRICT_SPACE}"({self.TEXT})"{self.SPACE}$', command)
        if not m:
            raise Exception('Interpreter Error: command INSERT unknown syntax\n    INSERT <collection_name> "<value>"')

        self.db.insert_in_collection(m.group(1),m.group(2))

    def __parse_print_index(self, command):
        m = re.match(rf'{self.SPACE}[pP][rR][iI][nN][tT]_[iI][nN][dD][eE][xX]{self.STRICT_SPACE}({self.COLLECTION}){self.SPACE}$', command)
        if not m:
            raise Exception("Interpreter Error: command PRINT_INDEX unknown syntax\n    PRINT_INDEX <collection_name>")

        self.db.print_collection_index(m.group(1))

    def __parse_search(self, command):
        m = re.match(rf'{self.SPACE}[sS][eE][aA][rR][cC][hH]{self.STRICT_SPACE}({self.COLLECTION}){self.SPACE}( [wW][hH][eE][rR][eE]{self.STRICT_SPACE}("{self.TOKEN}"{self.SPACE}\d+{self.SPACE}"{self.TOKEN}"|"{self.TOKEN}"{self.SPACE}-{self.SPACE}"{self.TOKEN}"|"[a-zA-Z0-9_]+"))?{self.SPACE}$', command)
        if not m:
            raise Exception('Interpreter Error: command SEARCH unknown syntax\n    SEARCH <collection_name> [WHERE <keyword>|<keyword1> - <keyword2>|<keyword1> <distance> <keyword2>]')

        if m.group(3):
            key1_d, n, key2_d, key1_r,key2_r, key = re.match(
                rf'"({self.TOKEN})"{self.SPACE}(\d+){self.SPACE}"({self.TOKEN})"|"({self.TOKEN})"{self.SPACE}-{self.SPACE}"({self.TOKEN})"|"([a-zA-Z0-9_]+)"',
                m.group(3)).groups()

            if key:
                self.db.search_by_keyword(m.group(1),key)
            elif key1_r and key2_r:
                self.db.search_by_range(m.group(1),key1_r,key2_r)
            elif key1_d and n and key2_d:
                self.db.search_by_keys(m.group(1),key1_d, n, key2_d)
            else:
                raise Exception("Interpreter Error: query unknown syntax\n    <keyword>|<keyword1> - <keyword2>|<keyword1> <distance> <keyword2>")
        else:
            self.db.search_in_collection(m.group(1))

    def help(self, command):
        print('''
There is all commands:
    CREATE <collection_name>
    INSERT <collection_name> "<value>"
    PRINT_INDEX <collection_name>
    SEARCH <collection_name> [WHERE <keyword>|<keyword1> - <keyword2>|<keyword1> <distance> <keyword2>]
        ''')

    def quit(self, command):
        exit(0);




