test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest 
. ssshtest

# functional tests for get_daily_rates.py on real data
run test_Colorado_Sept16 python get_daily_rates.py --state 'Colorado'  --query_date '2020-09-16'
assert_no_stderr
assert_stdout

# functional tests for get_daily_rates.py on real data Delaware
run test_Delaware_Sept16 python get_daily_rates.py --state 'Delaware' --query_date '2020-09-16'
assert_no_stderr
assert_in_stdout "[['Kent', 7.4], ['New Castle', 16.5], ['Sussex', 5.6]]"
