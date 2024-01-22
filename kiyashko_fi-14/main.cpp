#include <iostream>
#include <string>
#include <vector>
#include <fstream>
using namespace std;

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

kd_tree::kd_tree()
{
	root = NULL;
}

kd_tree::~kd_tree()
{
	delete_tree(root);
}

void kd_tree::delete_tree(Node *current)
{
    if (current != NULL){
        delete_tree(current->left);
        delete_tree(current->right);
        delete current;
    }
}

void kd_tree::insert(int l, int h)
{
    if (root!=NULL){
        Node *current = NULL;
        Node *next = root;
        bool a_comparison = 0;
        bool coordinate_bigger;
        while (next!=NULL){
            current = next;
            a_comparison = !(a_comparison);
            coordinate_bigger = 0;
            if (a_comparison){
                if ((current->a)<l)
                    coordinate_bigger = 1;
            } else {
                if ((current->b)<h)
                    coordinate_bigger = 1;
            }
            if (coordinate_bigger)
                next = current->right;
            else
                next = current->left;
        }
        next = new Node;
        next->left = NULL;
        next->right = NULL;
        next->a = l;
        next->b = h;
        if (coordinate_bigger)
            current->right = next;
        else
            current->left = next;
    }
    else {
        root = new Node;
        root->left = NULL;
        root->right = NULL;
        root->a = l;
        root->b = h;
    }
}

bool kd_tree::contains(int l, int h)
{
    bool in_tree = 0;
    if (root!=NULL){
        Node *current = NULL;
        Node *next = root;
        bool a_comparison = 0;
        bool coordinate_bigger;
        while (next!=NULL){
            current = next;
            if ((current->a == l)&&(current->b == h)){
                in_tree = 1;
                break;
            }
            a_comparison = !(a_comparison);
            coordinate_bigger = 0;
            if (a_comparison){
                if ((current->a)<l)
                    coordinate_bigger = 1;
            } else {
                if ((current->b)<h)
                    coordinate_bigger = 1;
            }
            if (coordinate_bigger)
                next = current->right;
            else
                next = current->left;
        }

    }
    return in_tree;
}

void kd_tree::print_tree()
{
    print_leaf(root, "", "");
}

void kd_tree::print_leaf(Node *current, string prefix, string childprefix)
{
    if (current!=NULL){
        cout<<prefix<<"["<<current->a<<", "<<current->b<<"]\n";
        Node *left = current->left;
        if (left==NULL){
            print_leaf(current->right, childprefix+"'---", childprefix + "    ");
        }
        else{
            print_leaf(current->right, childprefix+">---", childprefix + "|   ");
            print_leaf(current->left , childprefix+"'---", childprefix + "    ");
        }
    }
}

void kd_tree::search(string type, int l, int h)
{
    if (type == "EOF")
        all(root);
    else if (type == "RIGHT_OF")
        right_of(root, l, 1);
    else if (type == "CONTAINED_BY")
        cointained_by(root, l, h, 1);
    else if (type == "INTERSECTS")
        intersects(root, l, h, 1);
}

void kd_tree::all(Node *current)
{
    if (current!=NULL){
        all(current->left);
        all(current->right);
        cout<<"["<<current->a<<", "<<current->b<<"] ";
    }
}

void kd_tree::cointained_by(Node *current, int l, int h, bool a_comparison)
{
    if (current!=NULL){
        int a = current->a;
        int b = current->b;
        if (a_comparison){
            if (a<=h) cointained_by(current->right, l, h, !(a_comparison));
            if (a>=l) cointained_by(current->left, l, h, !(a_comparison));
        } else {
            if (b<=h) cointained_by(current->right, l, h, !(a_comparison));
            if (b>=l) cointained_by(current->left, l, h, !(a_comparison));
        }
        if ((l<=a)&&(b<=h)) cout<<"["<<a<<", "<<b<<"] ";
    }
}

