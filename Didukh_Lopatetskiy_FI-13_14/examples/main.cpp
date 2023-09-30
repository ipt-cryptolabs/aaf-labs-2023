#include <invertedIndex.hpp>

int main() {
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