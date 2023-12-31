import re
from tabulate import tabulate

class Table:
    def __init__(self, columns):
        self.columns = columns
        self.rows = []

    def insert(self, values):
        if len(values) != len(self.columns):
            print("Number of values must match the number of columns")
        else:
            self.rows.append(values)
            print(f"1 row inserted into {table_name}")

    def select(self, condition1=None, condition2=None):
        if condition1:
            ind=columns.index(condition1)
            return [row for row in self.rows if row[ind]==condition2]
        else:
            return self.rows

    def display_as_table(self):
        data = [self.columns] + self.rows

        table = tabulate(data, tablefmt="fancy_grid", numalign="center", stralign="center")
        print(table)


def parse_command(command):
    if re.match(r'^\s*CREATE', command, re.IGNORECASE):
        return parse_create(command)
    elif re.match(r'^\s*INSERT', command, re.IGNORECASE):
        return parse_insert(command)
    elif re.match(r'^\s*SELECT', command, re.IGNORECASE):
        return parse_select(command)
    else:
        return None
    
def parse_create(command):
    create_pattern = r'CREATE\s+(\w+)\s+\(([\w\s,]+)\);'
    match = re.match(create_pattern, command, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        columns = [col.strip() for col in match.group(2).split(',')]
        return "CREATE",table_name, columns
    else:
        return None
    
def parse_insert(command):
    insert_pattern = r'INSERT\s+(?:INTO\s+)?(\w+)\s+\(([^)]+)\);'
    match = re.match(insert_pattern, command, re.IGNORECASE)
    if match:
        table_name = match.group(1)
        values = [value.strip() for value in match.group(2).split(',')]
        return "INSERT", table_name, values
    else:
        return None
    
def parse_select(command):
    select_pattern_simpl = r'SELECT\s+FROM\s+(\w+);'
    match = re.match(select_pattern_simpl, command, re.IGNORECASE)
    if match:
        print(match.group(1))
        return "SELECT_SIMPL", match.group(1)
    select_pattern_FJ = r'SELECT\s+FROM\s+(\w+)\s+FULL_JOIN\s+(\w+)\s+ON\s+([\w_]+=[\w_]+);'
    match = re.match(select_pattern_FJ, command, re.IGNORECASE)
    if match:
        c1, c2 = match.group(3).split('=')
        return "SELECT_FJ", match.group(1), match.group(2), c1, c2
    select_pattern_W = r'SELECT\s+FROM\s+(\w+)\s+WHERE\s+([\w_]+=[\w_]+);'
    match = re.match(select_pattern_W, command, re.IGNORECASE)
    if match:    
        c1, c2 = match.group(2).split('=')
        return "SELECT_W", match.group(1), c1, c2
    select_pattern_FJW = r'SELECT\s+FROM\s+(\w+)\s+FULL_JOIN\s+(\w+)\s+ON\s+(\w+)\s*=\s*(\w+)\s+WHERE\s+([\w_]+=[\w_]+);'
    match = re.match(select_pattern_FJW, command, re.IGNORECASE)
    if match:
        c1, c2 = match.group(5).split('=')
        return "SELECT_FJW", match.group(1), match.group(2), match.group(3), match.group(4), c1, c2

tables={}

while 1:
    command = input("Введіть команду SQL: ")
    parsed = parse_command(command)

    if parsed:
        command_type, *args = parsed
        if command_type == "CREATE":
            table_name, columns = args
            if table_name in tables:
                print(f"Table {table_name} already exists")
            else:
                tables[table_name]=Table(columns)
                print(f"Table {table_name} created")
        elif command_type == "INSERT":
            table_name, values = args
            tables[table_name].insert(values)
        elif command_type == "SELECT_SIMPL":
            table_name = args
            tbl=tables[table_name[0]]
            tbl.display_as_table()
        elif command_type == "SELECT_FJ":
            table_name1, table_name2, cond1, cond2 = args
            tbl1=tables[table_name1]
            tbl2=tables[table_name2]
            ind1=tbl1.columns.index(cond1)
            ind2=tbl2.columns.index(cond2)
            backup1=tbl1
            backup2=tbl2
            tbl1.columns+=tbl2.columns
            c=len(tbl1.rows)+1
            for i in tbl1.rows:
                c-=1
                if c==0:
                    break
                toDelete=[]
                notfound=True
                flag=False
                for j in tbl2.rows:
                    if i[ind1]==j[ind2]:
                        if flag==False:
                           i+=j
                           flag=True
                        else:
                            tbl1.insert(i[:2]+j)
                        toDelete.append(j)
                        notfound=False
                flag=True
                for dead in toDelete:
                    tbl2.rows.remove(dead)
                if notfound:
                    i+=(['None']*len(tbl2.columns))
                
            for b in tbl2.rows:
                print(['None']*len(tbl2.columns)+b)
                tbl1.insert(['None']*len(tbl2.columns)+b)
            tbl1.display_as_table()
            tbl1=backup1
            tbl2=backup2

        elif command_type == "SELECT_W":
            table_name, cond1, cond2 = args
            tbl=tables[table_name]
            ind=tbl.columns.index(cond1)
            data=[tbl.columns]+[row for row in tbl.rows if row[ind]==cond2]
            tmptable=tabulate(data, tablefmt="fancy_grid", numalign="center", stralign="center")
            print(tmptable)
        elif command_type == "SELECT_FJW":
            table_name1, table_name2, cond1, cond2, cond3, cond4 = args
            tbl1=tables[table_name1]
            tbl2=tables[table_name2]
            ind1=tbl1.columns.index(cond1)
            ind2=tbl2.columns.index(cond2)
            backup1=tbl1
            backup2=tbl2
            tbl1.columns+=tbl2.columns
            c=len(tbl1.rows)+1
            for i in tbl1.rows:
                c-=1
                if c==0:
                    break
                toDelete=[]
                notfound=True
                flag=False
                for j in tbl2.rows:
                    if i[ind1]==j[ind2]:
                        if flag==False:
                           i+=j
                           flag=True
                        else:
                            tbl1.insert(i[:2]+j)
                        toDelete.append(j)
                        notfound=False
                flag=True
                for dead in toDelete:
                    tbl2.rows.remove(dead)
                if notfound:
                    i+=(['None']*len(tbl2.columns))
                
            for b in tbl2.rows:
                print(['None']*len(tbl2.columns)+b)
                tbl1.insert(['None']*len(tbl2.columns)+b)
            ind=tbl1.columns.index(cond3)
            data=[tbl1.columns]+[row for row in tbl1.rows if row[ind]==cond4]
            tmptable=tabulate(data, tablefmt="fancy_grid", numalign="center", stralign="center")
            print(tmptable)
            tbl1=backup1
            tbl2=backup2
    else:
        print("Команда не валідна.")

#CREATE table1 (AuthorID, AuthorName);
#INSERT INTO table1 (1, Bob Dilan);
#INSERT INTO table1 (2, Ron Seeman);
#INSERT INTO table1 (3, Pate Heople);
#CREATE table2 (BookID, BookName);
#INSERT INTO table2 (3, How to breathe);
#INSERT INTO table2 (1, Spoon user manual);
#INSERT INTO table2 (3, Quantum death);
#INSERT INTO table2 (4, Introduction to C cross cross);
#SELECT FROM table1 FULL_JOIN table2 ON AuthorID=BookID WHERE BookID=3;