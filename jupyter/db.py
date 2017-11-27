import os, pandas as pd, traceback, random, jaydebeapi as jdbc, numpy as np, re
import intuit_env, easygui
from string import Template
from IPython.display import display, HTML

# convert java.lang.Long to numpy.int64
jdbc._DEFAULT_CONVERTERS.update({'BIGINT': jdbc._java_to_py('longValue')})

VERTICA_SERVER = 'pprddaavth-vip.ie.intuit.net'
IFA_SERVER = 'oraifaprd01.corp.intuit.net'

def peekTable(conn, table):
    sql = 'select * from {} limit 10'.format(table)
    display(sqlQuery(conn, sql))

def showColumnValues(conn, table, col):
    sqlTemp = Template('select ${col}, count(1) from ${table} group by ${col} order by ${col}')
    sql = sqlTemp.substitute(col=col, table=table)
    display(sqlQuery(conn, sql))

def grant(conn, table, permission='all', userString='PTG_USERS, PTG_ADMINS, PTG_ANALYSTS'):
    sqlUpdate(conn, 'grant {} on {} to {}'.format(permission, table, userString))
    
def sqlUpdate(conn, sql):
    cur = conn.cursor()
    print(sql)
    cur.execute(sql)

## slow for Oracle
def sqlQueryDF(conn, sql):
    print(sql)
    return pd.read_sql(sql, conn)

## Good performance overall
def sqlQuery(conn, sql):
    cur = conn.cursor()
    print(sql)
    cur.execute(sql)
    
    qryCols = [i[0] for i in cur.description]
    df = pd.DataFrame()
    while True:
        rows = cur.fetchmany(200000) # RAM can handle this
        if len(rows) == 0:
            break
        
        tmp = pd.DataFrame(rows, columns=qryCols)
        if df is None or df.shape[0] == 0:
            df = tmp
        else:
            df = df.append(tmp)
            
    cur.close()
    return df

def dropTable(conn, table):
    sql = "drop table if exists %s" % table
    sqlUpdate(conn, sql)
    return

def createTableWithDataFrame(conn, table, dd):
    print('----------------------------------------------')
    dd.columns = [col.replace('/', '_') for col in dd.columns]
    dd.columns = [col.replace('-', '_') for col in dd.columns]

    sql = "CREATE TABLE {} (".format(table)
    for col in dd.columns:
        print(col)
        colType = dd[col].dtype
        if colType == np.object or colType == bool:
            ss = dd[col].map(str)
            maxChar = ss.map(len).max()+3
            sql = '{} {} varchar({}), '.format(sql, col, maxChar)
        else:
            if colType == np.float64:
                sql = '{} {} numeric(30, 6), '.format(sql, col)
            else:
                sql = '{} {} numeric(19, 0), '.format(sql, col)

    sql = re.sub(', $', '', sql)
    sql += ')'
    dropTable(conn, table)
    sqlUpdate(conn, sql)
    importIntoVertica(conn, dd, table, truncate=True)

def createTableWithSelect(conn, table, sql):
    print('----------------------------------------------')
    dropTable(conn, table)
    sql = "create table %s as %s" % (table, sql)
    sqlUpdate(conn, sql)

    sql = "select count(1) as COUNT from %s" % table
    dd = sqlQuery(conn, sql)
    print("Total %d rows in %s" % (dd.iloc[0,0], table))
    return

## Any hope of using pandas.to_sql(table_name, conn)?
def importIntoVertica(vertica, df, table, truncate=True):
    outfile = '%s/_import_.csv' % intuit_env.LOG_DIR
    df.to_csv(outfile, index=False, header=False)
    if truncate:
        sqlUpdate(vertica, 'truncate table %s' % table)

    tag = int(random.random()*1000000)
    excepFile = '%s/vertica_exception_%07d.txt' % (intuit_env.LOG_DIR, tag)
    sql = "COPY %s FROM local '%s' DELIMITER ',' NULL AS '' ENCLOSED BY '\"' EXCEPTIONS '%s'" % (table, outfile, excepFile)
    sqlUpdate(vertica, sql)
    print("Import %d rows of data into table %s is completed" % (df.shape[0], table))
    if os.path.isfile(excepFile):
        print("Vertica import has exceptions in %s" % excepFile)
    else:
        print("Vertica import has no exceptions")
        
    return

## ===========*****  Database Connections *****============
def getDBConnection(dbName):
    dbFile = '{}/.ssh/db.txt'.format(intuit_env.DB_FILE_DIR)
    df = pd.DataFrame.from_csv(dbFile, sep=' ', header=-1)
    login = df.loc[dbName]
    if login is None:
        raise(Exception('Cannot recognize DB name: {}'.format(dbName)))

    conn = None
    if dbName.startswith('ifa'):
        conn = ifaConnection(login[1], login[2])
    elif dbName.startswith('vertica'):
        conn = verticaConnection(login[1], login[2])
    else:
        raise(Exception('Function to connect to {} is not implemented yet.'.format(dbName)))

    return conn

def verticaConnection(user, password=None):
    if password is None:
        password = easygui.passwordbox("Vertica user %s password:" % user)
    conStr = 'jdbc:vertica://%s:5433/Analytics' % VERTICA_SERVER
    print(conStr)

    connection = None
    try:
        connection = jdbc.connect("com.vertica.jdbc.Driver", conStr,
                                  [user, password], intuit_env.JDBC_JARS)
    except:
        traceback.print_stack()
        raise

    return connection

def ifaConnection(user, password=None):
    if password is None:
        password = easygui.passwordbox("IFA user %s password:" % user)
    conStr = 'jdbc:oracle:thin:@%s:1521:IFAPRD01' % IFA_SERVER
    print(conStr)
    
    connection = None
    try:
        connection = jdbc.connect("oracle.jdbc.driver.OracleDriver", conStr,
                                  [user, password], intuit_env.JDBC_JARS)
    except:
        traceback.print_stack()
        raise

    return connection
