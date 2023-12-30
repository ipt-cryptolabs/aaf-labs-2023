from abc import ABC, abstractmethod
from typing import List, Dict, Type
from re import sub
from patterns import Pattern, SPECIAL_CHARS, INITIAL_KEYWORDS, KEYWORDS, get_pattern


class Query:

    def __init__(self):
        self.named_params = dict()
        self.is_finished = False

    def add(self, param_value, param_name: str):
        if param_name is None:
            return  # If a param doesn't have name, it is not needed.
        elif param_name not in self.named_params.keys():
            self.named_params[param_name] = [param_value]
        else:
            self.named_params[param_name].append(param_value)


class ImplementationError(Exception):

    pass  # Class for bug testing purposes


class Match:

    pass


class Compare:

    def __init__(self, pattern: Pattern, token: str):
        self.pattern = pattern
        self.token = token
        self.matched = False
        self.go_to_next_pattern = False
        self.go_to_next_token = False
        self.expected_pattern = ""

    def match(self):
        if self.pattern.match(self.token):
            self.matched = True
            self.go_to_next_token = self.pattern.can_go_to_next_token()
            self.go_to_next_pattern = self.pattern.can_go_to_next_pattern()
            self.expected_pattern = ""
        elif self.pattern.is_optional():
            self.matched = True
            self.go_to_next_pattern = True
            self.expected_pattern = f"{self.pattern}"

    def to_save_in_query(self):
        return self.pattern.is_matching(self.token) and self.pattern.should_be_saved()

    def get_expected_pattern(self):
        return self.expected_pattern


class StandardInputDevice:

    @staticmethod
    def input(prompt: str):
        return input(prompt)


class StandardOutputDevice:

    @staticmethod
    def output(*args):
        print(*args, sep="\t"*5)



class InputProcessor:

    def __init__(self):
        self.input_device = StandardInputDevice()
        self.output_device = StandardOutputDevice()
        self.text = ""
        self.new_string = ""
        self.tokens = []
        self.command = ""
        self.query = Query()

    def clear(self):
        self.text = ""
        self.new_string = ""
        self.tokens = []
        self.command = ""
        self.query = Query()

    def user_input(self):
        prompt = "..." if self.text else ">"
        self.new_string = self.input_device.input(prompt)

    def is_keyword_valid(self) -> bool:
        first_word = self.new_string.split(maxsplit=1)[0].lower()
        if first_word not in INITIAL_KEYWORDS:
            self.output_device.output(f"Error: {first_word} is not a valid keyword")
            return False
        return True

    def is_input_finished(self) -> bool:
        without_quotes = sub("\"(.*?)\"", "", self.text)
        return ";" in without_quotes

    def is_last_input_good(self) -> bool:
        return self.new_string.count("\"") % 2 == 0

    def append_line(self):
        self.text += self.new_string + " "

    def extract_tokens(self):
        text_divided_by_quotes: List[str] = self.text.split(sep="\"")  # count("\"") % 2 == 0

        # remove_text_after_first_semicolon
        for i in range(0, len(text_divided_by_quotes), 2):
            #print(i, text_divided_by_quotes[i])
            if ";" in text_divided_by_quotes[i]:
                text_divided_by_quotes = list(text_divided_by_quotes[:i+1])
                text_divided_by_quotes[-1] = text_divided_by_quotes[-1].split(sep=";", maxsplit=1)[0]
                break
        else:
            self.clear()
            raise ImplementationError("Could not find semicolon by unknown reason. "
                                      "Please send your input to the developer")

        for i in range(0, len(text_divided_by_quotes), 2):
            for char in SPECIAL_CHARS:
                text_divided_by_quotes[i] = text_divided_by_quotes[i].replace(char, f" {char} ")
            text_divided_by_quotes[i] = sub("\s+", " ", text_divided_by_quotes[i])

        self.tokens += text_divided_by_quotes[0].split()
        for i in range(1, len(text_divided_by_quotes), 2):
            self.tokens.append(f"\"{text_divided_by_quotes[i]}\"")  # Just put everything in brackets as a single token
            self.tokens += text_divided_by_quotes[i+1].split()


    def lexical_analysis(self):
        for token in self.tokens:
            if token.lower() in KEYWORDS:
                continue
            elif token in SPECIAL_CHARS:
                continue
            elif token[0] == "\"" and token[-1] == "\"":
                continue
            elif sub("[a-zA-Z][a-zA-Z0-9_]*", "", token):
                self.output_device.output(f"Error: {token} is not a valid token!")
                self.clear()
                break

    def syntax_analysis(self):
        self.command = self.tokens[0].lower()
        self.query.add(self.command, param_name="command")
        patterns = get_pattern(self.command)
        tokens = self.tokens[1:].copy()
        expected_pattern = ""
        while tokens and patterns:
            compare = Compare(patterns[0], tokens[0])
            # print(pattern[0], tokens[0])
            if compare.to_save_in_query():
                self.query.add(tokens[0], param_name=patterns[0].name)
            compare.match()
            if compare.matched:
                expected_pattern = compare.get_expected_pattern()
            else:
                expected_pattern = expected_pattern + f" or {patterns[0]}" if expected_pattern else f"{patterns[0]}"
                self.output_device.output(f"Expected {expected_pattern}, got: '{tokens[0]}'")
                self.clear()
                break
            if compare.go_to_next_pattern:
                patterns = patterns[1:]
            if compare.go_to_next_token:
                tokens = tokens[1:]
        else:
            for pattern in patterns:
                if not pattern.is_optional():
                    self.output_device.output(f"Expected {pattern}, got nothing")
                    self.clear()
                    return

    def get_command(self) -> Query:
        while not self.query.is_finished:  # Until the correct input is given

            # Would be cool if Python had do-whiles
            self.user_input()
            if self.is_last_input_good():
                self.append_line()
            else:
                self.output_device.output("Error: Unfinished string literals are not allowed!")
                self.clear()
                continue

            if not self.is_keyword_valid():
                self.clear()
                continue

            while not self.is_input_finished():
                self.user_input()
                if self.is_last_input_good():
                    self.append_line()
                else:
                    self.output_device.output("Error: Unfinished string literals are not allowed!")
                    self.clear()  # TODO Make this prettier
                    continue

            self.extract_tokens()
            self.lexical_analysis()
            if self.tokens:
                self.syntax_analysis()
                self.query.is_finished = True

        return self.query


