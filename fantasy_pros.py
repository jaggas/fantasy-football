import pandas as pd
import re

def parse_last_name(last_name: str) -> str:
    remove_name_strings = ['II', 'III', 'IV', 'V', 'Sr', 'Jr']
    last_name = re.sub(' +', ' ', last_name)
    pieces = re.split(" |-", last_name.strip().replace('.', ''))
    pieces = list(filter(lambda x: x not in remove_name_strings, pieces))
    return pieces[-1].upper()

file = "superflex/FantasyPros_superflex.csv"
df = pd.read_csv(file)
df = df[df['PLAYER NAME'].notna()]
df = df[df['TEAM'].notna()]
df['POS'] = df['POS'].str.replace('\d+', '')
first_name = df.apply(lambda x: x['PLAYER NAME'][0], axis=1)
last_name = df.apply(lambda x: parse_last_name(x['PLAYER NAME']), axis=1)
df['pid'] = first_name + "_" + last_name + "_" + df['TEAM'] + "_" + df['POS']
df.set_index(['pid'], inplace=True, drop=True)
df.to_csv(file)

print()
