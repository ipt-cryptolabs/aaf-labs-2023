import aparser
import database

if __name__ == "__main__":
    output = []
    connection = database.Database()
    while True:
        print("Type the command(SQL-like):")
        
        input_str = input()
        bracket_count = 0
        parentheses_count = 0
        quote_open = False

        for char in input_str:
                if char == '(':
                    parentheses_count += 1
                elif char == ')':
                    parentheses_count -= 1
                elif char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                elif char == '"':
                    quote_open = not quote_open

        while not (input_str.endswith(';') and bracket_count == 0 and parentheses_count == 0 and not quote_open):
            # Continuously read input
            new_input = input('> ')
            input_str += ' ' + new_input

            for char in new_input:
                if char == '(':
                    parentheses_count += 1
                elif char == ')':
                    parentheses_count -= 1
                elif char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                elif char == '"':
                    quote_open = not quote_open
        
        
        output = aparser.parseString(input_str)
        if(len(output)>2):
            connection.execute(output[0],output[1],output[2])
        
        if(output[0] == -1):
            break
            