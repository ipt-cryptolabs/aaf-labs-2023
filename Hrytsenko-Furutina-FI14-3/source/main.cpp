#include <iostream>
#include <string>
#include "Functional.cpp"

int main() {

    Database db;
    std::string current_command = "";

    while (true) {
        std::string line;
        std::cout << "Enter an SQL-like command: ";
        std::getline(std::cin, line);

        current_command += " " + line;

        // If the line ends with a ';', execute the command and reset current_command
        if (line.find(';') != std::string::npos) {
            db.execute_query(current_command);
            current_command = "";
        }
    }

    return 0;
}
