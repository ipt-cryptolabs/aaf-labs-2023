import re


regForCreate = r'''\A(?P<command>create)
\s+(?P<table>[a-zA-Z]\w*)
\s+\((?P<names>
(\s*[a-zA-Z]\w*\s*(\sindexed)?\s*,)*
(\s*[a-zA-Z]\w*\s*(\sindexed)?\s*,?))\)\s*;'''

regForInsert = r'''\A(?P<command>insert(\s+into)?)\s+
(?P<table>[a-zA-Z]\w*)\s+\(
(?P<names>(\s*\"[\w\s]*\"\s*,)*
(\s*\"[\w\s]*\"\s*,?))\)\s*;'''

regForSelect = r'''\A(?P<command>select\s+from)\s+(?P<table>[a-zA-Z]\w*)\s*
(\swhere\s+(?P<whereLeft>[a-zA-Z]\w*)\s+\>\s+(?P<whereRight>(?:[a-zA-Z]\w*)|(?:"[\w\s]*")))?\s*
(\sorder_by(?P<names>(\s*[a-zA-Z]\w*(\s+(?:asc)|\s+(?:desc))?\s*,)*\s*
([a-zA-Z]\w*(\s+(?:asc)|\s+(?:desc))?))\s*)?;'''

regCreateNames = r'\s*([a-zA-Z]\w*)\s*(\sindexed)?\s*,'
regInsertNames = r'("[\w\s]*")'
regSelectNames = r'\s*([a-zA-Z]\w*)(\s+(?:(?:asc)|(?:desc)))?\s*,'

regCreateNames = re.compile(regCreateNames, re.X|re.IGNORECASE)

regForCreate = re.compile(regForCreate, re.X|re.IGNORECASE)
regForInsert = re.compile(regForInsert, re.X|re.IGNORECASE)
regForSelect = re.compile(regForSelect, re.X|re.IGNORECASE)

def parseString(input_str: str):
    input_str = input_str.strip()
    output = []

    #case if command is CREATE
    #return array = ["command", "table name", "array of pairs: (column, isIndexed)",]
    if(re.match(regForCreate, input_str) != None):  
        output.append(1)
        match = re.match(regForCreate, input_str)
        #here check if table with this name is exist
        output.append(match.group("table"))
        matchNames = re.findall(regCreateNames,match.group("names") + ",")
        arrayForNames = []
        for name in matchNames:
            if("indexed" in name[1].lower()):
                arrayForNames.append((name[0],1))
            else:
                arrayForNames.append((name[0],0))
        output.append(arrayForNames)
        s = f"Table {match.group('table')} has been created"
        print(s)
        return output
    
    #case if command is INSERT
    #returns array ["command", "table name", "array of values"]
    if(re.match(regForInsert, input_str)):     
        output.append(2)
        match = re.match(regForInsert, input_str)
        #here check if table with this name DOESNT exist
        output.append(match.group("table"))
        matchNames = re.findall(regInsertNames ,match.group("names"))
        #and one more check if number of columns != number of columns in existing table
        arrayForValue = []
        for name in matchNames:
            name = name.strip('"')
            arrayForValue.append(name)
        output.append(arrayForValue)
        s = f"1 row has been inserted into {match.group('table')}"
        print(s)
        return output

    #case if command is SELECT
    #return array ["command", "table name", "whereLeft","whereRight", "array of (column,isDesc) for ORDER_BY"], where last 3 values can be None
    if(re.match(regForSelect,input_str)):
        output.append(3)
        match = re.match(regForSelect,input_str)
        #here check if table with this name DOESNT exist
        output.append(match.group("table"))
        output.append(match.group("whereLeft"))
        output.append(match.group("whereRight"))
        #here check if column "whereLeft" exist, and if value of "whereRight" not in quotes check again
        matchNames = []
        if(match.group("names") != None):
            matchNames = re.findall(regSelectNames, match.group("names")+',')
        #here check if columns exist
        arrayForNames = []
        for name in matchNames:
            if("desc" in name[1].lower()):
                arrayForNames.append((name[0],1))
            else:
                arrayForNames.append((name[0],0))
        output.append(arrayForNames)
        return output
    #case, if command is EXIT
    if(re.match(r"\s*exit\s*", input_str, re.IGNORECASE)):
        output.append(-1)
        return output
    

    print("error: this command doesnt exist")
    output.append(0)
    return output
