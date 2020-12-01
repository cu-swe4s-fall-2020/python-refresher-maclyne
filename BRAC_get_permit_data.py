""" get Cycling race permit data during the Covid19 pandemic

    Initial date: 30 Nov 2020
    Author: Margot Clyne

    File BRAC_get_permit_data.py

    * get_county_names_all - make master list of all BRAC counties \
            involved with this dataset
    * BRAC_get_permit_data_with_caserates - for each race, \
            get county caserate per capita at that date.\
            return output: a copy of the BRAC permit dataset file with an\
            extra new column of county caserate per capita.
"""
from my_utils import get_column
from my_utils import remove_list_duplicates
import sys
import argparse
from datetime import date

def get_county_names_all(file_name):
    '''
    make master list of all BRAC counties involved with this dataset

    Parameter:
    ---------
    file_name: str      name of BRAC permit dataset CSV file
                        example: 'BRAC_races_permits.csv'

    Returns:
    ---------
    all_countys: list of str
                        list of unique names of all Counties
                        That are in the dataset
    '''
    # parse command line arguments
    parser = argparse.ArgumentParser(description='process args for \
                                     reading BRAC cycling permits file')

    parser.add_argument('--file_name',
                        type=str,
                        help='Name of the BRAC permits data file',
                        required=True)
    
    args = parser.parse_args()
    file_name = args.file_name

    # hard coded values:
    permit_column = 4
    county_column = 2

    # run get_column() to get BRAC permit data
    BRAC_permits_yes = get_column(file_name, permit_column, 'yes',
                       result_columns=[county_column], date_column=None,
                       return_dates=False)

    BRAC_permits_no = get_column(file_name, permit_column, 'no',
                       result_columns=[county_column], date_column=None,
                       return_dates=False)

    countys_yes = BRAC_permits_yes[0]
    countys_no = BRAC_permits_no[0]

    # make all_countys unique list of all countys involved
    all_countys = remove_list_duplicates(countys_yes.append(countys_no))
    print(all_countys)
    return all_countys

def BRAC_permit_data_with_caserates(BRAC_county_caserates_file,
                                    BRAC_race_info_file):
    """
    for each race, get county caserate per capita at that date.\
            return output: a copy of the BRAC permit dataset file with an\
            extra new column of county caserate per capita.

    Parameters:
    -----------
    BRAC_county_caserates_file: str
                                string path name of file containing
                                data output from get_rates.py\
                                File is of format:
                                [list, list of lists, list of lists]
                                where the first list is of county names,\
                                the second list of lists is of dates,\
                                the third list of lists is of caserates per\
                                capita (per 100,000 populaiton). The superlists\
                                correspond to the countys, and the \
                                sublists are the data for each county.
                                

    BRAC_race_info_file: str 
                        name of BRAC permit dataset CSV file
                        example: 'BRAC_races_permits.csv'

                        

    Returns:
    --------
    out_dataset_file: str   string path name of CSV out file
                        'BRAC_countycases_at_races.csv'
    """
    # parse command line arguments
    parser = argparse.ArgumentParser(description='process args for \
                                     BRAC_permit_data_with_caserates')

    parser.add_argument('--BRAC_county_caserates_file',
                        type=str,
                        help='Name of the data file containing\
                                countynames, dates, caserates for\
                                counties involving BRAC race permits',
                        required=True)

    parser.add_argument('--BRAC_race_info_file',
                        type=str,
                        help='Name of the BRAC permits data file',
                        required=True)
    
    args = parser.parse_args()
    BRAC_county_caserates_file = args.BRAC_county_caserates_file
    BRAC_race_info_file = args.BRAC_race_info_file

    # get caserate timeseries lists data
    f1 = open(BRAC_county_caserates_file, 'r')
    cases_data = f1.read()
    cases_data_countys = cases_data[0]
    cases_data_dates_lists = cases_data[1]
    cases_data_rates_lists = cases_data[2]
    f1.close()

    # Import BRAC races data
    BRAC_races = get_column(BRAC_race_info_file, state_column, 'Colorado',
                       result_columns=[1, 2, 3, 4], date_column=None,
                       return_dates=False)

    # make variables from BRAC_races columns easier to follow
    BRAC_races_racenames = BRAC_races[0]
    BRAC_races_countys = BRAC_races[1]
    BRAC_races_dates_iso= BRAC_races[2]
    BRAC_races_permits = BRAC_races[3]
    
    # convert BRAC dates from iso format to match cases_data format
    BRAC_races_dates = []
    for r_date in range(len(BRAC_races_racenames)):
        BRAC_races_dates.append(date.fromisoformat(BRAC_races_dates_iso[r_date]))

    # match races to caserates
    caserate_races = []
    for race in range(len(BRAC_races_racenames)):
            county_ind = cases_data_countys.index(BRAC_races_countys[race])
            date_ind = cases_data_dates_lists[county_ind][0].index(BRAC_race_dates[race])
            caserate_atrace = cases_data_rates_lists[county_ind][0][date_ind]
            caserate_races.append(caserate_atrace)

    # write data to new file that is a copy of old file with added column:
    fin = open(BRAC_race_info_file, 'r')
    out_line_list = []
    # parse through file lines
    for l in fin:
        out_line_list.append(l)
    fin.close()

    fout = open(out_dataset_file, 'w')
    # write header
    fout.write("state,race name,county,date,permit approved y/n, \
                county caserate per capita 100000 ppl \n")
    # print all lines of previus file but with caserates added as new column
    for line in range(len(out_line_list)):
        out_line_list[line].append(','+str(caserate_races[line]))
        fout.write(out_line_list[line])

    fout.close()
    
    return out_dataset_file

