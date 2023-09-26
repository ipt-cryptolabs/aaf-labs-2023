#include "invertedIndex.hpp"

int main() {

    std::vector<int> vec = { 11, 11, 11 };

    InvertedIndex ii;
    ii.create("first colletion");
    ii.insert("first colletion", vec);
    ii.print_index();

    ii.create("MyCollectionName");
    ii.parse("INSERT MyCollectionName { 22, 22, 22 };");
    ii.print_index();

    // ii.parse("INSERT MyCollectionName {1488, 228, 666, 999};");

    
    // /n, /t
    // std::string t1 = "INSERT MyCollectionName {1488, 228, 666, 999};";
    // std::string t2 = "    Insert      Another_Collection   {   111,  231, 4522    }  ;";
    // std::string t3 = "INSERT MissingSemicolon {1023, 14};";
    // std::string t4 = "INSERT 123InvalidName {31209837, 2};";
    // std::string t5 = "inSeRt CaseSensitiveName {1, 24};";
    // std::string t6 = "INSERT SpecialCollection {124, 24, 12874};";
    // std::string t7 = "INSERT SingleValueCollection {1110101};";




    // Parser pars;
    // pars.lexer(t1);
    // pars.lexer(t2);
    // pars.lexer(t3);
    // pars.lexer(t4);
    // pars.lexer(t5);
    // pars.lexer(t6);
    // pars.lexer(t7);



    return 0;
}





