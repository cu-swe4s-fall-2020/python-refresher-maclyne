""" get Covid19 rates for plotting
    Per Captia Rates are per 100,000 people

    Initial date: 22 Oct 2020 for HW5
    Author: Margot Clyne
    Updated: Nov 29 add ability to get and plot multiple counties
            Also consolidate required vs optional args in argparse
            No longer plots in this script

    File get_rates.py
"""
from my_utils import get_column
from my_utils import binary_search
from my_utils import plot_lines
from my_utils import make_statefile
import sys
import argparse
from operator import itemgetter
from datetime import datetime
import numpy as np

def main():
    """
    get Covid19 case data and census data and convert to per-capita rates
    data are from two different files.
    Per Capita Rates are per 100,000 people

    Required Args:
    ---------------
    state: str        Name of USA State (No abbreviations)
    coviddata_countys_list: list of str
    
    Optional Args (have defaults): see argparser section
    -------------------------------------------
    data_out_file: str  name of CSV file if want one to be made. or '[]'
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
    out_data : list of lists of lists:
                [census_countys_list,
                 [[dates for c1],[dates for c2],..],
                 [per_capita_rates c1],[per_capita_rates c2],...]
    Where:
    ------
    per_capita_rates: list
            list of cases / population
            (these are per 100,000 people)

    dates: list
            list of dates in format datetime.date(YYYY, MM, D)

    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description='process args for \
                                     reading covid data CSV file')

    parser.add_argument('--state',
                        type=str,
                        help='Name of the State',
                        required=True)

    parser.add_argument('--coviddata_countys_list',
                        type=str,
                        nargs='+',
                        help='list of strings for \
                        Name(s) of the county(s) in covid CSV file \
                        that we want to look at',
                        required=True)

    parser.add_argument('--data_out_file',
                        type=str,
                        help='Name of the CSV file to write this data \
                                out to. If not wanted, is "[]", which\
                                is coded to not return any data_out_file',
                        default='[]')
    
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
                        help='daily newcases. default is cumulativ dailycases')

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
    state = args.state
    coviddata_countys_list = args.coviddata_countys_list
    data_out_file = args.data_out_file
    coviddata_file_name = args.covid_file_name
    coviddata_county_column = args.coviddata_county_column
    cases_column = args.cases_column
    date_column = args.date_column
    daily_new = args.daily_new
    running_avg = args.running_avg
    window = args.window
    census_file_name = args.census_file_name
    census_state_column = args.census_state_column
    census_county_column = args.census_county_column
    pop_column = args.pop_column


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
    
    elif coviddata_file_name == 'covid-19-data/'+state+'-counties.csv':
            state_coviddata_file_name = coviddata_file_name
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

    # get census data for all counties in the state
    census_state_data = get_column(census_file_name, census_state_column,
                                   state,
                                   result_columns=[census_county_column,
                                                   pop_column],
                                   date_column=None)
   
    # sort census_state_data by county name
    # census_state_data is of list [[county_names], [census2010pops])
    sorted_pairs = sorted(zip(census_state_data[0], census_state_data[1]))
    tuples = zip(*sorted_pairs)
    list1, list2 = [list(tuple) for tuple in tuples]
    census_state_data_sorted = [list1, list2]

    # pre-allocate structure of out_data list of lists of lists
    #   out_data[0] will be coviddata_countys_list
    #   out_data[1] will be list of dates for each county
    #   out_data[2] will be list of per_capita_rates for each county
    out_data = [[], [], []]

    # run for each county
    for county_index in range(0, len(coviddata_countys_list)):
        coviddata_county_name = coviddata_countys_list[county_index]
        out_data[0].append(coviddata_county_name)
        # run get_column() on covid data and census data
        cases_data_cumulative = get_column(state_coviddata_file_name,
                                           coviddata_county_column,
                                           coviddata_county_name,
                                           result_columns=[cases_column],
                                           date_column=date_column,
                                           return_dates=True)

        # convert cases from type str to int
        cases_data_cumulative[0] = list(map(int, cases_data_cumulative[0]))

        # dates are stored in last index of list, in datetime format
        dates = cases_data_cumulative[-1]

        # daily cases option
        if daily_new is True:
            from my_utils import get_daily_count
            cases = get_daily_count(cases_data_cumulative[0])  # not dates column
        else:
            cases = cases_data_cumulative[0]

        # print runing average cases option
        if running_avg is True:
            from my_utils import running_average
            cases = running_average(cases, window)

        # use binary search to get county pop census data out of state data
        census_county_name = coviddata_county_name + ' County'
        county_pop = binary_search(census_county_name, census_state_data_sorted)

        # raise error if county census not found
        if county_pop is None:
            ValueError
            print('county census not found')
            sys.exit(1)

        county_pop = int(county_pop)

        # convert cases to per-capita rates by dividing county case by population
        if type(cases) == list:
            cases = np.asarray(cases)

        per_capita_rates = np.round(cases / county_pop * 100000,2)

        # convert per_capita_rates back from nparray to list
        per_capita_rates = per_capita_rates.tolist()

        # append to out_data lists
        out_data[1].append([dates])
        out_data[2].append([per_capita_rates])

##    print(out_data)

    # write out_data to a CSV file in format 'County','date','per_capita_rate'
    if data_out_file != '[]':
        fout = open(data_out_file, 'w')
        fout.write("county,date,per_capita_rate \n" )
        for county_index in range(0, len(out_data[0])):
            print(out_data[0][county_index],'out_data[0][county_index]')
            for date_ind in range(0, len(out_data[1][county_index][0])):
                #print(out_data[1][county_index][0][date_ind],'out_data[1][county_index][0][date_ind]')
                fout.write(out_data[0][county_index]+','+ str(out_data[1][county_index][0][date_ind])+','+ str(out_data[2][county_index][0][date_ind])+'\n')
        fout.close()

    return out_data


if __name__ == '__main__':
    main()
