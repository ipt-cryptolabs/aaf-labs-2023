
Tables = {}

def contains_more_than_one_word(input_string):
    words = input_string.split()
    return len(words) > 1

def forbidden_name(name):
    ReservedWords = ["CREATE","TABLE", "WHERE", "JOIN", "INDEXED", "INSERT","INTO", "SELECT", "FROM", "ON"]
    if name in ReservedWords:
        return True
    for i in "()+/:;'\"*^%":
        if i in name:
            return True
    return False

def StringParser(input):
    end_index = input.find(";")
    if end_index== -1 :
        print('Incorrect syntax. Command must end with a semicolon')
        return 
    
    command = input[:end_index+1]
    command = command.replace("\n", " ")
    command = command.replace("\t", " ")
    command = command.replace("\r", " ")
    while '  ' in command:
        command = command.replace("  ", " ") 
    ## Now checking for special words or arguments


    if command.startswith("CREATE TABLE"):
        ARGUMENTS_tokens  = {}
        temp_command = command

        temp_command = temp_command[12:]
        paranthesis_check1 = temp_command.count("(")
        paranthesis_check2 = temp_command.count(")")
        if paranthesis_check1 !=1  or  paranthesis_check2 != 1:
            print('Incorrect syntax. Too much "(" or ")" chars')
            return
        first_paranthesis = temp_command.find("(")
        last_paranthesis = temp_command.find(")")

        #checking table name
        TABLE_token = temp_command[:first_paranthesis-1]
        if contains_more_than_one_word(TABLE_token):
            print("Incorrect TABLE name. Transaction forbidden.")
            return
        TABLE_token = TABLE_token.replace(" ", "")
        if (not TABLE_token[0].isalpha()) or forbidden_name(TABLE_token):
            print("Incorrect TABLE name. Transaction forbidden.")
            return

        ## parsing arguments
        arguments_string = temp_command[first_paranthesis+1:last_paranthesis]
        # arguments_string = arguments_string.replace(" ", "")
        arguments = arguments_string.split(',')
        # print(arguments)
        for argument in arguments:
            if "INDEXED" in argument:
                argument = argument.replace('INDEXED',"").strip()
                ARGUMENTS_tokens[argument] = True
            else:
                ARGUMENTS_tokens[argument.strip()] = False
        # print(ARGUMENTS_tokens)
        for ARGUMENTS_token in ARGUMENTS_tokens:
            if len(ARGUMENTS_token) == 0:
                print("One of Column Names is 0 length string. Transaction forbidden.")
                return
            if (not ARGUMENTS_token[0].isalpha()) or forbidden_name(ARGUMENTS_token):
                print("One of COLUMN names is incorrect. Transaction forbidden.")
                return

        # print("TABLE_token:",TABLE_token)
        # print("ARGUMENTS_token:",ARGUMENTS_token)
        CreateTableFunc(TABLE_token, ARGUMENTS_tokens)

    elif command.startswith("INSERT"):
        ARGUMENTS_token = []
        temp_command = command
        temp_command = temp_command[6:]

        paranthesis_check1 = temp_command.count("(")
        paranthesis_check2 = temp_command.count(")")
        if paranthesis_check1 !=1  or  paranthesis_check2 != 1:
            print('Incorrect syntax. Too much "(" or ")" chars')
            return
        first_paranthesis = temp_command.find("(")
        last_paranthesis = temp_command.find(")")
        # checking table name
        TABLE_token = temp_command[:first_paranthesis-1]
        if contains_more_than_one_word(TABLE_token):
            print("Incorrect TABLE name. Transaction forbidden.")
            return
        TABLE_token = TABLE_token.replace(" ", "")
        if not TABLE_token[0].isalpha():
            print("Incorrect TABLE name. Transaction forbidden.")
            return

        ##parsing arguments
        arguments_string = temp_command[first_paranthesis + 1:last_paranthesis]
        arguments_string = arguments_string.replace(" ", "")
        arguments_string = arguments_string.replace("'", "")
        while "," in arguments_string:
            coma_index = arguments_string.find(",")
            ARGUMENTS_token.append(arguments_string[:coma_index])
            arguments_string = arguments_string[coma_index + 1:]
        ARGUMENTS_token.append(arguments_string)

        #check for empty insert
        i = 0
        while i < len(ARGUMENTS_token):
            if len(ARGUMENTS_token[i]) == 0:
                print("Empty insert detected. Transaction forbidden.")
                return
            i = i + 1

        #print("TABLE_token:",TABLE_token)
        #print("ARGUMENTS_token:",ARGUMENTS_token)
        InsertIntoTableFunc(TABLE_token, ARGUMENTS_token)

    elif command.startswith("SELECT FROM"):
        TABLE_token = ""
        JOIN_token = ""
        ON_token = ""
        WHERE_token = ""
        temp_command = command
        temp_command = temp_command[11:]

        if "ON " in temp_command and "JOIN " not in temp_command:
            print("JOIN is missing. Transaction forbiden.")
            return

        if "JOIN" in temp_command:
            JOIN_index = temp_command.find("JOIN ")
            TABLE_token = temp_command[:JOIN_index-1]
            if contains_more_than_one_word(TABLE_token):
                print("Incorrect TABLE name. Transaction forbidden.")
                return
            TABLE_token = TABLE_token.replace(" ", "")
            if "ON" not in temp_command:
                print("ON is missing. Transaction forbiden.")
                return
            ON_index = temp_command.find("ON ")
            JOIN_token = temp_command[JOIN_index+5:ON_index-1]
            if contains_more_than_one_word(JOIN_token):
                print("Incorrect joined TABLE name. Transaction forbidden.")
                return
            JOIN_token = JOIN_token.replace(" ", "")
            TABLE_token = TABLE_token.replace(" ", "")
            if not JOIN_token[0].isalpha():
                print("Incorrect JOIN TABLE name. Transaction forbidden.")
                return
            if "WHERE " in temp_command:
                WHERE_index = temp_command.find("WHERE ")
                ON_token = temp_command[ON_index+3:WHERE_index-1]
                ON_token = ON_token.replace(" ", "")
                WHERE_token = temp_command[WHERE_index+6:]
                WHERE_token = WHERE_token.replace(";","")
                WHERE_token = WHERE_token.replace(" ", "")

        else:
            if "WHERE " in temp_command:
                WHERE_index = temp_command.find("WHERE ")
                WHERE_token = temp_command[WHERE_index + 6:]
                WHERE_token = WHERE_token.replace(";", "")
                WHERE_token = WHERE_token.replace(" ", "")

                TABLE_token = temp_command[:WHERE_index-1]

            else:
                TABLE_token = temp_command.replace(";","")
            if contains_more_than_one_word(TABLE_token):
                print("Incorrect TABLE name. Transaction forbidden.")
                return
            TABLE_token = TABLE_token.replace(" ", "")

        if not TABLE_token[0].isalpha():
            print("Incorrect TABLE name. Transaction forbidden.")
            return

        print("TABLE_token:", TABLE_token)
        print("JOIN_token:", JOIN_token)
        print("ON_token:", ON_token)
        print("WHERE_token:", WHERE_token)
        SelectFromTableFunc(TABLE_token, JOIN_token, ON_token, WHERE_token)

    else:
        print(f"Unknown command '{command[:12]}...'")