class Column:

    def __init__(self, name):
        self.name = name


class Entry:

    def __init__(self, *values):
        self.values = values


class Table:

    def __init__(self, name: str, columns: List[Column]):
        self.name = name
        self.columns = columns
        self.len = len(columns)
        self.entries = []

    def insert(self, values):
        entry = dict()
        for index in range(len(values)):
            entry[index] = values[index]
            entry[self.columns[index].name] = values[index]
        self.entries.append(entry)

    def columns_as_strings(self):
        return [column.name for column in self.columns]


class Database:

    def __init__(self):
        self.tables = dict()

    def create(self, name: str, columns: List[Column]):
        self.tables[name] = Table(name, columns)


class AggregatedFunction(ABC):

    def __init__(self, column: str):
        self.column = column

    @abstractmethod
    def update(self, old_value, entry):
        pass

    @abstractmethod
    def default_value(self):
        pass


class Count(AggregatedFunction):

    def update(self, old_value, entry):
        return old_value + 1

    def default_value(self):
        return 0

    def __repr__(self):
        return f"Count({self.column})"


class Max(AggregatedFunction):

    def update(self, old_value, entry):
        return old_value if old_value > entry[self.column] else entry[self.column]

    def default_value(self):
        return ""

    def __repr__(self):
        return f"Max({self.column})"


class Longest(AggregatedFunction):

    def update(self, old_value, entry):
        return old_value if len(old_value) > len(entry[self.column]) else entry[self.column]

    def default_value(self):
        return ""

    def __repr__(self):
        return f"Longest({self.column})"


AGGREGATED_FUNCTIONS: Dict[str, Type] = {"count": Count, "max": Max, "longest": Longest}


