#!/bin/bash
  
# File: run.sh
# Initial date: 21 Sept 2020
# Author: Margot Clyne

# School assignment: For Assignment #2 of class MCDB6440: Software Engineering for Scientists

# Description: Shell Script for print_cases.py using my_utils.py
# Objective of Assignment: become familiar with best practices

# make file executable


echo ... checking pycodestyle for my_utils.py ...
pycodestyle my_utils.py

echo ... checking pycodestyle for print_cases.py ...
pycodestyle print_cases.py

echo ... checking pycodestyle for test_my_utils.py ...
pycodestyle test_my_utils.py

echo ... running print_cases.py run1 ...
python print_cases.py --file_name covid-19-data/us-counties.csv --county Boulder --county_column 1 --cases_column 4 --daily True --running_avg True --window 5
echo ... running print_cases.py run2 incorrect county ...
python print_cases.py --file_name covid-19-data/us-counties.csv --county Colorado --county_column 1 --cases_column 4
echo ... running print_cases.py run3 ...
python print_cases.py --file_name covid-19-data/us-counties.csv --county Denver --county_column 1 --cases_column 4--running_avg True --window 7

echo ... runing test_print_cases.sh ...
bash test_print_cases.sh

echo ... running test_my_utils.py ...
python test_my_utils.py