def CreateTableFunc(TABLE_token, ARGUMENTS_token):
    if TABLE_token in Tables:
        print("Table already exists. Transaction forbidden.")
        return

    #adding table to the dictionary of tables
    Tables[TABLE_token] = []

    #adding dictionary of columns to the corresponding table
    Tables[TABLE_token].append(ARGUMENTS_token)
    i = 0
    while i < len(ARGUMENTS_token):
        Tables[TABLE_token].append([])
        i = i + 1


def InsertIntoTableFunc(TABLE_token, ARGUMENTS_token):
    if TABLE_token in Tables:
        if len(ARGUMENTS_token) > (len(Tables[TABLE_token])-1):
            print("Too many arguments. Transaction forbidden")
            return

        i = 1
        j = 0
        while i < len(Tables[TABLE_token]):
            Tables[TABLE_token][i].append(ARGUMENTS_token[j])
            i = i + 1
            j = j + 1
    else:
        print(f"Table '{TABLE_token}' doesn't exist. Transaction forbidden.")
        return


def TempTableCreate(TABLE_token, JOIN_token, ON_token, WHERE_token):
    print("Hello!")



def PrintDataFunc(TABLE_token, JOIN_token, ON_token, WHERE_token):
    columns_data = Tables[TABLE_token][1:]  # data
    #print(columns_data)
    columns = [key for key in Tables[TABLE_token][0].keys()]  # column names
    #print(columns)

    # check for the longest string in each column
    total_length_of_row = 0
    max_len_array = []
    i = 0
    while i < len(columns_data):
        longest_string = max(columns_data[i], key=len)
        max_len_array.append(len(longest_string))
        i = i + 1

    i = 0
    while i < len(max_len_array):
        if len(columns[i]) > max_len_array[i]:
            max_len_array[i] = len(columns[i])
        i = i + 1

    #print(max_len_array)

    # Creating first row
    print("-"*100)
    print(f"Table {TABLE_token}")
    row = '+-----'
    i = 0
    while i < len(max_len_array):
        row += "+-"
        row += "-" * max_len_array[i]
        row += "-"
        i += 1
    row += "+"
    print(row)

    # Second row
    row = '|  №  '
    i = 0
    while i < len(max_len_array):
        row += "| "
        row += columns[i]
        row += " " * (1 + (max_len_array[i] - len(columns[i])))
        i += 1
    row += "|"
    print(row)

    # Third row
    row = '+-----'
    i = 0
    while i < len(max_len_array):
        row += "+-"
        row += "-" * max_len_array[i]
        row += "-"
        i += 1
    row += "+"
    print(row)

    # other rows
    i = 0
    while i < len(columns_data[0]):
        row = '| ' + str(i) + ' '* (4 - len('| ')+len(str(i)))
        h = 0
        while h < len(max_len_array):
            row += "| "
            row += columns_data[h][i]
            row += " " * (1 + (max_len_array[h] - len(columns_data[h][i])))
            h += 1
        row += "|"
        print(row)

        j = 0
        row = '+-----'
        while j < len(max_len_array):
            row += "+-"
            row += "-" * max_len_array[j]
            row += "-"
            j += 1
        row += "+"
        print(row)

        i = i + 1


