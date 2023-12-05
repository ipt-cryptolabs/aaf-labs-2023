from re import sub
from patterns import Pattern, PATTERNS, SPECIAL_CHARS, INITIAL_KEYWORDS, KEYWORDS


class Query:

    def __init__(self):
        self.unnamed_params = list()
        self.named_params = dict()
        self.is_finished = False

    def add(self, param_value, param_name=None):
        if param_name is None:
            self.unnamed_params.append(param_value)
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

    def match(self):
        if self.pattern.match(self.token):
            print("aclehwelifhwleifhwfe!")
            self.matched = True
            self.go_to_next_token = self.pattern.can_go_to_next_token()
            self.go_to_next_pattern = self.pattern.can_go_to_next_pattern()
        elif self.pattern.is_optional():
            self.matched = True
            self.go_to_next_pattern = True

    def to_save_in_query(self):
        return self.pattern.is_matching(self.token)


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
        print(self.text)
        without_quotes = sub("\"(.*?)\"", "", self.text)
        print(";" in without_quotes)
        return ";" in without_quotes

    def is_last_input_good(self) -> bool:
        return self.new_string.count("\"") % 2 == 0

    def append_line(self):
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
        self.command = self.tokens[0].lower()
        self.query.add(self.command, param_name="command")
        pattern = PATTERNS[self.command]
        tokens = self.tokens[1:].copy()
        while tokens:
            compare = Compare(pattern[0], tokens[0])
            print(f"Comparing: {pattern[0]} {tokens[0]}")
            if compare.to_save_in_query():
                self.query.add(tokens[0], param_name=pattern[0].name)
            compare.match()
            if not compare.matched:
                self.output_device.output(f"Expected {pattern[0]}, got: '{tokens[0]}'")
                self.clear()
                break
            if compare.go_to_next_pattern:
                pattern = pattern[1:]
            if compare.go_to_next_token:
                print("Going to next token")
                tokens = tokens[1:]
        else:
            if pattern:
                self.output_device.output(f"Expected {pattern[0]}, got nothing")

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
                print("Invalid keyword")
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
            self.syntax_analysis()
            self.query.is_finished = True

        return self.query



class Database:

    def __init__(self):
        self.running = True
        self.input_processor = InputProcessor()

    def run(self):
        while self.running:
            query = self.input_processor.get_command()
            print(query.unnamed_params, query.named_params)
            self.running = False


if __name__ == "__main__":
    database = Database()
    database.run()
