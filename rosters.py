'''
This script scrape webside for players in NBA teams and returns list of names
It was written to help create players table in db
'''
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

URL_BASE = 'https://www.cbssports.com/nba/teams/'
roster = '/roster/'
rest = ['ATL/atlanta-hawks', 'BOS/boston-celtics', 'BKN/brooklyn-nets', 'CHA/charlotte-hornets', 'CHI/chicago-bulls', 'CLE/cleveland-cavaliers', 'DET/detroit-pistons', 'IND/indiana-pacers', 'MIA/miami-heat', 'MIL/milwaukee-bucks','NY/new-york-knicks','ORL/orlando-magic','PHI/philadelphia-76ers','TOR/toronto-raptors','WAS/washington-wizards','DAL/dallas-mavericks','DEN/denver-nuggets','GS/golden-state-warriors','HOU/houston-rockets','LAC/los-angeles-clippers','LAL/los-angeles-lakers','MEM/memphis-grizzlies','MIN/minnesota-timberwolves','NO/new-orleans-pelicans','OKC/oklahoma-city-thunder','PHO/phoenix-suns','POR/portland-trail-blazers','SAC/sacramento-kings','SA/san-antonio-spurs','UTA/utah-jazz']

driver = webdriver.Chrome()

for team in rest:
    #go to site with list of games in one day
    links_id = set()
    URL = URL_BASE + team + roster
    driver.get(URL)
    time.sleep(5)
    response = driver.find_element(By.CLASS_NAME, 'Page-colMain')

    response = response.find_element(By.CLASS_NAME, 'TableBase-shadows')

    names = response.find_elements(By.CLASS_NAME, 'CellPlayerName--long')

    players = []

    for item in names:
        players.append(item.text)
    print(players)
