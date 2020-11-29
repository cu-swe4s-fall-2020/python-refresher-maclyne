"""Various utilities

    * make_statefile - extracts and makes state file of covid CSV file county \
                       data specifically from covid-19-data/us-counties.csv
    * get_column - reads a CSV file and gets results filtered by query value
    * has_decreasing_values - tells if array of ints has any decreasing vals \
                              when read in order(returns bool)
    * get_daily_count - takes cumulative values of cases deliminated daily \
                        and returns daily numbers (today minus yesterday)
    * running_average - running average of an array (moving forward) using \
                        a given window size \
                        note: moving window covers only past and current values
    * binary_search - a binary search of sorted data

    * plot_lines - Take a list of list of points and plot each list as a line
"""
import array
import numpy as np
import sys
import datetime
from datetime import date
from datetime import timedelta

def make_statefile(state):
    '''
    extracts and makes state file of covid CSV file county \
    data specifically from covid-19-data/us-counties.csv
    
    Parameters:
    ------------
    state   : str
              USA State name (capitalized first letter)
    
    Out:
    -----------
    state_outfile_name: str
                        copies data to outfile_name
    '''
    infile_name = 'covid-19-data/us-counties.csv'
    state_outfile_name = 'covid-19-data/'+state+'-counties.csv'
    query_column = 2
    query_value = state
    
    f = open(infile_name, 'r')
    out_line_list = []
    # parse through file lines
    for l in f:
        A = l.rstrip().split(',')
        # filter lines by where query_value is met and append results to output array
        if A[query_column] == query_value:
            out_line_list.append(l)

    f.close()

    fout = open(state_outfile_name, 'w')
    # write header
    fout.write("date,county,state,fips,cases,deaths \n" )
    # print all lines where query_column == query_value
    for line in range(len(out_line_list)):
        fout.write(out_line_list[line])

    fout.close()
    return state_outfile_name

def get_column(file_name, query_column, query_value, result_columns=[1],
               date_column=None, return_dates=False):
    """
    Reads a CSV file and outputs the values of the results corresponding \
            to the lines in which the query value is met

    Robust to missing or out of order dates:
    gaps (missing) dates padded in with no new cases
    our of order dates raises a ValueError and exits

    required imports:
    ---------
    array

    Parameters
    ----------
    file_name       : string
                    name of the CSV file (including path if needed)

    query_column    : int
                    index number of column query in CSV file

    query_value     : string
                    the desired value to flter the query_column by

    results_columns : list of int
                    index numbers of columns results in CSV file

    date_column     : int (or None)
                    index number of column dates in CSV file
                    dates must be in isoformat (strings).

    return_dates    : bool
                    if True, function returns dates_list as the
                    final list in the returned list of lists


    Returns
    ---------
    hits            : list of list of int
                    of values from  results columns
                    filtered by lines that have the query_value
                    gaps in dates are filled in
    """
    # catch possible exceptions when opening files
    try:
        f = open(file_name, 'r', encoding='ISO-8859-1')
        f.close()  # NOTE: added line to rm file not closed error. idk if right
    except FileNotFoundError:
        print("Couldn't find file " + file_name)
        sys.exit(1)
    except PermissionError:
        print("Couldn't access file " + file_name)
        sys.exit(1)

    # open and read file
    f = open(file_name, 'r', encoding='ISO-8859-1')
    hits = []
    for result_column in result_columns:
        hits.append([])
    dates_list = []
    # if date_column == None, do short version
    if date_column is None:
        # parse through file lines
        for line in f:
            A = line.rstrip().split(',')
            # filter by where query_value is met
            if A[query_column] == query_value:
                for ind in np.arange(len(result_columns)):
                    hits[ind].append(A[result_columns[ind]])
    # if there is a date_column, ensure no gaps and in order
    else:
        # parse through file lines
        for line in f:
            A = line.rstrip().split(',')
            # filter by where query_value is met
            if A[query_column] == query_value:
                # simply append data first time query value is reached
                if dates_list == []:
                    dates_list.append(date.fromisoformat(A[date_column]))
                    for ind in np.arange(len(result_columns)):
                        hits[ind].append(A[result_columns[ind]])
                # track dates and fill any gaps
                else:
                    date_last = dates_list[-1]
                    date_now = date.fromisoformat(A[date_column])
                    delta = date_now - date_last
                    gap = delta.days
                    if gap < 0:
                        ValueError
                        print('dates out of order, system exit')
                        sys.exit(4)
                    else:
                        add_day = 1 # added 11/9
                        while gap > 1:
                            for ind in np.arange(len(result_columns)):
                                hits[ind].append(hits[ind][-1])
                                dates_list.append(date_last + datetime.timedelta(days=add_day)) #added 11/9
                                ##dates_list.append(date_last)
                            add_day = add_day + 1 # added 11/9
                            gap = gap - 1
                        # now that gap is closed, append new data
                        for ind in np.arange(len(result_columns)):
                            hits[ind].append(A[result_columns[ind]])
                            dates_list.append(date_now)
    f.close()
    if return_dates is True:
        hits.append(dates_list)

    return hits


