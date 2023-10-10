#include "parser.h"

TokenTypes checkToken(std::string const &str)
{
    if (str == "CREATE")
        return TokenTypes::CREATE_QUERY;
    if (str == "INSERT")
        return TokenTypes::INSERT_QUERY;
    if (str == "PRINT_INDEX")
        return TokenTypes::PRINT_INDEX_QUERY;
    if (str == "SEARCH")
        return TokenTypes::SEARCH_QUERY;
    if (str == "WHERE")
        return TokenTypes::WHERE_QUERY;

    return TokenTypes::STRING_ARG;
}

std::vector<Token> lexer(std::string const &raw_input)
{
    // TODO: REFACTOR
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
            if ((isspace(raw_input[i + 1]) && !isspace(raw_input[i])) || i == raw_input.size() - 1)
            {
                string word = raw_input.substr(word_start, i - word_start + 1);
                word_start = i + 1;
                token.type = checkToken(word);
                token.data = token.type == STRING_ARG ? word : "";
                tokens_vec.push_back(token);
            }
            else if (raw_input[i] == '"')
            {
                if (i == raw_input.size() - 1)
                    throw new exception();
                state = STR;
            }
        }
        else if (state == STR)
        {
            if (raw_input[i] == '"')
            {
                token.type = TokenTypes::STRING_ARG;
                token.data = raw_input.substr(word_start + 1, i - word_start);
                tokens_vec.push_back(token);
                state = WORD;
            }
        }
        else
        {
            // Обробка некоректних станів
        }
    }

    return tokens_vec;
}

std::string parse(const std::vector<Token> &token_vec)
{
    if (token_vec.size() < 2) return "MORE ARGUMENTS PLEASE";

    switch (token_vec[0].type)
    {
    case TokenTypes::CREATE_QUERY:
        if (token_vec.size() == 2)
        {
            if (token_vec[1].type != STRING_ARG)
            {
                return "ERROR: CREATE ARG MUST BE STRING ARG";
            }
            create(token_vec[1].data);
            return "CREATE COMMAND PROCCESSE: " + token_vec[1].data + ".";
        }
        else
        {
            return "ERROR! CREATE MUST HAVE ONE ARGUMENT!";
        }
        break;
    case TokenTypes::INSERT_QUERY:
        if (token_vec.size() == 3)
        {
            if (token_vec[1].type != STRING_ARG || token_vec[2].type != STRING_ARG)
            {
                return "ERROR: INSERT ARGS MUST BE STRING ARG";
            }
            insert(token_vec[1].data, token_vec[2].data);
            return "INSERT COMMAND PROCCESSED WITH ARGS: " + token_vec[1].data + " " + token_vec[2].data + ".";
        }
        else
        {
            return "ERROR! INSERT MUST HAVE TWO ARGUMENTS!";
        }
        break;
    case TokenTypes::PRINT_INDEX_QUERY:
        if (token_vec.size() == 2)
        {
            if (token_vec[1].type != STRING_ARG)
            {
                return "ERROR: PRINT_INDEX ARG MUST BE STRING ARG";
            }
            print_index(token_vec[1].data);
            return "PRINT_INDEX COMMAND PROCCESS: " + token_vec[1].data + ".";
        }
        else
        {
            return "ERROR! PRINT_INDEX MUST HAVE ONE ARGUMENT!";
        }
        break;
    case TokenTypes::SEARCH_QUERY:
        if (token_vec.size() == 3)
        {
            if (token_vec[1].type != STRING_ARG || token_vec[2].type != STRING_ARG)
            {
                return "ERROR: SEARCH ARGS MUST BE STRING ARG";
            }
            search(token_vec[1].data, token_vec[2].data);
            return "SEARCH COMMAND PROCCESSED WITH ARGS: " + token_vec[1].data + " " + token_vec[2].data + ".";
        }
        else
        {
            return "ERROR! SEARCH MUST HAVE TWO ARGUMENTS!";
        }
        break;
    default:
        return "INVALID INPUT";
    }

}

void create(std::string collection_name)
{
}

void insert(std::string collection_name, std::string arg)
{
}

void search(std::string collection_name, std::string arg)
{
}

void print_index(std::string collection_name)
{
}

void where()
{
}