# python-refresher

Objective: become familiar with python

Initial date: 17 Sept 2020
Author: Margot Clyne

Updated date: 8 Oct 2020
School assignment: For Assignment #3 of class MCDB6440: Software Engineering for Scientists


File: my_utils.py	This file imports a CSV file and outputs desired data
			includes function get_column(file_name, query_column, query_value, result_columns=[1])
			includes function has_decreasing_values() for an array of int
			includes function get_daily_count(cumulative_values)
			includes function running_average(daily_values, window=5)
			now satisfies Pep8

File: print_cases.py	Uses get_column() from my_utils.py to read Covid19 cases and output desired data
			uses argparse for input command line parameters
			optionally runs get_daily_count()
			optionally runs running_average()
			now satisfies Pep8

File: run.sh		runs print_cases.py
			checks pycodestyle for all .py scripts
			runs unit tests test_my_utils.py
			runs function tests test_print_cases.sh

File: covid-19-data/us-counties-testfile-Boulder.csv 	testfile used for some unit tests
							mainly used for test_get_column()

File: make_newtestfile.py	python script I used to make my initial testfile of covid19 data
				note: other testfiles were manually edited from this product

File: test_print_cases.sh	usses Stupid Simple Bash Testing for function tests

File: test_my_utils.py		unit tests for my_utils.py

File: .travis.yml		uses Travis CI (continuous integration) test driven devo
				runs essentially same things as bash file run.sh, but does in Travis CI
				https://travis-ci.com (has access to github repo)