def has_decreasing_values(A):
    """
    check to see if there are any descreasing values
    if there are, then return True.
    If values are never decreasing, then return False

    Parameters
    ------------
    A: array of int

    Returns
    -----------
    bool    True if values ever decrease
            False if values are never decreasing (staying the same is ok)
    """
    return any(A[i] > A[i+1] for i in range(len(A)-1))


def get_daily_count(cumulative_values, allow_decreasing=True):
    """
    takes cumulative values of cases deliminated daily \
            and returns daily numbers (today minus yesterday)

    Parameters
    ----------
    cumulative_values   : array of int
                        cumulative daily cases
                        (example: output from get_column() )

    allow_decreasing    : bool
                        If True: allow for decreasing cumulative values
                        and do not call function has_decreasing_values
                        If False: check has_decreasing_values() and may
                        have Value Error sys.exit(2).
                        (This bool option was added because the covid case
                        data has non-uniform adjustments that may cause
                        cumulative decreasing values)

    Returns
    ----------
    daily_values        : array of int
                        number of daily new cases
    """
    if allow_decreasing is False:
        if has_decreasing_values(cumulative_values) is True:
            ValueError
            print('Warning: cumulative_values are decreasing somewhere.')
            sys.exit(2)

    daily_values = np.zeros(len(cumulative_values))
    try:
        daily_values[0] = cumulative_values[0]
    except IndexError:
        return None

    for d in np.arange(1, len(cumulative_values)):
        daily_values[d] = cumulative_values[d] - cumulative_values[d-1]
    return daily_values


def running_average(daily_values, window=5):
    """
    calculated the running average of an array over a given window.
    Average taken over the current and previous values, not future values.
    During the first days when the cumulative number of days is below \
            the window, the running average until that point is taken

    Parameters
    ----------
    daily_values        : array of int
                        number daily new cases (or deaths, etc)

    window              : int
                        number of days to do the running average window

    Returns
    ---------
    running_avg_values  : array of floats
                        running average at each day for given window size
    """
    running_avg_values = np.zeros(len(daily_values))
    # running avg while cumulative number of days < window:
    for d in np.arange(0, min(len(daily_values), window)):
        running_avg_values[d] = np.average(daily_values[0:d+1])
    # once cumulative number of days has reached window size, \
    # use that same window size for the rest of the data
    for d in np.arange(window, len(daily_values)):
        running_avg_values[d] = np.average(daily_values[d-window+1:d+1])

    return running_avg_values


def binary_search(key, data):
    """
    binary search of sorted data

    Parameters:
    -----------
    key     : str or int
            the value we want to find

    data    : list of two lists
            a sorted list of lists we are searching through
            of format [[keys],[values]]

    Outputs:
    ----------
    value   :
            the value of data matching the key.
            note: returns None if value not found

    """
    low = -1
    high = len(data[0])
    while (high - low > 1):
        mid = (high + low) // 2
        if key == data[0][mid]:
            value = data[1][mid]
            return value
        if (key < data[0][mid]):
            high = mid
        else:
            low = mid
    return None


def plot_lines(points, labels, file_name):
    """Take a list of list of points and plot each list as a line.
    Parameters
    ----------
    points    : list of list of points
                Each sublist corresponds to the points for one element.
                Each point has two values, the first will be the X value
                and the second the Y value
    labels    : list of strings
                Each element in lables corresponds to the sublist at the
                same poisiting in data
    file_name : string
                Name of the output file.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pylab as plt

    fig = plt.figure(figsize=(10, 3), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    i = 0
    for pairs in points:
        X = []
        Y = []
        for pair in pairs:
            X.append(pair[0])
            Y.append(pair[1])

        ax.plot(X, Y, lw=0.5)
        ax.text(X[-1], Y[-1], labels[i], size=5)

        i += 1

    plt.savefig(file_name, bbox_inches='tight')


def main():
    """
    main function. Currently blank because this file is only a library

    """
    print('main function in my_utils.py is run')
    return None


if __name__ == '__main__':
    main()
