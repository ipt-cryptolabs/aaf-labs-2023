from pyparsing import *

create = Keyword("create")  
insert_into = Keyword("insert into")
insert = Keyword("insert")
select = Keyword("select from")   
from_kw = Keyword("from")
where = Keyword("where")
exit_kw = Keyword("exit")
semicolon = Suppress(";")
comma = Suppress(",")
identifier = Word(alphas + "_")
table_name = identifier("table_name")  
column_name = identifier("column_name")
value = QuotedString('"')
condition = column_name + Suppress("<") + value("condition")
data = delimitedList(value)

create_command = (create + table_name + Suppress("(") + delimitedList(column_name) +  Suppress(")") + semicolon)

insert_into_command = (insert_into + table_name +  Suppress("(") + data +  Suppress(")") + semicolon)
                       
insert_command = (insert + table_name + Suppress("(") + data + Suppress(")") + semicolon)
                  
select_all_command = (select + table_name + semicolon)

select_with_where_command = (select + table_name +  where + condition + semicolon)
                             
exit_command = (exit_kw + semicolon)

command = (create_command | insert_into_command | insert_command | select_all_command | select_with_where_command | exit_command)
           
def parse(a: str) -> list:
    res = command.parseString(a.lower())  
    return res.asList()