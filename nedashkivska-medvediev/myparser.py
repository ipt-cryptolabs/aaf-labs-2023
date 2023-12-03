from pyparsing import *


CREATE = Keyword("CREATE")
INSERT_INTO = Keyword("INSERT INTO")
SELECT = Keyword("SELECT")
FROM = Keyword("FROM")
STAR = Keyword("*")
EXIT = Keyword("exit")
SEMICOLON = Suppress(";")
COMMA = Suppress(",")


identifier = Word(alphas + "_")
table_name = identifier("table_name")
column_name = identifier("column_name")


value = QuotedString('"')
condition = column_name + Suppress("<") + value("condition")
data = value + ZeroOrMore(COMMA + value)


create_command = (CREATE + table_name + Suppress("(") + column_name + ZeroOrMore(COMMA + column_name) + Suppress(")") + SEMICOLON)
insert_command = (INSERT_INTO + table_name + Suppress("(") + data + Suppress(")") + SEMICOLON)
select_all_command = ("SELECT * FROM" + table_name + SEMICOLON)
select_with_where_command = ("SELECT FROM" + table_name + Suppress('WHERE') + condition + SEMICOLON)
exit_command = (EXIT + SEMICOLON)


command = create_command | insert_command | select_all_command | select_with_where_command | exit_command

def parse(a: str) -> list:
    res = command.parseString(a)
    return res.asList()