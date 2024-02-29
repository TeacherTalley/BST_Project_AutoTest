/**
* ---------------------------------------------------------------------
* @copyright
* Copyright 2024 Michelle Talley University of Central Arkansas
*
* @author: Michelle Talley
* @course: Data Structures (CSCI 2320)
*
* @file AutoTest_gtests.cpp
* @brief Google Test for BST Project.
-----------------------------------------------------------------------
*/

#include <iostream>
#include <string>
#include <regex>

#include <gtest/gtest.h>

#include "BST.h"

// String trim functions - std::str does not have a built-in trim function
// see: https://stackoverflow.com/questions/216823/how-to-trim-a-stdstring
// trim from start (in place)
inline void ltrim(std::string &s)
{
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch)
                                    { return !std::isspace(ch); }));
}

// trim from end (in place)
inline void rtrim(std::string &s)
{
    s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char ch)
                         { return !std::isspace(ch); })
                .base(),
            s.end());
}

// remove extra consecutive whitespaces
void trimString(std::string &str)
{

    std::regex pattern("\\s+");

    str = std::regex_replace(str, pattern, " ");
}

// trim from both ends (in place)
inline void trim(std::string &s)
{
    rtrim(s);
    ltrim(s);
    trimString(s);
}

// trim from start (copying)
inline std::string ltrim_copy(std::string s)
{
    ltrim(s);
    return s;
}

// trim from end (copying)
inline std::string rtrim_copy(std::string s)
{
    rtrim(s);
    return s;
}

// trim from both ends (copying)
inline std::string trim_copy(std::string s)
{
    trim(s);
    return s;
}

// Test suite for BST

TEST(BSTTest, Empty)
{
    BST<int> bstint;
    BST<std::string> bststring;

    ASSERT_TRUE(bstint.empty());
    bstint.insert(5);
    ASSERT_FALSE(bstint.empty());

    ASSERT_TRUE(bststring.empty());
    bststring.insert("hello");
    ASSERT_FALSE(bststring.empty());
}


TEST(BSTTest, Search)
{
    BST<int> bstint;
    BST<std::string> bststring;

    bstint.insert(5);
    bstint.insert(3);
    bstint.insert(7);
    bstint.insert(2);
    bstint.insert(4);
    bstint.insert(6);
    bstint.insert(8);
    ASSERT_TRUE(bstint.search(5));
    ASSERT_TRUE(bstint.search(8));
    ASSERT_TRUE(bstint.search(2));

    bststring.insert("hello");
    bststring.insert("world");
    bststring.insert("foo");
    bststring.insert("bar");
    ASSERT_TRUE(bststring.search("hello"));
    ASSERT_TRUE(bststring.search("world"));
    ASSERT_TRUE(bststring.search("bar"));
    ASSERT_TRUE(bststring.search("world"));
}

TEST(BSTTest, SearchNotFound)
{
    BST<int> bstint;
    BST<std::string> bststring;

    bstint.insert(5);
    bstint.insert(3);
    bstint.insert(7);
    bstint.insert(2);
    bstint.insert(4);
    bstint.insert(6);
    bstint.insert(8);
    ASSERT_FALSE(bstint.search(9));
    ASSERT_FALSE(bstint.search(1));

    bststring.insert("hello");
    bststring.insert("world");
    bststring.insert("bar");
    ASSERT_FALSE(bststring.search("foo"));
}

TEST(BSTTest, SearchFoundAndNotFound)
{
    BST<int> bstint;
    BST<std::string> bststring;

    bstint.insert(5);
    bstint.insert(3);
    bstint.insert(7);
    bstint.insert(2);
    bstint.insert(4);
    bstint.insert(6);
    bstint.insert(8);
    ASSERT_TRUE(bstint.search(5));
    ASSERT_TRUE(bstint.search(8));
    ASSERT_TRUE(bstint.search(2));

    bststring.insert("hello");
    bststring.insert("world");
    bststring.insert("foo");
    bststring.insert("bar");
    ASSERT_TRUE(bststring.search("hello"));
    ASSERT_TRUE(bststring.search("world"));
    ASSERT_TRUE(bststring.search("bar"));
    ASSERT_TRUE(bststring.search("world"));

    BST<int> bstint2;
    BST<std::string> bststring2;

    bstint2.insert(5);
    bstint2.insert(3);
    bstint2.insert(7);
    bstint2.insert(2);
    bstint2.insert(4);
    bstint2.insert(6);
    bstint2.insert(8);
    ASSERT_FALSE(bstint2.search(9));
    ASSERT_FALSE(bstint2.search(1));

    bststring2.insert("hello");
    bststring2.insert("world");
    bststring2.insert("bar");
    ASSERT_FALSE(bststring2.search("foo"));

}


