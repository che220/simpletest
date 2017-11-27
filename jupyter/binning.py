import pandas as pd, numpy as np, os, sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from IPython.display import display, HTML

# Only increase font size in jupyter.
#font = {'size'   : 18}
#matplotlib.rc('font', **font)

def __plotProbs(probs, xcol):
    """
    probs: the output of inBinProbs, greaterThanProbs, lessThanProbs
    """
    if probs.shape[0] == 0:
        return
    
    a = probs.sort_values(xcol)
    plt.figure(figsize=(16,6))
    interval = 5.0

    def __plotSubPlot(ys, ylabel):
        plt.plot(a[xcol], ys, marker='^')
        plt.xlabel(xcol)
        plt.ylabel(ylabel)
        axes = plt.gca()
        ymin, ymax = axes.get_ylim()
        ymin = interval*int((ymin+interval)/interval)
        ymax = interval*int((ymax+interval)/interval)
        plt.yticks(np.arange(ymin, ymax, interval))
        plt.grid()
        
    plt.subplot(121)
    __plotSubPlot(a.prob*100.0, 'Probability (%)')
    plt.subplot(122)
    __plotSubPlot(a.freq_pct*100.0, 'Count Pct (%)')
    plt.tight_layout()

def __plotStats(probs, xcol, ycol):
    """
    probs: the output of inBinStats, greaterThanStats, lessThanStats
    """
    if probs.shape[0] == 0:
        return
    
    a = probs.sort_values(xcol)
    plt.figure(figsize=(16,6))
    interval = 5.0

    def __plotSubPlot(ys, ylabel):
        plt.plot(a[xcol], ys, marker='^')
        plt.xlabel(xcol)
        plt.ylabel(ylabel)
        axes = plt.gca()
        ymin, ymax = axes.get_ylim()
        ymin = interval*int((ymin+interval)/interval)
        ymax = interval*int((ymax+interval)/interval)
        plt.yticks(np.arange(ymin, ymax, interval))
        plt.grid()
        
    plt.subplot(131)
    __plotSubPlot(a[ycol+'_mean'], 'Mean of '+ycol)
    plt.subplot(132)
    __plotSubPlot(a.freq_pct*100.0, 'Count Pct (%)')
    plt.subplot(133)
    __plotSubPlot(a.sum_pct*100.0, 'Sum of '+ycol+' Pct (%)')
    plt.tight_layout()

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

def inBinProbs(x, y, binSize, positiveClass=True, minx=None, maxx=None, minCnt=20, plot=False):
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
    bins = bins.tolist()
    bins.append(float('inf'))
    
    def stats(bmin, bmax):
        aa = binDF[(binDF.x >= bmin) & (binDF.x < bmax)]
        buc = '{:.3f} '.format(bmin)+'~ {:.3f}'.format(bmax)
        if aa.shape[0] == 0:
            return buc, aa.shape[0], 0.0
        
        aaPos = aa[aa.y == positiveClass]
        return buc, aa.shape[0], float(aaPos.shape[0])/float(aa.shape[0])

    rsDF = pd.DataFrame(bins[:-1], columns=[x.name])
    size = len(bins)
    
    stats = [stats(bins[i], bins[i+1]) for i in range(size-1)]
    stats = pd.DataFrame(stats, columns=['bucket', 'freq', 'prob'])
    rsDF = pd.concat([rsDF, stats], axis=1)

    rsDF['freq_pct'] = rsDF.freq/x.shape[0]
    rsDF = rsDF[rsDF.freq >= minCnt].copy()
    if plot:
        __plotProbs(rsDF, x.name)
    return rsDF

def greaterThanProbs(x, y, binSize, positiveClass=True, minx=None, maxx=None, minCnt=20, plot=False):
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
    
    def stats(bmin):
        aa = binDF[binDF.x >= bmin]
        buc = '>= {:.3f}'.format(bmin)
        if aa.shape[0] == 0:
            return buc, aa.shape[0], 0.0
        
        aaPos = aa[aa.y == positiveClass]
        return buc, aa.shape[0], float(aaPos.shape[0])/float(aa.shape[0])

    rsDF = pd.DataFrame(bins, columns=[x.name])
    stats = [stats(thresh) for thresh in bins]
    stats = pd.DataFrame(stats, columns=['bucket', 'freq', 'prob'])
    rsDF = pd.concat([rsDF, stats], axis=1)
    
    rsDF['freq_pct'] = rsDF.freq/x.shape[0]
    rsDF = rsDF[rsDF.freq >= minCnt].copy()
    if plot:
        __plotProbs(rsDF, x.name)

    return rsDF

