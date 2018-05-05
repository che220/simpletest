import pandas as pd, numpy as np, os, sys, re, pickle, math, copy
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.stats import boxcox
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error

def showDF(df):
    display(df.head(4))
    display(df.dtypes)
    display(df.shape)

def evaluteRegression(model, trainData, trainLabels, testData, testLabels):
    trainPreds = model.predict(trainData)
    trainMSE = np.sqrt(mean_squared_error(trainLabels, trainPreds))
    print('Training MSE:', trainMSE)

    testPreds = model.predict(testData)
    testMSE = np.sqrt(mean_squared_error(testLabels, testPreds))
    print('Testing MSE:', testMSE)
    
    ratio = trainMSE/testMSE
    print('Training MSE/testing MSE: {:.2f}%'.format(ratio*100.0))
    if ratio < 0.8:
        print('Overfitting!!!')
    else:
        print('Likely did not overfit.')

class DataFrameCategoricalColumns(BaseEstimator, TransformerMixin):
    def __init__(self):
        return
    
    def fit(self, X, y=None):
        return self;
    
    def transform(self, X, y=None):
        """
        return DataFrame
        """
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        numCols = list(X.select_dtypes(include=numerics).columns)
        X = X.drop(numCols, axis=1)
        return X

class DataFrameNumericColumns(BaseEstimator, TransformerMixin):
    def __init__(self):
        return
    
    def fit(self, X, y=None):
        return self;
    
    def transform(self, X, y=None):
        """
        return DataFrame
        """
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        X = X.select_dtypes(include=numerics).copy()
        return X
    
class DataFrameToNArray(BaseEstimator, TransformerMixin):
    def __init__(self):
        return
    
    def fit(self, X, y=None):
        return self;
    
    def transform(self, X, y=None):
        return X.values

class DataFrameColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        """
        return DataFrame
        """
        return X[self.columns]
    
class BoxCoxTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, debug=False):
        self.debug = debug
        self.lmbdas = []
        return
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        out = None
        self.lmbdas = []
        for i in range(X.shape[1]):
            if self.debug:
                print(type(self).__name__, ': working on column', i)
                
            col = X[:, i].reshape(-1, 1)
            col -= np.min(col) - 1e-5 # make sure all data are positive
            col, lmbda = boxcox(col)
            self.lmbdas.append(lmbda)
            
            if out is None:
                out = col
            else:
                out = np.c_[out, col]
        if self.debug:
            print('Box-Cox lambdas:', self.lmbdas)
            print("Done BoxCoxTransformer's transform")
        return out
    
class StandardizedBoxCoxTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, debug=False):
        self.scaler = StandardScaler()
        self.debug = debug
        self.lmbdas = []
        return
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        out = None
        self.lmbdas = []
        for i in range(X.shape[1]):
            if self.debug:
                print(type(self).__name__, ': working on column', i)
                
            col = X[:, i].reshape(-1, 1)
            col -= np.min(col) - 1e-5 # make sure all data are positive
            col, lmbda = boxcox(col)
            self.lmbdas.append(lmbda)
            
            col = self.scaler.fit(col).transform(col)
            if out is None:
                out = col
            else:
                out = np.c_[out, col]
        if self.debug:
            print('Box-Cox lambdas:', self.lmbdas)
            print("Done StandardizedBoxCoxTransformer's transform")
        return out