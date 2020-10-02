import array

file_name = 'covid-19-data/us-counties-Copy1.csv'
outfile_name = 'covid-19-data/us-counties-testfile-Boulder.csv'
query_column = 1
query_value = 'Boulder'

f = open(file_name, 'r')
out_line_list = []
# parse through file lines
for l in f:
    A = l.rstrip().split(',')
    # filter lines by where query_value is met and append results to output array
    if A[query_column] == query_value:
        out_line_list.append(l)
            
f.close()

fout = open(outfile_name, 'w')
# write header
fout.write("date,county,state,fips,cases,deaths \n" )
# print last 20 lines where query_column == query_value
for line in range(len(out_line_list)-20,len(out_line_list)):
    fout.write(out_line_list[line])

fout.close()

