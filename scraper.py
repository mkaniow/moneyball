'''
This script/module scrape main basketball data
'''
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np


def scrape_data(dates_between):
    BASE_URL = 'https://www.nba.com'
    GAMES_DATE = '/games?date='
    BOX_SCORE = '/box-score'

    teams = {
        'ATLANTA HAWKS' : 'ATL',
        'BOSTON CELTICS' : 'BOS',
        'BROOKLYN NETS' : 'BKN',
        'CHARLOTTE HORNETS' : 'CHA',
        'CHICAGO BULLS' : 'CHI',
        'CLEVELAND CAVALIERS' : 'CLE',
        'DETROIT PISTONS' : 'DET',
        'INDIANA PACERS' : 'IND',
        'MIAMI HEAT' : 'MIA',
        'MILWAUKEE BUCKS' : 'MIL',
        'NEW YORK KNICKS' : 'NYK',
        'ORLANDO MAGIC' : 'ORL',
        'PHILADELPHIA 76ERS' : 'PHI',
        'TORONTO RAPTORS' : 'TOR',
        'WASHINGTON WIZARDS' : 'WAS',
        'DALLAS MAVERICKS' : 'DAL',
        'DENVER NUGGETS' : 'DEN',
        'GOLDEN STATE WARRIORS' : 'GSW',
        'HOUSTON ROCKETS' : 'HOU',
        'LA CLIPPERS' : 'LAC',
        'LOS ANGELES LAKERS' : 'LAL',
        'MEMPHIS GRIZZLIES' : 'MEM',
        'MINNESOTA TIMBERWOLVES' : 'MIN',
        'NEW ORLEANS PELICANS' : 'NOP',
        'OKLAHOMA CITY THUNDER' : 'OKC',
        'PHOENIX SUNS' : 'PHX',
        'PORTLAND TRAIL BLAZERS' : 'POR',
        'SACRAMENTO KINGS' : 'SAC',
        'SAN ANTONIO SPURS' : 'SAS',
        'UTAH JAZZ' : 'UTA'
    }

    list_of_labels = ['GAME_ID', 'PLAYER', 'MIN', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO',  'PF', 'PTS', '+/-', 'TEAM']

    list_of_labels_2 = ['GAME_ID', 'HOME', 'AWAY', 'PTS_HOME', 'PTS_AWAY', 'DATE']

    df = pd.DataFrame(columns=list_of_labels)
    df2 = pd.DataFrame(columns=list_of_labels_2)

    driver = webdriver.Chrome()

    for date in dates_between:

        #go to site with list of games in one day
        links_id = set()
        URL = BASE_URL + GAMES_DATE + date
        driver.get(URL)
        time.sleep(7)
        response = driver.find_element(By.CLASS_NAME, 'GamesView_gameCardsContainer__c_9fB')

        #find all links to every game
        try:    
            links = response.find_elements(By.TAG_NAME, 'a')
            for elem in links:
                l = elem.get_attribute("href")
                if len(l) < 50 and l[0:24] == 'https://www.nba.com/game':
                    links_id.add(l)
        except:
            pass

        #go to every boxscore
        j = 0
        for attempt in list(links_id):
            if j < 10:
                game_id = int(f'{date[2:4]}{date[5:7]}{date[8:10]}0{j}')
            else:
                game_id = int(f'{date[2:4]}{date[5:7]}{date[8:10]}{j}')
            print(game_id)
            j += 1

            try:
                driver = webdriver.Chrome()
                driver.get(attempt + BOX_SCORE)

                time.sleep(5)

                tabele = driver.find_elements(By.TAG_NAME, 'table')

                team_one = tabele[0].find_element(By.TAG_NAME, 'tbody')
                team_one = team_one.find_elements(By.TAG_NAME, 'tr')

                team_two = tabele[1].find_element(By.TAG_NAME, 'tbody')
                team_two = team_two.find_elements(By.TAG_NAME, 'tr')

                team_name = driver.find_elements(By.CLASS_NAME, 'GameBoxscoreTeamHeader_gbt__b9B6g')

                teams_list = [team_one, team_two]

                holder_2 = [0 for i in range(6)]

                for team in range(len(teams_list)):
                    i = 1
                    for item in teams_list[team]:
                        if i < 6:
                            row_data = item.find_elements(By.TAG_NAME, 'td')
                            holder = []
                            holder.append(game_id)
                            for data in row_data:
                                holder.append(data.text)
                            holder[1] = holder[1][:-2]
                            if len(holder) != len(list_of_labels)-1:
                                name = holder[1]
                                holder = [np.nan for i in range(21)]
                                holder[1] = name
                            i += 1
                        else:
                            row_data = item.find_elements(By.TAG_NAME, 'td')
                            holder = []
                            holder.append(game_id)
                            for data in row_data:
                                holder.append(data.text)
                            if len(holder) != len(list_of_labels)-1:
                                name = holder[1]
                                holder = [np.nan for i in range(22)]
                                holder[1] = name
                                holder[0] = game_id
                            if holder[1] == 'TOTALS':
                                if team == 0:
                                    holder_2[0] = game_id
                                    holder_2[2] = teams[team_name[team].text]
                                    holder_2[4] = holder[20]
                                    holder_2[5] = date
                                else:
                                    holder_2[1] = teams[team_name[team].text]
                                    holder_2[3] = holder[20]        
                                continue
                            i += 1
                        if team_name[team].text in teams:
                            holder.append(teams[team_name[team].text])
                        else:
                            holder.append(np.nan)
                        df.loc[len(df)] = holder
                df2.loc[len(df2)] = holder_2
                time.sleep(5)
            except:
                pass
    return df, df2