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