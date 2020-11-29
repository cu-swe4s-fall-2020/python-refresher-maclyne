""" Covid19 rates per capita by State County using hash tables
    Rates are per 100,000 people

    Initial date: 9 Nov 2020
    Author: Margot Clyne

    File: get_daily_rates.py (based on code from get_rates.py) but now\
            upgraded by using hash tables instead of sorting and searching lists

    Summary:
    --------
    * Take a state name and a date as command line parameters.
    * Make a hash table where the keys are county names and\
    the values are populations.
    * Loop over all of the counties in that state and print the\
    county name and case rate for the given day.
"""
from my_utils import get_column
from my_utils import binary_search
from my_utils import plot_lines
from my_utils import make_statefile
import hash_table
import sys
import argparse
from datetime import date
from operator import itemgetter


def main():
    """
    calculate the number of covid19 cases per capita\
    for each county in a given State for a given date.
    Cases are per 100,000 people and rounded to 1 decimal
   
    Required Args:
    ---------------
    state: str        Name of USA State (No abbreviations)
    query_date: str   date in ISO format 'YYYY-MM-DD'

    Optional Args (have defaults): see argparser section
    -------------------------------------------
    covid_file_name: str
    census_file_name: str
    daily_new: bool     default=True
    running_avg: bool   default=False
    window: int
    coviddata_county_column: int *
    cases_column: int *
    date_column: int *
    census_state_column: int *
    census_county_column: int *
    pop_column: int *

    Note: *= only needs to be changed if format of 
         covid19 and census data files are changed

    Returns:
    ---------
    out_lists: list of [str, float]
                        [county_name, county_caserate_at_date]

    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description='process args for \
                                     reading covid data CSV file')

    parser.add_argument('--state',
                        type=str,
                        help='Name of the State',
                        required=True)

    parser.add_argument('--query_date',
                        type=str,
                        help='date in ISO format "YY-MM-DD" ',
                        required=True)

    parser.add_argument('--covid_file_name',
                        type=str,
                        help='Name of the input covid cases data file',
                        default='covid-19-data/us-counties.csv')

    parser.add_argument('--census_file_name',
                        type=str,
                        help='Name of the input census data file',
                        default='census-data/co-est2019-alldata.csv')
    
    parser.add_argument('--coviddata_county_column',
                        type=int,
                        help='column ind for county names in covid CSVfile',
                        default=1)

    parser.add_argument('--cases_column',
                        type=int,
                        help='column ind for number of cases in covid CSVfile',
                        default=4)

    parser.add_argument('--date_column',
                        type=int,
                        default=0,
                        help='column ind for date in covid CSV file')

    parser.add_argument('--census_state_column',
                        type=int,
                        help='column ind for state names in census CSV file',
                        default=5)

    parser.add_argument('--census_county_column',
                        type=int,
                        help='column ind for county names in census CSV file',
                        default=6)

    parser.add_argument('--pop_column',
                        type=int,
                        help='column ind for populaiton in census CSV file',
                        default=7)

    parser.add_argument('--daily_new',
                        type=bool,
                        default=True,
                        help='daily newcases. False gives cumulativ cases')

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
    cases_column = args.cases_column
    date_column = args.date_column
    daily_new = args.daily_new
    running_avg = args.running_avg
    window = args.window
    census_file_name = args.census_file_name
    census_state_column = args.census_state_column
    state = args.state
    census_county_column = args.census_county_column
    pop_column = args.pop_column
    query_date = date.fromisoformat(args.query_date)

    # make CSV file copy of only state covid-19-data
    # TODO: make this ^ into Snakefile
    if coviddata_file_name == 'covid-19-data/us-counties.csv':
        state_coviddata_file_name ='covid-19-data/'+state+'-counties.csv'
        try:
            f1 = open(state_coviddata_file_name, 'r')
            f1.close()
        except FileNotFoundError:
            print('creating state_covidfile')
            state_coviddata_file_name = make_statefile(state)
            print(state_coviddata_file_name, 'state_coviddata_file_name')
    else:
        Warning('This script must be run on data within only \
                one state or else has error if counties of \
                the same name in different states across USA.\
                if not using default args.covid_file_name, please\
                check that county names are not duplicated.\
                NOTE: Proceeding by assigning variable\
                state_coviddata_file_name = args.covid_file_name ;\
                Watch out for errors from this issue.')
        state_coviddata_file_name = args.covid_file_name
    
    # get state county names and population data from census file
    census_state_data = get_column(census_file_name, census_state_column,
                                   state,
                                   result_columns=[census_county_column,
                                                   pop_column],
                                   date_column=None)
    county_pop_list = census_state_data[1][1:]
    
    # census file has names as "countyname + County", so rm " County"
    county_names_list_withcounty = census_state_data[0][1:]
    county_names_list = []
    for c in range(len(county_names_list_withcounty)):
        county_names_list.append(county_names_list_withcounty[c][:-7])

    # make hashtable of (key-county_name, value= county_pop)
    N = 260  #hashtable size. Max number of counties in a State is Texas with 254
    census_hashtable = [ [] for i in range(N) ]
    for c in range(len(county_names_list)):
        hash_table.put(census_hashtable, N, county_names_list[c],
                       county_pop_list[c], method='rolling')

    # daily cases option and running avg cases option
    if daily_new is True:
        from my_utils import get_daily_count
    if running_avg is True:
        from my_utils import running_average
    
    # Loop through each county in state
    out_lists = []
    for c in range(len(county_names_list)):
        county_cases_data_cumulative = get_column(state_coviddata_file_name,
                                                  coviddata_county_column,
                                                  county_names_list[c],
                                                  result_columns=[cases_column],
                                                  date_column=date_column,
                                                  return_dates=True)
        # dates are stored in last index of list, in datetime format
        dates = county_cases_data_cumulative[-1]
        # convert cases from type str to int
        county_cases = list(map(int, county_cases_data_cumulative[0]))

        # daily cases option and running avg options
        if daily_new is True:
            county_cases = get_daily_count(county_cases)
        if running_avg is True:
            county_cases = running_average(county_cases, window)

        # binary search for county cases at date
        county_cases_at_date = binary_search(query_date, [dates, county_cases])
        # case rate per 100,000 people
        if county_cases_at_date is not None:
            county_caserate_at_date = county_cases_at_date * 100000 \
                                      / int(hash_table.get(census_hashtable,
                                            N,
                                            county_names_list[c],
                                            method='rolling'))
            out_lists.append([county_names_list[c],
                             round(county_caserate_at_date,1)])
    print(out_lists)
    return out_lists


if __name__ == '__main__':
    main()
