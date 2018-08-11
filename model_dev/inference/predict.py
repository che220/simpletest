import os, sys, pickle, pandas as pd, logging
import model.model_env as model_env

logger = logging.getLogger(os.path.basename(__file__))

model_dir = '/opt/ml/model'

def predict(input_data):
    logger.info('RECEIVED DATA: %s', input_data)
    response = input_data
    return response
