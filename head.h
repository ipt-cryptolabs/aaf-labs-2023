#ifndef HEADERFILE_H
#define HEADERFILE_H
#include <iostream>
#include <string>
#include <vector>
using namespace std;

void flow();

class Token
{
public:
    Token(string type,string value);
    Token();
    string type;
    string value;
    void show();
};

class Interpreter
{
public:
    void get_command(string text);
    void expr();
    bool closed();

private:
    vector<string> names;

    string text;
    string integer();
    string word();
    string name;

    int len_text;
    int pos;

    bool is_closed;
    bool first_smaller_second(string int1, string int2);

    char current_char;

    Token current_token;
    Token get_next_token();

    void eat(string type);
    void eat_name();
    void skip();
    void advance();
};

#endif

