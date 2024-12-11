#!/bin/bash
repo=BST_Project_AutoTest
echo "#################### START: AutoTest Setup ##################################"
echo " To be consistent with the grading environment, assume we are starting out "
echo " in the source directory (i.e., the parent of the AutoTest directory)."
echo " You will get a cd error if you execute directly from the AutoTest directory."
echo "#############################################################################"
cd $repo
echo
echo "#################### START: AutoTest Results #####################"
echo "--- Checking code format (cpplint) ---"
./AutoTest_Style.sh $repo main.cpp BST.h
echo
echo "--- Checking main output (diff) ---"
cd build
# Output test disabled for now
# ../AutoTest_OutputTest.sh
echo
echo "--- Unit testing (googletest - all tests at once) ---"
ctest
echo
echo "--- Test user commands individually ---"
# AutoTest_OutputTest.py assumes starting in the source directory
cd ../..
./$repo/AutoTest_OutputTest.py -t test_exit
./$repo/AutoTest_OutputTest.py -t test_search 
./$repo/AutoTest_OutputTest.py -t test_search_not_found
./$repo/AutoTest_OutputTest.py -t test_add
./$repo/AutoTest_OutputTest.py -t test_add_already_present
./$repo/AutoTest_OutputTest.py -t test_watch
./$repo/AutoTest_OutputTest.py -t test_delete
./$repo/AutoTest_OutputTest.py -t test_delete_not_found
./$repo/AutoTest_OutputTest.py -t test_print
echo
# GitHub Classroom auto-grading runs the following commands from the current
# directory of the project being tested.  To similate that here, we need to
# change to the project directory before running the tests.
#
echo "--- Unit testing (single test at a time) ---"
./BST_Project_AutoTest/AutoTest_gtest.sh BSTTest.Empty
./BST_Project_AutoTest/AutoTest_gtest.sh BSTTest.Search
./BST_Project_AutoTest/AutoTest_gtest.sh BSTTest.SearchNotFound
./BST_Project_AutoTest/AutoTest_gtest.sh BSTTest.Insert
./BST_Project_AutoTest/AutoTest_gtest.sh BSTTest.Remove
./BST_Project_AutoTest/AutoTest_gtest.sh BSTTest.Inorder
./BST_Project_AutoTest/AutoTest_gtest.sh BSTTest.Preorder
./BST_Project_AutoTest/AutoTest_gtest.sh BSTTest.Postorder
./BST_Project_AutoTest/AutoTest_gtest.sh BSTTest.RemoveException
./BST_Project_AutoTest/AutoTest_gtest.sh BSTTest.InsertException

echo
echo "#################### END: AutoTest Results   #####################"
echo
