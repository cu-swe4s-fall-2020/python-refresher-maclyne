"""Print desired data filtered from CSV file of Covid19 cases

    Initial date: 17 Sept 2020, updated 21 Sept 2020
    Author: Margot Clyne

"""

from my_utils import get_column
import sys
import argparse

# parse command line arguments
parser = argparse.ArgumentParser(description = 'process args for reading covid data CSV file')

parser.add_argument('--file_name',
                    type=str,
                    help='Name of the input data file',
                    required=True)

parser.add_argument('--county',
                    type=str,
                    help='Name of the county')

parser.add_argument('--county_column',
                    type=int,
                    help='column number in CSV file that denotes county names') 

parser.add_argument('--cases_column',
                    type=int,
                    help='column number in CSV file that denotes number of cases') 

parser.add_argument('--date',
                    type=str,
                    help="date of the data. Must be in string format 'yyyy-mm-dd' ")

# parse arguments and store them in args
args = parser.parse_args()

# assign arguments
file_name = args.file_name
county_column = args.county_column
county = args.county
cases_column = args.cases_column

# call function to run
cases = get_column(file_name,county_column, county,result_column=cases_column)

# print outputs
print(cases,'cumulative cases by each date')
print(cases[-1],'most recent cumulative number of cases')
