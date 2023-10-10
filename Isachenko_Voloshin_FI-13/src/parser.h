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
};

struct Token
{
    TokenTypes type;
    std::string data;
};

TokenTypes checkToken(std::string const& str);
std::string parse (const std::vector<Token> &token_vec);
std::vector<Token> lexer (const std::string& raw_input);

void create(std::string collection_name);
void insert(std::string collection_name, std::string arg);
void search(std::string collection_name, std::string arg);
void print_index(std::string collection_name);
void where();

#endif //AAF_LABS_2023_PARSER_H
