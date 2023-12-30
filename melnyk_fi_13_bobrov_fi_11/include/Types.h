#pragma once

#include <string>

enum class Characters : char 
{
    UNDEFINED_CHARACTER = ' '
};

namespace Tokens 
{
    extern std::string STRING;
    extern std::string FULL_STRING;

    extern std::string CREATE;
    extern std::string PRINT_TREE;
    extern std::string INSERT;
    extern std::string CONTAINS;
    extern std::string SEARCH;

    extern std::string COMMA; 
    extern std::string QUOTE; 
    extern std::string WHERE; 

    extern std::string BETWEEN;
    extern std::string MATCH;

    extern std::string ASC;
    extern std::string DESC;
    extern std::string eof;
    extern std::string SEMICOLON;
}