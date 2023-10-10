#include <iostream>
#include <string>
#include "parser.h"

int main ()
{
    using namespace std;

    vector<Token> tokensvec ;
    string input;

    while (true)
    {
        cout << "->";
        getline(cin, input);
        if (input == "EXIT")
        {
            return 0;
        }
        tokensvec = lexer(input);

        cout << parse(tokensvec) << endl;

        cout << endl;
    }
}
