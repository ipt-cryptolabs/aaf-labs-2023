#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>
#include <map>

class Table {
public:
    std::vector<std::string> columns;
    std::vector<std::vector<int>> data;


    Table(const std::vector<std::string>& columns) : columns(columns) {}

   
    void printColumns() const {
        
        
        std::vector<int> maxd;
        std::vector<std::vector<int>> count(100, std::vector<int>(columns.size(), 0));
        std::vector<int> num;
        int j = 0;
        maxd.resize(columns.size());
       
        
        for (int i = 0; i < columns.size(); i++) {
            maxd[i] = columns[i].size();
            j = 0;
            for(const auto& column2 : data){
                int col3 = column2[i];
                
                
                while(col3 != 0){
                    col3 = col3/10;
                    count[i][j]++;
                }
                maxd[i] = std::max(maxd[i],count[i][j]);
                j++;
            }
            
            
        }
            
            
        std::cout << "+";
        for(int i = 0; i < maxd.size(); i++){
            for(int j = 0; j < maxd[i]+2; j++){
                std::cout << "-";
            }
            std::cout << "+";
        }
        std::cout << std::endl;
        int x = 0;
        std::cout << "|";
        for (const auto& column : columns) {
            for(int i = 0; i < (maxd[x]-column.size())/2+1; i++){
                std::cout << " ";
            }
            std::cout << column;
            for(int i = 0; i < ((maxd[x]-column.size())+1)/2+1; i++){
                std::cout << " ";
            }
            std::cout << "|";
            x++;
        }
        std::cout << std::endl << "+";
        for(int i = 0; i < maxd.size(); i++){
            for(int j = 0; j < maxd[i]+2; j++){
                std::cout << "-";
            }
            std::cout << "+";
        }
        // std::cout << std::endl << "|";;
        int num1 = 0;
        for(const auto& column2 : data){
            std::cout << std::endl;
            std::cout << "|";
            for(int i = 0; i < column2.size(); i++){
                // std::cout << "(maxd[i]-col3[i]) = " << maxd[i]-count[i][num1]<< " " << maxd[i] << " " << count[i][num1]  << " " << num1 << " " << i << std::endl;
                for(int j = 0; j < (maxd[i]-count[i][num1])/2+1; j++){
                    std::cout << " ";
                }
                std::cout << column2[i];
                for(int j = 0; j < (((maxd[i]-count[i][num1])+1)/2)+1; j++){
                    std::cout << " ";
                }
            std::cout << "|";
            }
           num1++;
        }
        std::cout << std::endl << "+";
        for(int i = 0; i < maxd.size(); i++){
            for(int j = 0; j < maxd[i]+2; j++){
                std::cout << "-";
            }
            std::cout << "+";
        }
        std::cout << std::endl;
    }

    void createTable() {
       
        std::cout << "Table has been created." << std::endl;
       
        printColumns();
    }

    void insertRow(const std::vector<int>& row) {

        if (row.size() != columns.size()) {
            std::cerr << "Number of values does not match the number of columns." << std::endl;
            return;
        }

        data.push_back(row);
        std::cout << "1 row has been inserted." << std::endl;
    }

    void select(const std::string& conditionColumn, int conditionValue) {

        std::vector<std::vector<int>> result;

        for (const auto& row : data) {
            if (std::find(row.begin(), row.end(), conditionValue) != row.end()) {
                result.push_back(row);
            }
        }


        for (const auto& row : result) {
            for (const auto& value : row) {
                std::cout << value << " ";
            }
            std::cout << std::endl;
        }
        
        std::vector<int> maxd;
        std::vector<std::vector<int>> count(100, std::vector<int>(columns.size(), 0));
        std::vector<int> num;
        int j = 0;
        maxd.resize(columns.size());
 
        
        for (int i = 0; i < columns.size(); i++) {
            maxd[i] = columns[i].size();
            j = 0;
            for(const auto& column2 : result){
                int col3 = column2[i];
                
                
                while(col3 != 0){
                    col3 = col3/10;
                    count[i][j]++;
                    
                }
                maxd[i] = std::max(maxd[i],count[i][j]);
                j++;
            }
           
        }
            
            
        std::cout << "+";
        for(int i = 0; i < maxd.size(); i++){
            for(int j = 0; j < maxd[i]+2; j++){
                std::cout << "-";
            }
            std::cout << "+";
        }
        std::cout << std::endl;
        int x = 0;
        std::cout << "|";
        for (const auto& column : columns) {
            for(int i = 0; i < (maxd[x]-column.size())/2+1; i++){
                std::cout << " ";
            }
            std::cout << column;
            for(int i = 0; i < ((maxd[x]-column.size())+1)/2+1; i++){
                std::cout << " ";
            }
            std::cout << "|";
            x++;
        }
        std::cout << std::endl << "+";
        for(int i = 0; i < maxd.size(); i++){
            for(int j = 0; j < maxd[i]+2; j++){
                std::cout << "-";
            }
            std::cout << "+";
        }
        // std::cout << std::endl << "|";;
        int num1 = 0;
        for(const auto& column2 : result){
            std::cout << std::endl;
            std::cout << "|";
            for(int i = 0; i < column2.size(); i++){
                // std::cout << "(maxd[i]-col3[i]) = " << maxd[i]-count[i][num1]<< " " << maxd[i] << " " << count[i][num1]  << " " << num1 << " " << i << std::endl;
                for(int j = 0; j < (maxd[i]-count[i][num1])/2+1; j++){
                    std::cout << " ";
                }
                std::cout << column2[i];
                for(int j = 0; j < (((maxd[i]-count[i][num1])+1)/2)+1; j++){
                    std::cout << " ";
                }
            std::cout << "|";
            }
           num1++;
        }
        std::cout << std::endl;
    }
    
};


