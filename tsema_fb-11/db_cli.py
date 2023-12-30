import os
from query_parser import Parser


WHITE = "\u001b[37m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
BOLD = "\u001b[1m"
RESET = "\u001b[0m"

class CLI:
    def __init__(self, cli_cmd_symbol: str, wait_for_full_q_symbol: str) -> None:
        self.cli_cmd_symbol = cli_cmd_symbol
        self.wait_for_full_q_symbol = wait_for_full_q_symbol
        self.EOQ = ';'
        self.query = ""
        self.start_cli()


    def clear_cli(self) -> None:
        if os.name == "posix": 
            os.system("clear")
        else: 
            os.system("cls")


    def wait_for_query(self):
        yield (qline := input(f"{BOLD}{WHITE}{self.cli_cmd_symbol}{RESET}"))

        while not self.EOQ in qline:
            yield (qline := input(f"{BOLD}{WHITE}{self.wait_for_full_q_symbol}{RESET}"))


    def start_cli(self) -> None:
        self.clear_cli()

        p = Parser()
        while True:
            query = " ".join([line for line in self.wait_for_query()])
            
            try:
                p.get_query(query)
                success = p.exec()
                print(f"\n{BOLD}{WHITE}[{GREEN}*{WHITE}] {success}{RESET}\n")
            except Exception as e:
                print(f"\n{BOLD}{WHITE}[{RED}!{WHITE}] {e}{RESET}\n")

                
if __name__ == "__main__":
    cli = CLI("query> ", "-> ")
    cli.start_cli()
