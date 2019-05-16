import pandas as pd, numpy as np

a = [
    {'col1' : 'joe1', 'col2' : 1},
    {'col1': 'joe2', 'col2': 2},
    {'col1': 'joe3', 'col2': 3},
    {'col1': 'joe4', 'col2': 4},
]

df = pd.DataFrame(a)
print(df)
vs = df.values
print(vs.dtype)
print(vs.shape)
print(vs)
print(type(vs))
print(type(vs[0]))
print(vs[0])
print(vs[0].dtype)
print(type(vs[0, 0]))
print(type(vs[0, 1]))

arr = np.array([1,2,3,'joe'], np.object)
print(arr)
