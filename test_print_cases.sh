test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

# functional tests for print_cases.py
run test_shouldwork python print_cases.py --file_name covid-19-data-old/us-counties-testfile-Boulder.csv --county Boulder --county_column 1 --cases_column 4
assert_in_stdout 'cumulative cases by each date:'
assert_no_stderr 



run test_shouldwork_daily_and_avg python print_cases.py --file_name covid-19-data-old/us-counties-testfile-Boulder.csv --county Boulder --county_column 1 --cases_column 4 --daily True --running_avg True --window 5
assert_in_stdout 'cumulative cases by each date:'
assert_in_stdout 'daily cases:'
assert_in_stdout 'running average cases'
assert_no_stderr

run test_badfile python print_cases.py --file_name 'name-of-some-file-that-doesnt-exist-in-path.csv' \
	--county Boulder --county_column 1 --cases_column 4
assert_in_stdout "Couldn't find file "
assert_exit_code 1

run test_date_out_of_order python print_cases.py --file_name covid-19-data-old/us-counties-testfile-Boulder-fakemissingdates-badorder.csv --county Boulder --county_column 1 --cases_column 4 --daily True --running_avg True --window 5 --date_column 0
assert_in_stdout 'dates out of order, system exit'
assert_exit_code 4

