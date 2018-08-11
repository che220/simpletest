import os, sys, logging, boto3, re
from training import train_env

logger = logging.getLogger(os.path.basename(__file__))
S3_BUCKET = 'anything'
S3_DIR = "s3://{}/my_dir".format(S3_BUCKET)

def get_s3_client(profile='default'):
    sess = boto3.session.Session(profile_name=profile)
    s3client = sess.client('s3')
    return s3client

def list_buckets(s3_client):
    list_buckets_resp = s3_client.list_buckets()
    for bucket in list_buckets_resp['Buckets']:
        logger.info('S3 bucket: %s', bucket['Name'])

def upload_file(s3_client, infile, s3_dir):
    filename = os.path.basename(infile)
    ss = re.sub('^s://', '', s3_dir)
    bucket = re.sub('/.*', '', ss)
    key = ss if '/' not in ss else ss[(len(bucket)+1):]
    key += filename
    s3_client.upload_file(infile, bucket, key)
    s3_path = 's3://{}/{}'.format(bucket, key)
    logger.info('%s has been uploaded as %s', infile, s3_path)
    return s3_path

if __name__ == '__main__':
    train_env.define_dirs_for_local()
    tar_file = train_env.model_dir + '/opt/ml/model.tar.gz'
    s3_dir = re.sub('s3://', '', S3_DIR + '/training/model/')

    s3 = get_s3_client()
    upload_file(s3, tar_file, s3_dir)

