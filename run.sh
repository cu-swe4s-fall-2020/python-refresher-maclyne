#!/bin/bash
  
# File: run.sh
# Initial date: 21 Sept 2020
# Author: Margot Clyne

# School assignment: For Assignment #2 of class MCDB6440: Software Engineering for Scientists

# Description: Shell Script for print_cases.py using my_utils.py
# Objective of Assignment: become familiar with best practices

# make file executable
chmod -x run.sh

echo ... running print_cases.py run1 ...
python print_cases.py --file_name covid-19-data/us-counties.csv --county Boulder --county_column 1 --cases_column 4
echo ... running print_cases.py run2 ...
python print_cases.py --file_name covid-19-data/us-counties.csv --county Colorado --county_column 1 --cases_column 4
echo ... running print_cases.py run3 ...
python print_cases.py --file_name covid-19-data/us-counties.csv --county Boulder --county_column 1 --cases_column 2

