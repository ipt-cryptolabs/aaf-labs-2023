#include "invertedIndex.hpp"

int main() {
    // /n, /t
    // std::string t1 = "INSERT MyCollectionName {1488, 228, 666, 999};";
    // std::string t2 = "    Insert      Another_Collection   {   111,  231, 4522    }  ;";
    // std::string t3 = "INSERT MissingSemicolon {1023, 14};";
    // std::string t4 = "INSERT 123InvalidName {31209837, 2};";
    // std::string t5 = "inSeRt CaseSensitiveName {1, 24};";
    // std::string t6 = "INSERT SpecialCollection {124, 24, 12874};";
    // std::string t7 = "INSERT SingleValueCollection {1110101};";




    // Collections collections;
    
    // collections.parse("CREATE MyCollectionName;");
    // collections.parse("CREATE collection1;");
    // collections.parse("INSERT MyCollectionName { 22, 22, 22 };");
    // collections.parse("INSERT MyCollectionName { 22, 22, 22 };");
    // collections.parse("INSERT MyCollectionName { 22, 22, 22 };");

    // collections.parse("PRINT_INDEX MyCollectionName");

    // collections.parse("INSERT MyCollectionName {1488, 228, 666, 999};");
    // collections.parse("PRINT_INDEX MyCollectionName;");
    // collections.parse("CONTAINS MyCollectionName {626, 82828, 123};");
    // collections.parse("SEARCH MyCollectionName {626, 82828, 123};");
    // collections.parse("PRINT_INDEX MyCollectionName;");

    Collections collections;

    std::cout << "Hey, it's inverted index structure\n";

    for(;;) {
        std::cout << "Enter a command or type 'q' to quit: ";
        std::string userInput;
        std::getline(std::cin, userInput);
        
        if(userInput == "q"){
            std::cout << "Exiting program...\n";
            break;
        }

        collections.parse(userInput);
    }

    return 0;
}