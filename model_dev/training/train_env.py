import os, logging, datetime as dt, pandas as pd, numpy as np

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)
np.set_printoptions(threshold=np.nan) # print out all values, regardless length

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s', level=logging.INFO)

logger = logging.getLogger(os.path.basename(__file__))
data_dir = '/data/input/training'
model_dir = '/opt/ml/model'

def define_dirs_for_local():
    global data_dir, model_dir
    if 'DATA_CACHE_DIR' in os.environ:
        data_dir = os.environ['DATA_CACHE_DIR']
    else:
        logger.error('env var DATA_CACHE_DIR is not defined')
        exit(1)

    if 'MODEL_OUTPUT_DIR' in os.environ:
        model_dir = os.environ['MODEL_OUTPUT_DIR']
    else:
        logger.error('env var MODEL_OUTPUT_DIR is not defined')
        exit(1)
    logger.info('data dir: %s', data_dir)
    logger.info('model output dir: %s', model_dir)

def show_info(df):
    logger.info('DataFrame Info:\n%s\n%s\n%s', df.head(5), df.shape, df.dtypes)

