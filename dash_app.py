# Imports
import plotly.express as px
import numpy as np
from plotly import figure_factory as ff
from dash import Dash, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash_daq as daq
from collections import Counter
import random
import pandas as pd
import plotly.graph_objects as go
import corr_section
import draft_section
import Pca_section
import draft_section
import pentagon_section
import Salary_section
import compare_players_section as cwps
import box_plot_section

#Global paramete
app = Dash(__name__, suppress_callback_exceptions=True)
server=app.server

# DF's
players_2018 = corr_section.pre_processing()
pca_players = Pca_section.pre_processing()
player_2018_draft = draft_section.pre_processing()
players_2018_norm = pentagon_section.get_norm_df_players(player_2018_draft)
salary = Salary_section.pre_processing()
games_details,games = cwps.pre_processing()

#Models
lg_draft = draft_section.create_lin_reg(player_2018_draft)

#Params
players_names = list(player_2018_draft['Player'])
img_nba = 'https://www.wallpaperflare.com/static/296/615/731/nba-basketball-logo-wallpaper.jpg'
ATK_features = ['MPG','AST','PTS','FT.','X2P.','X3P.']
DFS_features = ['ORB','DRB','BLK','STL','PF','DBPM']


#fig
pca_fig = Pca_section.make_players_graph_pca(pca_players)


#HTML's
matrix_html = dcc.Graph('matrix_corr_graph',figure=corr_section.make_matrix_corr_graph(players_2018,ATK_features))
corr_html = dcc.Graph('corr_graph',figure=corr_section.make_empty_scatter_graph())
pca_html = dcc.Graph('pca_graph',figure=pca_fig)
image_html = html.Div([html.Img(src=img_nba,style={'height':'350px', 'width':'700px'})],style={'textAlign': 'center'})
submit_button_html = html.Div([html.Button('Go!',id="submit_button",n_clicks=0,style={'font-size': '24px', 'width': '140px', 'height':'37px'})],style={'textAlign': 'center'})
salary_html = html.Div([dcc.Graph('salary_graph',figure=Salary_section.make_players_graph_salary())],style={'width': '33%', 'display': 'inline-block','verticalAlign': '10%'})
team_graph = html.Div([dcc.Graph('team_graph',figure=Salary_section.make_players_graph_teams())],style={'width': '33%', 'display': 'inline-block','verticalAlign': '10%'})
wins_pie_html = html.Div([dcc.Graph('wins_graph',figure=cwps.make_empty_pie_chart())])
pie_hist_selector_html = html.Div([dcc.RadioItems(['Pie', 'Hist'], id="pie_hist_selector",value='Pie', inline=True)])

atk_def_selector_html = html.Div([dcc.RadioItems(['ATK', 'DFS'], id="atk_def_selector",value='ATK', inline=True)])

pentagon_html = html.Div([dcc.Graph('pentagon_graph',figure=pentagon_section.get_empty_pentagon(ATK_features))])
pentagon_html = html.Div([pentagon_html,atk_def_selector_html],style={'width': '33%', 'display': 'inline-block'})

box_plot_html = html.Div([dcc.Graph('box_plot_graph',figure=box_plot_section.box_plot(players_2018,ATK_features))])



    ## player1
down_menu_player1_html = dcc.Dropdown(players_names,id="player_drop_down1",style={'backgroundColor': '#0096FF','text': '#C0C0C0'})
Draft1_html = html.Div([""],id="result_draft1")
player_1_html = html.Div([html.I("Choose Your Player",id='your_player'),down_menu_player1_html, Draft1_html],id="player1",style={'width': '49%', 'display': 'inline-block'})

    ## player2
down_menu_player2_html = dcc.Dropdown(players_names,id="player_drop_down2",style={'backgroundColor': '#FF0000'})
Draft2_html = html.Div([""],id="result_draft2")
player_2_html = html.Div([html.I("Choose Your Rival"),down_menu_player2_html, Draft2_html],id="player2",style={'width': '49%', 'display': 'inline-block'})


# Main page
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    image_html,
    submit_button_html,
    html.Div([player_1_html,player_2_html],style={'textAlign': 'center'}),
    html.Div([team_graph,pentagon_html,salary_html],style={'textAlign': 'center'}),
    html.Div([wins_pie_html,pie_hist_selector_html],style={'textAlign': 'center'}),
    pca_html,
    box_plot_html,
    matrix_html,corr_html])

### Main page callback ###
# update matrix_corr
@app.callback(
    Output('matrix_corr_graph', 'figure'),
    Input('submit_button', 'n_clicks'),
    Input('atk_def_selector', 'value')
)
def update_matrix(n_clicks,atk_or_dfs):
  if atk_or_dfs=='ATK':
    fig = corr_section.make_matrix_corr_graph(players_2018,ATK_features)
  else:
    fig = corr_section.make_matrix_corr_graph(players_2018,DFS_features)
  return fig

# update corr_scatter
@callback(Output('corr_graph', 'figure'),
              [Input('matrix_corr_graph', 'clickData')])
def check_click(clickData):
  try:
    x1 = clickData['points'][0]['x']
    x2 = clickData['points'][0]['y']
    fig = corr_section.make_scatter_graph(players_2018, x1, x2)
  except:
    fig = corr_section.make_empty_scatter_graph()
  return fig

