#include "utils.h"

std::string toLowerStr(const std::string& str)
{
	std::string res;

	for (int i = 0; i < str.length(); i++)
	{
		res += (tolower(str[i]));
	}

	return res;
}