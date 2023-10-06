#include "parser.h"

void parse (Token *tokens, int size)
{

}
std::vector<Token> lexer (std::string const& raw_input, Token *tokens, int& size)
{
    //TODO: REFACTOR
    using namespace std;

    const char WORD = 0;
    const char STR = 1;
    const char EXPR = 3;

    int word_start = 0;
    vector<Token> tokens_vec;
    char state = WORD;
    Token token;

    for (int i = 0; i < raw_input.size(); i++)
    {
        if (state == WORD)
        {
            if (isspace(raw_input[i]) && !isspace(raw_input[i - 1]))
            {
                string word = raw_input.substr(word_start, i - word_start);
                word_start = i + 1;
                token.type = checkToken(word);
                token.data = token.type != STRING_ARG ? word : "";
                tokens_vec.push_back(token);
                if (token.type == TokenTypes::WHERE_QUERY)
                {
                    state = EXPR;
                }
            }
            else if (raw_input[i] == '"')
            {
                if (i == raw_input.size() - 1) throw new exception();
                state = STR;
            }
        }
        else if (state == STR)
        {
            if (raw_input[i] == '"')
            {
                token.type = TokenTypes::STRING_ARG;
                token.data = raw_input.substr(word_start, i - word_start);
                tokens_vec.push_back(token);
                state = WORD;
            }
        }
        else if (state == EXPR)
        {
            // TODO
            break;
        }
        else
        {
            // Обробка некоректних станів
        }
    }

    return tokens_vec;

}

TokenTypes checkToken(std::string const& str)
{
    if (str == "CREATE") return TokenTypes::CREATE_QUERY;
    if (str == "INSERT") return TokenTypes::INSERT_QUERY;
    if (str == "PRINT_INDEX") return TokenTypes::PRINT_INDEX_QUERY;
    if (str == "SEARCH") return TokenTypes::SEARCH_QUERY;
    if (str == "WHERE") return TokenTypes::WHERE_QUERY;

    return TokenTypes::STRING_ARG;
}

