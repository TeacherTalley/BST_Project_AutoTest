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
./AutoTest_Style.sh
echo
echo "--- Checking main output (diff) ---"
cd build
# Output test disabled for now
# ../AutoTest_OutputTest.sh
# echo
# echo "--- Unit testing (googletest - all tests at once) ---"
# ctest
# echo
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
echo "--- Unit testing (single test at a time) ---"
cd $repo/build
./AutoTest_gtests --gtest_filter=BSTTest.Empty
./AutoTest_gtests --gtest_filter=BSTTest.Search
./AutoTest_gtests --gtest_filter=BSTTest.SearchNotFound
./AutoTest_gtests --gtest_filter=BSTTest.SearchFoundAndNotFound
./AutoTest_gtests --gtest_filter=BSTTest.Insert
./AutoTest_gtests --gtest_filter=BSTTest.Delete
./AutoTest_gtests --gtest_filter=BSTTest.Inorder
./AutoTest_gtests --gtest_filter=BSTTest.Preorder
./AutoTest_gtests --gtest_filter=BSTTest.Postorder
./AutoTest_gtests --gtest_filter=BSTTest.RemoveException
./AutoTest_gtests --gtest_filter=BSTTest.InsertException

echo
cd ..
echo "#################### END: AutoTest Results   #####################"
echo
