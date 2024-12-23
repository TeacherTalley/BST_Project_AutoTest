#!/usr/bin/env python
#--------------------------------------------------------------------------
# File: AutoTest_OutputTest.py
# Description: Python script to test the BST_Project
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#--------------------------------------------------------------------------
import sys
import os
import subprocess
import shutil
import argparse
import re


#--------------------------------------------------------------------------
# list all test cases to be executed here - modify as needed
#--------------------------------------------------------------------------
TEST_CASES = ['test_exit',
              'test_search', 
              'test_search_not_found', 
              'test_add', 
              'test_add_already_present', 
              'test_watch', 
              'test_delete', 
              'test_delete_not_found', 
              'test_print'
              ]

#--------------------------------------------------------------------------
# Global variables - modify as needed
#--------------------------------------------------------------------------
PARENT_PROJECT = '../..'
PROJECT = 'BST_Project_AutoTest'
BUILD = 'build'
TEST_DIR = os.path.join(PROJECT, BUILD)
EXECUTABLE = './main'

DATA_DIR = '..'
AUTOTEST_MOVIE_QUEUE_FILE = 'AutoTest_movie_queue.txt'
STUDENT_MOVIE_QUEUE_FILE = 'movie_queue.txt'
TESTDATAFILES = [AUTOTEST_MOVIE_QUEUE_FILE]
DATAFILES = [STUDENT_MOVIE_QUEUE_FILE]

AUTOTEST_MAIN_MISSING_FILE = 'AutoTest_main_missing_file.txt'
STUDENT_MAIN_MISSING_FILE = 'test_main_missing_file.txt'

AUTOTEST_MAIN_OUTPUT_FILE = 'AutoTest_main_output.txt'
STUDENT_MAIN_OUTPUT_FILE = 'test_main_output.txt'

AUTOTEST_MOVIE_QUEUE_UPDATE_FILE = 'AutoTest_movie_queue_updated.txt'
AUTOTEST_MOVIE_QUEUE_UPDATE_FILE_ADDS = 'AutoTest_movie_queue_updated_adds.txt'
AUTOTEST_MOVIE_QUEUE_UPDATE_FILE_DELS = 'AutoTest_movie_queue_updated_dels.txt'
STUDENT_MOVIE_QUEUE_UPDATE_FILE = 'movie_queue_updated.txt'

#--------------------------------------------------------------------------
# Program commands - modify as needed
#--------------------------------------------------------------------------
USER_COMMANDS = {'search': 's',
                 'add': 'a', 
                 'watch': 'w', 
                 'delete': 'd', 
                 'print': 'p',
                 'exit': 'x'
                }

ADD_MOVIE = 'Black Widow'
ADD_MOVIES = ['Zoolander', 'Arthur', 'Meatballs']
DEL_MOVIES = ['Barbie', 'Oppenheimer']
SEARCH_MOVIE_FOUND = 'Black Panther'
SEARCH_MOVIE_NOT_FOUND = 'The Godfather'

#--------------------------------------------------------------------------
# Helper functions
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
# Font colors for terminal output
#--------------------------------------------------------------------------
BLUE = '\033[34m'
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

def report_failure(msg):
    """
    Prints a failure message in red font.
    Parameters:
         msg (str): The message to print.
    Returns:
         None
    """
    print(f'{RED}[----------]{RESET}')
    print(f'{RED}[  FAILED  ] {msg}{RESET}')
    print(f'{RED}[----------]{RESET}')
    return

def report_success(msg):
    """
    Prints a success message in green font.
    Parameters:
         msg (str): The message to print.
    Returns:
         None
    """
    print(f'{GREEN}[----------]{RESET}')
    print(f'{GREEN}[  PASSED  ] {msg}{RESET}')
    print(f'{GREEN}[----------]{RESET}')
    return

def report_info(msg, color=RESET):
    """
    Prints an informational message in the specified font color.
    Parameters:
         msg (str): The message to print.
         color (str): The font color to use. Defaults to GREEN.
    Returns:
         None
    """
    print(f'{color}{msg}{RESET}')
    return


