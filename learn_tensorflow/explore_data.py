import pandas as pd, numpy as np, matplotlib
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing()
housing = pd.DataFrame(housing.data, columns = housing.feature_names)
print(housing.head(4))
print(housing.dtypes)
print(housing.shape)
