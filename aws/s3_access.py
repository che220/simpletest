import os, sys, re, boto3, pandas as pd, numpy as np, logging
import sagemaker as sage
from sagemaker.predictor import csv_serializer
import datetime as dt

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)

def list_buckets(profile='default'):
    sess = boto3.session.Session(profile_name=profile)
    s3client = sess.client('s3')
    list_buckets_resp = s3client.list_buckets()
    for bucket in list_buckets_resp['Buckets']:
        logger.info('S3 bucket: %s', bucket['Name'])

def upload_file(infile, bucket='pcg-ds-s3', profile='default'):
    sess = boto3.session.Session(profile_name=profile)
    s3client = sess.client('s3')
    filename = os.path.basename(infile)
    s3client.upload_file(infile, bucket, filename)
    logger.info('%s has been uploaded as %s in bucket %s (profile: %s)', infile, filename, bucket, profile)

# as user hwang7, so far I get an error:
# botocore.exceptions.ClientError: An error occurred (AccessDenied) when calling the ListRoles operation:
#     User: arn:aws:iam::011152746114:user/hwang7 is not authorized to perform: iam:ListRoles on resource:
#         arn:aws:iam::011152746114:role/ with an explicit deny
def list_roles(profile='default'):
    sess = boto3.session.Session(profile_name=profile)
    client = sess.client('iam')
    roles = client.list_roles()['Roles']
    role = None
    for i, elem in enumerate(roles):
        logger.info('%d: %s', i, elem)

if __name__ == '__main__':
    list_buckets()
    upload_file('/Users/hwang7/myacct_cache/family_modules.pickle')
    #list_roles()
