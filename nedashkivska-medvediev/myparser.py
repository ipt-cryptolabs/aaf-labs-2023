from pyparsing import *

create = Keyword("create")
insert_into = Keyword("insert into")
insert = Keyword("insert")
select = Keyword("select from")
from_kw = Keyword("from")
exit_kw = Keyword("exit")
semicolon = Suppress(";")
comma = Suppress(",")

identifier = Word(alphas + "_")
table_name = identifier("table_name")
column_name = identifier("column_name")

value = QuotedString('"')
condition = column_name + Suppress("<") + value("condition")
data = value + ZeroOrMore(comma + value)

create_command = (create + table_name + Suppress("(") + column_name + ZeroOrMore(comma + column_name) + Suppress(")") + semicolon)
insert_command = (insert_into + table_name + Suppress("(") + data + Suppress(")") + semicolon)
insert_command_without_into = (insert + table_name + Suppress("(") + data + Suppress(")") + semicolon)
select_all_command = (select + table_name + semicolon)
select_with_where_command = (select  + table_name + Suppress('where') + condition + semicolon)
exit_command = (exit_kw + semicolon)

command = create_command | insert_command| insert_command_without_into | select_all_command | select_with_where_command | exit_command

def parse(a: str) -> list:
    res = command.parseString(a.lower())  
    return res.asList()