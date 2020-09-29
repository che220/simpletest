import snowflake.connector
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
import pandas as pd

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_colwidth', 5000)
pd.set_option('max_columns', 600)
pd.set_option('display.float_format', lambda x: '%.2f' % x)  # disable scientific notation for print


with open("snowflake_rsa_key.p8", "rb") as key:
    p_key = serialization.load_pem_private_key(key.read(),
                                               password=os.environ['SNOWSQL_PRIVATE_KEY_PASSPHRASE'].encode(),
                                               backend=default_backend())
pkb = p_key.private_bytes(encoding=serialization.Encoding.DER,
                          format=serialization.PrivateFormat.PKCS8,
                          encryption_algorithm=serialization.NoEncryption())

ctx = snowflake.connector.connect(user='username',
                                  account='account_name',
                                  private_key=pkb)
cs = ctx.cursor()
try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchall()
    print(one_row[0])
finally:
    cs.close()
ctx.close()
