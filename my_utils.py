"""Various utilities

    * get_column - use for reading a CSV file and retrieving results filtered by query value

"""
import array
import numpy as np 
import sys

def get_column(file_name, query_column, query_value, result_column=1):
    """
    Reads a CSV file and outputs the values of the results corresponding to the lines in which the query value is met

    required imports:
    ---------
    array

    Parameters
    ----------
    file_name: string       name of the CSV file (including path if needed)

    query_column: int       index number of the column containing the query in the CSV file

    query_value: string     the desired value to flter the query_column by

    results_column: int     index number of the column containing the results in the CSV file

    Returns
    ---------
    out_array: array of integers     an array of integers in the results column filtered by lines corresponding to the query_value

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
    out_array = array.array('i',[])
    # parse through file lines
    for l in f:
        A = l.rstrip().split(',')
        # filter lines by where query_value is met and append results to output array
        if A[query_column] == query_value:
            out_array.append(int(A[result_column]))

    f.close()

    return out_array

def get_daily_count(cumulative_values):
    """
    takes cumulative values in nytimes/covid-19 repo and returns daily numbers (today minus yesterday)
    
    Parameters
    ----------
    cumulative_values: array of integers      cumulative daily cases (example: output from get_column() )

    Returns
    ----------
    daily_values: array of integers      number of daily new cases   

    """
    daily_values = np.zeros(len(cumulative_values))
    for d in np.arange(1,len(cumulative_values)):
        daily_values[d] = cumulative_values[d] - cumulative_values[d-1] 

    return daily_values

def running_average(daily_values, window=5):
    """
    calculated the running average of an array over a given window. 
    The average is taken over the current and previous values, not future values.
    During the first days when the cumulative number of days is below the window, the running average until that point is taken

    Parameters
    ----------
    daily_values:   array of integers       number of daily new cases (or deaths, etc)

    window: integer     number of days over which to do the running average window

    Returns
    ---------
    running_avg_values: array of floats     the running average at each day for the given window size
    """
    running_avg_values = np.zeros(len(daily_values))
    # running avg while cumulative number of days < window:
    for d in np.arange(0,window):
        running_avg_values[d] = np.average(daily_values[0:d+1])
    # once cumulative number of days has reached window size, use that same window size for the rest of the data
    for d in np.arange(window,len(daily_values)):
        running_avg_values[d] = np.average(daily_values[d-window+1:d+1])

    return running_avg_values

def main():
    """
    main function. Currently blank because this file is only a library

    will update main function if anything needs to be added to this file that isnt a library. This is a placeholder.
    """
    print('main function in my_utils.py is run')
    
    return None


if __name__ == '__main__':
    main()