def SelectFromTableFunc(TABLE_token, JOIN_token, ON_token, WHERE_token):
    if TABLE_token in Tables and len(JOIN_token) == 0 and len(ON_token) == 0 and len(WHERE_token) == 0:
        PrintDataFunc(TABLE_token, JOIN_token, ON_token, WHERE_token)
    elif TABLE_token in Tables:
        TempTableCreate(TABLE_token, JOIN_token, ON_token, WHERE_token) #New instance of a table called TEMP with needed WHERE condtion has to be created in Tables then printed with PrintDataFunc() then immediately deleted.
    else:
        print(f"Table '{TABLE_token}' doesn't exist. Transaction forbidden.")
        return

InputString1 = "CREATE  TABLE Table1   (Column1 INDEXED, Column2, Column3, Column4); abrakadabra"
InputString2 = "INSERT Table1 ('num1','num2212112','num3121121211','num4'); awdawdwa"
InputString2_1 = "INSERT Table1 ('numaaaaaaaaaaaaaaaaaaaa1','num2212112','num3121121211','num4'); awdawdwa"
InputString3 = "SELECT FROM Table1 JOIN Table2 ON bladbla WHERE condition;"
InputString4 = "SELECT FROM Table1;"
InputString5 = "SELECT FROM Table1 WHERE Column1=num1;"
InputString6 = "SELECT FROM _Table** WHERE condition;"

StringParser(InputString1)
StringParser(InputString2)
StringParser(InputString2)
StringParser(InputString2)
StringParser(InputString2_1)
StringParser(InputString4)
#StringParser(InputString2)




