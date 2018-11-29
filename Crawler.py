from RiotAPI import RiotAPI as riot
import pprint



#  Features
# (1/Game duration)   * win or lose


api = riot()

#id = api.getAccountID("ethreal9")
matches = api.getRecent50Matches("ethreal9")
match_data = api.get_match_data(matches[0]['gameId'])
pprint.pprint(match_data)
#v = api.get_version()
# champions = api.get_champions()
# pprint.pprint (champions)

ini = "ethreal9"

def crawl(name):
    matches = api.getRecent50Matches(name)