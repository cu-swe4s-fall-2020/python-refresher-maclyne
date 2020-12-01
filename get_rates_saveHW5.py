""" get Covid19 rates and plot them

    Initial date: 22 Oct 2020
    Author: Margot Clyne

    File get_rates.py
"""
from my_utils import get_column
from my_utils import binary_search
from my_utils import plot_lines
import sys
import argparse
from operator import itemgetter
from datetime import datetime
import matplotlib
import matplotlib.pylab as plt
matplotlib.use('Agg')


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

    parser.add_argument('--plot_file_name',
                        type=str,
                        help='output plot file generated',
                        required=True)

    parser.add_argument('--state',
                        type=str,
                        help='Name of the State',
                        required=True)

    parser.add_argument('--coviddata_county',
                        type=str,
                        help='Name of the county in covid CSV file',
                        required=True)

    parser.add_argument('--census_county',
                        type=str,
                        help='Name of the county in census CSV file',
                        required=True)

    parser.add_argument('--coviddata_county_column',
                        type=int,
                        help='column ind for county names in covid CSVfile')

    parser.add_argument('--cases_column',
                        type=int,
                        help='column ind for number of cases in covid CSVfile')

    parser.add_argument('--date_column',
                        type=int,
                        default=0,
                        help='column ind for date in covid CSV file')

    parser.add_argument('--census_state_column',
                        type=int,
                        help='column ind for state names in census CSV file')

    parser.add_argument('--census_county_column',
                        type=int,
                        help='column ind for county names in census CSV file')

    parser.add_argument('--pop_column',
                        type=int,
                        help='column ind for populaiton in census CSV file')

    parser.add_argument('--daily_new',
                        type=bool,
                        default=False,
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
    coviddata_file_name = args.covid_file_name
    coviddata_county_column = args.coviddata_county_column
    plot_file_name = args.plot_file_name
    coviddata_county_name = args.coviddata_county
    cases_column = args.cases_column
    date_column = args.date_column
    daily_new = args.daily_new
    running_avg = args.running_avg
    window = args.window
    census_file_name = args.census_file_name
    census_state_column = args.census_state_column
    state = args.state
    census_county_name = args.census_county
    census_county_column = args.census_county_column
    pop_column = args.pop_column

    # run get_column() on covid data and census data
    cases_data_cumulative = get_column(coviddata_file_name,
                                       coviddata_county_column,
                                       coviddata_county_name,
                                       result_columns=[cases_column],
                                       date_column=date_column,
                                       return_dates=True)

    census_state_data = get_column(census_file_name, census_state_column,
                                   state,
                                   result_columns=[census_county_column,
                                                   pop_column],
                                   date_column=None)

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

    # census_state_data is of list [[county_names], [census2010pops])
    # sort census_state_data by county name
    sorted_pairs = sorted(zip(census_state_data[0], census_state_data[1]))
    tuples = zip(*sorted_pairs)
    list1, list2 = [list(tuple) for tuple in tuples]
    census_state_data_sorted = [list1, list2]

    # use binary search to get county pop census data out of state data
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

    per_capita_rates = cases / county_pop

    # convert per_capita_rates back from nparray to list
    per_capita_rates = per_capita_rates.tolist()

    # plot using plot_lines
    plot_points = [[]]
    for point in range(0, len(per_capita_rates)):
        plot_points[0].append([dates[point], per_capita_rates[point]])

    plot_labels = ['dates', 'per_capita_rates']

    plot = plot_lines(plot_points, plot_labels, plot_file_name)

    return plot  # NOTE: idk if this line is needed?


if __name__ == '__main__':
    main()
