from sportsipy.nfl.teams import Team
import pandas as pd

from bs4 import BeautifulSoup, Comment
import requests

"""
Page List
    Root: https://www.pro-football-reference.com/
    Team: teams/{team}/{year}.htm
    Team (advanced): teams/{team}/{year}_advanced.htm
    Team (roster): teams/{team}/{year}_roster.htm
    Passing: years/{year}/passing.htm
    Rushing: years/{year}/rushing.htm
    Receiving: years/{year}/receiving.htm
    
    Fantasy Rank: years/{year}/fantasy.htm
    RZ Passing: years/{year}/redzone-passing.htm
    RZ Rushing: years/{year}/redzone-rushing.htm
    RZ Receiving: years/{year}/redzone-receiving.htm
   
    Team Defense: years/{year}/opp.htm 
    
    

"""

if __name__ == "__main__":

    url = 'https://www.pro-football-reference.com/teams/det/2020.htm'
    RELOAD = False

    if RELOAD:
        html = requests.get(url).text
        with open("test.html", 'w') as fp:
            fp.write(html)
    else:
        with open("test.html", 'r') as fp:
            html = fp.read()

    soup = BeautifulSoup(html, "lxml")
    comments = soup.findAll(string=lambda text: isinstance(text, Comment))

    tables = []
    for c in comments:
        if 'table' in c:
            try:
                tables.append(pd.read_html(c)[0])
            except:
                continue

    tables = soup.findAll("table")
    passing = soup.find('', {'id': 'passing'})

    for t in tables:
        if t.findParent("table") is None:
            print(str(t))

    print()
