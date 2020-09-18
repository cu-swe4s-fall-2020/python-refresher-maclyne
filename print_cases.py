from my_utils import get_column

county='Boulder'
county_column = 1
cases_column = 4
file_name = 'covid-19-data/us-counties.csv'
cases = get_column(file_name,county_column, county,result_column=cases_column)
print(cases,'cumulative cases by each date')
print(cases[-1],'most recent cumulative number of cases')
