#include <iostream>
#include <string>
#include "parser.h"

int main ()
{
    using namespace std;

    vector<Token> Tokensvec ;

    Token * tokens;

    int size=0;

    string input;

    while (true)
    {
        cout << "->";
        getline(cin, input);
        Tokensvec = lexer(input, tokens, size);

        for (int i = 0; i < Tokensvec.size(); i++)
        {
            cout << Tokensvec[i].type << ", ";
        }
        cout << endl;
    }
}
