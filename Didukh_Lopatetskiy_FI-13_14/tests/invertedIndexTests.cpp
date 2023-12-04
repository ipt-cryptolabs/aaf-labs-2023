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