#include <iostream>
#include <string>

#include "parser.h"
#include "invindexdb.h"

const char* const HELPSTR = "Laboratory work. 8 variant.\n"
"Implementation of a collection of text documents with the possibility of full - text search using inverted indexes.\n"
"\n"
"Authors:\n"
"FI-13 Igor Voloshin\n"
"FI-13 Isachenko Nikita\n"
"\n"
"Commands :\n"
" - Semicolon means end of the line. If only one line, semicolon can be dropped.\n"
" - Commands and words out of \"\" are case insensitive.\n"
"\n"
"CREATE [table name];\n"
"INSERT [table name] \"[TEXT]\";\n"
"PRINT_INDEX [table_name];\n"
"SEARCH [table_name] WHERE [WHERE_EXPRESSION];\n"
"! - for exit\n"
"HELP - for the string to appear\n";

void cli();
std::ostream& operator<< (std::ostream& out, const QueryResult& qRes);

int main ()
{
    cli();
    return 0;
}

void cli()
{
    using namespace std;
    string input;
    QueryBuilder qb;
    InvIndDB db;

    cout << HELPSTR << endl;

    while (true)
    {
        cout << "-> ";

        getline(cin, input);
        
        if (input == "!")
        {
            break;
        }
        if (input.size() == 4 && toLowerStr(input) == "help")
        {
            cout << HELPSTR << endl;
            continue;
        }
        if (!input.empty() && input.back() != ';')
        {
            input += ';';
        }

        Query* query = qb.getQueryFromString(input);

        if (query == nullptr)
        {
            cout << "Build Querry Error!" << endl;
            continue;
        }

        QueryResult qRes = query->execute(db);

        cout << qRes << endl;
    }
}

std::ostream& operator<<(std::ostream& out, const QueryResult& qRes)
{
    out << qRes.queryType << " query:  " << qRes.message;
    return out;
}