def lessThanProbs(x, y, binSize, positiveClass=True, minx=None, maxx=None, minCnt=20, plot=False):
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
    
    def stats(bmin):
        aa = binDF[binDF.x <= bmin]
        buc = '<= {:.3f}'.format(bmin)
        if aa.shape[0] == 0:
            return buc, aa.shape[0], 0.0
        
        aaPos = aa[aa.y == positiveClass]
        return buc, aa.shape[0], float(aaPos.shape[0])/float(aa.shape[0])

    rsDF = pd.DataFrame(bins, columns=[x.name])
    stats = [stats(thresh) for thresh in bins]
    stats = pd.DataFrame(stats, columns=['bucket', 'freq', 'prob'])
    rsDF = pd.concat([rsDF, stats], axis=1)
    
    rsDF['freq_pct'] = rsDF.freq/x.shape[0]
    rsDF = rsDF[rsDF.freq >= minCnt].copy()
    if plot:
        __plotProbs(rsDF, x.name)

    return rsDF

def inBinStats(x, y, binSize, minx=None, maxx=None, minCnt=20, plot=False):
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
    bins = bins.tolist()
    bins.append(float('inf'))

    def stats(bmin, bmax):
        aa = binDF[(binDF.x >= bmin) & (binDF.x < bmax)]
        return '{:.3f} '.format(bmin)+'~ {:.3f}'.format(bmax), aa.shape[0], np.mean(aa.y), np.sum(aa.y)
        
    rsDF = pd.DataFrame(bins[:-1], columns=[x.name])
    size = len(bins)
    
    meanCol = str(y.name) + '_mean'
    sumCol = str(y.name) + '_sum'
    stats = [stats(bins[i], bins[i+1]) for i in range(size-1)]
    stats = pd.DataFrame(stats, columns=['bucket', 'freq', meanCol, sumCol])
    rsDF = pd.concat([rsDF, stats], axis=1)
    
    rsDF['freq_pct'] = rsDF.freq/x.shape[0]
    totY = y.sum()
    rsDF['sum_pct'] = rsDF[sumCol]/totY

    rsDF = rsDF[rsDF.freq >= minCnt].copy()
    if plot:
        __plotStats(rsDF, x.name, y.name)
    return rsDF

def greaterThanStats(x, y, binSize, minx=None, maxx=None, minCnt=20, plot=False):
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
    
    def stats(bmin):
        aa = binDF[binDF.x >= bmin]
        return '>= {:.3f}'.format(bmin), aa.shape[0], np.mean(aa.y), np.sum(aa.y)

    rsDF = pd.DataFrame(bins, columns=[x.name])
    
    meanCol = str(y.name) + '_mean'
    sumCol = str(y.name) + '_sum'
    stats = [stats(thresh) for thresh in bins]
    stats = pd.DataFrame(stats, columns=['bucket', 'freq', meanCol, sumCol])
    rsDF = pd.concat([rsDF, stats], axis=1)

    rsDF['freq_pct'] = rsDF.freq/x.shape[0]
    totY = y.sum()
    rsDF['sum_pct'] = rsDF[sumCol]/totY
    
    rsDF = rsDF[rsDF.freq >= minCnt].copy()
    if plot:
        __plotStats(rsDF, x.name, y.name)
    return rsDF

def lessThanStats(x, y, binSize, minx=None, maxx=None, minCnt=20, plot=False):
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
    def stats(bmin):
        aa = binDF[binDF.x <= bmin]
        return '<= {:.3f}'.format(bmin), aa.shape[0], np.mean(aa.y), np.sum(aa.y)
    
    rsDF = pd.DataFrame(bins, columns=[x.name])
    
    meanCol = str(y.name) + '_mean'
    sumCol = str(y.name) + '_sum'
    stats = [stats(thresh) for thresh in bins]
    stats = pd.DataFrame(stats, columns=['bucket', 'freq', meanCol, sumCol])
    rsDF = pd.concat([rsDF, stats], axis=1)

    rsDF['freq_pct'] = rsDF.freq/x.shape[0]
    totY = y.sum()
    rsDF['sum_pct'] = rsDF[sumCol]/totY
    
    rsDF = rsDF[rsDF.freq >= minCnt].copy()
    if plot:
        __plotStats(rsDF, x.name, y.name)
    return rsDF