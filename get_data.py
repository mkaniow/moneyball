'''
This is a main script to scrape, clean and insert basketball data 
'''
import datetime as DT
import time
import pandas as pd
import numpy as np
import mysql.connector
from datetime import date
from create_tuples import create_list_of_tuples
from scraper import scrape_data
from min_sec import separate_min_and_sec
from password import *

#connect to db
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password=pw,
    database='moneyball_db'
    )

mycursor = db.cursor()

#get last date from db
mycursor.execute('SELECT MAX(game_date) FROM games')

myresult = mycursor.fetchall()

#funcion that returns list of dates (Y####-M##-D##) between 2 dates
def get_dates_between(start_date, end_date):
    return [str(start_date + DT.timedelta(days=i)) for i in range((end_date - start_date).days + 1)]

#to switch between today and exact day just uncomment correct line
today = date.today()
#today = date(Y####, M##, D##)

#pop first element because data from this date is in db
dates_between = get_dates_between(myresult[0][0], today)
dates_between.pop(0)
dates_between.pop(-1)

df, df2 = scrape_data(dates_between)

#check if there is some data in dataframe (because sometimes there is no games)
if len(df) > 5:
    #clean details df
    df = separate_min_and_sec(df)

    #insert data to db
    nba_details = create_list_of_tuples(df)
    nba_games = create_list_of_tuples(df2)

    query = 'INSERT INTO games (game_id, home, away, pts_home, pts_away, game_date) VALUES (%s,%s,%s,%s,%s,%s)'
    query2 = 'INSERT INTO game_details (game_id, player, minute, second, fgm, fga, fg_pct, 3pm, 3pa, 3p_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, tos, pf, pts, plus_minus, team) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    mycursor.executemany(query, nba_games)
    mycursor.executemany(query2, nba_details)

    db.commit()
    print('Successfully scraped and inserted data')
elif len(df) <= 5:
    print('Everything up to date')