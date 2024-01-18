'''
This script adds new players to table
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

#rookies dictionary contains all new players that will be transferred to for loop
#in dict all parts are str (key -> player name: value -> team id)
rookies = {
    #'LeBron James': 'LAL'
}

if len(rookies) == 0:
    print('There is no changes to make')
else:
    for key, value in rookies.items():
        mycursor.execute(f'INSERT IGNORE INTO players SET player_name = "{key}", team_id = "{value}";')
        db.commit()
    print('Successfully updated data in table players')