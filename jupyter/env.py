import os, sys, inspect
import importlib
import datetime as dt
import pandas as pd
import numpy as np
from _csv import QUOTE_NONNUMERIC
import platform
import inspect
import traceback, socket
import smtplib
from email.mime.text import MIMEText

#pd.set_option('display.height', 1000)
#pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 5000) 
pd.set_option('max_columns', 600) 

# print out all values, regardless length
np.set_printoptions(threshold=np.nan)

osName = platform.system().upper()
__scriptDir = os.path.dirname(os.path.realpath(__file__))
ML_ROOT = __scriptDir
print('Script dir: %s' % (__scriptDir))
print('ML root dir: %s' % (ML_ROOT))

HOME = ''
DATA_CACHE_DIR = ''
WORKSPACE_DIR = ''
if osName == 'LINUX':
    HOME = os.environ['HOME']
    USER = os.environ['USER']
    if USER == 'root':
        HOME = '/home/pcg_ifa_owner'
        os.environ['HOME'] = HOME

    WORKSPACE_DIR = '{}/{}'.format(HOME, 'workspace')
    DATA_CACHE_DIR = '{}/{}'.format(HOME, 'spark_cache')
elif osName == 'WINDOWS':
    HOME = 'C:/Users/{}'.format(os.environ['USERNAME'])
    WORKSPACE_DIR = '{}/Box Sync/work/workspace'.format(HOME)
    DATA_CACHE_DIR = 'C:/PTG_DataScience/spark_cache'

print('Data cache dir: %s' % (DATA_CACHE_DIR))
LOG_DIR = '%s/%s' % (WORKSPACE_DIR, 'log')
DB_FILE_DIR = HOME
if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR)
    
print('home dir: %s' % (HOME))
print('Workspace dir: %s' % (WORKSPACE_DIR))
print('Log dir: %s' % (LOG_DIR))
print('DB file dir: %s' % (DB_FILE_DIR))

ORACLE_JAR = '{}/java_lib/ojdbc7.jar'.format(ML_ROOT)
VERTICA_JAR = '%s/java_lib/vertica-jdbc-7.0.1-0.jar' % ML_ROOT
POSTGRESQL_JAR = '%s/java_lib/postgresql-9.4-1201.jdbc41.jar' % ML_ROOT
JDBC_JARS = [ORACLE_JAR, VERTICA_JAR, POSTGRESQL_JAR]

BAD_CHARS = bytearray(range(0x80, 0x100)) # non-ASCII chars
BAD_CHARS.append(0x1A) # Octal 032 was blended in
BAD_CHARS.append(0xa0) # Octal 032 was blended in

PRODUCT_GROUPS = ['LACERTE', 'REP', 'PROSERIES', 'PPR', 'BASIC']

# Use Apr 15th as the line to figure out current TY for order data
def getCurrentOrderTY():
    a = dt.datetime.now()
    today = int(a.strftime("%Y%m%d"))
    year = int(today/10000)
    monthDate = today%10000
    if monthDate > 415:
        return year
    else:
        return year-1

## Use Dec 31 as the line to figure out current TY for filing
def getCurrentFilingTY():
    a = dt.datetime.now()
    today = int(a.strftime("%Y%m%d"))
    year = int(today/10000)
    return year-1

## Use July 31 as the line to figure out current FY
def getCurrentFY():
    a = dt.datetime.now()
    today = int(a.strftime("%Y%m%d"))
    year = int(today/10000)
    monthDate = today%10000
    if monthDate >= 801:
        return year+1
    else:
        return year

def currentYYYYMMDD():
    return int(dt.date.today().strftime("%Y%m%d"))

def daysAgoYYYYMMDD(days=0):
    a = dt.datetime.now() - dt.timedelta(days=days)
    return int(a.strftime("%Y%m%d"))

def minisecondsFromEpoch():
    return (dt.datetime.now() - dt.datetime(1970,1,1)).total_seconds() * 1000

def filePath(fileDir, fileName):
    return '%s/%s' % (fileDir, fileName)

def shouldAccept():
    ans=input("Accept this (y/n/q to abort)? ")
    ans = ans.upper().strip()
    if ans == 'Q':
        print("Aborted")
        sys.exit()
        
    return ans.upper() == 'Y';

def cleanNA(df, column, defaultVal):
    x = df[column]
    x.values[x.isnull()] = defaultVal
    return df

def replaceNullStringWithZero(dd):
    for col in dd.columns:
        if isinstance(dd[col][0], str):
            x = dd[col]
            x.values[x.isnull() | (x == 'NAN')] = '0'
    return dd

def examCounts(dd, groupCols, ignoreUnique=True):
    print("Counts on %s ..." % groupCols)
    x = dd.groupby(groupCols)[[groupCols]].size()
    if ignoreUnique:
        x = x[x > 1.1].copy()
    x = x.sort_values(ascending=False)
    print(x.head(5))
    return None

def read_csv(dataFile, dtype=None):
    return pd.read_csv(dataFile, dtype=dtype, encoding='utf-8')

def to_csv(dataFile, dd):
    dd.to_csv(dataFile, index=False, quoting=QUOTE_NONNUMERIC, quotechar='"', encoding='utf-8')
    return

def exitProc(i):
    try:
        if i == 0:
            sys.exit(0)
        else:
            sys.exit(i)
    except:
        if i == 0:
            pass
    return

def rmBadChars(myStr):
    myStr = myStr.translate(None, BAD_CHARS)
    return myStr

def getThisFunctionNmae():
    return (inspect.stack())

def showInfo(df):
    print(df.head(5))
    print(df.shape)
    print(df.dtypes)
    return

def reload(name):
    modin = importlib.import_module(name, package=None)
    importlib.reload(modin)
    return None

def inspectFunction(name):
    lines = inspect.getsourcelines(name)
    print("".join(lines[0]))

def sendEmail(text, subject, addressList):
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = '{}@{}'.format(os.environ['USER'], socket.gethostname())
    msg['To'] = ', '.join(addressList)

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

def sendMultiLineEmail(lines, subject, addressList):
    text = "<html><body><table>"
    for line in lines:
        text = '{}<tr>{}</tr>'.format(text, line)
    text = "{}</table></body></html>".format(text)
    
    msg = MIMEText(text, 'html')
    msg['Subject'] = subject
    msg['From'] = '{}@{}'.format(os.environ['USER'], socket.gethostname())
    msg['To'] = ', '.join(addressList)

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
    