
import pandas as pd
import re

def parse_last_name(last_name: str) -> str:
    remove_name_strings = ['II', 'III', 'IV', 'V', 'Sr', 'Jr']
    last_name = re.sub(' +', ' ', last_name)
    pieces = re.split(" |-", last_name.strip().replace('.', ''))
    pieces = list(filter(lambda x: x not in remove_name_strings, pieces))
    return pieces[-1].upper()

file = "superflex/cbs_top200.txt"
with open(file, 'r') as fp:
    lines = fp.readlines()

players = []
rank = 1
for line in lines:
    line = re.sub(' +', ' ', line.strip())
    pieces = line.split()
    team = pieces[-2]
    pos = pieces[-1].replace('(', '').replace(')', '')
    name = ' '.join(pieces[:-2])
    first_name = name[0].upper()
    last_name = parse_last_name(name)
    pid = "{}_{}_{}_{}".format(first_name, last_name, team, pos)

    players.append({
        'pid': pid,
        'rank': rank,
        'name': name,
        'pos': pos,
        'team': team
    })
    rank += 1

df = pd.DataFrame(players)
df.set_index(['pid'], inplace=True, drop=True)
df.to_csv("superflex/cbs_superflex.csv")