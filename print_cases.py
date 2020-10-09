"""print desired data filtered from CSV file of Covid19 cases

    Initial date: 17 Sept 2020, updated 21 Sept 2020
    Author: Margot Clyne

"""

from my_utils import get_column
import sys
import argparse

# parse command line arguments
parser = argparse.ArgumentParser(description='process args for \
                                 reading covid data CSV file')

parser.add_argument('--file_name',
                    type=str,
                    help='Name of the input data file',
                    required=True)

parser.add_argument('--county',
                    type=str,
                    help='Name of the county')

parser.add_argument('--county_column',
                    type=int,
                    help='column number in CSV file denoting county names')

parser.add_argument('--cases_column',
                    type=int,
                    help='column number in CSV file denoting number of cases')

parser.add_argument('--date',
                    type=str,
                    help="date of data. Must be string format 'yyyy-mm-dd' ")

parser.add_argument('--daily',
                    type=bool,
                    default=False,
                    help='print daily new cases. default is False')

parser.add_argument('--running_avg',
                    type=bool,
                    default=False,
                    help='print running average new cases.\
                            default is False, window size is required')

parser.add_argument('--window',
                    type=int,
                    default=5,
                    help='Window size of running average')

# parse arguments and store them in args
args = parser.parse_args()

# assign arguments
file_name = args.file_name
county_column = args.county_column
county = args.county
cases_column = args.cases_column
print_daily = args.daily
print_running_avg = args.running_avg
window = args.window

# call function to run
cases = get_column(file_name, county_column,
                   county, result_column=cases_column)

# print daily cases option
if print_daily is True:
    from my_utils import get_daily_count
    day_cases = get_daily_count(cases)

# print runing average cases option
if print_running_avg is True:
    from my_utils import running_average
    running_avg_cases = running_average(day_cases, window)

# print outputs. (print one value per line)
print('cumulative cases by each date:')
for c in range(0, len(cases)):
    print(cases[c])

if print_daily is True:
    print('daily cases:')
    for c in range(0, len(day_cases)):
        print(day_cases[c])

if print_running_avg is True:
    print('running average cases, window = '+str(window)+" :")
    for c in range(0, len(running_avg_cases)):
        print(running_avg_cases[c])
