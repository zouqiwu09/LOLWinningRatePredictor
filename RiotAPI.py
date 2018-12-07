import requests
import matplotlib.pyplot as plt
import json
import time


class RiotAPI:
    def __init__(self):
        self.APIKey = "RGAPI-66dea204-ae2a-4a39-9511-4f9cdc2f0b0a"
        self.basic_url = "https://na1.api.riotgames.com/lol/"

    def getAccountID(self, summonerName):
        url = self.basic_url + "summoner/v3/summoners/by-name/" + summonerName
        params = {}
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        data = response.json()
        try:
            accountID = data["accountId"]
            return accountID
        except:
            if (data["status"]["status_code"] == 429):
                print ("Please wait for API cooling down")
            elif (data["status"]["status_code"] == 404):
                print ("Summoner not found")
                return ("not found")
            else:
                return None

    def getSummonerID(self, summonerName):
        url = self.basic_url + "summoner/v3/summoners/by-name/" + summonerName
        params = {}
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        data = response.json()

        summonerId = data["id"]
        return summonerId

    def get_Champion_Dictionary(self):
        url = self.basic_url + "static-data/v3/champions"
        params = {}
        params['locale'] = "en_US"
        params['dataById'] = 'false'
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        data = response.json()
        try:
            champion_dict = {data["data"][i]["id"]:data["data"][i]["name"] for i in data["data"]}
            return champion_dict
        except:
            if (data["status"]["status_code"] == 429):
                print ("Please wait for API cooling down")
            elif (data["status"]["status_code"] == 404):
                print ("Summoner not found")
                return ("not found")
            else:
                return None


    def getRecent50Matches(self, summonerName):
        if(type(summonerName) is str):
            accountId = str(self.getAccountID(summonerName))
        else:
            accountId = str(summonerName)
        url = self.basic_url + "match/v3/matchlists/by-account/" + accountId

        params = {}
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        try:
            data = response.json()
            return data["matches"][:2]
        except:
            if (data["status"]["status_code"] == 429):
                print ("Please wait for API cooling down")
            elif (data["status"]["status_code"] == 404):
                print ("Summoner not found")
                return ("not found")
            else:
                return None
    def get_gold(self,summonerName, matchID, index):
        url = self.basic_url + "/match/v3/matches/" + str(matchID)
        params = {}
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        data = response.json()
        return data["participants"][index]["stats"]["goldEarned"]
    def get_match_data(self, matchID):
        url = self.basic_url + "match/v3/matches/" + str(matchID)
        params = {}
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        data = response.json()
        return data
    def get_match_data_by_name(self, summnonerName):
        recent = self.getRecent50Matches(summnonerName)
        data = []
        if (recent == None):
            return IOError
        for i in recent[:5]:
            data.append(self.get_match_data(i['gameId']))
        return data


    def get_total_damage(self,summonerName, matchID, index):
        url = self.basic_url + "match/v3/matches/" + str(matchID)
        params = {}
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        data = response.json()
        return data["participants"][index]["stats"]["totalDamageDealtToChampions"]

    def get_total_kills(self,summonerName, matchID, index):
        url = self.basic_url + "match/v3/matches/" + str(matchID)
        params = {}
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        data = response.json()
        return data["participants"][index]["stats"]["kills"]

    def get_assists(self,summonerName, matchID, index):
        url = self.basic_url + "match/v3/matches/" + str(matchID)
        params = {}
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        data = response.json()
        return data["participants"][index]["stats"]["assists"]

    def get_version(self):
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
        response = requests.get(url)
        v = response.json()
        return (v[0])

    def get_champions(self):
        with open("champion.json", encoding='utf-8') as f:
            data = json.load(f)
        return data

    def get_champion_dict(self):
        data = self.get_champions()
        champion_dict = {data["data"][i]["key"]: data["data"][i]["name"] for i in data["data"]}

    def get_Individual_Score(self, summonerId, championId):
        url = self.basic_url + "champion-mastery/v3/scores/by-summoner/" + str(summonerId)
        params = {}
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        data = response.json()
        total_score = data
        url = self.basic_url + "champion-mastery/v3/champion-masteries/by-summoner/" + str(summonerId) + "/by-champion/" + str(championId)
        params = {}
        params['api_key'] = self.APIKey
        response = requests.get(url, params=params)
        data = response.json()
        try:
            champion_score = data["championPoints"]
        except Exception as e:
            print (e)
            if (data["status"]["status_code"] == 429):
                print ("Please wait for API cooling down")
                time.sleep(60)
                response = requests.get(url, params=params)
                data = response.json()
                champion_score = data["championPoints"]
            else:
                print ("Other exceptions")

        return [champion_score, total_score]