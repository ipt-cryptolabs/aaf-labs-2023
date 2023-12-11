#include <iostream>
#include "Table.hpp"
#include "Database.hpp"

using namespace std;

int main() {
	Database DB1("DB1");

	DB1.join("test_join1", "test_join2", "owner_ID", "ID").select({ "ID", "Name", "owner_ID", "Name"});

	DB1.Parser();

}
