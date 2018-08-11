import os, pandas as pd, numpy as np, re, pyodbc, decimal, logging, platform, datetime as dt
from string import Template
from subprocess import call

pd.set_option('display.width', 5000)
pd.set_option('max_columns', 600)
np.set_printoptions(threshold=np.nan) # print out all values, regardless length

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))

S3_DIR = "s3://my-s3/my_project"
data_dir = os.environ['DATA_CACHE_DIR']
TODAY = int(dt.datetime.now().strftime("%Y%m%d"))

def file_exists(the_file, dailyFile=False):
    """
    If dailyFile = true and the file is not created today, the file is regarded as non-existing

    :param theFile: file to be checked
    :param dailyFile: Controls to check if the file is up-to-date
    :return:
    """
    if os.path.isfile(the_file):
        if not dailyFile:
            return True

        mdate = int(dt.datetime.fromtimestamp(os.path.getmtime(the_file)).strftime('%Y%m%d'))
        logger.info("file = %s, mtime = %s", the_file, mdate)
        return mdate >= TODAY
    else:
        return False

def secondsSinceMidnight():
    now = dt.datetime.now()
    return int((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())

def peekTable(conn, table):
    sql = 'select * from {} limit 10'.format(table)
    logger.info("SQL Resultset:\n%s", sqlQuery(conn, sql))

def showColumnValues(conn, table, col):
    sqlTemp = Template('select ${col}, count(1) from ${table} group by ${col} order by ${col}')
    sql = sqlTemp.substitute(col=col, table=table)
    logger.info("SQL Resultset:\n%s", sqlQuery(conn, sql))

def grant(conn, table, permission='all', userString='everyone'):
    sqlUpdate(conn, 'grant {} on {} to {}'.format(permission, table, userString))
    
def sqlUpdate(conn, sql):
    cur = conn.cursor()
    logger.info("SQL update:\n\t%s", sql)
    cur.execute(sql)

## Good performance overall
def sqlQuery(conn, sql):
    """
    Fix the annoying decimal.Decimal object type to float64
    Int type in database is correctly mapped to int64
    """
    cur = conn.cursor()
    logger.info("SQL select:\n\t%s", sql)
    
    cur.execute(sql)
    qryCols = []
    decType = type(decimal.Decimal())
    intType = type(int(0))
    intCols = decCols = {}
    for i in cur.description:
        col = i[0]
        if i[1] == decType:
            decCols[col] = 'float'
        elif i[1] == intType:
            intCols[col] = 'int64'
        qryCols.append(col)

    result = cur.fetchall()
    if len(result) == 0:
        df = pd.DataFrame(columns=qryCols)
    else:
        df = pd.DataFrame(np.array(result), columns=qryCols)
    if len(decCols) > 0:
        df = df.fillna(dict(zip(decCols.keys(), [0.0]*len(decCols))))
        df = df.astype(decCols)
    if len(intCols) > 0:
        df = df.fillna(dict(zip(intCols.keys(), [0]*len(intCols))))
        df = df.astype(intCols)
    cur.close()
    return df

def dropTable(conn, table):
    sql = "drop table if exists %s" % table
    sqlUpdate(conn, sql)
    return

def createTableWithDataFrame(conn, table, dd, truncate=True, recreateTable=True):
    logger.info("----- createTableWithDataFrame -----")
    dd.columns = [col.replace('/', '_') for col in dd.columns]
    dd.columns = [col.replace('-', '_') for col in dd.columns]

    sql = "CREATE TABLE {} (".format(table)
    for col in dd.columns:
        #print(col)
        colType = dd[col].dtype
        if colType == np.object or colType == bool:
            ss = dd[col].map(str)
            maxChar = ss.map(len).max()+3
            sql = '{} {} varchar({}), '.format(sql, col, maxChar)
        else:
            if colType == np.float64:
                sql = '{} {} numeric(30, 6), '.format(sql, col)
            elif colType == 'datetime64[ns]':
                sql = '{} {} timestamp, '.format(sql, col)
            else:
                sql = '{} {} numeric(19, 0), '.format(sql, col)

    sql = re.sub(', $', '', sql)
    sql += ')'
    if recreateTable:
        dropTable(conn, table)
        sqlUpdate(conn, sql)
    importIntoVertica(conn, dd, table, truncate=truncate)

def verticaTableExists(vertica, tableWithSchema):
    schema = re.sub('\\..*', '', tableWithSchema)
    table = re.sub('.*\\.', '', tableWithSchema)
    sql = "SELECT * FROM ALL_TABLES where SCHEMA_NAME='{}' and TABLE_NAME='{}'".format(schema, table)
    dd = sqlQuery(vertica, sql)
    return dd.shape[0] > 0

def createTableWithSelect(conn, table, sql):
    logger.info("----- createTableWithSelect -----")
    dropTable(conn, table)
    sql = "create table %s as /*+ direct */ %s" % (table, sql)
    sqlUpdate(conn, sql)

    sql = "select count(1) as COUNT from %s" % table
    dd = sqlQuery(conn, sql)
    logger.info("Total %d rows in %s", dd.iloc[0,0], table)
    return

## Any hope of using pandas.to_sql(table_name, conn)?
def importIntoVertica(vertica, df, table, truncate=True):
    pid = os.getpid()
    outfile = '%s/_import_%s.csv' % (data_dir, pid)
    df.to_csv(outfile, index=False, header=False)
    if truncate:
        sqlUpdate(vertica, 'truncate table %s' % table)

    excepFile = '%s/vertica_exception_%07d.txt' % (data_dir, pid)
    sql = "COPY %s FROM local '%s' DELIMITER ',' NULL AS '' ENCLOSED BY '\"' EXCEPTIONS '%s'" % (table, outfile, excepFile)
    sqlUpdate(vertica, sql)
    logger.info("Import %d rows of data into table %s is completed", df.shape[0], table)
    if os.path.isfile(excepFile):
        logger.info("Vertica import has exceptions in %s", excepFile)
    else:
        logger.info("Vertica import has no exceptions")

    os.remove(outfile)
    return

## ===========*****  Database Connections *****============
def getDBConnection(dsn):
    logger.debug('HOME: %s', os.environ['HOME'])
    logger.debug('connecting to dsn: %s', dsn)
    osName = platform.system().upper()
    if osName == 'LINUX' and dsn == 'sbg_vertica':
        cmd = ['/usr/bin/kinit', 'sys_vertica_cdo', '-k', '-t',
               '{}/.ssh/sys_vertica_cdo.keytab'.format(os.environ['HOME'])]
        logger.info('Run kinit: %s', ' '.join(cmd))
        call(cmd)

    conn = pyodbc.connect('DSN={}'.format(dsn), autocommit=True)

    # encodings are needed for Mac OSX
    conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    if osName == 'DARWIN':
        conn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-32le')
    conn.setencoding(encoding='utf-8')
    return conn

if __name__ == '__main__':
    h = getDBConnection('sbg_vertica')
    sql = "select * from s1.t1 limit 10"
    df = sqlQuery(h, sql)
    logger.info('DataFrame Info:\n%s\n%s\n%s', df.head(5), df.shape, df.dtypes)
