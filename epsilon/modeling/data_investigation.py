import os, sys, pandas as pd, numpy as np, logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)

data_dir = os.path.dirname(__file__) + "/interview"
trains = pd.read_csv(data_dir + '/train.csv')
logger.info(trains.shape)
logger.info('Columns: %s', trains.columns)
logger.info('Labels:\n%s', trains.response.value_counts(dropna=False))
logger.info('Nans: %s', trains.isnull().values.any()) # found no missing values


logger.info('Features:')
vals = set()
for col in trains.columns:
    for i in trains[col].unique():
        vals.add(i)
#    logger.info('%s:\n%s', col, trains[col].value_counts(dropna=False))

logger.info("All values: %s", vals) # only found [0, 1]

# no missing values, all values are zero and one
