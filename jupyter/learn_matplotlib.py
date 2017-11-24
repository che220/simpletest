
# coding: utf-8

# In[1]:

get_ipython().magic('config IPCompleter.greedy=True')
get_ipython().magic('matplotlib inline')


# In[2]:

import pandas as pd, numpy as np, os, sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from IPython.display import display, HTML
from IPython.core.debugger import Tracer
from IPython.core.debugger import Pdb

font = {'size'   : 18}
matplotlib.rc('font', **font)

def plotHorizontalBars(series, xlabel, title):
    xpos = np.arange(len(series.index), 0, -1)
    plt.barh(xpos, series, align='center', alpha=0.5, color='g')
    plt.grid(axis='x')
    plt.yticks(xpos, series.index)
    plt.xlabel(xlabel)
    plt.title(title)

def plotVerticalBars(series, ylabel, title):
    xpos = np.arange(len(series.index), 0, -1)
    plt.bar(xpos, series, align='center', alpha=0.5, color='g')
    plt.grid(axis='y')
    plt.xticks(xpos, series.index)
    plt.ylabel(ylabel)
    plt.title(title)

def greaterThanProbs(x, y, binSize, positiveClass=True, minx=None, maxx=None, minCnt=20):
    """
    both x is numeric and y is categorical. returns y's probabilities in each x bin
    """
    assert(y is not None)
    
    binDF = pd.concat([x,y], axis=1, ignore_index=True)
    binDF.columns = ['x', 'y']
    if minx is None:
        minx = binDF.x.min()
    if maxx is None:
        maxx = binDF.x.max()

    minx, maxx = [minx, maxx]
    bins = np.arange(minx, maxx*1.0001, binSize)
    rsDF = pd.DataFrame(bins, columns=[x.name])
    rsDF['bucket'] = '>= '
    rsDF['bucket'] = rsDF.bucket.map(str) + rsDF[x.name].map(lambda x: '{:.3f}'.format(x))

    freqCol = 'freq'
    rsDF[freqCol] = [binDF.loc[binDF.x >= thresh, 'y'].shape[0] for thresh in bins]
    rsDF['freq_pct'] = rsDF[freqCol]/x.shape[0]
    
    def prob(threshold):
        aa = binDF[binDF.x >= threshold]
        if aa.shape[0] == 0:
            return 0.0
        
        aaPos = binDF[binDF.y == positiveClass]
        return float(aaPos.shape[0])/float(aa.shape[0])

    rsDF['prob'] = [prob(thresh) for thresh in bins]
    
    rsDF = rsDF[rsDF[freqCol] >= minCnt].copy()
    return rsDF

def greaterThanProbs(x, y, binSize, positiveClass=True, minx=None, maxx=None, minCnt=20):
    """
    both x is numeric and y is categorical. returns y's probabilities in each x bin
    """
    assert(y is not None)
    
    binDF = pd.concat([x,y], axis=1, ignore_index=True)
    binDF.columns = ['x', 'y']
    if minx is None:
        minx = binDF.x.min()
    if maxx is None:
        maxx = binDF.x.max()

    minx, maxx = [minx, maxx]
    bins = np.arange(minx, maxx*1.0001, binSize)
    rsDF = pd.DataFrame(bins, columns=[x.name])
    rsDF['bucket'] = '>= '
    rsDF['bucket'] = rsDF.bucket.map(str) + rsDF[x.name].map(lambda x: '{:.3f}'.format(x))

    freqCol = 'freq'
    rsDF[freqCol] = [binDF.loc[binDF.x >= thresh, 'y'].shape[0] for thresh in bins]
    rsDF['freq_pct'] = rsDF[freqCol]/x.shape[0]
    
    def prob(threshold):
        aa = binDF[binDF.x >= threshold]
        if aa.shape[0] == 0:
            return 0.0
        
        aaPos = binDF[binDF.y == positiveClass]
        return float(aaPos.shape[0])/float(aa.shape[0])

    rsDF['prob'] = [prob(thresh) for thresh in bins]
    
    rsDF = rsDF[rsDF[freqCol] >= minCnt].copy()
    return rsDF

