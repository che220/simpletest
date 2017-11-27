import math, numpy as np, pandas as pd

def entropy(labels):
    t = labels.value_counts()
    t /= sum(t)
    return np.sum(-t*np.log(t))

# x is between -Inf and +Inf. Transform to between 0 and 1
def sigmoid(x):
    return math.exp(x)/(1.0 + math.exp(x))

# x is between 0 and 1. Transform makes it from -inf to +inf for Nelder-Mead search
def revSigmoid(x):
    x = max(x, np.finfo('float64').min)
    x = max(x, 1e-12)
    return math.log(x/(1.0-x))

# xs: feature series
# ys: label series
# cutPoints: array of cut points out of MDLP, if available
#
# if the entropy reduction is less than 0.5% of original entropy, returns None. Otherwise return info
def crossTabEntropy(xs, ys, cutPoints=None, positiveClass=True):
    ent0 = entropy(ys)
    threshold = ent0 * 0.001

    def __info(x):
        return '{:.2f}%/{:.0f}'.format(x[positiveClass]*100.0, x['tot'])

    ct = pd.crosstab(xs, ys)+1e-12 # to avoid zeros
    tot = ct.sum(axis=1)
    ct = ct.divide(ct.sum(axis=1), axis=0)
    ct['portion'] = tot/tot.sum()
    ct['tot'] = tot
    
    sizeThreshold = 20
    if ct[ct.tot >= sizeThreshold].shape[0] < 2:
        return None
    
    z = ct[ct.tot >= sizeThreshold]
    info = z.apply(__info, axis=1)
    rateGap = z[positiveClass].max() - z[positiveClass].min()
    ct = ct.as_matrix()
    ent = np.sum(np.multiply(np.sum(-ct[:,0:2]*np.log(ct[:,0:2]), axis=1), ct[:,2]))
    if (ent0 - ent) < threshold:
        return None
    else:
        return [xs.name, (ent0-ent)/ent0, cutPoints, info.tolist(), rateGap]

def getNPRange(arr, colIdx):
    amin = np.min(arr[:, colIdx])
    amax = np.max(arr[:, colIdx])
    return amin, amax

def normalizeDFByRanges(df):
    rgs = df.max(axis=0) - df.min(axis=0)
    return df.divide(rgs) # divide each column by array