def execute_command(cmd, args=None, accept_rc=[0]):
    """
    Executes a shell command and provides verbose and debug output based on the given arguments.
    Parameters:
         cmd (str): The shell command to execute.
         args (object, optional): An object containing verbose and debug flags. Defaults to None.
         accept_rc (list, optional): A list of acceptable return codes. Defaults to [0].
    Returns:
         int: The return code of the executed command.
    Behavior:
    - If `args.verbose` is True, prints the command execution details.
    - If `args.debug` is False, executes the command using `subprocess.call`.
    - If `args.verbose` is True, prints the result of the command execution, including specific messages for segmentation faults (rc=139) and uncaught exceptions (rc=134).
    """
    rc = 0

    if not args:
        args.verbose = False
        args.debug = False

    if args.verbose:
        print(f'{GREEN}[==========]{RESET}')
        print(f'{GREEN}[ EXECUTE  ] {cmd}{RESET}')
        print(f'{GREEN}[==========]{RESET}')

    if not args.debug:
        rc = subprocess.call(cmd, shell=True)

    if args.verbose:
        if rc == 139:
            report_failure('Segmentation Fault')
        elif rc == 134:
            report_failure('Uncaught Exception')
        elif rc not in accept_rc:
            report_failure(f'rc = {rc}')
        else:
            report_success(f'rc = {rc}')
    return rc


def file_print(file, args=None):
    """
    Prints the contents of a file.

    Args:
        file (str): The path of the file to be printed.
        args (optional): Additional arguments (not used in this function).

    Returns:
        None
    """
    with open(file, 'r') as f:
        filedata = f.read()
    print(filedata)
    return

def file_diff(file1, file2, diff_args=None, args=None):
    """
    Compare two files and return the difference.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.
        diff_args (str, optional): Additional arguments for the diff command. Defaults to None.
        args (str, optional): Additional arguments for the execute_command function. Defaults to None.

    Returns:
        int: Return code of the execute_command function.
    """
    diffcmd = 'diff'
    if not diff_args:
        # diff_args = '--ignore-case --ignore-blank-lines --side-by-side  --ignore-space-change  --suppress-common-lines --color=always'
        diff_args = '--ignore-case --ignore-blank-lines --side-by-side  --ignore-space-change --color=always'
    cmd = f'{diffcmd} {diff_args} {file1} {file2}'
    rc = execute_command(cmd, args)
    return rc

def file_contains_file(file, searchfile, args=None):
    """
    Check if a file contains another file.

    Args:
        file (str): The path to the file to be checked.
        searchfile (str): The path to the file to search for.
        args (argparse.Namespace, optional): Additional arguments. Defaults to None.

    Returns:
        int: 0 if the searchfile is found in the file, 1 otherwise.
    """
    if not args:
        args.verbose = False
        args.debug = False

#    if args.verbose:
#        report_info(f'Check file {file} contains file {searchfile}')

    with open(file, 'r') as f:
        filedata = f.read()
    with open(searchfile, 'r') as f:
        searchdata = f.read()
    if searchdata in filedata:
        if args.verbose:
            report_success(f'{searchfile} found in {file}')
        return 0
    else:
        if args.verbose:
            report_failure(f'{searchfile} not found in {file}')
            report_info(f'\nExpected:\n{searchdata}')
            report_info(f'\nActual:\n{filedata}')
        return 1

def file_contains_string(file, searchstring, args=None):
    """
    Check if a file contains a specific string.

    Args:
        file (str): The path to the file to be checked.
        searchstring (str): The string to search for in the file.
        args (argparse.Namespace, optional): Additional arguments. Defaults to None.

    Returns:
        int: 0 if the searchstring is found in the file, 1 otherwise.
    """
    if not args:
        args.verbose = False
        args.debug = False

#    if args.verbose:
#        report_info(f'Check file {file} contains "{searchstring}"')

    with open(file, 'r') as f:
        filedata = f.read()
    if searchstring in filedata:
        if args.verbose:
            report_success(f'{searchstring} found in {file}')
        return 0
    else:
        if args.verbose:
            report_failure(f'"{searchstring}" not found in {file}')
            report_info(f'\nExpected:\n{searchstring}')
            report_info(f'\nActual:\n{filedata}')
        return 1

