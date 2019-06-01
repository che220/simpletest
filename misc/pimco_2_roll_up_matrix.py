def findMatrix(a):
    if not a:
        return None

    rows = len(a)
    cols = len(a[0])
    b = []
    for r in range(rows):
        b_last_row = [0] * cols
        if r > 0:
            b_last_row = b[r-1]

        b_row = []
        tot = 0
        for c in range(cols):
            tot += a[r][c]
            b_row.append(tot + b_last_row[c])

        b.append(b_row)

    return b

if __name__ == '__main__':
    a = [[1,2,3]]
    b = findMatrix(a)
    print(b)
