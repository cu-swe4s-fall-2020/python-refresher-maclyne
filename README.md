# Python Repository ADD OVERALL TITLE
# MCDB6440: Software Engineering for Scientists

# Step 1: get Covid19 data from NYT database
In the root directory of this repository, clone the NYT COVID-19 repo
(bash command line)           git clone https://github.com/nytimes/covid-19-data.git

or, to simply update data after already cloning once (I think??):

(bash command line)
wget https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv


# Step 2: get USA census data:
(say something about the census data?)

(bash command line)
wget https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv

# Step 3: At this point, everything should be set up to be ready to run the Snakefile
( I think??)
(command to run the Snakefile)

(explaination of Snakefile parameter options)


# (bash command contents of snakefile):

python make_statefile_cases.py 'Colorado'

python BRAC_get_permit_data.py --function_name 'get_county_names_all' --BRAC_race_info_file 'BRAC_races_permits.csv' > 'BRAC_county_names_involving_permits.txt'

COVID_COUNTYS_LIST=$(cat BRAC_county_names_involving_permits.txt | xargs printf "%s" | awk -F',' '{gsub(" ","-"); print}' | awk -F',' '{gsub(","," "); print}' | sed 's/[][]//g')

python get_rates.py --state 'Colorado' --coviddata_countys_list $COVID_COUNTYS_LIST --running_sum True --window 14 --data_out_file 'potential_BRAC_county_cases_2weeksum.txt'

python BRAC_get_permit_data.py --function_name 'BRAC_permit_data_with_caserates' --BRAC_county_caserates_file 'potential_BRAC_county_cases_2weeksum.txt' --BRAC_race_info_file 'BRAC_races_permits.csv'

LABELS=$(cat BRAC_county_names_involving_permits.txt | xargs printf "%s" | awk -F',' '{gsub(" ","-"); print}' | awk -F',' '{gsub(","," "); print}' | sed 's/[][]//g')

python ss_plots/timeseries.py --in_file 'potential_BRAC_county_cases_2weeksum.txt' --out_file 'Mass_Start_Bike_Race_Permits_during_Covid_2weeksum.png' --x_label 'Date' --y_label 'Cases Per Capita 14day sum (per 100,000 populaiton)' --height 10 --width 15 --labels $LABELS --add_overlay_data True --overlay_data_file 'BRAC_countycases_at_races.csv' --title 'Mass Start Bike Race Permits'


# Step 4?: Travis


# Below, a list of the scripts in this repo and what the do


# python-refresher

### old stuff below I need to update README file for
Objective: become familiar with python

Initial date: 17 Sept 2020
Author: Margot Clyne

Updated date: 28 Nov 2020
School assignment: For Assignment #3 of class MCDB6440: Software Engineering for Scientists


File: my_utils.py	This file imports a CSV file and outputs desired data
			function make_statefile to copy covid19 case State data to its own CSV file
			includes function get_column(file_name, query_column, query_value, result_columns=[1])
			includes function has_decreasing_values() for an array of int
			includes function get_daily_count(cumulative_values, allow_decreasing=True)
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
				updated tests to be comparing strings for get_column() outputs on Nov 9 2020

File: .travis.yml		uses Travis CI (continuous integration) test driven devo
				runs essentially same things as bash file run.sh, but does in Travis CI
				https://travis-ci.com (has access to github repo)
				updated python version to 3.8 on Nov 9 2020