def greaterThanStats(x, y, binSize, minx=None, maxx=None, minCnt=20):
    """
    both x and y are numeric. If y = None, y will be set to x
    """
    if y is None:
        y = x
    binDF = pd.concat([x,y], axis=1, ignore_index=True)
    binDF.columns = ['x', 'y']
    if minx is None:
        minx = binDF.x.min()
    if maxx is None:
        maxx = binDF.x.max()

    minx, maxx = [minx, maxx]
    bins = np.arange(minx, maxx*1.0001, binSize)
    rsDF = pd.DataFrame(bins, columns=[x.name])
    rsDF['bucket'] = '>= ' + rsDF[x.name]

    freqCol = 'freq'
    rsDF[freqCol] = [binDF.loc[binDF.x >= thresh, 'y'].shape[0] for thresh in bins]
    rsDF['freq_pct'] = rsDF[freqCol]/x.shape[0]

    meanCol = '{}_mean'.format(y.name)
    rsDF[meanCol] = [np.mean(binDF.loc[binDF.x >= thresh, 'y']) for thresh in bins]

    sumCol = '{}_sum'.format(y.name)
    rsDF[sumCol] = [np.sum(binDF.loc[binDF.x >= thresh, 'y']) for thresh in bins]
    totY = y.sum()
    rsDF['sum_pct'] = rsDF[sumCol]/totY
    
    rsDF = rsDF[rsDF[freqCol] >= minCnt].copy()
    return rsDF

def lessThanStats(x, y, binSize, minx=None, maxx=None, minCnt=20):
    """
    both x and y are numeric. If y = None, y will be set to x
    """
    if y is None:
        y = x
    binDF = pd.concat([x,y], axis=1, ignore_index=True)
    binDF.columns = ['x', 'y']
    if minx is None:
        minx = binDF.x.min()
    if maxx is None:
        maxx = binDF.x.max()

    bins = np.arange(maxx, minx, -binSize)
    rsDF = pd.DataFrame(bins, columns=[x.name])

    freqCol = 'freq'
    rsDF[freqCol] = [binDF.loc[binDF.x <= thresh, 'y'].shape[0] for thresh in bins]
    rsDF['freq_pct'] = rsDF[freqCol]/x.shape[0]

    meanCol = '{}_mean'.format(y.name)
    rsDF[meanCol] = [np.mean(binDF.loc[binDF.x <= thresh, 'y']) for thresh in bins]

    sumCol = '{}_sum'.format(y.name)
    rsDF[sumCol] = [np.sum(binDF.loc[binDF.x <= thresh, 'y']) for thresh in bins]
    totY = y.sum()
    rsDF['sum_pct'] = rsDF[sumCol]/totY
    
    rsDF = rsDF[rsDF[freqCol] >= minCnt].copy()
    return rsDF


# In[ ]:




# In[3]:

get_ipython().run_cell_magic('time', '', "cacheDir = '/Users/huiwang/dev/PTG_DataScience/spark_cache'\ninFile = '{}/desktop_profile_complete_TY2015.csv'.format(cacheDir)\nallData = pd.read_csv(inFile)")


# In[4]:

display(allData.shape)
a = allData.PRODUCT_GROUP + ' - ' + allData.PRODUCT_SEGMENT
a = a.value_counts().sort_index()
plt.figure(figsize=(16,12))
plotHorizontalBars(a, 'CANs', 'CANs by Product Segments')


# In[6]:

df = allData[(allData.PRODUCT_GROUP == 'LACERTE') & (allData.PRODUCT_SEGMENT != 'DIAMOND PASSPORT') & (~allData.IS_PM)]
display(df.AT_RISK.value_counts())

plt.figure(figsize=(16,4))
a = df.PRODUCT_SEGMENT.value_counts().sort_index()
plotHorizontalBars(a, 'CANs', 'CANs by Product Segments')


# In[7]:

a = df.LACERTE_NET_BILL
plt.figure(figsize=(16,6))
plt.hist(a, bins=30, range=[0,30000])
plt.title("{} Distribution".format(a.name))
plt.grid(axis='y')
plt.xlabel(a.name)
plt.ylabel("CANs")


