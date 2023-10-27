#include <iostream>
#include "Table.hpp"
#include "Parser.hpp"

using namespace std;

int main() {
	Table test1("C:\\Users\\Acer\\Downloads\\test_join1.csv");
	Table test2("C:\\Users\\Acer\\Downloads\\test_join2.csv");
	test1.join(test2, "owner_ID");
	test1.toCSV("C:\\Users\\Acer\\Downloads\\test1.csv");
	test1.select();
}