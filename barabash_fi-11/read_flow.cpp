#include "head.h"

void flow()
{
    cout<<"Program for building a KD-tree using console. Version 2\nTo close the program use command END\n";
    bool is_closed = 0;
    //ifstream infile("input.txt");
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


const string key_words[10] ={"CREATE", "INSERT", "PRINT_TREE",
                            "CONTAINS", "SEARCH", "WHERE",
                            "CONTAINED_BY", "INTERSECTS", "RIGHT_OF",
                            "END"};

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
        throw std::runtime_error("integer '" + result + "' has zeros before number");

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
        else throw std::runtime_error("symbol '" + string(1, current_char) + "' doesn't support");
    }
    return Token("EOF", "NULL");
}

void Interpreter::eat(string type)
{
    if (current_token.type == type)
        current_token = get_next_token();
    else
        throw std::runtime_error("sequence expected '" + type +"', received '"+current_token.type+"'");
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
            throw std::runtime_error("set '" + name + "' doesn't exist");
    }
    else throw std::runtime_error("sequence expected 'NAME', received '"+current_token.type+"'");
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
        else throw std::runtime_error("sequence expected 'NAME', received '"+current_token.type+"'");
        current_token = get_next_token();
        eat("EOF");

        for(vector<int>::size_type i=0; i<names.size(); ++i)
            if (names[i] == name)
                throw std::runtime_error("set '" + name + "' have already existed");
        if (names.size()<=10000){
            names.push_back(name);
            cout<<"  Set '" + name + "' has created\n";
        }
        else
            throw std::runtime_error("are too many sets in program");
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
        if (first_smaller_second(int1, int2) == 0) throw std::runtime_error("range can't exist, because " + int1 + " > " + int2);
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
        cout<<"  Range [" + int1 + ", " + int2 + "] has added to '" + name + "'\n";
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
        if (first_smaller_second(int1, int2) == 0) throw std::runtime_error(" range can't exist, because " + int1 + " > " + int2);
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
                if (first_smaller_second(int1, int2) == 0) throw std::runtime_error(" range can't exist, because " + int1 + " > " + int2);
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
                if (first_smaller_second(int1, int2) == 0) throw std::runtime_error(" range can't exist, because " + int1 + " > " + int2);
                if (first_smaller_second(int1, int2) == 0) throw std::runtime_error("range can't exist, because " + int1 + " > " + int2);
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
                throw std::runtime_error("sequence expected 'RIGHT_OF'/'CONTAINED_BY'/'INTERSECTS', received '"+current_token.type+"'");
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
            throw std::runtime_error("sequence expected 'EOF'/'WHERE', received '"+current_token.type+"'");

    }
    else
        throw std::runtime_error("sequence expected 'CREATE'/'INSERT'/'PRINT_TREE'/'CONTAINS'/'SEARCH', received '"+current_token.type+"'");
}

