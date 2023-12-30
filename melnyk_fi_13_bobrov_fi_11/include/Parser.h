#pragma once

#include <string>
#include <cctype>
#include <regex>
#include <iostream>
#include "Types.h"

bool is_digit(char c);
bool is_space(char c);
bool is_alpha(char c);

std::string upper(const std::string& input);
bool matches_regex(const std::string& input);

// To trow exceptions
class MyException : public std::runtime_error 
{
public:
    MyException(const std::string& message) : std::runtime_error(message) { }
};

struct Token
{    
    Token() : type(""), value("") { }
    Token(const std::string& type, const std::string& value) : type(type), value(value) { }

    std::string type;
    std::string value;
};

class Lexer
{
public:
    Lexer() : text(""), pos(0), current_char(0) { }
    Lexer(const std::string& text) : text(text), pos(0), current_char(text[0]) { }

    // Advancing current position
    void advance();

    // Skipping whitespaces
    void skip_whitespace();

    // Getting string from input (all characters until space)
    std::string get_string();

    // Getting string of all characters within the quotes   
    std::string get_full_string();

    // Getting next token (might raise an error)
    Token get_next_token();

private:
    std::string text;
    int pos;
    char current_char;
};


class Interpreter
{
    // Chacking correspodance of current token type and expected type. If types are equal, gets new token. Otherwise
    // raises an exception.
    void eat(std::string expected_type);

    // calling type 1 functions: create and print_tree
    void type1();
    
    // calling type 2 functions: insert and contains
    void type2();
    
    // calling type 3 function: search
    void type3();
    
    // calling query, which can be "BETWEEN" or "MATCH"
    void query(std::string set_name);



public:
    Interpreter() = default;
    Interpreter(Lexer lexer);

    // Start of the programm
    void command();

private:
    Lexer lexer;
    Token current_token;
};