# In[8]:

x = df.LACERTE_NET_BILL
y = df.LACERTE_NET_BILL_DISCOUNT_PCT
stats = lessThanStats(x, y, binSize=1000, minx=0)
a = stats.sort_values(x.name)

plt.figure(figsize=(16,6))
meanCol = y.name + '_mean'
plt.plot(a[x.name], a[meanCol], marker='^')
plt.xlabel(x.name)
plt.ylabel(meanCol)
plt.tight_layout()
plt.show()

display(stats)


# In[9]:

x = df.LACERTE_NET_BILL
y = df.ATTEMPTS
stats = lessThanStats(x, y, binSize=1000, minx=0, maxx=20000)
a = stats.sort_values(x.name)

plt.figure(figsize=(16,5))
plt.subplot(131)
meanCol = y.name + '_mean'
plt.plot(a[x.name], a[meanCol], marker='^')
plt.xlabel(x.name)
plt.ylabel(meanCol)

plt.subplot(132)
sumCol = y.name + '_sum'
plt.plot(a[x.name], a[sumCol], marker='^')
plt.xlabel(x.name)
plt.ylabel(sumCol)

plt.subplot(133)
plt.plot(a[x.name], a['sum_pct'], marker='^')
plt.xlabel(x.name)
plt.ylabel('sum_pct')
plt.tight_layout()
plt.show()

display(stats)


# In[10]:

display(np.sort(df.columns))


# In[11]:

x = df.LACERTE_NET_BILL_DISCOUNT_PCT
y = df.AT_RISK
stats = greaterThanProbs(x, y, binSize=0.02)
a = stats.sort_values(x.name)

plt.figure(figsize=(16,6))
plt.plot(a[x.name], a.prob, marker='^')
plt.grid(axis='y')
plt.xlabel(x.name)
plt.ylabel(y.name+' Probability')
plt.tight_layout()
plt.show()

display(stats)


# In[32]:

def inBinProbs(x, y, binSize, positiveClass=True, minx=None, maxx=None, minCnt=20):
    """
    both x is numeric and y is categorical. returns y's probabilities in each x bin
    """
    assert(y is not None)
    
    binDF = pd.concat([x,y], axis=1, ignore_index=True)
    binDF.columns = ['x', 'y']
    if minx is None:
        minx = binDF.x.min()
    if maxx is None:
        maxx = binDF.x.max()

    minx, maxx = [minx, maxx]
    bins = np.arange(minx, maxx*1.0001, binSize)
    rsDF = pd.DataFrame(bins, columns=[x.name])
    rsDF['bucket'] = rsDF[x.name].map(lambda x: '>= {:.3f}'.format(x))
    
    rsDF['freq'] = [binDF.loc[binDF.x >= thresh, 'y'].shape[0] for thresh in bins]
    rsDF['freq_pct'] = rsDF.freq/x.shape[0]
    
    def prob(bmin, bmax):
        aa = binDF[(binDF.x >= bmin) & (binDF.x < bmax)]
        if aa.shape[0] == 0:
            return 0.0
        
        aaPos = binDF[binDF.y == positiveClass]
        Pdb.set_trace()
        return float(aaPos.shape[0])/float(aa.shape[0])

    bins = bins.tolist()
    bins.append(float('inf'))
    print(bins)
    size = len(bins)
    rsDF['prob'] = [prob(bins[i], bins[i+1]) for i in range(size-1)]
    
    rsDF = rsDF[rsDF.freq >= minCnt].copy()
    return rsDF


# In[33]:

x = df.ATTEMPTS
y = df.AT_RISK
stats = inBinProbs(x, y, binSize=1)
a = stats.sort_values(x.name)

plt.figure(figsize=(16,6))
plt.plot(a[x.name], a.prob, marker='^')
plt.grid(axis='y')
plt.xlabel(x.name)
plt.ylabel(y.name+' Probability')
plt.tight_layout()
plt.show()

display(stats)


# In[ ]:



