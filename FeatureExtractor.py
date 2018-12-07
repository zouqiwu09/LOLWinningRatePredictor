import json
def get_rank_score(rank):
    score = 0
    if (rank == "UNRANKED"):
        score = 0
    elif (rank == "BRONZE"):
        score = 1
    elif (rank == "SILVER"):
        score = 2
    elif (rank == "GOLD"):
        score = 3
    elif (rank == "PLATINUM"):
        score = 5
    elif (rank == "DIAMOND"):
        score = 8
    elif (rank == "MASTER"):
        score = 12
    elif (rank == "CHALLENGER"):
        score = 15
    return score

def get_champions():
    with open("champion.json", encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_champion_dict():
    data = get_champions()
    champion_dict = {data["data"][i]["key"]: data["data"][i]["id"] for i in data["data"]}
    return champion_dict

def get_champion_combo(champion_list):
    champion_dict = get_champion_dict()
    champion_data = get_champions()["data"]
    # Fighter, Tank, Mage, Marksman, Support, Assassin
    combo = [0,0,0,0,0,0]
    for i in champion_list:
        champion_name = champion_dict[str(i)]
        tags = champion_data[champion_name.replace(" ", "")]["tags"]
        if ("Fighter" in tags):
            combo[0] += 1
        if ("Tank" in tags):
            combo[1] += 1
        if ("Mage" in tags):
            combo[2] += 1
        if ("Marksman" in tags):
            combo[3] += 1
        if ("Support" in tags):
            combo[4] += 1
        if ("Assassin" in tags):
            combo[5] += 1
    return combo
