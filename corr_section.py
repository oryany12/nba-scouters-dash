import plotly
import pandas as pd
import numpy as np
import plotly.express as px
from google.colab import drive

def pre_processing():
  path_players = "merge_2018_player.csv"
  players_2018 = pd.read_csv(path_players,index_col=0)
  players_2018 = players_2018.fillna(0)
  return players_2018

def make_matrix_corr_graph(df,features):
  features_corr = round(df[features].corr(),2)
  fig = px.imshow(features_corr, text_auto=True)
  fig.update_layout(title_text="Features Correlation Matrix", title_x=0.5)
  fig.update_xaxes(side="top")
  return fig

def make_scatter_graph(df, x1, x2):
  fig = px.scatter(df, x=x1, y=x2, trendline="ols")
  fig.update_layout(title_text="Features Correlation Scatter", title_x=0.5)
  return  fig

def make_empty_scatter_graph():
  fig = px.scatter()
  fig.update_layout(title_text="Features Correlation Scatter", title_x=0.5)
  return  fig