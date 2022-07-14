import plotly.express as px
import numpy as np
from plotly import figure_factory as ff
from dash import Dash, dcc, html, Input, Output, callback, State
import plotly.graph_objects as go
import dash_daq as daq
from collections import Counter
import random
import pandas as pd
import plotly.graph_objects as go

def get_norm_df_players(df):
  players_2018_norm = df.drop(['Player','Pos', 'Age','Tm'], axis=1)
  players_2018_norm = (players_2018_norm-players_2018_norm.mean())/(players_2018_norm.std())
  players_2018_norm = (players_2018_norm-players_2018_norm.min())/(players_2018_norm.max()-players_2018_norm.min())

  players_2018_norm = pd.concat((df[['Player','Pos', 'Age','Tm']], players_2018_norm), 1)
  return players_2018_norm

def get_player_pentagon(df,name,features):
  player = df[df['Player']==name]
  pentagon = player[features]

  fig = go.Figure(data=go.Scatterpolar(
  r=list(pentagon.iloc[0]),
  theta=features,
  fill='toself'
  ))

  fig.update_layout(
    polar=dict(
      radialaxis=dict(
        visible=False,
        range=[0, 1]
      )),
    showlegend=False
  )
  fig.update_layout(title_text="Attribute Overview Comparison", title_x=0.5)
  return fig
  
def get_2_player_pentagon(df,name1,name2,features):
  player1 = df[df['Player']==name1]
  pentagon1 = player1[features]

  player2 = df[df['Player']==name2]
  pentagon2 = player2[features]

  fig = go.Figure()

  fig.add_trace(go.Scatterpolar(
        r=list(pentagon1.iloc[0]),
        theta=features,
        fill='toself',
        name=name1
  ))
  fig.add_trace(go.Scatterpolar(
      r=list(pentagon2.iloc[0]),
      theta=features,
      fill='toself',
      name=name2
  ))

  fig.update_layout(
    polar=dict(
      radialaxis=dict(
        visible=False,
        range=[0, 1]
      )),
    showlegend=False
  )
  fig.update_layout(title_text="Attribute Overview Comparison", title_x=0.5)
  return fig


def get_empty_pentagon(features):
  features = ['PTS','AST','TRB','BLK','STL','MPG']
  fig = go.Figure(data=go.Scatterpolar(
  r=[0]*6,
  theta=features,
  fill='toself'
  ))

  fig.update_layout(
    polar=dict(
      radialaxis=dict(
        visible=False,
        range=[0, 1]
      )),
    showlegend=False
  )
  fig.update_layout(title_text="Attribute Overview Comparison", title_x=0.5)
  return fig