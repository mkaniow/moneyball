'''
This script separate values in string ('min:sec' -> int(min), int(sec)) from dataframe
'''
import pandas as pd
import numpy as np


def separate_min_and_sec(df):
    new = df["MIN"]

    mins = []
    secs = []

    for item in new:
        try:
            holder = item.split(':')
            holder[0] = int(holder[0])
            holder[1] = int(holder[1])
        except:
            holder = [np.NAN, np.NAN]
        mins.append(holder[0])
        secs.append(holder[1])

    df['MINUTE'] = mins
    df['SECOND'] = secs
    df = df.drop('MIN', axis=1)

    df = df.loc[:,['GAME_ID','PLAYER','MINUTE','SECOND','FGM','FGA','FG%','3PM','3PA','3P%','FTM','FTA','FT%','OREB','DREB','REB','AST','STL','BLK','TO','PF', 'PTS','+/-','TEAM']]

    return df