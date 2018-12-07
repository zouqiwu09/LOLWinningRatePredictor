from RiotAPI import RiotAPI as riot
from FeatureExtractor import *
import pprint
import csv
import time



#  Features
# (1/Game duration)   * win or lose


api = riot()

#id = api.getAccountID("ethreal9")
#matches = api.getRecent50Matches("ethreal9")
#match_data = api.get_match_data(matches[0]['gameId'])
#pprint.pprint(match_data)
#v = api.get_version()
# champions = api.get_champions()
# pprint.pprint (champions)
# 'baronKills': 1,
#             'dominionVictoryScore': 0,
#             'dragonKills': 1,
#             'firstBaron': True,
#             'firstBlood': True,
#             'firstDragon': True,
#             'firstInhibitor': True,
#             'firstRiftHerald': True,
#             'firstTower': True,
#             'inhibitorKills': 3,
#             'riftHeraldKills': 1,
#             'teamId': 100,
#             'towerKills': 11,
#             'vilemawKills': 0,
#             'win': 'Win

ini = 230314864
crawled_summoner = []


def crawl(name, summoner_list):
    with open("Crawled_game.txt", "a+") as f:
        matches = api.getRecent50Matches(name)
        for i in matches:
            f.write(str(i['gameId']))
            f.write("\n")
            match_data = api.get_match_data(i["gameId"])
            try:
                summoner_list.extend(crawl_data(match_data))
            except Exception as e:
                print ("hitting rating limit")
                print (e)
                time.sleep(60)

def crawler_master(summoner_list):
    for i in summoner_list:
        if (len(summoner_list) == 0 or len(crawled_summoner)>500):
            print ("finished crawling")
            break
        crawl(i, summoner_list)
        with open("Crawled_summoner.txt", "a+") as f:
            f.write(str(i))
            f.write("\n")
        summoner_list.remove(i)
    crawler_master(summoner_list)


def crawl_data(match_data):
    gameId = match_data["gameId"]
    gameDuration = match_data["gameDuration"]
    team1_data = []
    team2_data = []
    team1_win = 0
    team2_win = 0
    if match_data["teams"][0]["win"] == "Win":
        team1_win = 1
    if match_data["teams"][1]["win"] == "Win":
        team2_win = 1

    team1Rank = 0
    team2Rank = 0

    championList1 = []
    championList2 = []
    for i in match_data["participants"][:5]:
        team1Rank += get_rank_score(i["highestAchievedSeasonTier"])
        championList1.append(i["championId"])

    for i in match_data["participants"][5:]:
        team2Rank += get_rank_score(i["highestAchievedSeasonTier"])
        championList2.append(i["championId"])

    summonerIdList1 = []
    summonerIdList2 = []
    accountIdList = []
    for i in match_data["participantIdentities"][:5]:
        summonerIdList1.append(i["player"]["summonerId"])
        accountIdList.append(i["player"]["accountId"])

    for i in match_data["participantIdentities"][5:]:
        summonerIdList2.append(i["player"]["summonerId"])
        accountIdList.append(i["player"]["accountId"])

    team1_total_score = (0,0)
    team2_total_score = (0,0)

    for i in range(5):
        championScore, totalScore = api.get_Individual_Score(summonerIdList1[i], championList1[i])
        team1_total_score = (team1_total_score[0] + championScore, team1_total_score[1] + totalScore)
    combo1 = get_champion_combo(championList1)
    for i in range(5):
        championScore, totalScore = api.get_Individual_Score(summonerIdList2[i], championList2[i])
        team2_total_score = (team2_total_score[0] + championScore, team2_total_score[1] + totalScore)
    combo2 = get_champion_combo(championList2)

    with open("crawled_data.csv", "a+", newline='') as csvfile:
        writer = csv.writer(csvfile)
        team1_data = [str(gameId), str(gameDuration), str(team1Rank-team2Rank), str(team1_total_score[0]-team2_total_score[0]), str(team1_total_score[1]-team2_total_score[1])]
        team2_data = [str(gameId), str(gameDuration), str(team2Rank-team1Rank), str(team2_total_score[0]-team1_total_score[0]), str(team2_total_score[1]-team1_total_score[1])]

        team1_data.extend(combo1)
        team1_data.append(team1_win)
        team2_data.extend(combo2)
        team2_data.append(team2_win)
        writer.writerow(team1_data)
        writer.writerow(team2_data)

    return accountIdList




# pprint.pprint(api.get_Individual_Score(32604148))
# print(api.get_Individual_Score(70311457,245))


# id = api.getAccountID("ethreal9")
# matches = api.getRecent50Matches("ethreal9")
# match_data = api.get_match_data(matches[0]['gameId'])
# pprint.pprint(match_data)


summoner_list = [ini]
crawler_master(summoner_list)