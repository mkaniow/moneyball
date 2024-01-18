'''
This script contains 3 modules:
    make_dataframe - create dataframe with whole content of chosen table from db
        input: str - name of table in db
        output: pandas.database
    merged_dataframes - create dataframe based on 3 tables from db
        output: pandas.database
    list_of_players - create list of players from db
        output: list 
'''
import pandas as pd
import numpy as np
import mysql.connector
from password import *


def make_dataframe(table):
    
    #connect to db
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password=pw,
        database='moneyball_db'
        )
    mycursor = db.cursor()

    #select all data from table
    mycursor.execute(f'SELECT * FROM {table}')

    data = mycursor.fetchall()

    df = pd.DataFrame(data)

    df.columns = mycursor.column_names

    return df

def merged_dataframes():
    df_details = make_dataframe('game_details')
    df_games = make_dataframe('games')
    df_players = make_dataframe('players')

    df_players.columns = df_players.columns.str.replace('player_name', 'player') 
    df_players.columns = df_players.columns.str.replace('team_id', 'curr_team') 

    df_merged = df_details.merge(df_games[['game_id', 'game_date']], on = 'game_id', how = 'left')

    df_merged_2 = df_merged.merge(df_players[['player', 'curr_team']], on = 'player', how = 'left')

    return df_merged_2

def list_of_players():
    
    #connect to db
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password=pw,
        database='moneyball_db'
        )
    mycursor = db.cursor()  

    #select all data from table
    mycursor.execute('SELECT player_name FROM players')

    data = mycursor.fetchall()

    df = pd.DataFrame(data)

    players_list = df[0].tolist()

    return players_list