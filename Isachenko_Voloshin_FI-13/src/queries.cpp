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
	expression = WhereExpression();
}

SearchQuery::SearchQuery(std::string collectionName, WhereExpression expression) : collectionName(collectionName), expression(expression)
{
}

QueryResult CreateQuery::execute(InvIndDB& db)
{
	QueryResult qRes;
	qRes.queryType = CREATE;

	db.addCollection(collectionName);
	qRes.message = "Collection " + collectionName + " succesfully added";
	return qRes;
}

QueryResult InsertQuery::execute(InvIndDB& db)
{
	QueryResult qRes;
	qRes.queryType = INSERT;
	db.addDocument(collectionName, document);
	qRes.message = "perform operation on inserting:  " + document + "  in " + collectionName + " table";
	return qRes;
}

QueryResult PrintIndexQuery::execute(InvIndDB& db)
{
	QueryResult qRes;
	qRes.queryType = PRINT_INDEX;
	qRes.message = "perform operation on printing indexes of table " + collectionName + ".\n\n";
	qRes.message += db.getIndex(collectionName);
	return qRes;
}

QueryResult SearchQuery::execute(InvIndDB& db)
{
	QueryResult qRes;
	qRes.queryType = SEARCH;
	qRes.message = "perform operation searching indexes of table " + collectionName + " which appears in docs: \n\n";
	if (expression.keyword1 != "")
		qRes.message += db.getDocsByWord(collectionName, expression.keyword1);
	return qRes;
}

void WhereExpression::parseExpressionString(std::string exprString)
{
	// TODO
}

WhereExpression::WhereExpression()
{
	keyword1 = "";
	keyword2 = "";
	prefix = "";
	distance = 0;
}

WhereExpression::WhereExpression(std::string expressionString)
{
	keyword1 = expressionString;
	keyword2 = "";
	prefix = "";
	distance = 0;
}
