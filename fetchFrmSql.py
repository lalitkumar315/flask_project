import pyodbc
import pandas as pd

def fetchSqlData(driver,server,database,userId,password,tblName):
    try:  
        conn = pyodbc.connect(f'Driver={driver};Server={server};Database={database};UID={userId};PWD={password};Trusted_Connection=yes;')
        conn.timeout = 60    
        conn.autocommit = True 
        query = (f'SELECT * FROM {tblName};')
        df = pd.read_sql(query, conn)  
        print('EXTRACTED data') 
        print (df)
        conn.close()
        print('closed db connection')
        return df
    except pyodbc.Error as err:
        print('Error !!!!! %s' % err)
    except:
        print('something else failed miserably')

    
fetchSqlData('SQL Server','.','Assignment','lalit','','tblJsonData')