
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

using namespace std;

void Parser() {
	string toParse, line;
	while (getline(cin, line)) {
		if (line.find(';') != string::npos) {
			stringstream s(line);
			getline(s, line, ';');
			toParse += line + "\n";
			break;
		}
		toParse += line + "\n";
	}


}