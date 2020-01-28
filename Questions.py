""""
Test :
Babak Emami,
emami.babak@gmail.com
Python 3.6

"""




# importing the requirments 
import pandasql as ps
import pandas as pd
import numpy as np

import converter
from converter import  pro_to_dec, us_to_dec
from decimal import Decimal
import sqlite3
import webbrowser

#Import Databases 
df = pd.read_csv('MLB2016.csv')
dfline=pd.read_csv('df_lines.csv')

# Creat SQLite dabase 
databasename= 'SQ.db'
db = sqlite3.connect(databasename)

#Add 2 columns Twin: shoes which team have acied, Winners: shows the winner for each game

df['Twin'] = np.where(df.FinalScoreAway<df.FinalScoreHome, 2, np.where(df.FinalScoreAway > df.FinalScoreHome,1, 0))
df['winner'] = np.where(df.FinalScoreAway<df.FinalScoreHome, df.HomeTeam, np.where(df.FinalScoreAway > df.FinalScoreHome,df.AwayTeam, 0)) 

#-------------------------Q1------------------
Q1 = pd.Series(df.loc[df['DoubleHeaderGame'] >= 1, ['HomeTeam', 'AwayTeam']].squeeze().values.ravel()).value_counts()


#-------------------------Q2------------------

QQ2= pd.merge(pd.DataFrame({'TeamName':df[['HomeTeam','AwayTeam']].stack().value_counts().index,'TotalGame':df[['HomeTeam','AwayTeam']].stack().value_counts().values}),
              pd.DataFrame({'TeamName':df['winner'].value_counts().index,'TotalWin':df['winner'].value_counts().values} ),
                 left_on='TeamName', right_on='TeamName', how='left').fillna(0)

qr = """ SELECT * ,(TotalGame-TotalWin) as looses, (TotalWin/TotalGame ) as WinPct
FROM QQ2 order by  (TotalWin/TotalGame ) DESC ,TotalWin DESC ;"""
QQ2= ps.sqldf(qr, locals())


dfline['TotalOddsChange']=dfline['GameId']
dd=dfline.groupby('GameId').agg({'MoneyUS1':['max', 'mean',('PRBMoneyUS1',lambda x:(pro_to_dec (us_to_dec(x.mean()))))], 
                         'MoneyUS2':[ 'max', 'mean',('PRBMoneyUS2', lambda x:(pro_to_dec (us_to_dec(x.mean()))))], 
                         'TotalPoints':['max', 'mean','count'],
                         'TotalOddsChange': 'count' }).sort_values(by=[('TotalOddsChange', 'count')], ascending=0)

#-------------------------Q3------------------
QQ3=dd[[('TotalOddsChange', 'count'),('MoneyUS1','PRBMoneyUS1'),('MoneyUS2','PRBMoneyUS2')]].head(5)

Q3a=df[['GameID','AwayTeam','HomeTeam','winner']].merge(QQ3, left_on='GameID', right_on='GameId', how='right').sort_values(by=[('TotalOddsChange', 'count')], ascending=0)

Qt4= df.merge(dd, left_on='GameID', right_on='GameId', how='outer')


#-------------------------Q4------------------


Qt4.to_sql("Q3", db, if_exists="replace")


QQ4 ="""SELECT  HomeStartingPicher,
 (SUM(CASE WHEN Twin = 1
         THEN "('MoneyUS1', 'PRBMoneyUS1')"
      	ELSE 0
    END)) +
 (SUM(CASE WHEN Twin = 2
         THEN "('MoneyUS2', 'PRBMoneyUS1')"
      ELSE 0
    END))AS us2 , 
    Count (HomeStartingPicher) as total_game
FROM Q3
GROUP BY HomeStartingPicher
having total_game >=10 
order by total_game DESC, us2 DESC ;"""

qq4=pd.read_sql(QQ4, db, index_col=None)


# export results to the Excle file


writer = pd.ExcelWriter('Results.xlsx')
Q1.to_excel(writer,'Q1')
dd.to_excel(writer,'Q2_1')
QQ2.to_excel(writer,'Q2_2')
Q3a.to_excel(writer,'Q3')
qq4.to_excel(writer,'Q4')
writer.save()






#---------------------- statics graphs

from flask import Flask

import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()


# regarding the use of interactive graph, I have to define the X , and Y-axixs for each graph id,
# Dash cannot extract the data from Pandas DataFrame directly


#-------------------------Q1------------------

YDuble = np.array(Q1.values).tolist()
XQ1= np.array(Q1.index).tolist()
#-------------------------Q2------------------
YGame= np.array(QQ2.TotalGame.values).tolist()
YWin=np.array(QQ2.TotalWin.values).tolist()
YLoos=np.array(QQ2.looses.values).tolist()
XX = np.array(QQ2.TeamName.values).tolist()
XxX= np.array(QQ2.TeamName.index).tolist()
#-------------------------Q3------------------
YTood=np.array(Q3a[('TotalOddsChange', 'count')].values).tolist()
YUS1=np.array(Q3a[('MoneyUS1','PRBMoneyUS1')].values).tolist()
YUS2=np.array(Q3a[('MoneyUS2','PRBMoneyUS2')].values).tolist()
XQ3 = np.array(Q3a.GameID.values).tolist()
#-------------------------Q4------------------
YTUs=np.array(qq4.us2.values).tolist()
YTG=np.array(qq4.total_game.values).tolist()
XQ4 = np.array(qq4.HomeStartingPicher.values).tolist()




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Babak Emami, 6473266199'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(
        id='example-graph1',
        figure={
            'data': [

                {'x': XQ1, 'y': YDuble, 'type': 'bar', 'name': 'Total Odds'},

            ],
            'layout': {
                'title': 'Q1 : Most Double Headers '
            }
        }
    ),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': XX, 'y': YGame, 'type': 'bar', 'name': 'Totoal Game'},
                {'x': XX, 'y': YWin, 'type': 'bar', 'name': 'Total Win'},
                {'x': XX, 'y': YLoos, 'type': 'bar', 'name': 'Totoal Looses'},
                
            ],
            'layout': {
                'title': 'Q2 : Total Wins and Losses '
            }
        }
    ),
    dcc.Graph(
    id='example-graphq3',
    figure={
        'data': [

            {'x': XQ3, 'y': YTood, 'type': 'bar', 'name': 'Totoal OOds'},
            {'x': XQ3, 'y': YUS1, 'type': 'bar', 'name': 'ProbUS1'},
            {'x': XQ3, 'y': YUS2, 'type': 'bar', 'name': 'ProbUS2'},
            

        ],
        'layout': {
            'title': 'Q3 :  Top 5 Games Based on Odds Changes'
        }
    }
    ),
    dcc.Graph(
    id='example-graphq4',
    figure={
        'data': [

            {'x': XQ4, 'y':YTG, 'type': 'bar', 'name': 'Totoal Games'},
            {'x': XQ4, 'y':YTUs , 'type': 'bar', 'name': 'MeanMl'},
            
            

    ],
    'layout': {
        'title': 'Q4 : Best Pitcher'
    }
    }
    )
    
])
# call the browser to run the Dash server
webbrowser.open_new_tab('http://127.0.0.1:8050/')

if __name__ == '__main__':
    app.run_server(debug=True)
    








  











