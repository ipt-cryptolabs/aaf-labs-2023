#include "queries.h"

CreateQuery::CreateQuery(std::string collectionName) : collectionName(collectionName)
{
}

InsertQuery::InsertQuery(std::string collectionName, std::string document) : collectionName(collectionName), document(document)
{
}

PrintIndexQuery::PrintIndexQuery(std::string collectionName) : collectionName(collectionName)
{
}

SearchQuery::SearchQuery(std::string collection_name) : collectionName(collection_name)
{
}

SearchQuery::SearchQuery(std::string collectionName, WhereExpression expression) : collectionName(collectionName), expression(expression)
{
}

QueryResult CreateQuery::execute()
{
	QueryResult qRes;
	qRes.queryType = CREATE;
	qRes.message = "perform operation on creating table " + collectionName;
	return qRes;
}

QueryResult InsertQuery::execute()
{
	QueryResult qRes;
	qRes.queryType = INSERT;
	qRes.message = "perform operation on inserting " + document + " in " + collectionName + "table";
	return qRes;
}

QueryResult PrintIndexQuery::execute()
{
	QueryResult qRes;
	qRes.queryType = PRINT_INDEX;
	qRes.message = "perform operation on printing indexes of table " + collectionName;
	return qRes;
}

QueryResult SearchQuery::execute()
{
	QueryResult qRes;
	qRes.queryType = SEARCH;
	qRes.message = "perform operation searching indexes of table " + collectionName + "WHICH...";
	return qRes;
}

WhereExpression::WhereExpression(std::string expressionString)
{
}