def file_contains_regex(file, searchstring, args=None):
    """
    Check if a file contains a specific string using regular expression.

    Args:
        file (str): The path of the file to be checked.
        searchstring (str): The string to search for in the file.
        args (argparse.Namespace, optional): Additional arguments. Defaults to None.

    Returns:
        int: 0 if the searchstring is found in the file, 1 otherwise.
    """
    if not args:
        args.verbose = False
        args.debug = False

#    if args.verbose:
#        report_info(f'Check file {file} contains regex "{searchstring}"')

    with open(file, 'r') as f:
        filedata = f.read()
    if re.search(searchstring, filedata):
        if args.verbose:
            report_success(f'Regex "{searchstring}" found in {file}')
        return 0
    else:
        if args.verbose:
            report_failure(f'Regex "{searchstring}" not found in {file}')
            report_info(f'\nExpected:\nRegex {searchstring}')
            report_info(f'\nActual:\n{filedata}')
        return 1

import shutil

def file_copy(src, dest, args=None):
    """
    Copy a file from the source path to the destination path.

    Args:
        src (str): The path of the source file.
        dest (str): The path of the destination file.
        args (optional): Additional arguments (not used in this function).

    Returns:
        int: 0 if the file copy is successful, 1 otherwise.
    """
    try:
        shutil.copyfile(src, dest)
    except:
        report_failure(f'Unable to copy {src} to {dest}')
        return 1
    return 0

def file_exists(file, args=None):
    return os.path.exists(file)

def file_remove(file, args=None):
    if file_exists(file):
        os.remove(file)
    return

def copy_test_input_files():
    # make sure the data files exist; overwrite if necessary
    for file, testfile in zip(DATAFILES, TESTDATAFILES):
        rc = file_copy(os.path.join(DATA_DIR, testfile), file)
        if rc != 0:
            return rc
    return 0


#--------------------------------------------------------------------------
# Test functions - Add your test functions here
#
# setup(args) - function to execute before running tests
# cleanup(args) - function to execute after running tests
#--------------------------------------------------------------------------

def setup(args):
    """
    Set up the test environment by changing the current working directory to the test directory.

    Args:
        args (object): The command-line arguments.

    Returns:
        None
    """
    cwd = os.getcwd()
    if not cwd.endswith(TEST_DIR):
        try:
            os.chdir(TEST_DIR)
        except:
            report_failure(f'Unable to change directory to: {TEST_DIR}')
            sys.exit(1)
    if args.debug:
        report_info(f'\nsetup: Changed directory to: {os.getcwd()}')
    return


def cleanup(args):
    """
    Cleans up the current working directory by changing it to the parent project directory.

    Args:
        args: Command-line arguments.

    Returns:
        None
    """
    cwd = os.getcwd()
    if cwd.endswith(TEST_DIR):
        try:
            os.chdir(PARENT_PROJECT)
        except:
            report_failure(f'Unable to change directory to: {".."}')
            sys.exit(1)
    if args.debug:
        report_info(f'\ncleanup: Changed directory to: {os.getcwd()}')
    return


def test_missing_file(args):
    """
    Test case for checking if a file is missing.

    Args:
        args: Additional arguments for executing the command.

    Returns:
        int: Return code indicating the result of the test case.
    """
    # make sure the data files do NOT exist
    for file in DATAFILES:
        if os.path.exists(file):
            os.remove(file)

    # run the program
    cmd = f'{EXECUTABLE} > {STUDENT_MAIN_MISSING_FILE} 2>&1'
    rc = execute_command(cmd, args)

    autotest_file = os.path.join(DATA_DIR, AUTOTEST_MAIN_MISSING_FILE)

    if not file_exists(autotest_file):
        report_failure(f'{autotest_file} not found')
        return 1

    # check that the updated movie queue file contains the new movie
    rc = file_diff(autotest_file, STUDENT_MAIN_MISSING_FILE, args=args)
    return rc


def test_exit(args):
    """
    Test the 'exit' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        report_failure(f'Unable to copy test input files')
        return 1

    user_cmd = 'exit'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)    
    return rc


def test_search(args):
    """
    Test the 'search' functionality of the program where movie found.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        report_failure(f'Unable to copy test input files')
        return 1

    user_cmd = 'search'

    # build the command sequence into a string
    movie = SEARCH_MOVIE_FOUND
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{movie}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}_found.txt'

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc
    
    search_str = f'{movie}\s+found'
    rc = file_contains_regex(test_output_file, search_str, args=args)
    return rc


