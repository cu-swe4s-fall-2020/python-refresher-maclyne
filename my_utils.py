def get_column(file_name, query_column, query_value, result_column):
    f = open(file_name, 'r')
    out_list = []
    for l in f:
        A = l.rstrip().split(',')
        if A[query_column] == query_value:
            out_list.append(A[result_column])

    f.close()

    return out_list


