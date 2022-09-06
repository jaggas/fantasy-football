from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import re

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"} 

def parse_last_name(last_name: str) -> str:
    remove_name_strings = ['II', 'III', 'IV', 'V', 'Sr', 'Jr']
    last_name = re.sub(' +', ' ', last_name)
    pieces = re.split(" |-", last_name.strip().replace('.', ''))
    pieces = list(filter(lambda x: x not in remove_name_strings, pieces))
    return pieces[-1].upper()

def parse_rankings(scoring = "standard", category = "top200") -> list:
    url = "https://www.cbssports.com/fantasy/football/rankings/{}/{}".format(
        scoring, category
    )

    soup = BeautifulSoup(requests.get(url, headers).text, "html.parser")
    players = soup.find_all('div', attrs={'class': 'player-row'})

    rankings = []
    for player in players:
        # Player rank
        rank = int(player.findChildren('div', attrs={'class': 'rank'})[0].text)
        # Player name
        name = player.findChildren('span', attrs={'class', 'player-name'})[0].text

        # Team/position
        pieces = [None, None]
        if category != "DST":
            team_position = player.findChildren('span', attrs={'class', 'team position'})[0].text
            pieces = [x.strip() for x in team_position.strip().split('\n')]

        rankings.append(
            {
                'rank': rank,
                'name': name,
                'team': pieces[0],
                'position': pieces[1],
                'scoring': scoring,
                'category': category
            }
        )
    return rankings

def get_rankings(category="top200") -> pd.DataFrame:
    print("Parsing {}".format(category))
    rankings = parse_rankings("standard", category)
    time.sleep(2)
    rankings += parse_rankings("ppr", category)

    df = pd.DataFrame(rankings)
    if category == "DST":
         df = df.groupby(['name'], as_index=False)['rank'].mean()
    else:
        if category != "top200":
            df['position'] = category

        df = df.groupby(['name', 'team', 'position'], as_index=False)['rank'].mean()
        last_name = df.apply(lambda x: parse_last_name(x['name']), axis=1)
        first_name = df.apply(lambda x: x['name'][0], axis=1)
        df['pid'] = first_name + "_" + last_name + "_" + df['team'] + "_" + df['position']
        df.set_index(['pid'], inplace = True, drop = True)

    df = df.sort_values(by=['rank'], ascending=True)
    return df

top200 = get_rankings("top200")
qb = get_rankings("QB")
wr = get_rankings("WR")
rb = get_rankings("RB")
te = get_rankings("TE")
k = get_rankings("K")
dst = get_rankings("DST")

with pd.ExcelWriter('rankings2.xlsx') as writer:  
    top200.to_excel(writer, sheet_name='top200')
    qb.to_excel(writer, sheet_name='QB')
    rb.to_excel(writer, sheet_name='RB')
    wr.to_excel(writer, sheet_name='WR')
    te.to_excel(writer, sheet_name='TE')
    k.to_excel(writer, sheet_name='K')
    dst.to_excel(writer, sheet_name='DST')