# submit draft player1
@app.callback(
    Output('result_draft1', 'children'),
    Input('submit_button', 'n_clicks'),
    State('player_drop_down1', 'value'),
    State('player_drop_down2', 'value')
)
def update_draft1(n_clicks, value1, value2):
  message = "The Draft Pick Estimate is: "
  return message + str(draft_section.check_draft_pick(lg_draft,players_2018,value1))

# submit draft player2
@app.callback(
    Output('result_draft2', 'children'),
    Input('submit_button', 'n_clicks'),
    State('player_drop_down1', 'value'),
    State('player_drop_down2', 'value')
)
def update_draft2(n_clicks, value1, value2):
  message = "The Draft Pick Estimate is: "
  return message + str(draft_section.check_draft_pick(lg_draft,players_2018,value2))

# update pentagon
@app.callback(
    Output('pentagon_graph', 'figure'),
    Input('submit_button', 'n_clicks'),
    Input('atk_def_selector', 'value'),
    State('player_drop_down1', 'value'),
    State('player_drop_down2', 'value')
)
def update_pentagon(n_clicks,atk_or_dfs, value1, value2):
  global ATK_features
  global DFS_features
  if atk_or_dfs=='ATK':
    features = ATK_features
  else:
    features = DFS_features
  if value1 not in players_names and value2 not in players_names:
    fig = pentagon_section.get_empty_pentagon(features)
  elif value2 is None:
    fig = pentagon_section.get_player_pentagon(players_2018_norm,value1,features)
  elif value1 is None:
    fig = pentagon_section.get_player_pentagon(players_2018_norm,value2,features)
  else:
    fig = pentagon_section.get_2_player_pentagon(players_2018_norm,value1,value2,features)
  return fig

# update team
@app.callback(
    Output('team_graph', 'figure'),
    Input('submit_button', 'n_clicks'),
    State('player_drop_down1', 'value'),
    State('player_drop_down2', 'value')
)
def update_team(n_clicks, value1, value2):
  if value1 not in players_names and value2 not in players_names:
    fig = Salary_section.make_players_graph_teams()
  elif value2 is None:
    fig = Salary_section.make_players_graph_teams_1(salary,value1)
  elif value1 is None:
    fig = Salary_section.make_players_graph_teams_1(salary,value2)
  else:
    fig = Salary_section.make_players_graph_teams_2(salary,value2,value1)
  return fig

# update salary
@app.callback(
    Output('salary_graph', 'figure'),
    Input('submit_button', 'n_clicks'),
    State('player_drop_down1', 'value'),
    State('player_drop_down2', 'value')
)
def update_salary(n_clicks, value1, value2):
  if value1 not in players_names and value2 not in players_names:
    fig = Salary_section.make_players_graph_salary()
  elif value2 is None:
    fig = Salary_section.make_players_graph_salary_1(salary,value1)
  elif value1 is None:
    fig = Salary_section.make_players_graph_salary_1(salary,value2)
  else:
    fig = Salary_section.make_players_graph_salary_2(salary,value1,value2)
  return fig

# update wins
@app.callback(
    Output('wins_graph', 'figure'),
    Input('submit_button', 'n_clicks'),
    Input('pie_hist_selector', 'value'),
    State('player_drop_down1', 'value'),
    State('player_drop_down2', 'value')
)
def update_wins(n_clicks,choose, value1, value2,):
  if choose=='Pie':
    if value2 is None:
      fig = figure=cwps.make_empty_pie_chart()
    elif value1 is None:
      fig = figure=cwps.make_empty_pie_chart()
    else:
      fig = cwps.make_players_pie_chart(games_details,games,value1,value2)
  else:
    if value2 is None:
      fig = figure=cwps.make_empty_pie_chart()
    elif value1 is None:
      fig = figure=cwps.make_empty_pie_chart()
    else:
      fig = cwps.make_players_hist(games_details,games,value1,value2)
  return fig

# update PCA
@app.callback(
    Output('pca_graph', 'figure'),
    Input('submit_button', 'n_clicks'),
    State('player_drop_down1', 'value'),
    State('player_drop_down2', 'value')
)
def update_pca(n_clicks, value1, value2):
  global pca_fig
  if value1 not in players_names and value2 not in players_names:
    fig = pca_fig
  elif value1 is None or value1=="":
    fig = Pca_section.make_players_graph_pca_1(pca_players,value2)
  elif value2 is None or value2=="":
    fig = Pca_section.make_players_graph_pca_1(pca_players,value1)
  else:
    fig = Pca_section.make_players_graph_pca_2(pca_players,value1,value2)
  return fig

# update Box_plot
@app.callback(
    Output('box_plot_graph', 'figure'),
    Input('submit_button', 'n_clicks'),
    Input('atk_def_selector', 'value'),
    State('player_drop_down1', 'value'),
    State('player_drop_down2', 'value')
)
def update_box_plot(n_clicks,atk_or_dfs, value1, value2):
  global ATK_features
  global DFS_features
  if atk_or_dfs=='ATK':
    features = ATK_features
  else:
    features = DFS_features
  if value1 not in players_names and value2 not in players_names:
    fig = box_plot_section.box_plot(players_2018,features)
  elif value2 is None:
    fig = box_plot_section.box_plot_1(players_2018,features,value1)
  elif value1 is None:
    fig = box_plot_section.box_plot_1(players_2018,features,value2)
  else:
    fig = box_plot_section.box_plot_2(players_2018,features,value1,value2)
  return fig

if __name__ == '__main__':
    app.run_server(debug=True,)
