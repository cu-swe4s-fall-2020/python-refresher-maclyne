"""Various utilities

    * get_column - reads a CSV file and gets results filtered by query value
    * has_decreasing_values - tells if array of ints has any decreasing vals \
                              when read in order(returns bool)
    * get_daily_count - takes cumulative values of cases deliminated daily \
                        and returns daily numbers (today minus yesterday)
    * running_average - running average of an array (moving forward) using \
                        a given window size \
                        note: moving window covers only past and current values
    * binary_search - a binary search of sorted data

"""
import array
import numpy as np
import sys
import datetime
from datetime import date


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
    file_name: string       
                name of the CSV file (including path if needed)

    query_column: int       
                index number of column query in CSV file

    query_value: string     
                the desired value to flter the query_column by

    results_columns: list of int     
                index numbers of columns results in CSV file

    date_column: int (or None)
                index number of column dates in CSV file
                dates must be in isoformat (strings).

    return_dates: bool
                if True, function returns dates_list as the
                final list in the returned list of lists


    Returns
    ---------
    hits: list of list of int    
               of values from  results columns \
               filtered by lines that have the query_value
               gaps in dates are filled in
    """
    # catch possible exceptions when opening files
    try:
        f = open(file_name, 'r')
    except FileNotFoundError:
        print("Couldn't find file " + file_name)
        sys.exit(1)
    except PermissionError:
        print("Couldn't access file " + file_name)
        sys.exit(1)

    # open and read file
    f = open(file_name, 'r')
    hits = []
    for result_column in result_columns:
        hits.append([])
    dates_list = []
    # if date_column == None, do short version
    if date_column == None:
        # parse through file lines
        for line in f:
            A = line.rstrip().split(',')
            # filter by where query_value is met
            if A[query_column] == query_value:
                for result_column_ind in np.arange(len(result_columns)):
                    hits[result_column_ind].append(int(A[result_columns[result_column_ind]]))
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
                    ##dates_list.append(A[date_column])
                    for result_column_ind in np.arange(len(result_columns)):
                        hits[result_column_ind].append(int(A[result_columns[result_column_ind]]))
                # track dates and fill any gaps
                else:
                    date_last = dates_list[-1]
                    ##date_last = date.fromisoformat(dates_list[-1])
                    ##dates_list.append(A[date_column])
                    date_now = date.fromisoformat(A[date_column])
                    delta = date_now - date_last
                    gap = delta.days
                    if gap < 0:
                        ValueError
                        print('dates out of order, system exit')
                        sys.exit(4)
                    else:
                        while gap > 1:
                            for result_column_ind in np.arange(len(result_columns)):
                                hits[result_column_ind].append(hits[result_column_ind][-1])
                                dates_list.append(date_last) 
                            gap = gap - 1
                        # now that gap is closed, append new data
                        for result_column_ind in np.arange(len(result_columns)):
                            hits[result_column_ind].append(int(A[result_columns[result_column_ind]]))
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


def get_daily_count(cumulative_values):
    """
    takes cumulative values of cases deliminated daily \
            and returns daily numbers (today minus yesterday)

    Parameters
    ----------
    cumulative_values: array of int      cumulative daily cases
                                        (example: output from get_column() )

    Returns
    ----------
    daily_values: array of int      number of daily new cases
    """
    if has_decreasing_values(cumulative_values) is True:
        ValueError
        print('cumulative_values are decreasing somewhere. sys.exit(2)')
        sys.exit(2)

    daily_values = np.zeros(len(cumulative_values))
    daily_values[0] = cumulative_values[0]
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
    daily_values:   array of int       number daily new cases (or deaths, etc)

    window: int     number of days over which to do the running average window

    Returns
    ---------
    running_avg_values: array of floats     running average at each day \
                                                for the given window size
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

def binary_search(key,data):
    """
    binary search of sorted data

    Parameters:
    -----------
    key - the value we want to find

    data - a sorted list of lists we are searching through
            of format [[keys],[values]]

    Outputs:
    ----------
    value - the value of data matching the key.
            note: returns None if value not found

    """
    low = -1
    high = len(data)
    while (high - low > 1):
        mid = (high + low) // 2
        if key == data[mid][0]:
            value = data[mid][1]
            return value
        if (key < data[mid][0]):
            high = mid
        else:
            low = mid
    return None

def main():
    """
    main function. Currently blank because this file is only a library

    """
    print('main function in my_utils.py is run')
    return None


if __name__ == '__main__':
    main()
