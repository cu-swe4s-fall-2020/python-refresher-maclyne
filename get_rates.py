""" get Covid19 rates

    Initial date: 22 Oct 2020
    Author: Margot Clyne

    File get_rates.py
"""
from my_utils import get_column
from my_utils import binary_search
import sys
import argparse
from operator import itemgetter
from datetime import datetime

def main():
    """
    get Covid19 case data and census data and convert to per-capita rates
    data are from two different files

    Returns:
    ---------
    per_capita_rates: list
            list of cases / population

    dates: list
            list of dates in format datetime.date(YYYY, MM, D)

    """
    # TODO: add main def docstring

    # parse command line arguments
    parser = argparse.ArgumentParser(description='process args for \
                                     reading covid data CSV file')

    parser.add_argument('--covid_file_name',
                        type=str,
                        help='Name of the input covid cases data file',
                        required=True)

    parser.add_argument('--census_file_name',
                        type=str,
                        help='Name of the input census data file',
                        required=True)

    parser.add_argument('--state',
                        type=str,
                        help='Name of the State'
                        required=True)

    parser.add_argument('--county',
                        type=str,
                        help='Name of the county'
                        required=True)

    parser.add_argument('--coviddata_county_column',
                        type=int,
                        help='column number in covid CSV file denoting county names')

    parser.add_argument('--cases_column',
                        type=int,
                        help='column number in covid CSV file denoting number of cases')

    parser.add_argument('--date_column',
                        type=int,
                        default=0,
                        help='column number in covid CSV file denoting date')

    parser.add_argument('--census_state_column',
                        type=int,
                        help='column number in census CSV file denoting state names')

    parser.add_argument('--census_county_column',
                        type=int,
                        help='column number in census CSV file denoting county names')

    parser.add_argument('--pop_column',
                        type=int,
                        help='column number in census CSV file denoting population data')

    parser.add_argument('--daily_new',
                        type=bool,
                        default=False,
                        help='daily new cases. default is cumulative daily cases')

    parser.add_argument('--running_avg',
                        type=bool,
                        default=False,
                        help='running average of cases.\
                                default is False, window size is required')

    parser.add_argument('--window',
                        type=int,
                        default=5,
                        help='Window size of running average')


    # parse arguments and store them in args
    args = parser.parse_args()

    # assign arguments
    coviddata_file_name = args.covid_file_name
    coviddata_county_column = args.coviddata_county_column
    county = args.county
    cases_column = args.cases_column
    date_column = args.date_column
    daily_new = args.daily_new
    running_avg = args.running_avg
    window = args.window
    census_file_name = args.census_file_name
    census_state_column = args.census_state_column
    state = arg.state
    census_county_column = args.census_county_column
    pop_column = args.pop_column
    
    # run get_column() on covid data and census data
    cases_data_cumulative = get_column(coviddata_file_name, coviddata_county_column, county,
                            result_columns=[cases_column], 
                            date_column=date_column, return_dates=True)

    census_state_data = get_column(census_file_name, census_state_column, state,
                            result_columns=[census_county_column, pop_column], 
                            date_column=None) # Note: these arge might be different

    # dates are stored in last index of list, in datetime format
    dates = cases_data_cumulative[-1] #requires return_dates=True in get_column()

    # daily cases option
    if daily_new is True:
        from my_utils import get_daily_count
        cases = get_daily_count(cases_data_cumulative[:-1]) #exclude dates column
    else:
        cases = cases_data_cumulative[:-1]

    # print runing average cases option
    if running_avg is True:
        from my_utils import running_average
        cases = running_average(cases, window)
    

    # use binary search to get county pop census data out of state data
    # census_state_data is of list [[county_names], [census2010pops])
    county_pop = binary_search(county, census_state_data)

    # raise error if county census not found
    if county_pop == None
        ValueError
        print('county census not found')
        sys.exit(1)

    # convert cases to per-capita rates by dividing county case by population

    per_capita_rates = cases / county_pop

    return per_capita_rates, dates


if __name__ == '__main__':
    main()
