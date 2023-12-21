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
	// TODO
	std::string keyword1;
	std::string keyword2;
	unsigned int distance;
	std::string prefix;

	void parseExpressionString(std::string exprString);

	WhereExpression();
	WhereExpression(std::string expressionString);
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
	CreateQuery(std::string collectionName);
	QueryResult execute(InvIndDB& db) override;
};

class InsertQuery : public Query
{
private:
	std::string collectionName;
	std::string document;
public:
	InsertQuery(std::string collectionName, std::string document);
	QueryResult execute(InvIndDB& db) override;
};

class PrintIndexQuery : public Query
{
private:
	std::string collectionName;
public:
	PrintIndexQuery(std::string collectionName);
	QueryResult execute(InvIndDB& db) override;
};

class SearchQuery : public Query
{
private:
	std::string collectionName;
	WhereExpression expression;
public:
	SearchQuery(std::string collection_name);
	SearchQuery(std::string collection_name, WhereExpression expression);
	QueryResult execute(InvIndDB& db) override;
};

#endif