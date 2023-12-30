#include "../include/Parser.h"
#include "../include/CommandProcessor.h"

// returns "true" if char c is digit and "false" otherwise
bool is_digit(char c)
{
    return (int(c) >= 48 || int(c) <= 57);
}

// returns "true" if char c is a space character and "false" otherwise
bool is_space(char c)
{
    return (int(c) == 32 || c == '\n' || c == '\t' || c == '\r');
}

// returns "true" if char c is an alphabet character and "false" otherwise
bool is_alpha(char c)
{
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

// casting uppercase to the given string
std::string upper(const std::string& input)
{
    std::string result = input;
    for (char& c : result) 
        c = std::toupper(c);

    return result;
}

// Returns "true" if string matches regular expression and "false" otherwise. (Obviously, I was lazy)
bool matches_regex(const std::string& input) 
{
    std::regex pattern("[a-zA-Z][a-zA-Z0-9_]*");
    return std::regex_match(input, pattern);
}

void Lexer::advance()
{
    ++pos;
    if(pos <= text.length() - 1)
        current_char = text[pos];
    else 
        current_char = '\0';
}

void Lexer::skip_whitespace()
{
    while(is_space(current_char)) 
    {
        advance();
    }
}

std::string Lexer::get_string()
{
    std::string result = "";
    while(current_char && !is_space(current_char) && current_char != ';') 
    {
        result += current_char;
        advance();
    }

    if(matches_regex(result))
        return result;
    else
        throw MyException("Invalid characters within the input string");
}

std::string Lexer::get_full_string()
{
    std::string result = "";
    while(current_char && current_char != '"') 
    {
        result += current_char;
        advance();
    }

    return result;
}

Token Lexer::get_next_token() 
{
    while(int(current_char) != 0) 
    {
        skip_whitespace();
        if(is_alpha(current_char) || current_char == '?' || current_char == '*') 
        {
            std::string input = get_string();
            std::string upper_input = upper(input);

            // probably can be optimized
            if(upper_input == Tokens::CREATE || upper_input == Tokens::INSERT 
            || upper_input == Tokens::PRINT_TREE || upper_input == Tokens::CONTAINS 
            || upper_input == Tokens::SEARCH || upper_input == Tokens::ASC || upper_input == Tokens::DESC
            || upper_input == Tokens::WHERE || upper_input == Tokens::BETWEEN || upper_input == Tokens::MATCH) {
                return Token(upper_input, upper_input);
            }
            else return Token(Tokens::STRING, input);
        }
        else if(current_char == ',') {
            advance();
            return Token(Tokens::COMMA, "COMMA");
        }
        else if(current_char == '"') {
            advance();
            std::string result = get_full_string();
            advance();
            return Token(Tokens::FULL_STRING, result);
        }
        else if(current_char == ';') {
            advance();
            return Token(Tokens::SEMICOLON, ";");
        }
        else throw MyException("Invalid character: " + std::string(1, current_char));
    } 
    return Token(Tokens::eof, "");
}

Interpreter::Interpreter(Lexer lexer) : lexer(lexer)
{
    current_token = this->lexer.get_next_token();
}

void Interpreter::command()
{
    if(current_token.type == Tokens::CREATE || current_token.type == Tokens::PRINT_TREE) 
    {
        type1();
    }
    else if(current_token.type == Tokens::CONTAINS || current_token.type == Tokens::INSERT)
    {
        type2();   
    }
    else if(current_token.type == Tokens::SEARCH) 
    {
        type3();
    }
    else 
        throw MyException("Syntax error: unknown command: " + current_token.value);

    eat(Tokens::SEMICOLON); // Every input should contain ";" in the end. After that none of the symbols are read.
}

void Interpreter::query(std::string set_name)
{
    if(current_token.type == Tokens::BETWEEN)
    {
        eat(Tokens::BETWEEN);
        std::string from = current_token.value;

        eat(Tokens::FULL_STRING);
        eat(Tokens::COMMA);

        std::string to = current_token.value;
        eat(Tokens::FULL_STRING);

        std::string order = Tokens::ASC;
        if(current_token.type == Tokens::ASC) 
        {
            eat(Tokens::ASC);
        }
        else if(current_token.type == Tokens::DESC)
        {
            eat(Tokens::DESC);
            order = Tokens::DESC;
        }
        else if(current_token.type == Tokens::SEMICOLON) 
        {
            order = Tokens::ASC;
        }
        else 
        {
            throw MyException("Syntax error! Invalid token. Expected: ASC or DESC. Got: " + current_token.type);
        }

        CommandProcessor::get()->between(set_name, from, to, order);
    }
    else if(current_token.type == Tokens::MATCH) 
    {
        eat(Tokens::MATCH);

        std::string pattern = current_token.value;
        eat(Tokens::FULL_STRING);

        std::string order = Tokens::ASC;
        if(current_token.type == Tokens::ASC) 
        {
            eat(Tokens::ASC);
        }
        else if(current_token.type == Tokens::DESC)
        {
            eat(Tokens::DESC);
            order = Tokens::DESC;
        }
        else if(current_token.type == Tokens::SEMICOLON) 
        {
            order = Tokens::ASC;
        }
        else
        {
            throw MyException("Syntax error! Invalid token. Expected: ASC or DESC. Got: " + current_token.type);
        }

        CommandProcessor::get()->match(set_name, pattern, order);
    }
    else 
        throw MyException("Syntax error! Expected: MATCH or BETWEEN. Got: " + current_token.type);
}

void Interpreter::type3()
{
    eat(Tokens::SEARCH);

    std::string set_name = current_token.value;
    if(current_token.type == Tokens::STRING) 
        eat(Tokens::STRING);
    else if(current_token.type == Tokens::FULL_STRING)
        eat(Tokens::FULL_STRING);
    else 
        throw MyException("Syntax error! Expected STRING or FULL_STING token type. Got: " + current_token.type);

    if(current_token.type == Tokens::WHERE) 
    {
        eat(Tokens::WHERE);
        query(set_name);
    }
    else if(current_token.type == Tokens::ASC || current_token.type == Tokens::DESC || current_token.type == Tokens::SEMICOLON) 
    {
        if(current_token.type == Tokens::SEMICOLON) 
        {
            CommandProcessor::get()->search(set_name, Tokens::ASC);
        }
        else if(current_token.type == Tokens::ASC) 
        {
            eat(Tokens::ASC);
            CommandProcessor::get()->search(set_name, Tokens::ASC);
        }
        else if(current_token.type == Tokens::DESC)
        {
            eat(Tokens::DESC);
            CommandProcessor::get()->search(set_name, Tokens::DESC);
        }
    }
    else
        throw MyException("Syntax error! Invalid token. Expected: ASC or DESC or oef Got: " + current_token.type);
}

void Interpreter::type2()
{
    if(current_token.type == Tokens::INSERT) 
    {
        eat(Tokens::INSERT);

        std::string set_name = current_token.value;
        if(current_token.type == Tokens::STRING)
            eat(Tokens::STRING);
        else if(current_token.type == Tokens::FULL_STRING) 
            eat(Tokens::FULL_STRING);
        else 
            throw MyException("Syntax error! Expected STRING or FULL_STING token type. Got: " + current_token.type);
    
        std::string value = current_token.value;
        eat(Tokens::FULL_STRING);

        CommandProcessor::get()->insert(set_name, value);
    }
    else if(current_token.type == Tokens::CONTAINS) 
    {
        eat(Tokens::CONTAINS);

        std::string set_name = current_token.value;
        if(current_token.type == Tokens::STRING) 
            eat(Tokens::STRING);
        else if(current_token.type == Tokens::FULL_STRING)
            eat(Tokens::FULL_STRING);
        else
            throw MyException("Syntax error! Expected STRING or FULL_STING token type. Got: " + current_token.type);

        std::string value = current_token.value;
        eat(Tokens::FULL_STRING);
        
        CommandProcessor::get()->contains(set_name, value);
    }
}

void Interpreter::type1()
{
    if(current_token.type == Tokens::CREATE) 
    {
        eat(Tokens::CREATE);

        Token token = current_token;
        if(current_token.type == Tokens::STRING) 
            eat(Tokens::STRING);
        else if(current_token.type == Tokens::FULL_STRING)
            eat(Tokens::FULL_STRING);
        else 
            throw MyException("Syntax error! Expected STRING or FULL_STING token type. Got: " + current_token.type);

       CommandProcessor::get()->create(token.value);
    }
    else if(current_token.type == Tokens::PRINT_TREE) 
    {
        eat(Tokens::PRINT_TREE);

        Token token = current_token;
        if(current_token.type == Tokens::STRING) 
            eat(Tokens::STRING);
        else if(current_token.type == Tokens::FULL_STRING) 
            eat(Tokens::FULL_STRING);
        else
            throw MyException("Syntax error! Expected STRING or FULL_STING token type. Got: " + current_token.type);

        CommandProcessor::get()->print_tree(token.value);
    }
}

void Interpreter::eat(std::string expected_type)
{
    if(current_token.type == expected_type) 
        current_token = lexer.get_next_token();
    else
        throw MyException("Syntax error. Ivanlid token type. Expected: " + expected_type + " Got: " + current_token.type);
}