#ifndef HEADERFILE_H
#define HEADERFILE_H
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
using namespace std;

void flow();

class Node
{
public:
	int a,b;
	Node *left, *right;
};

class kd_tree{
public:
	kd_tree();
	~kd_tree();
	void print_leaf(Node *current, string prefix, string childrenprefix);
	void insert(int l, int h);
	bool contains(int l, int h);
	void print_tree();
	void search(string type, int l, int h);

private:
    void all(Node *current);
	void cointained_by(Node *current, int l, int h, bool a_comparison);
	void intersects(Node *current, int l, int h, bool a_comparison);
	void right_of(Node *current, int l, bool a_comparison);
    void delete_tree(Node *current);
	Node *root;
};

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
    kd_tree kd_trees [10000];

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

