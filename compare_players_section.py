
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


def new_col(df):
    if (df['WINS'] == 1) and (df['TEAM_ID_home'] ==df['TEAM_ID_x']):
        return df['PLAYER_NAME_x']
    elif (df['WINS'] == 0) and (df['TEAM_ID_away'] ==df['TEAM_ID_x']):
        return df['PLAYER_NAME_x']
    else:
        return df['PLAYER_NAME_y']

def pre_processing():
  games_details = pd.read_csv('games_details.csv',low_memory=False)
  games = pd.read_csv('games.csv')
  games = games[games['SEASON'] <= 2018]
  return games_details,games

def make_players_pie_chart(games_details,games,name1,name2):
  player_1 = games_details[games_details['PLAYER_NAME'] == name1]
  player_2 = games_details[games_details['PLAYER_NAME'] == name2]
  merge_two_players = pd.merge(player_1,player_2,on='GAME_ID',how='inner')
  games_details_players=pd.merge(merge_two_players,games,on='GAME_ID',how='inner')
  games_details_players['who_win'] = games_details_players.apply(new_col, axis = 1)
  an_array = np.zeros(len(games_details_players.columns))
  games_details_players.loc[-1] = an_array
  games_details_players.index = games_details_players.index + 1  
  games_details_players.sort_index(inplace=True) 
  games_details_players['who_win'].iloc[0]=name1
  fig = px.pie(games_details_players, names='who_win')  
  fig.update_layout(showlegend=False)    
  fig.update_layout(
    title="Plot Title",
    xaxis_title="Names",
    yaxis_title="Number of wins")  
  fig.update_layout(title_text="Wins Precentage", title_x=0.5)        
  return fig

def make_players_hist(games_details,games,name1,name2):
  player_1 = games_details[games_details['PLAYER_NAME'] == name1]
  player_2 = games_details[games_details['PLAYER_NAME'] == name2]
  merge_two_players = pd.merge(player_1,player_2,on='GAME_ID',how='inner')
  games_details_players=pd.merge(merge_two_players,games,on='GAME_ID',how='inner')
  games_details_players['who_win'] = games_details_players.apply(new_col, axis = 1)
  an_array = np.zeros(len(games_details_players.columns))
  games_details_players.loc[-1] = an_array
  games_details_players.index = games_details_players.index + 1  
  games_details_players.sort_index(inplace=True) 
  games_details_players['who_win'].iloc[0]=name1
  fig = px.histogram(games_details_players, x='who_win',color="who_win")   
  fig.update_layout(showlegend=False)    
  fig.update_layout(
    title="Plot Title",
    xaxis_title="Names",
    yaxis_title="Number of wins")
  fig.update_layout(title_text="Number of Wins", title_x=0.5)        
  return fig

def make_empty_pie_chart():
  d = {'col1': [1, 1]}
  df = pd.DataFrame(data=d)
  fig = px.pie(df, values='col1')
  fig.update_layout(title_text="Wins Precentage", title_x=0.5)
  return fig
def make_players_graph_teams():
  fig = px.histogram()
  fig.update_layout(title_text="Number of Wins", title_x=0.5)
  return fig 