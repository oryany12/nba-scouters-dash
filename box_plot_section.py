
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import  cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import plotly
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def pre_processing():
  player_2018 = pd.read_csv("merge_2018_player.csv",index_col=0)
  player_2018 = player_2018.drop(['Pos','Age','Tm','G','MP'], axis=1)
  player_2018 = player_2018.dropna()
  return player_2018

def box_plot(df,fetures):
  df=df[fetures]
  fig = make_subplots(
    rows=1, cols=6)
  for i in range(6):
    x= df[fetures[i]]
    fig.add_trace(go.Box(y=x,name=fetures[i],marker_color = 'black'),
                row=1, col=i+1)
  fig.update_layout(showlegend=False)
  fig.update_layout(title_text="Features Distribution", title_x=0.5)        
  return fig

def box_plot_1(df,fetures,name):
  player_1 = df[df['Player'] == name]
  player_1 = player_1.fillna(df.mean())
  player_1 = player_1[fetures]
  df=df[fetures]
  fig = make_subplots(
    rows=1, cols=6)
  for i in range(6):
    x= df[fetures[i]]
    y=float(player_1[fetures[i]].iloc[0])
    fig.add_trace(go.Box(y=x,name=fetures[i],marker_color = 'black'),
                row=1, col=i+1)
    fig.add_shape(type='line',
                  x0=-1,
                  y0=y,
                  x1=2,
                  y1=y,
                  line=dict(color='blue',),
                  xref='x',
                  yref='y',
                  row=1,
                  col=i+1
    )
  fig.update_layout(showlegend=False)
  fig.update_layout(title_text="Features Distribution", title_x=0.5)        
  return fig

def box_plot_2(df,fetures,name1,name2):
  player_1 = df[df['Player'] == name1]
  player_2 = df[df['Player'] == name2]
  player_1 = player_1.fillna(df.mean())
  player_2 = player_2.fillna(df.mean())
  player_1 = player_1[fetures]
  player_2 = player_2[fetures]
  df=df[fetures]
  fig = make_subplots(
    rows=1, cols=6)
  for i in range(6):
    x= df[fetures[i]]
    y=float(player_1[fetures[i]].iloc[0])
    z=float(player_2[fetures[i]].iloc[0])
    fig.add_trace(go.Box(y=x,name=fetures[i],marker_color = 'black'),
                row=1, col=i+1)
    fig.add_shape(type='line',
                  x0=-1,
                  y0=y,
                  x1=2,
                  y1=y,
                  line=dict(color='blue',),
                  xref='x',
                  yref='y',
                  row=1,
                  col=i+1
    )
    fig.add_shape(type='line',
                  x0=-1,
                  y0=z,
                  x1=2,
                  y1=z,
                  line=dict(color='red',),
                  xref='x',
                  yref='y',
                  row=1,
                  col=i+1
    )
  fig.update_layout(showlegend=False)
  fig.update_layout(title_text="Features Distribution", title_x=0.5)        
  return fig