from abc import ABC, abstractmethod
from re import sub, fullmatch
from typing import List


SPECIAL_CHARS = ("(", ")", "<", ",")
INITIAL_KEYWORDS = ("create", "insert", "select")
KEYWORDS = ("create", "insert", "into", "select", "from", "where", "group_by", "indexed")

class ImplementationError(Exception):

    pass  # Class for bug testing purposes


class Match:

    pass


class Pattern(ABC):

    @abstractmethod
    def match(self, value):
        pass

    @abstractmethod
    def is_optional(self) -> bool:
        pass

    @abstractmethod
    def is_finished(self) -> bool:
        pass


class StringPattern(Pattern):

    def __init__(self, string_value: str):
        self.string_value = string_value

    def match(self, token: str) -> bool:
        return token.lower() == self.string_value

    def is_optional(self) -> bool:
        return False

    def is_finished(self) -> bool:
        return True


class OptionalStringPattern(StringPattern):

    def is_optional(self) -> bool:
        return True


class IdentifierPattern(Pattern):

    def match(self, value) -> bool:
        if fullmatch("[a-zA-Z][a-zA-Z0-9_]*", value):
            print("Matched!")
            return True
        print("Unmatched!")
        return False

    def is_optional(self) -> bool:
        return False

    def is_finished(self) -> bool:
        return True


class RepeatedPattern(Pattern):

    def __init__(self, patterns: List[Pattern]):
        self.patterns = patterns
        self.last_index = len(patterns)-1
        self.index = 0
        self.finished = False

    def match(self, value):
        print(f"Matching {value} to pattern {self.patterns[self.index]}")
        if self.patterns[self.index].match(value):
            print("Matched!")
            self.index = 0 if self.index == self.last_index else self.index + 1
            return True
        elif self.index == self.last_index:
            print("Kind of matched...")
            self.finished = True
            return True
        elif self.patterns[self.index].is_optional():
            print("Skipping optional...")
            return True
        else:
            print("Not matched!")
            return False

    def is_optional(self) -> bool:
        return False

    def is_finished(self) -> bool:
        return self.finished


PATTERNS = {"create": [IdentifierPattern(),
                       StringPattern("("),
                       RepeatedPattern([IdentifierPattern(),
                                        OptionalStringPattern("indexed"),
                                        StringPattern(",")]),
                       StringPattern(")")]}



class Compare:

    def __init__(self, pattern: Pattern, token: str):
        self.pattern = pattern
        self.token = token
        self.matched = False
        self.go_to_next_pattern = False
        self.go_to_next_token = False

    def match(self):
        if self.pattern.match(self.token):
            self.matched = True
            self.go_to_next_token = True
            self.go_to_next_pattern = self.pattern.is_finished()
        elif self.pattern.is_optional():
            self.matched = True
            self.go_to_next_pattern = True


class StandardInputDevice:

    @staticmethod
    def input(prompt: str):
        return input(prompt)


class StandardOutputDevice:

    @staticmethod
    def output(s: str):
        print(s)



class InputProcessor:

    def __init__(self):
        self.input_device = StandardInputDevice()
        self.output_device = StandardOutputDevice()
        self.text = ""
        self.new_string = ""
        self.tokens = []
        self.query = dict()

    def clear(self):
        self.text = ""
        self.new_string = ""
        self.tokens = []
        self.query = dict()

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
        print(self.text)
        without_quotes = sub("\"(.*?)\"", "", self.text)
        print(";" in without_quotes)
        return ";" in without_quotes

    def check_last_input(self):
        if self.new_string.count("\"") % 2:
            self.output_device.output("Error: Unfinished string literals are not allowed!")
            self.clear()
        else:
            self.text += self.new_string + " "

    def extract_tokens(self):
        text_divided_by_quotes = self.text.split(sep="\"")  # count("\"") % 2 == 0

        # remove_text_after_first_semicolon
        for i in range(0, len(text_divided_by_quotes), 2):
            print(i, text_divided_by_quotes[i])
            if ";" in text_divided_by_quotes[i]:
                text_divided_by_quotes = list(text_divided_by_quotes[:i+1])
                text_divided_by_quotes[-1] = text_divided_by_quotes[-1].split(sep=";", maxsplit=1)[0]
                break
        else:
            self.clear()
            raise ImplementationError("Could not find semicolon by unknown reason. "
                                      "Please send your input to the developer")
        print(text_divided_by_quotes)

        for i in range(0, len(text_divided_by_quotes), 2):
            for char in SPECIAL_CHARS:
                text_divided_by_quotes[i] = text_divided_by_quotes[i].replace(char, f" {char} ")
            text_divided_by_quotes[i] = sub("\s+", " ", text_divided_by_quotes[i])

        self.tokens += text_divided_by_quotes[0].split()
        for i in range(1, len(text_divided_by_quotes), 2):
            self.tokens.append(f"\"{text_divided_by_quotes[i]}\"")  # Just put everything in brackets as a single token
            self.tokens += text_divided_by_quotes[i+1].split()

        print(self.tokens)


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
        command = self.tokens[0]
        pattern = PATTERNS[command]
        self.tokens = self.tokens[1:]
        while self.tokens:
            compare = Compare(pattern[0], self.tokens[0])
            compare.match()
            if not compare.matched:
                self.output_device.output(f"Expected {pattern[0]}, got: {self.tokens[0]}")
                self.clear()
                break
            if compare.go_to_next_pattern:
                pattern = pattern[1:]
            if compare.go_to_next_token:
                self.tokens = self.tokens[1:]
        else:
            print("Nice command!")



    def get_command(self) -> dict:
        while not self.query:  # Until the correct input is given

            self.user_input()
            self.check_last_input()
            if not self.is_keyword_valid():
                print("Invalid keyword")
                self.clear()
                continue
            while not self.is_input_finished():
                print("Input not finished")
                self.user_input()
                self.check_last_input()

            print("Input finished")
            self.extract_tokens()
            self.lexical_analysis()
            self.syntax_analysis()

        return self.query



class Database:

    def __init__(self):
        self.running = True
        self.input_processor = InputProcessor()

    def run(self):
        while self.running:
            self.input_processor.get_command()


if __name__ == "__main__":
    database = Database()
    database.run()
