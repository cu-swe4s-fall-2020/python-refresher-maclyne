test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest 
. ssshtest

# functional tests for get_rates.py on real data daily new cases
run test_real_Boulder python get_rates.py --covid_file_name 'covid-19-data/us-counties.csv' --census_file_name 'census-data/co-est2019-alldata.csv' --state 'Colorado' --plot_file_name 'plots/Boulder_daily_new_caserates' --coviddata_county 'Boulder' --census_county 'Boulder County' --coviddata_county_column 1 --cases_column 4 --date_column 0 --census_state_column 5 --census_county_column 6 --pop_column 7 --daily_new True --running_avg False

assert_no_stderr

# functional tests for get_rates.py on real data running avg new cases
run test_real_Boulder_avg python get_rates.py --covid_file_name 'covid-19-data/us-counties.csv' --census_file_name 'census-data/co-est2019-alldata.csv' --state 'Colorado' --plot_file_name 'plots/Boulder_5dayrunningavg_new_caserates' --coviddata_county 'Boulder' --census_county 'Boulder County' --coviddata_county_column 1 --cases_column 4 --date_column 0 --census_state_column 5 --census_county_column 6 --pop_column 7 --daily_new True --running_avg True --window 5

assert_no_stderr

# functional tests for get_rates.py on Boulder testfile
run test2 python get_rates.py --covid_file_name 'covid-19-data/us-counties-testfile-Boulder.csv' --census_file_name 'census-data/co-est2019-alldata.csv' --state 'Colorado' --plot_file_name 'plots/plot_test2_getrates' --coviddata_county 'Boulder' --census_county 'Boulder County' --coviddata_county_column 1 --cases_column 4 --date_column 0 --census_state_column 5 --census_county_column 6 --pop_column 7 --daily_new True --running_avg False --window 5

assert_no_stderr

# functional test for exiting if census_county is not in census_file
run test3 python get_rates.py --covid_file_name 'covid-19-data/us-counties-testfile-Boulder.csv' --census_file_name 'census-data/co-est2019-alldata.csv' --state 'Colorado' --plot_file_name 'plots/plot_test3_getrates_FakeCounty' --coviddata_county 'Boulder' --census_county 'Fake County' --coviddata_county_column 1 --cases_column 4 --date_column 0 --census_state_column 5 --census_county_column 6 --pop_column 7 --daily_new True --running_avg False --window 5

assert_in_stdout 'county census not found'
assert_exit_code 1
