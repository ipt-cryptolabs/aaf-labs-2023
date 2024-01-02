#ifndef QUERIES_H
#define QUERIES_H

#include <string>
#include "invindexdb.h"

// There stored all queries

const char* const CREATE = "create";
const char* const INSERT = "insert";
const char* const PRINT_INDEX = "print_index";
const char* const SEARCH = "search";
const char* const WHERE = "where";

struct QueryResult
{
	const char* queryType;
	std::string message;
};

struct WhereExpression
{
	enum ErrCode
	{
		Ok,
		DistanceProblem
	};

	std::string keyword1;
	std::string keyword2;
	unsigned int distance;
	std::string prefix;

	ErrCode parseExpressionString(const std::string& exprString);

	WhereExpression();
	WhereExpression(const std::string& expressionString, WhereExpression::ErrCode& errCode);
};

class Query
{
protected:
	Query() = default;
public:
	virtual ~Query() = default;
	virtual QueryResult execute(InvIndDB& db) = 0;
};

class CreateQuery : public Query
{
private:
	std::string collectionName;
public:
	CreateQuery(const std::string& collectionName);
	QueryResult execute(InvIndDB& db) override;
};

class InsertQuery : public Query
{
private:
	std::string collectionName;
	std::string document;
public:
	InsertQuery(const std::string& collectionName, const std::string& document);
	QueryResult execute(InvIndDB& db) override;
};

class PrintIndexQuery : public Query
{
private:
	std::string collectionName;
public:
	PrintIndexQuery(const std::string& collectionName);
	QueryResult execute(InvIndDB& db) override;
};

class SearchQuery : public Query
{
private:
	std::string collectionName;
	WhereExpression expression;
	WhereExpression::ErrCode exprCorectness;
public:
	SearchQuery(const std::string& collectionName);
	SearchQuery(const std::string& collectionName, const std::string& expr);
	QueryResult execute(InvIndDB& db) override;
};

#endif