def test_search_not_found(args):
    """
    Test the 'search' functionality when movie not found.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        report_failure(f'Unable to copy test input files')
        return 1

    user_cmd = 'search'

    # build the command sequence into a string
    movie = SEARCH_MOVIE_NOT_FOUND
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{movie}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}_not_found.txt'

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc
    
    search_str = f'{movie}\s+not found'
    rc = file_contains_regex(test_output_file, search_str, args=args)
    return rc


def test_add(args):
    """
    Test the 'add' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        report_failure(f'Unable to copy test input files')
        return 1

    user_cmd = 'add'

    # build the command sequence into a string
    test_cmd = ""
    for movie in ADD_MOVIES:
        test_cmd += f'{USER_COMMANDS[user_cmd]}\n{movie}\n'
    test_cmd += f'{USER_COMMANDS["exit"]}\n'
    # movie = ADD_MOVIE
    # test_cmd = f'{USER_COMMANDS[user_cmd]}\n{movie}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    autotest_queue_file = os.path.join(DATA_DIR, AUTOTEST_MOVIE_QUEUE_UPDATE_FILE_ADDS)

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc
    
    for movie in ADD_MOVIES:
        search_str = f'{movie}\s+added'
        rc = file_contains_regex(test_output_file, search_str, args=args)
        if rc != 0:
            return rc

    # check that the updated movie queue file contains the new movie
    rc = file_diff(autotest_queue_file, 
                   STUDENT_MOVIE_QUEUE_UPDATE_FILE,
                   args=args)
    return rc


def test_add_already_present(args):
    """
    Test the 'add' functionality if movie already present

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        report_failure(f'Unable to copy test input files')
        return 1

    user_cmd = 'add'

    # build the command sequence into a string
    movie = SEARCH_MOVIE_FOUND
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{movie}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    autotest_queue_file = os.path.join(DATA_DIR, AUTOTEST_MOVIE_QUEUE_UPDATE_FILE)

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc
    
    search_str = f'{movie}\s+already present'
    rc = file_contains_regex(test_output_file, search_str, args=args)
    if rc != 0:
        return rc

    # check that the updated movie queue file does not change
    rc = file_diff(autotest_queue_file, 
                   STUDENT_MOVIE_QUEUE_UPDATE_FILE,
                   args=args)
    return rc


def test_watch(args):
    """
    Test the 'watch' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        report_failure(f'Unable to copy test input files')
        return 1

    user_cmd = 'watch'

    # build the command sequence into a string
    test_cmd = ""
    for movie in DEL_MOVIES:
        test_cmd += f'{USER_COMMANDS[user_cmd]}\n{movie}\n'
    test_cmd += f'{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    autotest_queue_file = os.path.join(DATA_DIR, AUTOTEST_MOVIE_QUEUE_UPDATE_FILE_DELS)

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc 

    for movie in DEL_MOVIES:
        search_str = f'{movie}\s+watched'
        rc = file_contains_regex(test_output_file, search_str, args=args)
        if rc != 0:
            return rc
        
    # check that the updated movie queue file does not contain watched movies
    if args.verbose:
        report_info(f'Checking watched movies {DEL_MOVIES} removed')

    rc = file_diff(autotest_queue_file, 
                   STUDENT_MOVIE_QUEUE_UPDATE_FILE,
                   args=args)
    if rc != 0:
        if args.verbose:
            report_failure(f'{DEL_MOVIES} not removed from {STUDENT_MOVIE_QUEUE_UPDATE_FILE}')
        return rc 

    return rc


