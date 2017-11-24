"""
Utility functions for model data generation, model evaluation, and model training
"""
import os, pandas as pd, numpy as np, math, time
import scipy.optimize as optim
from _csv import QUOTE_NONNUMERIC

def to_csv(dataFile, dd):
    print('writing {} ...'.format(dataFile))
    dd.to_csv(dataFile, index=False, quoting=QUOTE_NONNUMERIC, quotechar='"', encoding='utf-8')

# print out current milli for performance tracking
def showMillisecond(prefix):
    millis = int(round(time.time() * 1000))
    print('{}: {}'.format(prefix, millis))

def entropy(probs):
    ent = 0
    for i in range(len(probs)):
        ent -= probs[i] * math.log(probs[i])
    return ent

# x is between -Inf and +Inf. Transform to between 0 and 1
def sigmoid(x):
    return math.exp(x)/(1.0 + math.exp(x))

# x is between 0 and 1. Transform makes it from -inf to +inf for Nelder-Mead search
def revSigmoid(x):
    return math.log(x/(1.0-x))

# xs and ys are both pandas.Series. It returns None if no seriouly info gain is seen.
# otherwise, it returns 2-element list: index 0 is the X cutpoint. Index 1 is the entropy reduction
# Note the entropy reduction can be used to order the importance of the Xs if you have many Xs
def infoGain(xs, ys):
    # objective function
    def totalEntropy(cutoff):
        cutoff = sigmoid(cutoff)
        x1 = ys[xs < cutoff].value_counts()
        ent = 0
        if len(x1) > 1:
            x1 /= float(sum(x1))
            ent += entropy(x1)

        x2 = ys[xs >= cutoff].value_counts()
        if len(x2) > 1:
            x2 /= float(sum(x2))
            ent += entropy(x2)
        return ent

    ent0 = totalEntropy(min(xs)-0.000001) # this is original entropy (all X on one side)
    x0 = np.median(xs) # median is a good starting point

    # minimize entropy. Limit max iteration to 100 for performance reason
    rs = optim.minimize(totalEntropy, revSigmoid(x0), method='Nelder-Mead', options={'maxiter': 100})
    delta = rs.fun - ent0
    cut = sigmoid(rs.x)

    # if entropy reduction is less than 0.2% of original entropy, xCol is declared useless. So return -1.0.
    # otherwise return the cut point
    if delta < ent0 * 0.002:
        return None
    else:
        return [cut, delta]

class FeatureSelector:
    def __init__(self, dataDF, isDebug):
        self.dataDF = dataDF
        self.isDebug = isDebug

    def selectFeatures(self):
        return


# if two features have correlation >= 80%, the less important feature is dropped
class CorrelationFeatureSelector(FeatureSelector):
    def __init__(self, dataDF, isDebug):
        super(CorrelationFeatureSelector, self).__init__(dataDF, isDebug)
        self.threshold = 0.8 # correlation >= 0.8 will leave features out
        return

    # featureDF: a dataframe of features. One of the columns must be "feature", and the features are ordered by importance
    #            The first feature is the most important
    def selectFeatures(self, featureDF):
        y = self.dataDF[featureDF.feature]
        corMat = y.corr()
        if self.isDebug:
            print("Correlation matrix:")
            print(corMat)

        cols = featureDF.reindex(index=featureDF.index[::-1]).feature
        dropCols = []
        if self.isDebug: # to see action in debug mode, set it lower
            self.threshold = 0.3

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
        print('total {} features are keeped by filtering correlation >= {}'.format(len(df), self.threshold))
        if self.isDebug:
            print(df.head(20))
        return df

# Supervised discretization. If info gain is less than original entropy * 0.002, the feature is dropped.
# all features in a dataframe are iterated
class InfoGainFeatureSelector(FeatureSelector):
    # dataDF: dataframe of the raw data
    # labelColum: the column name of label column
    # cacheDir: dir to cache the features picked by info-gain calculation
    # isDebug: if True, run in debug mode
    # noCache: if True, cached info-gain features are ignored and re-calculated
    def __init__(self, dataDF, labelColumn, cacheDir, isDebug, ignoreCache):
        super(InfoGainFeatureSelector, self).__init__(dataDF, isDebug)
        self.labelCol = labelColumn
        self.cacheDir = cacheDir
        self.ignoreCache = ignoreCache

    # return dataframe with 3 columns: feature, cutpoint, gain and the dataframe is sorted by gain in descending order
    def selectFeatures(self):
        # define the feature cache file. These features are picked by a lengthy info gain calculation
        if not os.path.isdir(self.cacheDir):
            os.makedirs(self.cacheDir)
        infoGainFeatureFile = '{}/{}'.format(self.cacheDir, 'info_gain_features.csv')

        # if the info gain features are found in the cache, just read it in to save us debugging time
        if (not self.ignoreCache) and os.path.isfile(infoGainFeatureFile):
            print("reading info-gain features from cache {} ...".format(infoGainFeatureFile))
            df = pd.read_csv(infoGainFeatureFile)
            return df

        labels = self.dataDF[self.labelCol]
        pickedCols = []
        cnt = 0
        for col in self.dataDF.columns:
            if col == self.labelCol:
                continue
            cnt += 1
            rs = infoGain(self.dataDF[col], labels)
            if not (rs is None):
                pickedCols.append([col, rs[0], rs[1]])
                print("KEEP {} - {} (Total: {})".format(cnt, col, len(pickedCols)))
                if self.isDebug and len(pickedCols) >= 10:
                    break

        df = pd.DataFrame(pickedCols, columns=['feature', 'cutpoint', 'gain'])
        df = df.sort_values('gain', ascending=False)
        print('total {} columns are picked by info gain'.format(df.shape[0]))
        if self.isDebug:
            print(df.head(20))
        to_csv(infoGainFeatureFile, df)
        return df
