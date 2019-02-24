def perm(arr):
    if len(arr) < 2:
        return arr

    rs = []
    for i in range(len(arr)):
        e = [arr[i]]
        if i < len(arr)-1:
            sub_arr = arr[0:i] + arr[i+1:]
        else:
            sub_arr = arr[0:i]
        sub_rs = perm(sub_arr)
        for s in sub_rs:
            if isinstance(s, int):
                s = [s]
            rs.append(e+s)
    return rs

a = [2,2,3,3,5]
rs = perm(a)
dedup = {}
for i in rs:
    dedup[','.join(str(i))] = i

for i, k in enumerate(dedup):
    print(i, dedup[k])
