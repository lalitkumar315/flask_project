from flask import Flask, jsonify, render_template, request
import pandas as pd
import numpy as np
import plotly
import pyodbc
import json
import plotly.graph_objs as go
import plotly.express as px



app = Flask(__name__)

## FUNCTION FOR FETCH THE DATA FROM SQL SERVER.
def fetchSqlData(driver,server,database,userId,password,tblName):
    try:  
        conn = pyodbc.connect(f'Driver={driver};Server={server};Database={database};UID={userId};PWD={password};Trusted_Connection=yes;')
        conn.timeout = 60    
        conn.autocommit = True 
        query = (f'SELECT * FROM {tblName};')
        data = pd.read_sql(query, conn)
        print('Extracted data from SQL SERVER') 
        conn.close()
        print('closed db connection')
        return data
    except pyodbc.Error as err:
        print('Error !!!!! %s' % err)
    except:
        print('something else failed miserably')

## CHANGE THE SERVER CREDENTIALS BELOW.
sql_df = fetchSqlData('SQL Server','.','Assignment','lalit','','tblJsonData')

## SAVE TO LOCAL FOR FASTER EXECUTION.
sql_df.to_csv('static/data/tmp_dataframe.csv', index=False)
df = pd.read_csv('static/data/tmp_dataframe.csv')
print('Saved to Local')

df['likelihood'] = df['likelihood'].fillna(0).astype(int)
df['intensity'] = df['intensity'].fillna(0).astype(int)

@app.route('/')
def index():
   return render_template('index.html', data = df)

@app.route('/charts', methods=['GET', 'POST'])
def charts():
    df_json = df.to_json(orient='records')
    metaData = uniqueList()
    # Get the filter parameters from the request
    region = request.form.get('region')
    sector = request.form.get('sector')

    # Filter the data based on the selected parameters
    filtered_data = df[(df['region'] == region) & (df['sector'] == sector)]

    # Create a Plotly figure object
    fig = go.Figure(
        data=[go.Bar(x=filtered_data['end_year'], y=filtered_data['relevance'])],
        layout=go.Layout(title='Sector by Year')
    )
    
    fig1 = px.scatter(df, x='end_year', y='likelihood', size='intensity', color='country', hover_data=['region', 'topic'], title='Energy Sector Likelihood by Country and Year')
    # Convert the Plotly figure to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('charts.html',chart=fig1 .to_html(full_html=False) ,graphJSON=graphJSON ,data = df_json,region = metaData[0], sector = metaData[5], country = metaData[1],topic = metaData[2],endyear =metaData[3],pest =metaData[4],source = metaData[6])

def uniqueList():
    regions = df['region'].unique()
    countries = df['country'].unique()
    topics = df['topic'].unique()
    years = df['end_year'].unique()
    pest = df['pestle'].unique()  
    sectors = df['sector'].unique()
    sources = df['source'].unique()
    return regions,countries,topics,years,pest,sectors,sources
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
