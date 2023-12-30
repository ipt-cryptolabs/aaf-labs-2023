#include "parser.h"

void QueryBuilder::lexer(const std::string& str)
{
	wordDividedString.clear();
	std::string word;
	
	const unsigned char WORD_DELIMITER = 0;
	const unsigned char STRING_DELIMITER = 1;
	const unsigned char EXPRESSION_DELIMITER = 2;

	unsigned char mode = 0;

	for (std::string::const_iterator i = str.begin(); i != str.cend(); i++)
	{
		switch (mode)
		{
		case WORD_DELIMITER:
			if (isspace(*i) || *i == ';')
			{
				if (i != str.begin() && (isspace(*(i - 1)) || (*(i - 1) == ';')))
				{
					continue;
				}
				if (toLowerStr(word) != WHERE)
				{
					wordDividedString.push_back(toLowerStr(word));
				}
				else
				{
					mode = EXPRESSION_DELIMITER;
				}
				word.clear();
				continue;
			}
			if (*i == '"')
			{
				mode = STRING_DELIMITER;
				continue;
			}
			break;
		case STRING_DELIMITER:
			if ((*(i) == '\\' && *(i + 1) == '"'))
			{
				continue;
			}
			if (*i == '"' && (*(i - 1) != '\\'))
			{
				wordDividedString.push_back(word);
				word.clear();
				continue;
			}
			if (*i == '\'' || *i == '.') continue;
			break;
		case EXPRESSION_DELIMITER:
			if (*i == ';')
			{
				wordDividedString.push_back(word);
				word.clear();
				continue;
			}
			break;
		}
		word += *i;
	}
}

QueryBuilder::QueryBuilder()
{
	query = nullptr;
}

QueryBuilder::~QueryBuilder()
{
	if (query != nullptr)
	{
		delete query;
		query = nullptr;
	}
}

Query* QueryBuilder::getQueryFromString(const std::string& str)
{
    if (query != nullptr) delete query;
    query = nullptr;
    lexer(str);

	if (wordDividedString.size() >= 3)
	{
		if (wordDividedString.front() == SEARCH)
		{
			query = new SearchQuery(wordDividedString[1], toLowerStr(wordDividedString[2]));
		}
		else if (wordDividedString.front() == INSERT)
		{
			query = new InsertQuery(wordDividedString[1], wordDividedString[2]);
		}
	}
	else if (wordDividedString.size() == 2)
	{
		if (wordDividedString.front() == CREATE)
		{
			query = new CreateQuery(wordDividedString[1]);
		}
		else if (wordDividedString.front() == PRINT_INDEX)
		{
			query = new PrintIndexQuery(wordDividedString[1]);
		}
		else if (wordDividedString.front() == SEARCH)
		{
			query = new SearchQuery(wordDividedString[1]);
		}
	}
	else
	{
		// TODO: Detailed error message?
	}
	
	return query;
}

