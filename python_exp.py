import os
import numpy as np

l = 50
deg = 3
x = np.arange(l * 1.0)
print(x)
print('-----------------------')

X = np.vstack(tuple(x ** n for n in range(deg, -1, -1))).T
print(X)
print('-----------------------')

pinv = np.linalg.pinv(X)
print(pinv)
