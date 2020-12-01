import array
import sys

state = sys.argv[1]

file_name = 'covid-19-data/us-counties.csv'
outfile_name = 'covid-19-data/'+state+'-counties.csv'
query_column = 2
query_value = state

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
# print all lines where query_column == query_value
for line in range(len(out_line_list)):
    fout.write(out_line_list[line])

fout.close()

