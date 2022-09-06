import sleeper_wrapper as sleeper
import xlwings as xw
import pandas as pd
import re
import time
import string

sheetname = "rankings2.py" 

# Constants
ALPHA = list(string.ascii_uppercase)
superflex = 871982150621282304
half = 872214817610575872
big = 872244883358924800
HL_COLOR = (100, 70,134)

def format_range_string(row: int, ncol: int):
    return "A{}:{}{}".format(
        row, ALPHA[ncol-1], row
    )

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def parse_last_name(last_name: str) -> str:
    remove_name_strings = ['II', 'III', 'IV', 'V', 'Sr', 'Jr']
    last_name = re.sub(' +', ' ', last_name)
    pieces = re.split(" |-", last_name.strip().replace('.', ''))
    pieces = list(filter(lambda x: x not in remove_name_strings, pieces))
    return pieces[-1].upper()

class SleeperPick:
    def __init__(self, response: dict):
        self._raw = response
        self.pid: str = None
        self.data: dict = {}
        self._parse()
        pass

    def _parse(self):
        meta = self._raw['metadata']
        meta['round'] = safe_cast(self._raw['round'], int)
        meta['pick'] = safe_cast(self._raw['pick_no'], int)
        meta['player_id'] = self._raw['player_id']

        # Fix Jacksonville
        if meta['team'].upper() == "JAX":
            meta['team'] = "JAC"

        # Store metadata
        self.data = meta

        # Form pid
        first_name = meta['first_name'][0].upper()
        last_name = parse_last_name(meta['last_name'])
        self.pid = "{}_{}_{}_{}".format(
            first_name, last_name, meta['team'], meta['position']).upper()

class SleeperDraft:
    def __init__(self, draft_id: int):
        self.id = draft_id
        self.draft = sleeper.Drafts(draft_id)
        self.idx = 0
    
    def get_picks(self) -> list:
        picks = self.draft.get_all_picks()
        picks = picks[self.idx:]
        self.idx += len(picks)
        return [SleeperPick(pick) for pick in picks]

class DraftList:
    def __init__(self, sheet):
        self.sheet = sheet
        self.df = self._read_df()
        self.ncol = len(self.df.columns)
    
    def _read_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.sheet.used_range.value)
        header = df.iloc[0]
        df = df[1:]
        df.columns = header
        return df

    def update(self, pick: SleeperPick):
        row = self.df.loc[self.df['pid'] == pick.pid].index
        if len(row) > 0:
            index = row[0]+1
            range_str = format_range_string(index, self.ncol)
            self.sheet.range(range_str).color = HL_COLOR
        else:
            print("Could not find: {}".format(pick.pid))

class DraftBoard:
    def __init__(self, filename: str):
        self.filename = filename
        self.book = xw.Book(filename)
        self.rankings = DraftList(self.book.sheets['superflex'])
        self.qb = DraftList(self.book.sheets['QB'])
        self.rb = DraftList(self.book.sheets['RB'])
        self.wr = DraftList(self.book.sheets['WR'])
        self.te = DraftList(self.book.sheets['TE'])
        self.k = DraftList(self.book.sheets['K'])
    
    def update(self, pick: SleeperPick):
        print("[{}] {}".format(pick.data['pick'], pick.pid))
        self.rankings.update(pick)
        position = pick.data.get('position', None)

        if (position == "QB"):
            self.qb.update(pick)
        elif (position == "RB"):
            self.rb.update(pick)
        elif (position == "WR"):
            self.wr.update(pick)
        elif (position == "TE"):
            self.te.update(pick)
        elif (position == "K"):
            self.k.update(pick)


draft_id = 872644666619838464
draft_board = DraftBoard("rankings2.xlsx")
sleeper_draft = SleeperDraft(draft_id)

while True:
    cnt = 0
    picks = sleeper_draft.get_picks()
    cnt += len(picks)
    for pick in picks:
        draft_board.update(pick)
    time.sleep(5)
    print("**HEARTBEAT** ({})".format(cnt))