void kd_tree::intersects(Node *current, int l, int h, bool a_comparison)
{
    if (current!=NULL){
        int a = current->a;
        int b = current->b;
        if (a_comparison){
            intersects(current->left, l, h, !(a_comparison));
            if (a<=h) intersects(current->right, l, h, !(a_comparison));
        } else {
            intersects(current->right, l, h, !(a_comparison));
            if (l<=b) intersects(current->left, l, h, !(a_comparison));
        }
        if (!((b<l)||(a>h))) cout<<"["<<a<<", "<<b<<"] ";
    }
}

void kd_tree::right_of(Node *current, int l, bool a_comparison)
{
    if (current!=NULL){
        int a = current->a;
        int b = current->b;
        if (a_comparison){
            right_of(current->right, l, !(a_comparison));
            if (l<=a){
                right_of(current->left, l, !(a_comparison));
                cout<<"["<<a<<", "<<b<<"] ";
            }
        } else {
            right_of(current->right, l, !(a_comparison));
            if (l<=b){
                right_of(current->left, l, !(a_comparison));
                if (l<=a) cout<<"["<<a<<", "<<b<<"] ";
            }
        }
    }
}


const string key_words[10] ={"CREATE", "INSERT", "PRINT_TREE","CONTAINS", "SEARCH", "WHERE","CONTAINED_BY", "INTERSECTS", "RIGHT_OF","END"};

class Token
{
public:
    Token(string type,string value);
    Token();
    string type;
    string value;
    void show();
};

Token::Token(string type, string value)
{
	this->type=type;
	this->value=value;
}

void Token::show()
{
    cout<<"Token("<<type<<","<<value<<")\n";
}

Token::Token()
{

}

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


void Interpreter::get_command(string text)
{
	this->text = text;
	len_text = text.length();
	pos = 0;
	current_char=text[pos];
	is_closed=0;
}

void Interpreter::advance()
{
    pos++;
    if (pos>len_text-1)
        current_char = 0;
    else
        current_char = text[pos];
}

void Interpreter::skip()
{
    while ((current_char!=0) && (isspace(current_char)!=0))
        advance();
}

bool Interpreter::closed()
{
    return is_closed;
}

string Interpreter::integer()
{
    string result = "";
    bool has_minus = 0;
    if (current_char=='-')
    {
        has_minus = 1;
        result += '-';
        advance();
    }
    while ((current_char!=0) && isdigit(current_char))
    {
        result += current_char;
        advance();
    }
    if ((result != "0")&&(result[has_minus]=='0'))
        throw std::runtime_error(result + " є 0 перед числом");

    return result;
}

bool Interpreter::first_smaller_second(string int1, string int2)
{
    bool is_correct = 1;
    if (int1[0] == '-')
    {
        if (int2[0] == '-')
        {
            if (int1.length() < int2.length())
                is_correct = 0;
            else
            if ((int1.length() == int2.length())&&(int1 < int2))
                is_correct = 0;
        }
    }
    else
    {
        if (int2[0] == '-')
            is_correct = 0;
        else
        {
            if (int1.length() > int2.length())
                is_correct = 0;
            else
            if ((int1.length() == int2.length())&&(int1 > int2))
                is_correct = 0;
        }
    }

    return is_correct;
}

string Interpreter::word()
{
    string result = "";
    while ((current_char!=0) && ((isalpha(current_char))||(current_char=='_')||isdigit(current_char)))
    {
        result += current_char;
        advance();
    }

    return result;
}

Token Interpreter::get_next_token()
{
    while (current_char!=0)
    {
        if (isspace(current_char)!=0)
            skip();
        else
        if (isalpha(current_char)){
            string w = word();
            string w_up = "";
            int len = w.length();
            if (len<=12)
            {
                for(int i=0; i<len; ++i)
                    w_up += toupper(w[i]);
                for(int i=0; i<10; ++i)
                    if(w_up == key_words[i])
                        return Token(w_up, w);
            }
            return Token("NAME", w);
        }
        else
        if ((isdigit(current_char))||(current_char == '-'))
            return Token("INTEGER", integer());
        else
        if (current_char == '['){
            advance();
            return Token("OPEN_BRACK", "[");
        }
        else
        if (current_char == ','){
            advance();
            return Token("COMMA", ",");
        }
        else
        if (current_char == ']'){
            advance();
            return Token("CLOSE_BRACK", "]");
        }
        else throw std::runtime_error("символ '" + string(1, current_char) + "' не підтримується");
    }
    return Token("EOF", "NULL");
}

