"""Various utilities

    * get_column - use for reading a CSV file and retrieving results filtered by query value

"""
import array

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

def main():
    """
    main function. Currently blank because this file is only a library

    will update main function if anything needs to be added to this file that isnt a library. This is a placeholder.
    """
    print('main function in my_utils.py is run')
    
    return None


if __name__ == '__main__':
    main()