class Database {
public:
    std::map<std::string, Table> tables;


    void addTable(const std::string& tableName, const std::vector<std::string>& columns) {
        tables.emplace(tableName, columns);
        tables.at(tableName).printColumns();
    }


    void insertRow(const std::string& tableName, const std::vector<int>& row) {
        auto it = tables.find(tableName);
        if (it != tables.end()) {
            it->second.insertRow(row);
        } else {
            std::cerr << "Table " << tableName << " not found." << std::endl;
        }
    }
    
    void select(const std::string& tableName){
        auto it = tables.find(tableName);
         if (it != tables.end()) {
            tables.at(tableName).printColumns();
        } else {
            std::cerr << "Table " << tableName << " not found." << std::endl;
        }
        
    }

    void select(const std::string& tableName, const std::vector<std::string>& columns, const std::string& conditionColumn, int conditionValue) {
        auto it = tables.find(tableName);
        if (it != tables.end()) {
            it->second.select(conditionColumn, conditionValue);
        } else {
            std::cerr << "Table " << tableName << " not found." << std::endl;
        }
    }
};


int main() {
    std::cout << "ПРАЦЮЮЧІ КОМАНДИ: CREATE <name> (...), INSERT [INTO] <name> (...),SELECT FROM <name>,SELECT FROM <name> WHERE <COLUMN> = ...";
    std::cout << "Enter text:\n";
    Database db;

    while (true) {
        std::string text = "";
        std::string line = "";

        std::cout << ">>>";
        getline(std::cin, line);

        while (line.find(';') >= line.length()) {
            text += (" " + line);
            getline(std::cin, line);
        }
        text += (" " +line.substr(0,line.find(';')));
        size_t commaPos = text.find(',');
        while (commaPos != std::string::npos) {
            text.replace(commaPos, 1, " ");
            commaPos = text.find(',', commaPos + 1);
        }


        std::istringstream iss(text);
        std::string command;
        iss >> command;
        
        std::string table_name;
        std::vector<std::string> columns;
        std::string column;
        if (command == "CREATE") {
            iss >> table_name;
            iss.ignore();
            
            while (iss >> column) {
                if (column == ";") {
                    break;
                }
                bool indexed = (column == "INDEXED" || column == "INDEXED,");
                if (indexed) {
                    iss >> column;
                }
                
                if (!column.empty() && column[0] == '(') {
                    column.erase(0, 1);
                }
            
           
                if (!column.empty() && column.back() == ')') {
                    column.pop_back();
                }
                columns.push_back(column);
            }
            if(column == ""){
                std::cout << "error, not enough information" << std::endl;
            }else{
                db.addTable(table_name,columns);
            }
            

        } else if (command == "INSERT") {

            std::string into;
            std::string table_name;
            if (iss >> into && into == "INTO") {
                iss >> table_name;
                iss.ignore();
            }else{
                table_name = into;
            }

            std::vector<int> data;
            int value;
            std::string value2;
                while (iss >> value2) {
                    if (!value2.empty() && value2[0] == '(') {
                        value2.erase(0, 1);
                    }
                
                    if (!value2.empty() && value2.back() == ')') {
                        value2.pop_back();
                    }
                    try {
                     int result = std::stoi(value2);
                     data.push_back(result);

                    } catch (const std::invalid_argument& e) {
                        std::cerr << "Ошибка: " << e.what() << std::endl;
                    } catch (const std::out_of_range& e) {
                        std::cerr << "Ошибка: " << e.what() << std::endl;
                    }
                    
                }
                // for(int i =0; i < data.size();i++){
                //     std::cout << data[i] << " ";
                // }
                // std::cout << std::endl;
                db.insertRow(table_name, data);
            
        } else if (command == "SELECT") {
            std::string from;
            std::string table_name;
            std::vector<std::string> selectColumns;
            std::string conditionColumn;
            std::string token;
            std::string equial;
            std::string conditionValue;
            std::vector<std::string> groupByColumns;
            std::vector<std::pair<std::string, std::string>> aggregationFunctions;
            if (iss >> from >> table_name && from == "FROM") {
                
                iss >> token;
                if (token == "WHERE") {
                    iss >> conditionColumn >> equial >> conditionValue;
                    if(equial != "="){
                        std::cout << "Invalid command.(equial != '=')" << std::endl;
                    }else{
                        db.select(table_name,columns,conditionColumn,std::stoi(conditionValue));
                    }
                } else if (token == "GROUP_BY") {
                    std::string groupByColumn;
                    while (iss >> groupByColumn) {
                        if (groupByColumn == ";") {
                            break;
                        }
                        groupByColumns.push_back(groupByColumn);
                    }
                }
            }
            if(token.empty()){
                    db.select(table_name);
            }
            // db.select(table_name, selectColumns, conditionColumn, conditionValue);
        }else {
            std::cout << "Invalid command." << std::endl;
        }
    }

    return 0;
}
