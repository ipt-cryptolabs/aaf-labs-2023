#ifndef AAF_LABS_2023_PARSER_H
#define AAF_LABS_2023_PARSER_H

#include <string>
#include <vector>
#include "queries.h"

std::string toLowerStr(const std::string& str);

class QueryBuilder
{
private:
	Query* query;
	std::vector<std::string> wordDividedString;

	void lexer(const std::string& str);
public:
	QueryBuilder();
	~QueryBuilder();

	Query* getQueryFromString(const std::string& str);
};


#endif //AAF_LABS_2023_PARSER_H
