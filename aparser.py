import re


regForCreate = r"""\A(?P<command>create)
\s+(?P<table>[a-zA-Z]\w*)
\s+\((?P<names>
(\s*[a-zA-Z]\w*\s*(\sindexed)?\s*,)*
(\s*[a-zA-Z]\w*\s*(\sindexed)?\s*,?))\)\s*;"""

regForInsert = r'''\A(?P<command>insert(\s+into)?)\s+(?P<table>[a-zA-Z]\w*)\s+\((?P<names>
(\s*\"[\w\s]*\"\s*,)*
(\s*\"[\w\s]*\"\s*,?))
\)\s*;
'''

regCreateNames = r"\s*([a-zA-Z]\w*)\s*(\sindexed)?\s*,"
regInsertNames = r'("[\w\s]*")'

regForCreate = re.compile(regForCreate, re.X|re.IGNORECASE)
regForInsert = re.compile(regForInsert, re.X|re.IGNORECASE)




def parseString(input: str):
    input = input.strip()
    output = []
    #case if command is CREATE
    #return array = ["command", "table name", "array of columns", "array indexes(1 = value indexed, 0 = otherwise)"]
    if(re.match(regForCreate, input) != None):  
        output.append(1)
        match = re.match(regForCreate, input)
        #here check if table with this name is exist
        output.append(match.group("table"))
        matchNames = re.findall(regCreateNames,match.group("names") + ",")
        arrayForNames = []
        arrayForInd = []
        for name in matchNames:
            arrayForNames.append(name[0])
            if("indexed" in name[1].lower()):
                arrayForInd.append(1)
            else:
                arrayForInd.append(0)
        output.append(arrayForNames)
        output.append(arrayForInd)
        s = f"Table {match.group('table')} has been created"
        print(s)
        return output
    #case if command is INSERT
    #returns array ["command", "table name", "array of values"]
    if(re.match(regForInsert, input)):     
        output.append(2)
        match = re.match(regForInsert, input)
        #here check if table with this name DOESNT exist
        output.append(match.group("table"))
        matchNames = re.findall(regInsertNames ,match.group("names"))
        #and one more check if number of columns != number of columns in existing table
        arrayForValue = []
        print(matchNames)
        for name in matchNames:
            name = name.strip('"')
            arrayForValue.append(name)
        output.append(arrayForValue)
        s = f"1 row has been inserted into {match.group('table')}"
        print(s)
        return output

    #here will be case for SELECT

    print("error: this command doesnt exist")
    return output


##testing(will be deleted)

sa = """

creAte table   (cat  , dog indexed, rabbit , oleq inDExed, BEE indexed);

34234234234
"""
sb = """


insert into name ("table", "not table","12313123123123") 


; 228 322



"""

print(parseString(sa))
print(parseString(sb))