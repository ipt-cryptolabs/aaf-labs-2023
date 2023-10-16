import aparser

if __name__ == "__main__":
    output = []
    while True:
        print("Type the command(SQL-like)")
        ins = input()
        output = aparser.parseString(ins)
        if(output[0] == -1):
            break
   