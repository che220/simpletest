import os, sys, re, boto3, pandas as pd, numpy as np, logging
import sagemaker as sage
from sagemaker.predictor import csv_serializer
import datetime as dt

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)

def list_buckets():
    # list S3 buckets
    s3client = boto3.client('s3')
    list_buckets_resp = s3client.list_buckets()
    for bucket in list_buckets_resp['Buckets']:
        logger.info('S3 bucket: %s', bucket['Name'])

def get_sagemaker_role():
    # search for Sagemaker role
    client = boto3.client('iam')
    roles = client.list_roles()['Roles']
    role = None
    for elem in roles:
        arn = elem['Arn']
        if 'AmazonSageMaker-ExecutionRole' in arn:
            role = arn
            break
    logger.info('Sagemaker Role: %s', role)
    return role

def upload_data(sage_session):
    # S3 prefix
    prefix = 'DEMO-scikit-byo-iris' # name of the dir to save the data etc. Will be under the default sagemaker S3 dir

    # upload data from data dir to S3
    WORK_DIRECTORY = 'data'
    data_location = sage_session.upload_data(WORK_DIRECTORY, key_prefix=prefix)
    logger.info('Data has been uploaded to S3 bucket: %s', data_location) # this is a dir
    return data_location

def get_account_and_region(sage_session):
    sts = sage_session.boto_session.client('sts')
    account = sts.get_caller_identity()['Account']
    logger.info('account: %s', account)

    region = sage_session.boto_session.region_name
    logger.info('region: %s', region)
    return account, region

def train_model(sage_session, container_name):
    data_location = upload_data(sage_session)
    account, region = get_account_and_region(sage_session)
    image = '{}.dkr.ecr.{}.amazonaws.com/{}:latest'.format(account, region, container_name)
    logger.info('ECR image: %s', image)

    logger.info('============================================')
    logger.info('Sagemaker default bucket: %s', sess.default_bucket())  # this call creates the bucket if it doesn't exist yet.
    tree = sage.estimator.Estimator(image, role, 1, 'ml.c4.2xlarge',
                                    output_path="s3://{}/output".format(sage_session.default_bucket()),
                                    sagemaker_session=sage_session)
    logger.info('Traing starts at: %s', dt.datetime.now())
    tree.fit(data_location)
    logger.info('Traing completed at: %s', dt.datetime.now())
    return tree

def deploy_model(model):
    logger.info('Deployment starts at: %s', dt.datetime.now())
    predictor = model.deploy(1, 'ml.m4.xlarge', serializer=csv_serializer)
    logger.info('Deployment completes at: %s', dt.datetime.now())
    return predictor

if __name__ == '__main__':
    list_buckets()
    role = get_sagemaker_role()
    sess = sage.Session()

    # ECR container should have been created. Its name is here
    container_name = 'che220-aws-decision-trees'
    tree = train_model(sess, container_name)
    deploy_model(tree)