void Interpreter::eat(string type)
{
    if (current_token.type == type)
        current_token = get_next_token();
    else
        throw std::runtime_error("потрібно '" + type +"', а ми отримали '"+current_token.type+"'");
}

void Interpreter::eat_name()
{
    if (current_token.type == "NAME")
    {
        bool flag = 0;
        name = current_token.value;
        for(vector <int>::size_type i=0; i<names.size(); ++i)
            if (names[i] == name)
            {
                flag = 1;
                break;
            }
        if (flag==0)
            throw std::runtime_error(name + " не існує");
    }
    else throw std::runtime_error("потрібно 'NAME', а ми отримали '"+current_token.type+"'");
    current_token = get_next_token();
}

void Interpreter::expr()
{
	current_token = get_next_token();

    if (current_token.type == "END"){
        is_closed = 1;
    }
    else
	if (current_token.type == "CREATE"){
        current_token = get_next_token();
        if (current_token.type == "NAME")
            name = current_token.value;
        else throw std::runtime_error("потрібно 'NAME', а ми отримали '"+current_token.type+"'");
        current_token = get_next_token();
        eat("EOF");

        for(vector<int>::size_type i=0; i<names.size(); ++i)
            if (names[i] == name)
                throw std::runtime_error(name + "' вже існує");
        if (names.size()<=10000){
            names.push_back(name);
            cout<< name + "' створено\n";
        }
        else
            throw std::runtime_error("sets занадто багато");
    }
    else
    if (current_token.type == "PRINT_TREE"){
        current_token = get_next_token();
        eat_name();
        eat("EOF");
        vector<int>::size_type index = 0;
        bool is_exist = 0;
        for(vector<int>::size_type i=0; i<names.size(); ++i)
            if (names[i] == name){
                index = i;
                is_exist = 1;
                break;
            }
        if (is_exist){
            cout<<'\n';
            kd_trees[index].print_tree();
        }
    }
    else
    if (current_token.type == "INSERT"){
        current_token = get_next_token();
        eat_name();
        eat("OPEN_BRACK");
        string int1 = current_token.value;
        eat("INTEGER");
        eat("COMMA");
        string int2 = current_token.value;
        eat("INTEGER");
        eat("CLOSE_BRACK");
        eat("EOF");
        if (first_smaller_second(int1, int2) == 0) throw std::runtime_error(int1 + " > " + int2);
        vector<int>::size_type index = 0;
        bool is_exist = 0;
        for(vector<int>::size_type i=0; i<names.size(); ++i)
            if (names[i] == name){
                index = i;
                is_exist = 1;
                break;
            }
        if (is_exist)
            kd_trees[index].insert(stoi(int1), stoi(int2));
        cout<<"  Відстань [" + int1 + ", " + int2 + "] Додана до '" + name + "'\n";
    }
    else
    if (current_token.type == "CONTAINS"){
        current_token = get_next_token();
        eat_name();
        eat("OPEN_BRACK");
        string int1 = current_token.value;
        eat("INTEGER");
        eat("COMMA");
        string int2 = current_token.value;
        eat("INTEGER");
        eat("CLOSE_BRACK");
        eat("EOF");
        if (first_smaller_second(int1, int2) == 0) throw std::runtime_error(int1 + " > " + int2);
        vector<int>::size_type index = 0;
        bool is_exist = 0;
        for(vector<int>::size_type i=0; i<names.size(); ++i)
            if (names[i] == name){
                index = i;
                is_exist = 1;
                break;
            }
        if (is_exist){
            bool in_tree = kd_trees[index].contains(stoi(int1), stoi(int2));
            if (in_tree)
                cout<<"TRUE\n";
            else
                cout<<"FALSE\n";
        }
    }
    else
    if (current_token.type == "SEARCH"){
        current_token = get_next_token();
        eat_name();
        if (current_token.type == "WHERE")
        {
            current_token = get_next_token();
            if (current_token.type == "RIGHT_OF")
            {
                current_token = get_next_token();
                string int1 = current_token.value;
                eat("INTEGER");
                eat("EOF");
                vector<int>::size_type index = 0;
                bool is_exist = 0;
                for(vector<int>::size_type i=0; i<names.size(); ++i)
                    if (names[i] == name){
                        index = i;
                        is_exist = 1;
                        break;
                    }
                if (is_exist)
                    kd_trees[index].search("RIGHT_OF", stoi(int1), 0);
                cout<<"\n";
            }

            else
            if (current_token.type == "CONTAINED_BY")
            {
                current_token = get_next_token();
                eat("OPEN_BRACK");
                string int1 = current_token.value;
                eat("INTEGER");
                eat("COMMA");
                string int2 = current_token.value;
                eat("INTEGER");
                eat("CLOSE_BRACK");
                eat("EOF");
                if (first_smaller_second(int1, int2) == 0) throw std::runtime_error(int1 + " > " + int2);
                vector<int>::size_type index = 0;
                bool is_exist = 0;
                for(vector<int>::size_type i=0; i<names.size(); ++i)
                    if (names[i] == name){
                        index = i;
                        is_exist = 1;
                        break;
                    }
                if (is_exist)
                    kd_trees[index].search("CONTAINED_BY", stoi(int1), stoi(int2));
                cout<<"\n";
            }
            else
            if (current_token.type == "INTERSECTS")
            {
                current_token = get_next_token();
                eat("OPEN_BRACK");
                string int1 = current_token.value;
                eat("INTEGER");
                eat("COMMA");
                string int2 = current_token.value;
                eat("INTEGER");
                eat("CLOSE_BRACK");
                eat("EOF");
                if (first_smaller_second(int1, int2) == 0) throw std::runtime_error(int1 + " > " + int2);
                if (first_smaller_second(int1, int2) == 0) throw std::runtime_error(int1 + " > " + int2);
                vector<int>::size_type index = 0;
                bool is_exist = 0;
                for(vector<int>::size_type i=0; i<names.size(); ++i)
                    if (names[i] == name){
                        index = i;
                        is_exist = 1;
                        break;
                    }
                if (is_exist)
                    kd_trees[index].search("INTERSECTS", stoi(int1), stoi(int2));
                cout<<"\n";
            }
            else
                throw std::runtime_error("потрібно 'RIGHT_OF'/'CONTAINED_BY'/'INTERSECTS', отримали '"+current_token.type+"'");
        }
        else
        if (current_token.type == "EOF")
        {
            vector<int>::size_type index = 0;
            bool is_exist = 0;
            for(vector<int>::size_type i=0; i<names.size(); ++i)
                if (names[i] == name){
                    index = i;
                    is_exist = 1;
                    break;
                }
            if (is_exist)
                kd_trees[index].search("EOF", 0, 0);
            cout<<"\n";
        }
        else
            throw std::runtime_error("потрібно 'EOF'/'WHERE', отримали '"+current_token.type+"'");

    }
    else
        throw std::runtime_error("потрібно 'CREATE'/'INSERT'/'PRINT_TREE'/'CONTAINS'/'SEARCH', отримали '"+current_token.type+"'");
}


// Приклад тексту:
//CREATE reservations;
//INSERT reservations [10, 20];
//PRINT_TREE reservations;
//CONTAINS reservations [10, 20];
//SEARCH reservations;
//SEARCH reservations WHERE CONTAINED_BY [0, 30];
//SEARCH reservations WHERE INTERSECTS [5, 20];
//SEARCH reservations WHERE RIGHT_OF 15;


int main()
{
     cout<<"Пишіть текст\n";
    bool is_closed = 0;
    Interpreter inter;
    while (is_closed == 0)
        try
        {
            string text="";
            string line="";
            cout<<">>>";
            while (line.find(';')>=line.length()){
                text += (" " + line);
                getline(cin, line);
                //getline(infile, line);
            }

            text += (" " +line.substr(0,line.find(';')));
            
            inter.get_command(text);
            inter.expr();
            is_closed = inter.closed();
        }
        catch(const std::exception& e)
        {
            std::cerr << "  Error: " << e.what()<< '\n';
        }
}