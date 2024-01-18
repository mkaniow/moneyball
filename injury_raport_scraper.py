'''
This script scrape data and create dataframe with players injury raport
'''
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

def get_injury_raport():

    teams = {
        'Atlanta' : 'ATL',
        'Boston' : 'BOS',
        'Brooklyn' : 'BKN',
        'Charlotte' : 'CHA',
        'Chicago' : 'CHI',
        'Cleveland' : 'CLE',
        'Detroit' : 'DET',
        'Indiana' : 'IND',
        'Miami' : 'MIA',
        'Milwaukee' : 'MIL',
        'New York' : 'NYK',
        'Orlando' : 'ORL',
        'Philadelphia' : 'PHI',
        'Toronto' : 'TOR',
        'Washington' : 'WAS',
        'Dallas' : 'DAL',
        'Denver' : 'DEN',
        'Golden St.' : 'GSW',
        'Houston' : 'HOU',
        'L.A. Clippers' : 'LAC',
        'L.A. Lakers' : 'LAL',
        'Memphis' : 'MEM',
        'Minnesota' : 'MIN',
        'New Orleans' : 'NOP',
        'Oklahoma City' : 'OKC',
        'Phoenix' : 'PHX',
        'Portland' : 'POR',
        'Sacramento' : 'SAC',
        'San Antonio' : 'SAS',
        'UtahZ' : 'UTA'
    }

    URL = 'https://www.cbssports.com/nba/injuries/'

    r = requests.get(URL)

    soup = BeautifulSoup(r.content, features="html.parser")

    #find all boxes with injury data
    s = soup.find_all('div', class_='TableBaseWrapper')

    #create dataframe with specific column names
    injury_raport = pd.DataFrame(columns=['team_id', 'player', 'position', 'update_date', 'injury', 'return_expected_date'])

    #main loop to search through all data
    for item in s:
        #find team name and get team_id from teams dict
        d = item.find('div', class_='TeamLogoNameLockup-name')
        name_team = teams[d.get_text()]
        #find all rows 
        f = item.find_all('tr', class_='TableBase-bodyTr')

        for row in f:
            #find all cells
            q = row.find_all('td', class_='TableBase-bodyTd')
            holder = [name_team]
            for cell in q:
                try:
                    name = cell.find('span', class_='CellPlayerName--long')
                    name = name.get_text()
                    holder.append(name)
                except:
                    text = cell.get_text()
                    #clear data
                    text = text.replace('\n', '')
                    res = re.sub(' +', ' ', text)
                    holder.append(str(res))
            injury_raport.loc[len(injury_raport.index)] = holder

    return injury_raport
