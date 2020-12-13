import array

file_name = 'covid-19-data/us-counties.csv'
outfile_name = 'covid-19-data/us-counties-testfile-Colorado2.csv'
query_column = 2
query_value = 'Colorado'
# outfile_name = 'covid-19-data/us-counties-testfile-Boulder.csv'
# query_column = 1
# query_value = 'Boulder'
# outfile_name = 'covid-19-data/us-counties-testfile-Sedgwick.csv'
# query_column = 1
# query_value = 'Sedgwick'

f = open(file_name, 'r')
out_line_list = []
# parse through file lines
for line in f:
    A = line.rstrip().split(',')
    # filter lines by where query_value met and append results to output array
    if A[query_column] == query_value:
        out_line_list.append(line)

f.close()

fout = open(outfile_name, 'w')
# write header
fout.write("date,county,state,fips,cases,deaths \n")
# print last 20 lines where query_column == query_value
for line in range(len(out_line_list)-20, len(out_line_list)):
# #for line in range(len(out_line_list)):
    fout.write(out_line_list[line])

fout.close()
