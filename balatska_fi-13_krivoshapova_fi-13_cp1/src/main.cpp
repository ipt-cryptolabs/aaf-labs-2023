#include "functions.h"
#include "parser.h"
#include <iostream>
#include <sstream>
#include <string>

int main() {
    std::string input;
    SelectionResult result;
    std::vector<Command> collection;


    while (true) {
        std::cout << "Enter a command (or 'exit' to quit): ";
        std::getline(std::cin, input);

        if (input == "exit") {
            break;
        }

        Command command = parseCommand(input);

        switch (command.type) {
        case CREATE:
            createTable(command, collection);
            break;
        case INSERT:
            insertRecord(command, collection, result);
            break;
        case DELETE:
            deleteAllRecords();
            break;
        case SELECT:
            performSelect(command, collection, result);
            printSelectionResult(result);
            break;
        case UNKNOWN:
            std::cout << "Unknown command." << std::endl;
            break;
        }
    }

    return 0;


    /*
    ������� ����� ������:
    CREATE cats id name age food
    INSERT INTO cats 1 Snizhok 5 meat
    SELECT FROM cats
    SELECT FROM cats WHERE age > 5
    SELECT FROM cats OBDER_BY age DESC
    SELECT FROM cats ORDER_BY name ASC
    */

}
