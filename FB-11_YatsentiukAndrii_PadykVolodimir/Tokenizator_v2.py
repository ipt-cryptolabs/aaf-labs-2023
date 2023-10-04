# ReservedWords = ["CREATE TABLE", "WHERE", "JOIN", "INDEXED", "INSERT INTO", "SELECT FROM", "ON"]
##Tables = {}

def contains_more_than_one_word(input_string):
    words = input_string.split()
    return len(words) > 1

def forbidden_name(name):
    ReservedWords = ["CREATE","TABLE", "WHERE", "JOIN", "INDEXED", "INSERT","INTO", "SELECT", "FROM", "ON"]
    if name in ReservedWords:
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
            if not ARGUMENTS_token[0].isalpha():
                print("One of COLUMN names is incorrect. Transaction forbidden.")
                return
            


        print("TABLE_token:",TABLE_token)
        print("ARGUMENTS_token:",ARGUMENTS_tokens)

        """#adding table to the dictionary of tables
        Tables[table_name] = []

        #adding list of columns to the corresponding table
        Tables[table_name].append(arguments)
        i = 0
        while i < len(arguments):
            Tables[table_name].append([])
            i = i + 1
        """

    elif command.startswith("INSERT"):
        ARGUMENTS_token = []
        temp_command = command
        temp_command = temp_command[6:]


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

        print("TABLE_token:",TABLE_token)
        print("ARGUMENTS_token:",ARGUMENTS_token)

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

    else:
        print(f"Unknown command '{command[:12]}...'")



InputString1 = "CREATE  TABLE table1   (Column1 INDEXED, Column2, Column3, Column4); abrakadabra"
InputString2 = "INSERT Table1 ('num1','num2','num3','num4'); awdawdwa"
InputString3 = "SELECT FROM Table11 JOIN Table12 ON bladbla WHERE condition;"
InputString4 = "SELECT FROM Table11;"
InputString5 = "SELECT FROM Table11 WHERE condition;"
InputString6 = "SELECT FROM _Table** WHERE condition;"

#StringParser(InputString1)
#StringParser(InputString2)
#StringParser(InputString1)




