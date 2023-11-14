
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
                # WHERE_token = WHERE_token.replace(" ", "")
            else:
                ON_token = temp_command[ON_index+3:-1]
                ON_token = ON_token.replace(" ", "")

        else:
            if "WHERE " in temp_command:
                WHERE_index = temp_command.find("WHERE ")
                WHERE_token = temp_command[WHERE_index + 6:]
                WHERE_token = WHERE_token.replace(";", "")
                # WHERE_token = WHERE_token.replace(" ", "")

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
        true_indices = [i for i, value in enumerate(Tables[TABLE_token][0].values()) if value]

        i = 0
        while i < len(true_indices):
            if ARGUMENTS_token[true_indices[i]] in Tables[TABLE_token][true_indices[i]+1]:
                print("Trying to add a clone data to INDEXED COLUMN. Transaction forbidden.")
                return
            i = i + 1



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
    if len(JOIN_token) != 0 and len(ON_token) != 0:
        FirstPart = ON_token[:ON_token.find("==")]
        SecondPart = ON_token[ON_token.find("==")+2:]

        FirstTable = FirstPart[:FirstPart.find(".")]
        FirstColumn = FirstPart[FirstPart.find(".")+1:]
        SecondTable = SecondPart[:FirstPart.find(".")]
        SecondColumn = SecondPart[FirstPart.find(".") + 1:]

        ARGUMENTS_token = {**Tables[FirstTable][0], **Tables[SecondTable][0]}
        CreateTableFunc("TEMP", ARGUMENTS_token)

        keys_list1 = list(Tables[FirstTable][0])
        keys_list2 = list(Tables[SecondTable][0])
        FirstColumnindex = keys_list1.index(FirstColumn)+1
        SecondColumnindex = keys_list2.index(SecondColumn)+1
        skipped_index = []
        i = 0
        while i < len(Tables[TABLE_token][1]):
            arguments_array = []
            j = 1
            while j < len(keys_list1)+1:
                arguments_array.append(Tables[FirstTable][j][i])
                j = j + 1
            try:
                #needed_secondtable_row = Tables[SecondTable][SecondColumnindex].index(Tables[FirstTable][FirstColumnindex][i])
                l = 0
                while l < len(Tables[SecondTable][SecondColumnindex]):
                    if Tables[SecondTable][SecondColumnindex][l] == Tables[FirstTable][FirstColumnindex][i] and l not in skipped_index:
                        needed_secondtable_row = l
                        skipped_index.append(needed_secondtable_row)
                        break
                    l = l + 1
            except:
                break
            j = 1
            while j < len(keys_list1)+1:
                arguments_array.append(Tables[SecondTable][j][needed_secondtable_row])
                j = j + 1
            i = i + 1
            InsertIntoTableFunc("TEMP",arguments_array)

        PrintDataFunc("TEMP", JOIN_token, ON_token, WHERE_token)
        del Tables["TEMP"]

def PrintDataFunc(TABLE_token, JOIN_token, ON_token, WHERE_token):
    columns_data = Tables[TABLE_token][1:]  # data
    columns = [key for key in Tables[TABLE_token][0].keys()]  # column names
    # Check for where token
    if len(WHERE_token) != 0:
        status, columns_data = WhereFilter(columns,columns_data,WHERE_token)
        if not status:
            return


    if len(columns_data[1])==0 :
        print(f"Table {TABLE_token} is empty.")
        return




  
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
    if TABLE_token in Tables and len(JOIN_token) == 0 and len(ON_token) == 0 :
        PrintDataFunc(TABLE_token, JOIN_token, ON_token, WHERE_token)
    elif TABLE_token in Tables:
        TempTableCreate(TABLE_token, JOIN_token, ON_token, WHERE_token) #New instance of a table called TEMP with needed WHERE condtion has to be created in Tables then printed with PrintDataFunc() then immediately deleted.
    else:
        print(f"Table '{TABLE_token}' doesn't exist. Transaction forbidden.")
        return

def WhereTokenSplit(WHERE_token):
    split_index = WHERE_token.find(' > ')
    if split_index == -1:
        return False, None, None
    else:
        first_column =WHERE_token[:split_index].replace(" ","")
        second_part = WHERE_token[split_index+3:]
        quote_index = second_part.find("'")
        if quote_index == -1:
            return True, first_column, {'column':second_part.replace(" ","")}
        else:
            next_quote_index = second_part[quote_index+1:].find("'")
            return True, first_column, {'value':second_part[quote_index+1:next_quote_index+1]}

def WhereFilter(columns,columns_data,WHERE_token):
    status, first_column, second_part = WhereTokenSplit(WHERE_token)
    if not status:
        print("Missing ' > ' in WHERE condition. Transaction forbidden.")
        return False, None
    else: 
        if first_column not in columns:
            print(f"Bad column name '{first_column}' in WHERE condition. Transaction forbidden.") 
            return False, None
        else:
            first_column_index = columns.index(first_column)
        for key in second_part:
            if key == 'column':
                second_column = second_part[key]
                if second_column not in columns:
                    print(f"Bad column name '{second_column}' in WHERE condition. Transaction forbidden.") 
                    return False, None
                else:
                    second_column_index = columns.index(second_column)
                match_indexes = []
                for i in range(len(columns_data[first_column_index])):
                    if columns_data[first_column_index][i] == columns_data[second_column_index][i]:
                        match_indexes.append(i)
            else:
                match_indexes = []
                for i in range(len(columns_data[first_column_index])):
                    # print('Cpmpare',columns_data[first_column_index][i],'with',second_part[key])
                    if columns_data[first_column_index][i] == second_part[key]:
                        
                        match_indexes.append(i)
    new_columns_data = []
    for column_data  in columns_data:
        new_column_data = []
        for i in match_indexes:
            new_column_data.append(column_data[i])
        new_columns_data.append(new_column_data)
    return status, new_columns_data
    

InputString1 = "CREATE  TABLE Table1   (Column1, Column2, Column3, Column4); abrakadabra"
InputString1_1 = "CREATE  TABLE Table2   (Col1, Col2, Col3, Col4); abrakadabra"
InputString2 = "INSERT Table1 ('num1','num2212112','num3121121211','num4'); awdawdwa"
InputString2_1 = "INSERT Table1 ('num1','num2212112','num3121121211','num4'); awdawdwa"
InputString2_2 = "INSERT Table2 ('num1','a','num3121121211','num4'); awdawdwa"
InputString2_3 = "INSERT Table2 ('num1','b','num3121121211','b'); awdawdwa"
InputString3 = "SELECT FROM Table1 JOIN Table2 ON Table1.Column1==Table2.Col1 WHERE Col2 > Col4;"
InputString4 = "SELECT FROM Table1 JOIN Table2 ON Table1.Column1==Table2.Col1 WHERE Col2 > 'a';"
InputString5 = "SELECT FROM Table1 JOIN Table2 ON Table1.Column1==Table2.Col1 ;"
InputString6 = "SELECT FROM Table2 WHERE Col2 > 'a';"
InputString7 = "SELECT FROM Table2 ;"

# InputString4 = "SELECT FROM Table1;"
# InputString5 = "SELECT FROM Table1 WHERE Column1===num1;"
# InputString6 = "SELECT FROM _Table** WHERE condition;"


StringParser(InputString1)
StringParser(InputString1_1)
StringParser(InputString2)
StringParser(InputString2_1)
StringParser(InputString2_2)
StringParser(InputString2_3)
StringParser(InputString3)
StringParser(InputString4)
StringParser(InputString5)
StringParser(InputString6)
StringParser(InputString7)






