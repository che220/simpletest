def func(n):
    if n == 0:
        return []
    if n == 1:
        return ['()']

    # array: score, num lefts, num rights
    rs = {'(' : (1, n-1, n-1)}
    while True:
        keys = list(rs.keys())
        cnt = len(rs)
        for key in keys:
            score, lefts, rights = rs.pop(key)
            if lefts > 0:
                key1 = key + '('
                score1 = score + 1
                lefts1 = lefts - 1
                rs[key1] = (score1, lefts1, rights)

            if score > 0:
                key1 = key + ')'
                score1 = score - 1
                rights1 = rights - 1
                rs[key1] = (score1, lefts, rights1)
        cnt1 = len(rs)
        if cnt1 == cnt:
            break

    keys = list(rs.keys())
    for key in keys:
        score, lefts, rights = rs.pop(key)
        for i in range(score):
            key += ')'
            score -= 1
        rs[key] = (score, lefts, 0)

    rs = list(rs.keys())
    rs.sort()
    return rs

print(func(4))