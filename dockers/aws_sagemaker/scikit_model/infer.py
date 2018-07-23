import os, sys, re, boto3, pandas as pd, numpy as np, logging, io

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    shape = pd.read_csv("data/iris.csv", header=None)
    logger.info('\n%s\n%s', shape.head(4), shape.shape)

    test_file = io.StringIO()
    test_X = shape.iloc[:, 1:]
    test_X.to_csv(test_file, header=None, index=None)

    endpoint_name = 'che220-aws-decision-trees-2018-07-23-17-39-32-683'
    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(EndpointName=endpoint_name,
                                      Body=test_file.getvalue(),
                                      ContentType='text/csv',
                                      Accept='Accept')
    logger.info(response['Body'].read().decode('utf-8'))