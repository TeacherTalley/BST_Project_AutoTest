#!/bin/bash
echo Testing: $1
./BST_Project_AutoTest/build/AutoTest_gtests --gtest_filter=$1
