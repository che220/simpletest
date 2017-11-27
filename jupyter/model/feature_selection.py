import pandas as pd, numpy as np, math
import scipy.optimize as optim
import model.functions as func
from mdlp.discretization import MDLP
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures._base import as_completed

# This function only tries to find one cutpoint in the range
#
# xs: continuous feature
# ys: labels, nomial feature
#
# xs and ys are both pandas.Series. It returns None if no seriouly info gain is seen.
# otherwise, it returns 2-element list: index 0 is the X cutpoint. Index 1 is the entropy reduction
# Note the entropy reduction can be used to order the importance of the Xs if you have many Xs
def infoGainViaOptimization(xs, ys):
    print('(infoGainViaOptimization) work on {}'.format(xs.name))
    
    # objective function
    def totalEntropy(cutoff):
        cutoff = cutoff[0]
        
        ent = 0
        
        a = ys[xs < cutoff]
        ent += func.entropy(a) * a.shape[0]/ys.shape[0]

        a = ys[xs >= cutoff]
        ent += func.entropy(a) * a.shape[0]/ys.shape[0]
        return ent
    
    ent0 = func.entropy(ys)
    x0 = np.median(xs) # median is a good starting point

    # minimize entropy. Limit max iteration to 100 for performance reason
    step = (xs.max() - xs.min()) /100.0
    
    # L-BFGS-B may not be thread-safe
    rs = optim.minimize(totalEntropy, x0, method='L-BFGS-B', 
                        bounds=[(xs.min(),xs.max())], options={'maxiter': 100, 'eps' : step})
    delta = (ent0 - rs.fun)/ent0
    cut = rs.x[0]

    # if entropy reduction is less than 0.2% of original entropy, xCol is declared useless. So return -1.0.
    # otherwise return the cut point
    if delta < 0.001:
        return None
    else:
        return [cut, delta]

def OptimizeGap(xs, ys, positiveClass=True):
    print('(OptimizeGap) work on {}'.format(xs.name))
    
    # objective function
    def totalEntropy(cutoff):
        cutoff = cutoff[0]
        
        a = ys[xs < cutoff]
        b = a[a == positiveClass]
        rate1 = b.shape[0]/a.shape[0]

        a = ys[xs >= cutoff]
        b = a[a == positiveClass]
        rate2 = b.shape[0]/a.shape[0]
        return -1.0 * abs(rate1 - rate2)

    ## not working due to lack of unique values for a lot of features
    if len(xs.unique()) < 42:
        return None
    
    z = np.sort(xs.unique())
    minx = z[21]
    maxx = z[len(z) - 21]
    x0 = np.median(xs) # median is a good starting point

    # minimize entropy. Limit max iteration to 100 for performance reason
    step = (maxx - minx) /100.0
    
    # L-BFGS-B may not be thread-safe
    rs = optim.minimize(totalEntropy, x0, method='L-BFGS-B', 
                        bounds=[(minx,maxx)], options={'maxiter': 100, 'eps' : step})
    delta = -1 * rs.fun
    cut = rs.x[0]

    # if entropy reduction is less than 0.2% of original entropy, xCol is declared useless. So return -1.0.
    # otherwise return the cut point
    if delta < 0.02:
        return None
    else:
        return [cut, delta]

class FeatureSelector:
    def __init__(self, dataDF, isDebug):
        self.dataDF = dataDF
        self.isDebug = isDebug

    def selectNumericFeatures(self):
        return None

    def selectNominalFeatures(self):
        return None


# if two features have correlation >= 80%, the less important feature is dropped
class CorrelationFeatureSelector(FeatureSelector):
    # dataDF: dataframe of the raw data
    # isDebug: if True, use 0.3 as strong correlation. Just to see the effect easier
    def __init__(self, dataDF, isDebug):
        super(CorrelationFeatureSelector, self).__init__(dataDF, isDebug)
        self.threshold = 0.8 # correlation >= 0.8 will leave features out
        if self.isDebug: # to see action in debug mode, set it lower
            self.threshold = 0.3
        return

    # featureDF: a dataframe of features. One of the columns must be "feature", and the features are ordered by importance
    #            The first feature is the most important
    def selectNumericFeatures(self, featureDF):
        y = self.dataDF[featureDF.feature]
        corMat = y.corr()
        if self.isDebug:
            print("Correlation matrix:")
            print(corMat)

        cols = featureDF.reindex(index=featureDF.index[::-1]).feature
        dropCols = []

        # record base and drop columns and their correlation
        for i in range(len(cols) - 1):
            col1 = cols.iloc[i]
            for k in range(i + 1, len(cols)):
                col2 = cols.iloc[k]
                corr = corMat.loc[col2, col1]
                if corr >= self.threshold:
                    dropCols.append([col2, col1, corr])
        dropCols = pd.DataFrame(dropCols, columns=['base_feature', 'drop_feature', 'correlation'])
        print("Dropped features based on correlation:")
        print(dropCols)

        df = featureDF[~featureDF.feature.isin(dropCols.drop_feature)]
        print('total {} features are keeped by filtering correlation >= {}'
              .format(len(df), self.threshold))
        if self.isDebug:
            print(df.head(20))
        return df