class DatabaseProcessor:

    def __init__(self):
        self.output_device = StandardOutputDevice()
        self.database = Database()

    def create(self, query):
        table_name = query["table_name"][0]
        if table_name in self.database.tables:
            self.output_device.output(f"Table {table_name} already exists")
            return
        columns_list: List[Column] = []
        keywords: List[str] = query["columns"]
        length = len(keywords)
        if length != len(set(keywords)):
            self.output_device.output("Can't create a table with dublicate columns")
            return
        for i in range(length):
            columns_list.append(Column(keywords[i]))

        self.database.create(table_name, columns_list)
        self.output_device.output(f"Table {table_name} is successfully created")

    def insert(self, query):
        table_name = query["table_name"][0]
        table = self.database.tables[table_name]
        values = query["values"]
        if len(values) != table.len:
            self.output_device.output(f"Expected {table.len} arguments, got {len(values)}")
        else:
            table.insert(values)
            self.output_device.output("Values inserted!")

    def __get_all(self, table: Table) -> list:
        return table.entries

    def __get_where(self, table: Table, identifier: str, lower_than: str) -> list:
        valid_entries = []
        if lower_than[0] == "\"":
            for entry in self.__get_all(table):
                if entry[identifier] < lower_than[1:-1]:
                    valid_entries.append(entry)

        else:
            for entry in self.__get_all(table):
                if entry[identifier] < entry[lower_than]:
                    valid_entries.append(entry)

        return valid_entries

    def __group(self, entries, groups, aggregated_functions: List[AggregatedFunction]) -> list:
        entries_groups = []
        entries_functions = []
        ret = []
        for entry in entries:
            new_entry = []
            for group in groups:
                new_entry.append(entry[group])

            if new_entry not in entries_groups:
                aggregated_values = []
                for func in aggregated_functions:
                    aggregated_values.append(func.default_value())
                entries_groups.append(new_entry)
                entries_functions.append(aggregated_values)

            for func_index in range(len(aggregated_functions)):
                old_value = entries_functions[entries_groups.index(new_entry)][func_index]
                entries_functions[entries_groups.index(new_entry)][func_index] =\
                    aggregated_functions[func_index].update(old_value, entry)

        for entry_index in range(len(entries_groups)):
            ret.append(entries_groups[entry_index] + entries_functions[entry_index])

        return ret

    def select(self, query):
        if "functions" in query and "group_by" not in query:
            self.output_device.output("Can't use Aggregated functions if you don't use GROUP_BY")
            return

        table: Table = self.database.tables[query["table_name"][0]]
        # Checking if all identifiers are in table
        if "functions" in query:
            for param in query["functions"][1::2]:
                if param not in table.columns_as_strings():
                    self.output_device.output(f"{param} is not {table.name}'s column")
                    return
        if "group_by" in query:
            for param in query["group_by"]:
                if param not in table.columns_as_strings():
                    self.output_device.output(f"{param} is not {table.name}'s column")
                    return
        if "where" in query:
            for param in query["where"]:
                if param not in table.columns_as_strings() and param[0] != "\"":
                    self.output_device.output(f"{param} is not {table.name}'s column")
                    return

        functions: List[AggregatedFunction] = []
        if "where" in query:
            entries = self.__get_where(table, query["where"][0], query["where"][1])
        else:
            entries = self.__get_all(table)

        if "group_by" in query:
            if "functions" in query:
                while query["functions"]:
                    functions.append(AGGREGATED_FUNCTIONS[query["functions"][0].lower()](query["functions"][1]))
                    query["functions"] = query["functions"][2:]

            entries = self.__group(entries, query["group_by"], functions)
            self.output_device.output(*query["group_by"], *functions)
            for entry in entries:
                self.output_device.output(*entry)
        else:
            self.output_device.output(*table.columns_as_strings())
            for entry in entries:
                l = len(entry)//2
                self.output_device.output(*[entry[i] for i in range(l)])



    def process_query(self, query):
        if query["command"] == ["create"]:
            self.create(query)
        elif query["command"] == ["insert"]:
            self.insert(query)
        elif query["command"] == ["select"]:
            self.select(query)
        else:
            raise ValueError(f"Unknown command: {query['command']}")


class DatabaseApp:

    def __init__(self):
        self.running = True
        self.input_processor = InputProcessor()
        self.database_processor = DatabaseProcessor()

    def run(self):
        while self.running:
            query = self.input_processor.get_command()
            if "command" in query.named_params:
                self.database_processor.process_query(query.named_params)
            self.input_processor.clear()


if __name__ == "__main__":
    database = DatabaseApp()
    database.run()
