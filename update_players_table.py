'''
This script updates players table
'''
import mysql.connector
from password import *

#connect to db
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password=pw,
    database='moneyball_db'
    )

mycursor = db.cursor()

#list of teams_id ['ATL','BOS','BKN','CHA','CHI','CLE','DET','IND','MIA','MIL','NYK','ORL','PHI','TOR','WAS','DAL','DEN','GSW','HOU','LAC','LAL','MEM','MIN','NOP','OKC','PHX','POR','SAC','SAS','UTA']

#trades dictionary contains all trades that will be transferred to for loop
#in dict all parts are str (key -> player name: value -> team id)
trades = {
    #'LeBron James': 'LAL'
}

if len(trades) == 0:
    print('There is no changes to make')
else:
    for key, value in trades.items():
        mycursor.execute(f'UPDATE players SET team_id = "{value}" WHERE player_name = "{key}";')
        db.commit()
    print('Successfully updated data in table players')