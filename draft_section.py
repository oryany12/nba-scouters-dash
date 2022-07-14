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


def report(df):
  print(df.head())
  print(df.describe().T)
  print(df.isnull().sum())

def pre_processing():
  draft_01 = pd.read_csv("draft01.csv")
  player_2018 = pd.read_csv("merge_2018_player.csv",index_col=0)
  player_2018_draft = draft_01.merge(player_2018,left_on='Player', right_on='Player')
  return player_2018_draft

def create_lin_reg(df):
  df = df.drop(['Pos','Age','Player','Tm','G','MP'], axis=1)
  df = df.dropna()

  y = df['Pick']
  x = df.drop(['Pick'], axis=1)
  X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)

  lin_reg = LinearRegression()
  lin_reg = lin_reg.fit(X_train, y_train)

  return lin_reg

def check_draft_pick(lin_reg, df, name): 
  result = None
  try:
    player = df[df['Player']==name]
    player = player.drop(['Player','Pos'	,'Age',	'Tm',	'G'	,'MP'], axis=1)
    player = player.fillna(df.mean())
    result = max(round(lin_reg.predict(player)[0]),1)
    if result>30:
      result = name +" will not pick in any Draft"
  except:
    result = ""
  return result