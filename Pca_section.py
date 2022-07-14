import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
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
import plotly.express as px
import plotly.graph_objects as go


double_columns_in_players = ['Player','Pos','Tm','Age','G','MP','GS']

def pre_processing():
  path_players = "merge_2018_player.csv"
  player_2018 = pd.read_csv(path_players,index_col=0)
  player_2018 = player_2018.fillna(0)
  player_2018= player_2018.replace([np.inf, -np.inf], np.nan)
  player_2018 = player_2018.dropna()
  player_pos = player_2018.iloc[:, 0:2].to_numpy()
  player_2018 = player_2018.drop(double_columns_in_players, axis=1)
  pca2 = PCA(n_components=2)
  player_2018_pca = pca2.fit_transform(player_2018)
  all = np.concatenate((player_pos, player_2018_pca), axis=1)
  df_players = pd.DataFrame(all,columns=['Player', 'Pos', 'x1','x2'])
  return df_players

#Report
def report(df):
  print(df.head())
  print(df.describe().T)
  print(df.isnull().sum())

def make_players_graph_pca(df):
  global double_columns_in_players
  fig = px.scatter(df,x='x1', y='x2',color = 'Pos', text='Player')
  fig.update_layout(title_text="World of Players(PCA)", title_x=0.5)
  fig.update_layout(
      height=800,
  )
  fig.update_traces(mode="markers",hovertemplate='%{text}')
  fig.update_yaxes(visible=False, showticklabels=False)
  fig.update_xaxes(visible=False, showticklabels=False)
  return fig


def make_players_graph_pca_1(df,name):
  global double_columns_in_players
  df_player1 = df[df['Player']== name]
  x1 = float(df_player1['x1'].iloc[0])
  x2 = float(df_player1['x2'].iloc[0])
  x3 = str(df_player1['Player'].iloc[0])
  fig = px.scatter(df,x='x1', y='x2',color = 'Pos', text='Player')
  fig.add_traces(go.Scatter(x=[x1], y=[x2],text =[''],showlegend=False,
                          marker = dict(size = 22,
                                        color='Blue',symbol='star')))
  fig.update_layout(
      height=800,
  )
  fig.update_traces(mode="markers",hovertemplate='%{text}')
  fig.update_yaxes(visible=False, showticklabels=False)
  fig.update_xaxes(visible=False, showticklabels=False)
  fig.update_layout(title_text="World of Players(PCA)", title_x=0.5)
  return fig

def make_players_graph_pca_2(df,name1,name2):
  global double_columns_in_players
  df_player1 = df[df['Player']== name1]
  df_player2 = df[df['Player']== name2]
  x1 = float(df_player1['x1'].iloc[0])
  x2 = float(df_player1['x2'].iloc[0])
  x3 = str(df_player1['Player'].iloc[0])
  y1 = float(df_player2['x1'].iloc[0])
  y2 = float(df_player2['x2'].iloc[0])
  y3 = str(df_player2['Player'].iloc[0])
  fig = px.scatter(df,x='x1', y='x2',color = 'Pos', text='Player')
  fig.add_traces(go.Scatter(x=[x1], y=[x2],text =[''],showlegend=False,
                          marker = dict(size = 22,
                                        color='Blue',symbol='star')))
  fig.add_traces(go.Scatter(x=[y1], y=[y2],text =[''],showlegend=False,
                          marker = dict(size = 22,
                                        color='Red',symbol='star')))
  fig.update_layout(
      height=800,
  )
  fig.update_traces(mode="markers",hovertemplate='%{text}')
  fig.update_yaxes(visible=False, showticklabels=False)
  fig.update_xaxes(visible=False, showticklabels=False)
  fig.update_layout(title_text="World of Players(PCA)", title_x=0.5)
  return fig