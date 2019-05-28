from itertools import permutations
import numpy as np

def permute(a, st_idx, end_idx):
    if st_idx == end_idx:
        print(a)
        return a
    else:
        for i in range(st_idx, end_idx+1):
            a[st_idx], a[i] = a[i], a[st_idx]
            permute(a, st_idx+1, end_idx)
            a[st_idx], a[i] = a[i], a[st_idx]

a = 'abcdf'
n = len(a)
a = list(a)
permute(a, 0, n-1)
