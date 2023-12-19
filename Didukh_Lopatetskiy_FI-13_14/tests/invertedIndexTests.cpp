#include <invertedIndex.hpp>
#include <gtest/gtest.h>

class InvertedIndexTests : public ::testing::Test {
protected:
    Collections collections;
};

TEST_F(InvertedIndexTests, InsertSetTest) {
    std::set<int> testSet = {1, 2, 3};
    collections.createCollection("TestCollection");
    collections.insertSet("TestCollection", testSet);
   
    EXPECT_TRUE(collections.containsCollection("TestCollection", testSet));
}

TEST_F(InvertedIndexTests, SearchInCollectionModifiedTest) {
    collections.createCollection("TestCollection");
    std::set<int> testSet1 = {1, 2, 3};
    std::set<int> testSet2 = {2, 3, 4};
    collections.insertSet("TestCollection", testSet1);
    collections.insertSet("TestCollection", testSet2);

    std::vector<std::set<int>> resultSets = collections.searchInCollection("TestCollection");

    ASSERT_EQ(resultSets.size(), 2);
    EXPECT_TRUE(resultSets[0] == testSet1 || resultSets[1] == testSet1);
    EXPECT_TRUE(resultSets[0] == testSet2 || resultSets[1] == testSet2);
}

TEST_F(InvertedIndexTests, SearchInNonExistentCollectionTest) {
    std::vector<std::set<int>> resultSets = collections.searchInCollection("NonExistentCollection");
    
    EXPECT_EQ(resultSets.size(), 0);
}

TEST_F(InvertedIndexTests, SearchInExistingCollectionTest) {
    collections.createCollection("TestCollection");
    std::vector<std::set<int>> resultSets = collections.searchInCollection("TestCollection");
    
    EXPECT_EQ(resultSets.size(), 0);
}

TEST_F(InvertedIndexTests, ContainsTest) {
    collections.createCollection("TestCollection");
    std::set<int> testSet1 = {11, 22, 33};
    std::set<int> testSet2 = {11, 22, 44};
    std::set<int> testSet3 = {11, 22};

    collections.insertSet("TestCollection", testSet1);
    collections.insertSet("TestCollection", testSet2);
    
    EXPECT_FALSE(collections.containsCollection("TestCollection", testSet3));
    EXPECT_TRUE(collections.containsCollection("TestCollection", testSet1));
}

TEST_F(InvertedIndexTests, IntersectsSearchTest) {
    collections.createCollection("TestCollection");
    std::set<int> testSet1 = {11, 22, 33, 44};
    std::set<int> testSet2 = {33, 44, 55};
    std::set<int> testSet3 = {44, 55, 66};
    std::set<int> testSet4 = {-44, -55, -66};

    collections.insertSet("TestCollection", testSet1);
    collections.insertSet("TestCollection", testSet2);
    collections.insertSet("TestCollection", testSet3);
    collections.insertSet("TestCollection", testSet4);

    std::set<int> searchSet = {33, 44};
    std::vector<std::set<int>> resultSets = collections.intersectsSearch("TestCollection", searchSet);

    ASSERT_EQ(resultSets.size(), 3);
    EXPECT_TRUE(resultSets[0] == testSet1 || resultSets[1] == testSet1 || resultSets[2] == testSet1);
    EXPECT_TRUE(resultSets[0] == testSet2 || resultSets[1] == testSet2 || resultSets[2] == testSet2);
    EXPECT_TRUE(resultSets[0] == testSet3 || resultSets[1] == testSet3 || resultSets[2] == testSet3);
}

TEST_F(InvertedIndexTests, ContainedBySearchTest) {
    collections.createCollection("TestCollection");
    std::set<int> testSet1 = {11, 22, 33};
    std::set<int> testSet2 = {22, 33, 44};
    std::set<int> testSet3 = {11, 22};
    std::set<int> testSet4 = {55, 66, 77};

    collections.insertSet("TestCollection", testSet1);
    collections.insertSet("TestCollection", testSet2);
    collections.insertSet("TestCollection", testSet3);
    collections.insertSet("TestCollection", testSet4);

    std::set<int> searchSet = {11, 22, 33, 44};
    std::vector<std::set<int>> resultSets = collections.containedBySearch("TestCollection", searchSet);

    ASSERT_EQ(resultSets.size(), 3);
    EXPECT_TRUE(resultSets[0] == testSet1 || resultSets[1] == testSet1 || resultSets[2] == testSet1);
    EXPECT_TRUE(resultSets[0] == testSet2 || resultSets[1] == testSet2 || resultSets[2] == testSet2);
    EXPECT_TRUE(resultSets[0] == testSet3 || resultSets[1] == testSet3 || resultSets[2] == testSet3);
}