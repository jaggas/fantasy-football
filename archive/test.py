
from espn_api.football import League
import pprint
pp = pprint.PrettyPrinter(indent=3)

league_id = 78678207
year = 2021
espn_s2 = "AEBFywES6w3mQjpL%2BeaKg1aqnnVhcXHaVUCroMS%2Fvr%2FNNJrS%2F3LubAGadrDrBUq393giTkOzvlMqwLvMq1ISmLhqU63R4q2lRMTnlT%2Fhe%2FAiEsPRhPfSu6zNQAyxX1FRT1xZcUGEHVDje2DdV1LpaOXzvcuh9qJ7v7y8bOJJ%2BwUNAcD3%2BleYYiO12GK%2FRW%2FCMjRd3ie1dU%2Bm4RTjlewmqxBwye48o2fFVHd1GLHQiWYOeJGM7ffkZ66jSYXSJzaPrvg6g4JeNjUBNG1XrpiAb5LD"
swid = "436BE508-43B6-4839-826E-EB09ECE5FC87"

l = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)


standings = l.standings()
for t in standings:
    print(t)
    for p in t.roster:
        print(p)
        pp.pprint(p.stats)

