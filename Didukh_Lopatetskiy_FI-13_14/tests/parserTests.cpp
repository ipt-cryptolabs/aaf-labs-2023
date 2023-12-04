#include <parser.hpp>
#include <gtest/gtest.h>

class ParserTest : public ::testing::Test {
protected:
    Parser parser;
};

TEST_F(ParserTest, TestInsertCommand) {
    std::string userInput = "INSERT MyCollectionName {188, 2248, 66, 999};";
    parser.lexer(userInput);

    auto tokens = parser.getTokens();

    ASSERT_EQ(tokens.size(), 6);
    ASSERT_EQ(tokens.at(0), "INSERT");
    ASSERT_EQ(tokens.at(1), "MyCollectionName");
    ASSERT_EQ(tokens.at(2), "188");
    ASSERT_EQ(tokens.at(3), "2248");
    ASSERT_EQ(tokens.at(4), "66");
    ASSERT_EQ(tokens.at(5), "999");
}

TEST_F(ParserTest, SpaceHandlingTest) {
    std::string userInput = "    INSERT    Another_Collection   {   111,      4522};";
    parser.lexer(userInput);

    auto tokens = parser.getTokens();

    ASSERT_EQ(tokens.size(), 4);
    ASSERT_EQ(tokens.at(0), "INSERT");
    ASSERT_EQ(tokens.at(1), "Another_Collection");
    ASSERT_EQ(tokens.at(2), "111");
    ASSERT_EQ(tokens.at(3), "4522");
}

TEST_F(ParserTest, MissingSemicolonTest) {
    std::string userInput = "INSERT Another_Collection {1023, 14}";
    parser.lexer(userInput);    

    auto tokens = parser.getTokens();

    ASSERT_EQ(tokens.size(), 0);
}

TEST_F(ParserTest, InvalidCollectionNameTest) {
    std::string userInput = "INSERT 111Another_Collection {1023, 14};";
    parser.lexer(userInput);    

    auto tokens = parser.getTokens();

    ASSERT_EQ(tokens.size(), 0);
}

TEST_F(ParserTest, StringValueTest) {
    std::string userInput = "INSERT Another_Collection {1023, kpop, 14};";
    parser.lexer(userInput);    

    auto tokens = parser.getTokens();

    ASSERT_EQ(tokens.size(), 0);
}

TEST_F(ParserTest, SingleValueSetTest) {
    std::string userInput = "INSERT Another_Collection {333};";
    parser.lexer(userInput);    

    auto tokens = parser.getTokens();

    ASSERT_EQ(tokens.size(), 3);
    ASSERT_EQ(tokens.at(0), "INSERT");
    ASSERT_EQ(tokens.at(1), "Another_Collection");
    ASSERT_EQ(tokens.at(2), "333");
}

TEST_F(ParserTest, NewLineSymbolHandlingTest) {
    std::string userInput = "INSERT \nMyCollectionName\n {188, 2248, 66, 999};";
    parser.lexer(userInput);

    auto tokens = parser.getTokens();

    ASSERT_EQ(tokens.size(), 6);
    ASSERT_EQ(tokens.at(0), "INSERT");
    ASSERT_EQ(tokens.at(1), "MyCollectionName");
    ASSERT_EQ(tokens.at(2), "188");
    ASSERT_EQ(tokens.at(3), "2248");
    ASSERT_EQ(tokens.at(4), "66");
    ASSERT_EQ(tokens.at(5), "999");
}

TEST_F(ParserTest, NegativeValueTest) {
    std::string userInput = "INSERT \nMyCollectionName\n {188, 2248, -66, 999};";
    parser.lexer(userInput);

    auto tokens = parser.getTokens();

    ASSERT_EQ(tokens.size(), 6);
    ASSERT_EQ(tokens.at(0), "INSERT");
    ASSERT_EQ(tokens.at(1), "MyCollectionName");
    ASSERT_EQ(tokens.at(2), "188");
    ASSERT_EQ(tokens.at(3), "2248");
    ASSERT_EQ(tokens.at(4), "-66");
    ASSERT_EQ(tokens.at(5), "999");
}