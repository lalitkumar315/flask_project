import pyodbc
import json
import pandas as pd

def jsonToSql(driver,server,database,userId,password,filePath):
    conn = pyodbc.connect(f'Driver={driver};Server={server};Database={database};UID={userId};PWD={password};Trusted_Connection=yes;')
    conn.timeout = 60    
    conn.autocommit = True

    with open(f"{filePath}", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
        json_string = json.dumps(data) 

    df = pd.DataFrame(data)
    print(df)

    try:        
        cursor = conn.cursor()
        cursor.execute('DROP TABLE tblJsonData;')
        cursor.execute('''CREATE TABLE [dbo].[tblJsonData](
                            end_year NVARCHAR(50),
                            intensity NVARCHAR(50),
                            sector NVARCHAR(50),
                            topic NVARCHAR(50),
                            insight NVARCHAR(150),
                            url NVARCHAR(150),
                            region NVARCHAR(50),
                            start_year NVARCHAR(50),
                            impact NVARCHAR(50),
                            added NVARCHAR(50),
                            published NVARCHAR(50),
                            country NVARCHAR(50),
                            relevance NVARCHAR(50),
                            pestle NVARCHAR(50),
                            source NVARCHAR(50),
                            title NVARCHAR(150),
                            likelihood NVARCHAR(50)
                            );''')
        cursor.execute('EXEC prcInsertJsonData @json = ?', json_string)
        print('data inserted')    
    except pyodbc.Error as err:
        print('Error !!!!! %s' % err)
    except:
        print('something else failed miserably')

    conn.close()
    print('closed db connection')

jsonToSql('SQL Server','.','Assignment','lalit','','static/data/jsondata.json')