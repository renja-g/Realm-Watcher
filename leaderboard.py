import orjson
import os
import sys

# set cwd to the directory of this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

tiers = {
    "IRON": 0,
    "BRONZE": 1,
    "SILVER": 2,
    "GOLD": 3,
    "PLATINUM": 4,
    "EMERALD": 4,
    "DIAMOND": 5,
    "MASTER": 6,
    "GRANDMASTER": 7,
    "CHALLENGER": 8,
}


def sort_summoners(summoners_list: list[dict], league: str) -> list[dict]:
    """
    Sorts the summoners by their rank.
    """
    if league == "solo":
        league = "420"
    elif league == "flex":
        league = "440"

    # remove summoners where the league == None
    summoners = []
    for summoner in summoners_list:
        if summoner["leagueEntries"][league] is not None:
            summoners.append(summoner)
    
    # sort by tier
    summoners = sorted(summoners, key=lambda summoner: tiers[summoner["leagueEntries"][league]["tier"]])
    # sort by division
    summoners = sorted(summoners, key=lambda summoner: summoner["leagueEntries"][league]["rank"])
    # sort by league points
    summoners = sorted(summoners, key=lambda summoner: summoner["leagueEntries"][league]["leaguePoints"])

    return summoners


def main():
    # python leaderboard.py solo | flex
    if len(sys.argv) != 2:
        print("Usage: python leaderboard.py solo | flex")
        sys.exit(1)
    if sys.argv[1] not in ["solo", "flex"]:
        print("Usage: python leaderboard.py solo | flex")
        sys.exit(1)
    
    with open("summoners.json", "r") as f:
        summoners = orjson.loads(f.read())
    summoners = sort_summoners(summoners, sys.argv[1])

    if sys.argv[1] == "solo":
        league = "420"
    elif sys.argv[1] == "flex":
        league = "440"

    rank = 1
    for summoner in summoners:
        print(f"{rank}. {summoner['name']} {summoner['leagueEntries'][league]['tier']} {summoner['leagueEntries'][league]['rank']} {summoner['leagueEntries'][league]['leaguePoints']}")
        rank += 1

if __name__ == "__main__":
    main()