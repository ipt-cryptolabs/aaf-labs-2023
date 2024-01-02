#include "queries.h"

CreateQuery::CreateQuery(const std::string& collectionName) : collectionName(collectionName)
{
}

InsertQuery::InsertQuery(const std::string& collectionName, const std::string& document) : collectionName(collectionName), document(document)
{
}

PrintIndexQuery::PrintIndexQuery(const std::string& collectionName) : collectionName(collectionName)
{
}

SearchQuery::SearchQuery(const std::string& collectionName) : collectionName(collectionName)
{
	expression = WhereExpression();
	exprCorectness = WhereExpression::ErrCode::Ok;
}

SearchQuery::SearchQuery(const std::string& collectionName, const std::string& expr) : collectionName(collectionName)
{
	exprCorectness = WhereExpression::ErrCode::Ok;
	expression = WhereExpression(expr, exprCorectness);
}

QueryResult CreateQuery::execute(InvIndDB& db)
{
	QueryResult qRes;
	qRes.queryType = CREATE;
	DBStatus status = DBStatus::Ok;
	db.addCollection(collectionName, status);
	switch (status)
	{
	case DBStatus::CollectionExists:
		qRes.message = "Collection " + collectionName + " is not added: it's already exists.";
		break;
	case DBStatus::Ok:
		qRes.message = "Collection " + collectionName + " succesfully added";
		break;
	}
	return qRes;
}

QueryResult InsertQuery::execute(InvIndDB& db)
{
	QueryResult qRes;
	qRes.queryType = INSERT;
	DBStatus status = DBStatus::Ok;
	db.addDocument(collectionName, document, status);
	switch (status)
	{
	case DBStatus::Ok:
		qRes.message = "perform operation on inserting:  " + document + "  in " + collectionName + " table";
		break;
	case DBStatus::CollectionNotExists:
		qRes.message = "collection " + collectionName + " is not exists!";
		break;
	}
	return qRes;
}

QueryResult PrintIndexQuery::execute(InvIndDB& db)
{
	QueryResult qRes;
	qRes.queryType = PRINT_INDEX;
	DBStatus status = DBStatus::Ok;
	std::string res = db.getIndex(collectionName, status);
	switch (status)
	{
	case DBStatus::Ok:
		qRes.message = "Print indexes of collection " + collectionName + ":\n\n" + res;
		break;
	case DBStatus::CollectionNotExists:
		qRes.message = "collection " + collectionName + " is not exists!";
		break;
	}
	return qRes;
}

QueryResult SearchQuery::execute(InvIndDB& db)
{
	QueryResult qRes;
	qRes.queryType = SEARCH;
	DBStatus status = DBStatus::Ok;
	std::string res;

	if (exprCorectness == WhereExpression::ErrCode::DistanceProblem)
	{
		qRes.message = "Where expression syntax is incorrect. Remember, value betweeen <> must be a number.\nKeywords must be in \"string\"";
		return qRes;
	}
	if (expression.distance != 0)
	{
		// TODO: Search by distance
		res = db.getDocsByWordDistance(collectionName, expression.keyword1, expression.keyword2, expression.distance, status);
	} else if (expression.prefix != "")
	{
		// TODO: Search by prefix
		qRes.message = "Search docs by prefix is not implemented yet.";
		return qRes;
	}
	else
	{
		res = db.getDocsByWord(collectionName, expression.keyword1, status);
	}
	
	switch (status)
	{
	case DBStatus::Ok:
		qRes.message = "Search in: " + collectionName + ":\n\n" + res;
		break;
	case DBStatus::CollectionNotExists:
		qRes.message = "collection " + collectionName + " is not exists!";
		break;
	case DBStatus::WordNotExists:
		qRes.message = "Word doesn't exists in collection " + collectionName;
		break;
	}

	return qRes;
}

WhereExpression::ErrCode WhereExpression::parseExpressionString(const std::string& exprString)
{
	const char IDLE = -1;
	const char KEYWORD = 0;
	const char PREFIX = 1;
	const char DISTANCE = 2;

	std::string word = "";
	char state = IDLE;
	ErrCode res = Ok;
	
	for (size_t i = 0; i < exprString.size(); i++)
	{
		if (exprString[i] == '"' && word.empty())
		{
			state = KEYWORD;
			continue;
		}
		if (exprString[i] == '<')
		{
			state = DISTANCE;
			continue;
		}
		switch (state)
		{
		case KEYWORD:
			if (exprString[i] == '"')
			{
				if (i + 1 < exprString.size() && exprString[i + 1] == '*')
				{
					state = PREFIX;
					continue;
				}
				else
				{
					switch (distance)
					{
					case 0:
						keyword1 = toLowerStr(word);
						break;
					default:
						keyword2 = toLowerStr(word);
						break;
					}
				}
				word = "";
				state = IDLE;
				continue;
			}
			word += exprString[i];
			continue;
		case PREFIX:
			prefix = toLowerStr(word);
			word = "";
			return Ok;
		case DISTANCE:

			if (exprString[i] == '>')
			{
				distance = stoi(word);
				state = IDLE;
				word = "";
				continue;
			}

			if (!isdigit(exprString[i]))
			{
				res = ErrCode::DistanceProblem;
				return res;
			}

			word += exprString[i];
			continue;
		}
	}

	if (distance != 0 && keyword2 == "")
	{
		res = DistanceProblem;
	}

	return res;
}

WhereExpression::WhereExpression()
{
	keyword1 = "";
	keyword2 = "";
	prefix = "";
	distance = 0;
}

WhereExpression::WhereExpression(const std::string& expressionString, WhereExpression::ErrCode& errCode) : WhereExpression()
{
	errCode = parseExpressionString(expressionString);
}
