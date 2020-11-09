""" hash functions and tables

    Initial date: 6 Nov 2020
    Author: Margot Clyne
    File: hash_table.py

    * hash_ascii_sum - hash function using ascii method
    * hash_polynomial_rolling - hash function using rolling poly method
    * put - function to put key,value into hash table
    * get - function to retrieve value mathcing query key from hashtable
"""


def hash_ascii_sum(key, N):
    '''
    hash function that takes a string and hash table size as input and using \
    ascii sum  method returns a value number less than the hashtable size
    NOTE: This is a bad method (very non-uniform output) and should be avoided

    Parameters
    -----------
    key: string     string of key

    N: int          hash table size

    Returns
    ---------
    hash_value: int     the returned hash value number. \
                        less than the table size
    '''
    s = 0
    for i in range(len(key)):
        s += ord(key[i])
    hash_value = s % N
    return hash_value


def hash_polynomial_rolling(key, N, p=53, m=2**64):
    '''
    hash function that takes a string and hash table size as input and using \
    rolling polynomial method returns a value number < the hashtable size

    Parameters
    -----------
    key: string     string of key

    N: int          hash table size

    p: int          a prime number roughly equal to the number of \
                    characters in the input alphabet

    m: int          should be a large number, since the probability of two \
                    random strings colliding is about 1/m. \
                    Sometimes m=2^64 is chosen

    Returns
    ---------
    hash_value: int     the returned hash value number. \
                        less than the table size
    '''
    # TODO: test driven development for returning None if not in table
    # TODO: test driven development for key being of type string, int, or float
    s = 0
    for i in range(len(key)):
        s += ord(key[i]) * p**i
    s = s % m
    hash_value = s % N
    return hash_value


def put(table, N, key, value, method='rolling'):
    """
    function to put key,value into hash table

    Parameters
    -----------
    table: hashtable    chain hashtable

    N: int              hash table size

    key: string         key to add in

    value: string       value corresponding to key to add in

    method: string      either 'rolling' (default) or 'ascii'\
                        this string determines whether the function of\
                        rolling_polynomial or ascii_sum will be used to\
                        find the open slot in the hash table. This must\
                        match the method the hashtable was built with
    Returns
    --------
    table: hashtable    chain hashtable with additional\
                        key,value put in a previously empty table slot
    """
    # find table slot
    if method == 'ascii':
        table_slot = hash_ascii_sum(key, N)
    elif method == 'rolling':
        table_slot = hash_polynomial_rolling(key, N)
#    else:
#        exit_with_error_code # TODO: add exit codes for method not found
    # put in table_slot
    table[table_slot].append((key, value))
    return table


def get(table, N, query_key, method='rolling'):
    """
    function to retrieve value matching query key from hashtable

    Parameters
    -----------
    table: hashtable    chain hashtable

    N: int              hash table size

    query_key: string   key we are looking to get the value of

    method: string      either 'rolling' (default) or 'ascii'\
                        this string determines whether the function of\
                        rolling_polynomial or ascii_sum will be used to\
                        find the open slot in the hash table. This must\
                        match the method the hashtable was built with
    Returns
    --------
    value: string       value corresponding to query_key.\
                        returns None if key not found.
    """
    # find table slot
    if method == 'ascii':
        table_slot = hash_ascii_sum(query_key, N)
    elif method == 'rolling':
        table_slot = hash_polynomial_rolling(query_key, N)
    else:
        exit_with_error_code  # TODO: add exit codes for method not found

    for key, value in table[table_slot]:
        if query_key == key:
            return value
    return None
