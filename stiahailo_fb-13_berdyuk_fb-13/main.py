'''
The entry point of the program.
Init CLI and push user`s commands to interpreter.
'''

from src.parser import Interpreter


def main():
    print("Welcome to the AAF lab 8v!\nEnter 'help;' to see the commands available.\nEnter 'quit;' to exit:")
    interpreter = Interpreter()
    while(True):
        try:
            commands = input('>>> ')
            interpreter.parse(commands)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()

