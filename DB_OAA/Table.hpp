#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>

using namespace std;

class Table {
private:
	fstream csv_file;
	string csv_file_path;
	vector<string> names;
	vector<vector<string>> data;
public:
	Table(string csv_file_path);
	void create(vector<string> names);
	void insert(vector<string> cells);
	void toCSV(string csv_file_path);
	void select();
	void select(vector<string> namess);
	Table join(Table& table, string name1, string name2);
};

Table::Table(string csv_file_path) : csv_file_path(csv_file_path){
	csv_file.open(csv_file_path, ios::in);

	string buff, word;
	bool zerorow = true;
	int i = 0;
	int j = 0;
	while (getline(csv_file, buff)) {
		stringstream s(buff);
		while (getline(s, word, ';')) {
			if (zerorow) {
				names.push_back(word);
			} else {
				if (j == i) {
					data.push_back(vector<string>());
					j++;
				}
				data[i].push_back(word);
				i++;
			}
		}
		if (zerorow)
			zerorow = false;
		i = 0;
	}

	csv_file.close();
}

void Table::create(vector<string> names) {
	this->names = names;
	data.clear();
	for (int i = 0; i < names.size(); i++)
		data.push_back(vector<string>());
	toCSV(csv_file_path);
}

void Table::insert(vector<string> cells) {
	if (names.size() == cells.size())
		for (int i = 0; i < names.size(); i++)
			data[i].push_back(cells[i]);
	else
		cerr << "count of cells not correct!\n";
	toCSV(csv_file_path);
}


void Table::toCSV(string csv_file_path) {
	csv_file.open(csv_file_path, ios::out|ios::trunc);

	for (int i = 0; i < names.size(); i++) {
		csv_file << names[i];
		if (i != names.size() - 1)
			csv_file << ";";
		else
			csv_file << "\n";
	}
	int i = 0;
	int j = 0;
	while (j < data[i].size()) {
		csv_file << data[i][j];
		if (i != data.size() - 1) {
			csv_file << ";";
			i++;
		} else {
			csv_file << "\n";
			i = 0;
			j++;
		}
	}

	csv_file.close();
}

string mlStr(string str, int ml) {
	string buf = str;
	for (int i = 0; i < ml; i++)
		str += buf;
	return str;
}

int MxSz(vector<string> strs) {
	int max_size = 0;
	for (string str : strs)
		if (max_size < str.size())
			max_size = str.size();
	return max_size;
}

void Table::select() {
	vector<int> max_sizes;
	for (int i = 0; i < names.size(); i++) {
		vector<string> strs;
		strs.push_back(names[i]);
		strs.insert(strs.end(), data[i].begin(), data[i].end());
		max_sizes.push_back(MxSz(strs));
	}
	string str1 = "";
	string str2 = "";
	bool firstrow = true;
	for (int i = 0; i < 2; i++) {
		for (int j = 0; j < names.size(); j++) {
			if (firstrow) {
				str1 += "+" + mlStr("-", max_sizes[j]) + "-";
			} else {
				str2 += "|" + mlStr(" ", max_sizes[j] - names[j].size()) + names[j] + " ";
			}
		}
		if (firstrow) {
			str1 += "+\n";
			cout << str1;
			firstrow = false;
		} else {
			str2 += "|\n";
			cout << str2 << str1;
		}
	}
	int i = 0;
	int j = 0;
	string str = "";
	bool kostyl = true;
	while (j < data[i].size()) {
		if (kostyl) {
			str += "|" + mlStr(" ", max_sizes[i] - data[i][j].size()) + data[i][j] + " ";
			if (i + 1 < data.size())
				i++;
			else
				kostyl = false;
		} else {
			str += "|\n";
			cout << str;
			str = "";
			i = 0;
			kostyl = true;
			j++;
		}
	}
	cout << str1;
}

void Table::select(vector<string> namess) {
	vector<int> columnID;
	for (int i = 0; i < namess.size(); i++) {
		bool exsist = false;
		for (int j = 0; j < names.size(); j++) {
			if (namess[i] == names[j]) {
				exsist = true;
				columnID.push_back(j);
				break;
			}
		}
		if (!exsist) {
			cerr << namess[i] << " doesn't exsist\n";
		}
	}

	vector<int> max_sizes;
	for (int i = 0; i < names.size(); i++) {
		vector<string> strs;
		strs.push_back(names[i]);
		strs.insert(strs.end(), data[i].begin(), data[i].end());
		max_sizes.push_back(MxSz(strs));
	}

	string str1 = "";
	string str2 = "";
	bool firstrow = true;
	for (int i = 0; i < 2; i++) {
		for (int j : columnID) {
			if (firstrow) {
				str1 += "+" + mlStr("-", max_sizes[j]) + "-";
			} else {
				str2 += "|" + mlStr(" ", max_sizes[j] - names[j].size()) + names[j] + " ";
			}
		}
		if (firstrow) {
			str1 += "+\n";
			cout << str1;
			firstrow = false;
		} else {
			str2 += "|\n";
			cout << str2 << str1;
		}
	}
	int i = 0;
	int j = 0;
	string str = "";
	bool kostyl = true;
	while (j < data[columnID[i]].size()) {
		if (kostyl) {
			str += "|" + mlStr(" ", max_sizes[columnID[i]] - data[columnID[i]][j].size()) + data[columnID[i]][j] + " ";
			if (columnID[i] + 1 < data.size() && i + 1 < columnID.size())
				i++;
			else
				kostyl = false;
		} else {
			str += "|\n";
			cout << str;
			str = "";
			i = 0;
			kostyl = true;
			j++;
		}
	}
	cout << str1;
}

Table Table::join(Table& table, string name1, string name2) {
	int nameID = -1, table_nameID = -1;
	for (int i = 0; i < names.size(); i++) {
		if (names[i] == name1)
			nameID = i;
	}
	if (nameID == -1) {
		cerr << name1 << " not found in table1\n";
		return Table("");
	}
	for (int i = 0; i < table.names.size(); i++) {
		if (table.names[i] == name2)
			table_nameID = i;
	}
	if (table_nameID == -1) {
		cerr << name2 << " not found in table2\n";
		return Table("");
	}

	vector<vector<string>> new_data(table.data.size(), vector<string>(data[0].size()));

	for (int j = 0; j < data[nameID].size(); j++)
		for (int tj = 0; tj < table.data[table_nameID].size(); tj++)
			if (data[nameID][j] == table.data[table_nameID][tj])
				for (int ti = 0; ti < table.data.size(); ti++)
					new_data[ti][j] = table.data[ti][tj];

	Table result("");
	result.names = names;
	result.data = data;
	result.names.insert(result.names.end(), table.names.begin(), table.names.end());
	result.data.insert(result.data.end(), new_data.begin(), new_data.end());
	return result;
}




