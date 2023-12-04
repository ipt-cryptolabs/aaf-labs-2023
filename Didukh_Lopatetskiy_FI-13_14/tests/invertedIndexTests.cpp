#include <invertedIndex.hpp>
#include <gtest/gtest.h>

class InvertedIndexTests : public ::testing::Test {
protected:
    Collections collections;
};

TEST_F(InvertedIndexTests, CreateCollectionTest) {
    collections.createCollection("TestCollection");
    EXPECT_TRUE(collections.searchInCollection("TestCollection"));
}

TEST_F(InvertedIndexTests, InsertSetTest) {
    std::set<int> testSet = {1, 2, 3};
    collections.createCollection("TestCollection");
    collections.insertSet("TestCollection", testSet);
    EXPECT_TRUE(collections.containsCollection("TestCollection", testSet));
}

TEST_F(InvertedIndexTests, SearchInCollectionTest) {
    collections.createCollection("TestCollection");
    EXPECT_TRUE(collections.searchInCollection("TestCollection"));
    EXPECT_FALSE(collections.searchInCollection("NonExistentCollection"));
}

TEST_F(InvertedIndexTests, ContainsCollectionComplexTest) {
    collections.createCollection("TestCollection");
    std::set<int> testSet1 = {1, 2, 3};
    std::set<int> testSet2 = {2, 3, 4};
    std::set<int> testSet3 = {5, 6, 7};

    collections.insertSet("TestCollection", testSet1);
    collections.insertSet("TestCollection", testSet2);

    EXPECT_TRUE(collections.containsCollection("TestCollection", testSet1));
    EXPECT_TRUE(collections.containsCollection("TestCollection", testSet2));
    EXPECT_FALSE(collections.containsCollection("TestCollection", testSet3));
}