#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <regex>

using namespace std;

class Database{
private:
	string folderPath;
	vector<string> tableNames;
	vector<Table> tables;

public:
	Database(string path);
	void create(string tableName, vector<string> names);
	void insert(string tableName, vector<string> cells);
	void select(string tableName);
	void select(string tableName, vector<string> namess);
	Table join(string tableName1, string tableName2, string name1, string name2);

	void Parser();
};

Database::Database(string path) : folderPath(path) {
	for (const auto& entry : filesystem::directory_iterator(folderPath))
		if (entry.is_regular_file() && entry.path().extension() == ".csv") {
			tableNames.push_back(entry.path().stem().string());
			tables.push_back(Table(entry.path().string()));
		}
}

inline void Database::create(string tableName, vector<string> names) {
	for(string name : tableNames)
		if (tableName == name) {
			cerr << "table " << name << " already exist\n";
			return;
		}
	tableNames.push_back(tableName);
	string file_path = folderPath + "\\" + tableName + ".csv";
	tables.push_back(Table(file_path));
	tables[tables.size() - 1].create(names);
}

inline void Database::insert(string tableName, vector<string> cells) {
	for (int i = 0; i < tableNames.size(); i++)
		if (tableName == tableNames[i])
			tables[i].insert(cells);

}

inline void Database::select(string tableName) {
	for (int i = 0; i < tableNames.size(); i++)
		if (tableName == tableNames[i])
			tables[i].select();
}

inline void Database::select(string tableName, vector<string> namess) {
	for (int i = 0; i < tableNames.size(); i++)
		if (tableName == tableNames[i])
			tables[i].select(namess);
}

inline Table Database::join(string tableName1, string tableName2, string name1, string name2) {
	for (int i = 0; i < tableNames.size(); i++)
		for (int j = 0; j < tableNames.size(); j++)
			if (tableName1 == tableNames[i] && tableName2 == tableNames[j])
				return tables[i].join(tables[j], name1, name2);
}

inline void Database::Parser() {
    string command, line;

    while (getline(cin, line)) {
        if (line.find(';') != string::npos) {
            stringstream s(line);
            getline(s, line, ';');
            command += line + "\n";
            break;
        }
        command += line + "\n";
    }

    smatch match;

    if (regex_search(command, match, regex("CREATE\\s+([a-zA-Z0-9_]+)\\s*\\((.+)\\)", regex_constants::icase))) {
        string tableName = match[1].str();
        string columnNames = match[2].str();
        columnNames = regex_replace(columnNames, regex("\\s+"), "");
        vector<string> columnNamesVec;
        istringstream iss(columnNames);
        string columnName;
        while (getline(iss, columnName, ','))
            columnNamesVec.push_back(columnName);

        create(tableName, columnNamesVec);
    } else if (regex_search(command, match, regex("INSERT\\s+INTO\\s+([a-zA-Z0-9_]+)\\s+\\((.+)\\)", regex_constants::icase))) {
        string tableName = match[1].str();
        string cellValues = match[2].str();

        vector<string> cellValuesVec;
        istringstream iss(cellValues);
        string cellValue;
        while (getline(iss, cellValue, ','))
            cellValuesVec.push_back(cellValue);

        insert(tableName, cellValuesVec);
    } else if (regex_search(command, match, regex("SELECT\\s+(.+)\\s+FROM\\s+([a-zA-Z0-9_]+)\\s+JOIN\\s+([a-zA-Z0-9_]+)\\s+ON\\s+(.+)\\s*=\\s*(.+)", regex_constants::icase))) {
        string columnNames = match[1].str();
        string tableName = match[2].str();
        string tableNamejoin = match[3].str();
        string colName = match[4].str();
        string colNamejoin = match[5].str();
        columnNames = regex_replace(columnNames, regex("\\s+"), "");
        
        vector<string> columnNamesVec;
        istringstream iss(columnNames);
        string columnName;
        while (getline(iss, columnName, ','))
            columnNamesVec.push_back(columnName);

        if (columnNamesVec.size() == 1 && columnNamesVec[0] == "*")
            join(tableName, tableNamejoin, colName, colNamejoin).select();
        else
            join(tableName, tableNamejoin, colName, colNamejoin).select(columnNamesVec);

    } else if (regex_search(command, match, regex("SELECT\\s+(.+)\\s+FROM\\s+([a-zA-Z0-9_]+)", regex_constants::icase ))) {
        string columnNames = match[1].str();
        string tableName = match[2].str();
        columnNames = regex_replace(columnNames, regex("\\s+"), "");

        vector<string> columnNamesVec;
        istringstream iss(columnNames);
        string columnName;
        while (getline(iss, columnName, ','))
            columnNamesVec.push_back(columnName);

        if (columnNamesVec.size() == 1 && columnNamesVec[0] == "*")
            select(tableName);
        else
            select(tableName, columnNamesVec);
    } else if (regex_search(command, match, regex("x"))) {
        return;
    } else {
        cerr << "Invalid SQL command: " << command << endl;
    }

    Parser();
}


