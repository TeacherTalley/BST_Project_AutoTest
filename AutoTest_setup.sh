#!/bin/bash
echo
echo "#################### START: AutoTest Setup #####################"
echo
echo "--- Copy student source from parent directory ---"
srcfiles="../main.cpp ../BST.h"
echo "Source files:" $srcfiles
cp $srcfiles .
echo "--- Building program ---"
cmake -S . -B build
cmake --build build
echo "--- Copy data files from AutoTest source to build directory ---"
cp AutoTest_movie_queue.txt build/movie_queue.txt
echo "##################### END: AutoTest Setup  #####################"
echo