def test_delete(args):
    """
    Test the 'delete' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        report_failure(f'Unable to copy test input files')
        return 1

    user_cmd = 'delete'

    test_cmd = ""
    for movie in DEL_MOVIES:
        test_cmd += f'{USER_COMMANDS[user_cmd]}\n{movie}\n'
    test_cmd += f'{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    autotest_queue_file = os.path.join(DATA_DIR, AUTOTEST_MOVIE_QUEUE_UPDATE_FILE_DELS)

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc 

    for movie in DEL_MOVIES:
        search_str = f'{movie}\s+removed'
        rc = file_contains_regex(test_output_file, search_str, args=args)
        if rc != 0:
            return rc
        
    # check that the updated movie queue file does not contain deleted movies
    if args.verbose:
        report_info(f'Checking {DEL_MOVIES} deleted from updated queue')

    rc = file_diff(autotest_queue_file, 
                STUDENT_MOVIE_QUEUE_UPDATE_FILE,
                args=args)
    if rc != 0:
        if args.verbose:
            report_failure(f'{DEL_MOVIES} not removed from {STUDENT_MOVIE_QUEUE_UPDATE_FILE}')
        return rc 
     
    return rc


def test_delete_not_found(args):
    """
    Test the 'delete' functionality when movie not found.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        report_failure(f'Unable to copy test input files')
        return 1

    user_cmd = 'delete'

    movie = SEARCH_MOVIE_NOT_FOUND
    test_cmd = ""
    test_cmd += f'{USER_COMMANDS[user_cmd]}\n{movie}\n'
    test_cmd += f'{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    autotest_queue_file = os.path.join(DATA_DIR, AUTOTEST_MOVIE_QUEUE_UPDATE_FILE)

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc 

    search_str = f'{movie}\s+not found'
    rc = file_contains_regex(test_output_file, search_str, args=args)
    if rc != 0:
        return rc
        
    # check that the updated movie queue file does not contain deleted movies
    if args.verbose:
        report_info(f'Checking movie list unchanged')

    rc = file_diff(autotest_queue_file, 
                   STUDENT_MOVIE_QUEUE_UPDATE_FILE, 
                   args=args)
    if rc != 0:
        if args.verbose:
            report_failure(f'[  FAILED  ] {STUDENT_MOVIE_QUEUE_UPDATE_FILE} is incorrect')
        return rc 
     
    return rc


def test_print(args):
    """
    Test the 'print' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        report_failure(f'Unable to copy test input files')
        return 1

    user_cmd = 'print'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    autotest_queue_file = os.path.join(DATA_DIR, AUTOTEST_MOVIE_QUEUE_UPDATE_FILE)

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc
    
    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        report_info(f'Checking print output')

    rc = file_contains_file(test_output_file, autotest_queue_file, args=args)
    return rc






#--------------------------------------------------------------------------
# Everything below this line is generic code to execute tests defined above
# Do not modify anything below this line
#--------------------------------------------------------------------------
def banner(msg, args):
    if args.verbose:
        print(f'{BLUE}[==========]{RESET}')
        print(f'{BLUE}[   TEST   ] {msg}{RESET}')
        print(f'{BLUE}[==========]{RESET}')

def footer(msg, rc, args):
    if args.verbose:
        print(f'{BLUE}[==========]{RESET}')
        print(f'{BLUE}[   END    ] {msg} rc: {rc}{RESET}')
        print(f'{BLUE}[==========]{RESET}')

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", default=True, 
                        help="Enable verbose output")
    parser.add_argument("-q", "--quiet", action="store_true", default=False, 
                        help="Enable quiet mode")
    parser.add_argument("--nosetup", action="store_true", default=False, 
                        help="Disable setup before running tests")
    parser.add_argument("--nocleanup", action="store_true", default=False, 
                        help="Disable cleanup after running tests")
    parser.add_argument("--debug", action="store_true", default=False, 
                        help="Enable debug mode")
    parser.add_argument("-t", "--test", nargs='+', type=str, default=None, 
                        help=f"Specify the test(s) to run from: {TEST_CASES}")
    return parser.parse_args()

def test_main():
    args = parse_arguments()

    if args.quiet:
        args.verbose = False

    if not args.nosetup:
        # execute the setup function if it exists
        try:
            setup(args)
        except NameError:
            pass

    # if no test ID is provided, run all tests
    if not args.test:
        tests = TEST_CASES
    else:
        tests = args.test

    for test in tests:
        banner(test, args)
        try:
            rc = globals()[test](args)
        except NameError:
            report_failure(f'Test function {test} not found.')
            rc = 0
        footer(test, rc, args)

    if not args.nocleanup:
        # execute the cleanup function if it exists
        try:
            cleanup(args)
        except NameError:
            pass

    sys.exit(rc)

def main():
    test_main()

if __name__ == "__main__":
    main()
