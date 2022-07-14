
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


def pre_processing():
  Player_Salary = pd.read_csv("Salaries.csv")
  return Player_Salary

def make_players_graph_salary():
  return None
#   fig =  px.histogram()
#   fig.update_layout(title_text="Salary over Years", title_x=0.5)
#   return fig


def make_players_graph_salary_2(df,name1,name2):
  df_player1 = df[df['Player']== name1]
  x1= df_player1['Season']
  y1 = df_player1['Salary']
  df_player2 = df[df['Player']== name2]
  x2= df_player2['Season']
  y2 = df_player2['Salary']
  f1 = go.Figure(
      data = [
          go.Scatter(x=x1, y=y1, name=name1),
          go.Scatter(x=x2, y=y2, name=name2),
      ],
    layout = {"xaxis": {"title": "Year"}, "yaxis": {"title": "Salary"}}
)
  f1.update_layout(showlegend=False)
  f1.update_layout(title_text="Salary over Years", title_x=0.5)
  return f1

def make_players_graph_salary_1(df,name):
  df_player1 = df[df['Player']== name]
  x1= df_player1['Season']
  y1 = df_player1['Salary']
  f1 = go.Figure(
      data = [
          go.Scatter(x=x1, y=y1, name=name),
      ],
    layout = {"xaxis": {"title": "Year"}, "yaxis": {"title": "Salary"}}
)
  f1.update_layout(showlegend=False)
  f1.update_layout(title_text="Salary over Years", title_x=0.5)
  return f1

def make_players_graph_teams():
  fig = px.histogram()
  fig.update_layout(title_text='Number of Seasons played each Team', title_x=0.5)
  return fig

def make_players_graph_teams_1(df,name):
  df_player1 = df[df['Player']== name]
  fig = px.histogram(df_player1, x="Long_team", text_auto=True, color="Player",barmode  = 'group',labels={
                     "Long_team": "Team ",
                 })
  fig.update_xaxes(tickangle=-45)
  fig.update_yaxes(title_text="Number of seasons")
  fig.update_layout(showlegend=False)
  fig.update_layout(title_text="Number of Seasons played each Team", title_x=0.5)
  return fig


def make_players_graph_teams_2(df,name1,name2):
  df_player1 = df[df['Player']== name1]
  df_player2 = df[df['Player']== name2]
  two_players = pd.concat([df_player2, df_player1])
  fig = px.histogram(two_players, x="Long_team", text_auto=True, color="Player",barmode  = 'group',labels={
                     "Long_team": "Team ",
                 })
  fig.update_xaxes(tickangle=-45)
  fig.update_yaxes(title_text="Number of seasons")
  fig.update_layout(showlegend=False)
  fig.update_layout(title_text="Number of Seasons played each Team", title_x=0.5)
  return fig