# Supervised discretization. If info gain is less than original entropy * 0.002, the feature is dropped.
# all features in a dataframe are iterated
class InfoGainFeatureSelector(FeatureSelector):
    # dataDF: dataframe of the raw data, numeric data only, except the label column
    # labelColum: the column name of label column
    # isDebug: if True, only pick max 5 columns to have a fast turn-around
    def __init__(self, dataDF, labelColumn, positiveClass, isDebug):
        super(InfoGainFeatureSelector, self).__init__(dataDF, isDebug)
        self.labelCol = labelColumn
        self.positiveClass = positiveClass

    def selectNumericFeatures(self):
        df = self.selectNumericFeaturesTheadPool()
        return df
    
    # return dataframe with 3 columns: feature, cutpoint, gain and the dataframe is sorted by gain in descending order
    def selectNumericFeaturesTheadPool(self):
        pickedCols = []
        with ThreadPoolExecutor(max_workers=mp.cpu_count()) as pool:
            print("{} threads in thread pool".format(mp.cpu_count()))
            
            labels = self.dataDF[self.labelCol]
            print('number of features to select from: {}'.format(len(self.dataDF.columns)-1))
            futures = {}
            cnt = 0
            for col in self.dataDF.columns:
                if self.isDebug and cnt >= 10:
                    break
                if col == self.labelCol or len(self.dataDF[col].unique()) < 2:
                    continue
                cnt += 1
                future = pool.submit(infoGainViaOptimization, self.dataDF[col], labels)
                futures[future] = col

            cnt = 0
            for future in as_completed(futures):
                col = futures[future]
                rs = future.result()
                cnt += 1
                if not (rs is None):
                    feature = self.dataDF[col].copy()
                    feature = feature.map(lambda x: 1.0 if x < rs[0] else 2.0)
                    a = func.crossTabEntropy(feature, labels, rs[0], positiveClass=self.positiveClass)
                    if not a is None:
                        pickedCols.append(a)
                        print('Keep {} - {}: cut = {}, gain = {}'.format(cnt, col, rs[0], rs[1]))

        df = pd.DataFrame(pickedCols, columns=['feature', 'gain', 'cut_point', 'info', 'rate_gap'])
        df = df.sort_values('rate_gap', ascending=False)
        print('total {} columns are picked by info gain'.format(df.shape[0]))
        if self.isDebug:
            print(df.head(10))
        return df

    # single-threaded, good for debugging purpose
    def selectNumericFeaturesSingleThread(self):
        labels = self.dataDF[self.labelCol]
        print('number of features to select from: {}'.format(self.dataDF.shape[1]-1))
        
        cnt = 0
        pickedCols = []
        for col in self.dataDF.columns:
            if self.isDebug and cnt >= 10:
                break
            
            if col == self.labelCol:
                continue
            
            if len(self.dataDF[col].unique()) < 2:
                continue
            
            rs = infoGainViaOptimization(self.dataDF[col], labels)
            cnt += 1
            if not (rs is None):
                feature = self.dataDF[col].copy()
                feature = feature.map(lambda x: 1.0 if x < rs[0] else 2.0)
                a = func.crossTabEntropy(feature, labels, rs[0], positiveClass=self.positiveClass)
                if not a is None:
                    pickedCols.append(a)
                    print('Keep {} - {}: cut = {}, gain = {}'.format(cnt, col, rs[0], rs[1]))

        df = pd.DataFrame(pickedCols, columns=['feature', 'gain', 'cut_point', 'info', 'rate_gap'])
        df = df.sort_values('rate_gap', ascending=False)
        print('total {} columns are picked by info gain'.format(df.shape[0]))
        if self.isDebug:
            print(df.head(10))
        return df

    # unless there are a lot of unique values per feature, this would not work!
    def selectNumericFeaturesWithGap(self):
        labels = self.dataDF[self.labelCol]
        print('number of features to select from: {}'.format(self.dataDF.shape[1]-1))
        
        cnt = 0
        pickedCols = []
        for col in self.dataDF.columns:
            if self.isDebug and cnt >= 10:
                break
            
            if col == self.labelCol:
                continue
            
            rs = OptimizeGap(self.dataDF[col], labels, positiveClass=self.positiveClass)
            cnt += 1
            if not (rs is None):
                pickedCols.append([col, rs[0], rs[1]])
                print('Keep {} - {}: cut = {}, rate_gap = {}'.format(cnt, col, rs[0], rs[1]))

        df = pd.DataFrame(pickedCols, columns=['feature', 'rate_gap', 'cut_point'])
        df = df.sort_values('rate_gap', ascending=False)
        print('total {} columns are picked by info gain'.format(df.shape[0]))
        if self.isDebug:
            print(df.head(10))
        return df

    # return dataframe with 3 columns: feature, cutpoint, gain and the dataframe is sorted by gain in descending order
    # single-threaded version
    def selectNumericFeaturesWithMDLP(self):
        labels = self.dataDF[self.labelCol]
        features = self.dataDF.drop(self.labelCol, axis=1)
        if self.isDebug and len(features.columns) > 10:
            features = features.iloc[:, 0:10]
        print('Number of features to select from based on info-gain: {}'.format(features.shape[1]))
        
        mdlp = MDLP()
        rs = mdlp.fit_transform(features, labels);
        converted = pd.DataFrame(rs, columns=features.columns)
        converted[self.labelCol] = labels
        
        rs = []
        idx = 0
        for col in converted.columns:
            if col == self.labelCol:
                continue
            
            a = func.crossTabEntropy(converted[col], converted[self.labelCol], 
                                     mdlp.cut_points_[idx], positiveClass=self.positiveClass)
            if not a is None:
                rs.append(a)
            idx += 1
            
        rs = pd.DataFrame(rs, columns=['feature', 'gain', 'cut_points', 'info', 'rate_gap'])
        rs = rs.sort_values('rate_gap', ascending=False)
        print('total {} columns are picked by info gain'.format(rs.shape[0]))
        if self.isDebug:
            print(rs.head(10))
        return rs