TEST(BSTTest, Insert)
{
    BST<int> bstint;
    BST<std::string> bststring;

    bstint.insert(5);
    ASSERT_TRUE(bstint.search(5));

    bststring.insert("hello");
    ASSERT_TRUE(bststring.search("hello"));
}


TEST(BSTTest, Delete)
{
    BST<int> bstint;
    BST<std::string> bststring;

    bstint.insert(5);
    ASSERT_TRUE(bstint.search(5));
    bstint.remove(5);
    ASSERT_FALSE(bstint.search(5));

    bststring.insert("hello");
    ASSERT_TRUE(bststring.search("hello"));
    bststring.remove("hello");
    ASSERT_FALSE(bststring.search("hello"));
}


TEST(BSTTest, Inorder)
{
    BST<int> bstint;
    BST<std::string> bststring;
    std::string output;

    bstint.insert(5);
    bstint.insert(3);
    bstint.insert(7);
    bstint.insert(2);
    bstint.insert(4);
    bstint.insert(6);
    bstint.insert(8);

    // capture std::cout output
    testing::internal::CaptureStdout();
    bstint.inorder(std::cout);
    output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(trim_copy(output), "2 3 4 5 6 7 8");

    bststring.insert("hello");
    bststring.insert("world");
    bststring.insert("foo");
    bststring.insert("bar");
    testing::internal::CaptureStdout();
    bststring.inorder(std::cout);
    output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(trim_copy(output), "bar foo hello world");
}

TEST(BSTTest, Preorder)
{
    BST<int> bstint;
    BST<std::string> bststring;
    std::string output;

    bstint.insert(10);
    bstint.insert(5);
    bstint.insert(12);
    bstint.insert(4);
    bstint.insert(8);
    bstint.insert(6);
    bstint.insert(7);
    bstint.insert(9);
    bstint.insert(14);

    // capture std::cout output
    testing::internal::CaptureStdout();
    bstint.preorder(std::cout);
    output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(trim_copy(output), "10 5 4 8 6 7 9 12 14");

    bststring.insert("hello");
    bststring.insert("world");
    bststring.insert("foo");
    bststring.insert("bar");
    testing::internal::CaptureStdout();
    bststring.preorder(std::cout);
    output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(trim_copy(output), "hello foo bar world");
}

TEST(BSTTest, Postorder)
{
    BST<int> bstint;
    BST<std::string> bststring;
    std::string output;

    bstint.insert(10);
    bstint.insert(5);
    bstint.insert(12);
    bstint.insert(4);
    bstint.insert(8);
    bstint.insert(6);
    bstint.insert(7);
    bstint.insert(9);
    bstint.insert(14);

    // capture std::cout output
    testing::internal::CaptureStdout();
    bstint.postorder(std::cout);
    output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(trim_copy(output), "4 7 6 9 8 5 14 12 10");

    bststring.insert("hello");
    bststring.insert("world");
    bststring.insert("foo");
    bststring.insert("bar");
    testing::internal::CaptureStdout();
    bststring.postorder(std::cout);
    output = testing::internal::GetCapturedStdout();
    EXPECT_EQ(trim_copy(output), "bar foo world hello");
}


TEST(BSTTest, RemoveException)
{
    BST<int> bstint;
    BST<std::string> bststring;

    bstint.insert(5);
    bstint.insert(3);
    bstint.insert(7);
    ASSERT_NO_THROW(bstint.remove(5)); 
    ASSERT_THROW(bstint.remove(6), std::runtime_error);

    bststring.insert("hello");
    bststring.insert("world");
    bststring.insert("foo");
    ASSERT_NO_THROW(bststring.remove("hello"));
    ASSERT_THROW(bststring.remove("bar"), std::runtime_error);
}


TEST(BSTTest, InsertException)
{
    BST<int> bstint;
    BST<std::string> bststring;

    bstint.insert(5);
    bstint.insert(3);
    bstint.insert(7);
    ASSERT_NO_THROW(bstint.insert(0));
    ASSERT_THROW(bstint.insert(3), std::runtime_error);

    bststring.insert("hello");
    bststring.insert("world");
    bststring.insert("foo");
    ASSERT_NO_THROW(bststring.insert("bar"));
    ASSERT_THROW(bststring.insert("foo"), std::runtime_error);
}
