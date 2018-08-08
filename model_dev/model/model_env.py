import os, pandas as pd, numpy as np, logging, multiprocessing

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)
np.set_printoptions(threshold=np.nan) # print out all values, regardless length

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))

CORES = multiprocessing.cpu_count()
logger.info("Cores: %d", CORES)

def get_numeric_columns(df):
    numerics = ['uint8', 'int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    return df.select_dtypes(include=numerics).copy()

def hasNan(df):
    nanCols = []
    for col in df.columns:
        x = df[pd.isnull(df[col])]
        if x.shape[0] > 0:
            nanCols.append(col)
    if len(nanCols) > 0:
        logger.info('>>>>> Following columns have Nans: %s', nanCols)
        return True
    else:
        logger.info('Did not find any columns which have NaNs')
        return False
