#ifndef AAF_LABS_2023_PARSER_H
#define AAF_LABS_2023_PARSER_H
#include <vector>
#include <string>
#include <sstream>

enum TokenTypes
{
    CREATE_QUERY,
    INSERT_QUERY,
    PRINT_INDEX_QUERY,
    SEARCH_QUERY,
    WHERE_QUERY,
    STRING_ARG,
    ERROR,
    EXIT,
};

struct Token
{
    TokenTypes type;
    std::string data;
};

TokenTypes checkToken(std::string const& str);


void parse (Token *tokens, int size);
std::vector<Token> lexer (std::string const& raw_input, Token *tokens, int& size);


#endif //AAF_LABS_2023_PARSER_H
