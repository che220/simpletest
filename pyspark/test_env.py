def selectNumericColumns(df):
    numCols = []
    for col in df.dtypes:
        if col[1] == 'bigint' or col[1] == 'double':
            numCols.append(col[0])
    print(numCols)
    df1 = df.select(numCols)
    return df1

def correlationMatrix(df):
    for i in range(0, len(df.columns)-1):
        c1 = df.columns[i]
        for k in range(i+1, len(df.columns)):
            c2 = df.columns[k]
            corr = df.corr(c1, c2)
            print('%s, %s: %.4f' % (c1, c2, corr))
    return