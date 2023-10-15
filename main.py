from re import sub


class ImplementationError(Exception):

    pass  # Class for bug testing purposes

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

    def user_input(self):
        prompt = "..." if self.text else ">"
        self.new_string = self.input_device.input(prompt)

    def is_input_finished(self) -> bool:
        print(self.text)
        without_quotes = sub("\"(.*?)\"", "", self.text)
        print(";" in without_quotes)
        return ";" in without_quotes

    def check_last_input(self):
        if self.new_string.count("\"") % 2:
            self.output_device.output("SyntaxError: Unfinished string literals are not allowed!")
            self.new_string = ""
            self.text = ""
        else:
            self.text += self.new_string + " "

    def lexical_analysis(self):
        text_divided_by_quotes = self.text.split(sep="\"")  # count("\"") % 2 == 0

        # remove_text_after_first_semicolon
        for i in range(0, len(text_divided_by_quotes), 2):
            print(i, text_divided_by_quotes[i])
            if ";" in text_divided_by_quotes[i]:
                text_divided_by_quotes = list(text_divided_by_quotes[:i+1])
                text_divided_by_quotes[-1] = text_divided_by_quotes[-1].split(sep=";", maxsplit=1)[0]
                break
        else:
            raise ImplementationError("Could not find semicolon by unknown reason. "
                                      "Please send your input to the developer")
        print(text_divided_by_quotes)

        for i in range(0, len(text_divided_by_quotes), 2):
            text_divided_by_quotes[i] = sub("\s+", " ", text_divided_by_quotes[i])

        self.tokens += text_divided_by_quotes[0].split()
        for i in range(1, len(text_divided_by_quotes), 2):
            self.tokens.append(f"\"{text_divided_by_quotes[i]}\"")  # Just put everything in brackets as a single token
            self.tokens += text_divided_by_quotes[i].split()

        print(self.tokens)





    def get_command(self) -> dict:
        while not self.tokens:  # Until the correct input is given

            while not self.is_input_finished():
                self.user_input()
                self.check_last_input()

            self.lexical_analysis()

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