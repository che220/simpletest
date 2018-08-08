import os, sys, logging, pandas as pd
import inference.predict as predict

logger = logging.getLogger(os.path.basename(__file__))

if __name__ == '__main__':
    data = {'userid' : 101}
    response = predict.predict(data)
    logger.info('1 - Response: %s', response)
