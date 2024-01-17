import orjson
import os
import sys

from rich.console import Console
from rich.table import Table


# set cwd to the directory of this file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

tiers = {
    "IRON": 0,
    "BRONZE": 1,
    "SILVER": 2,
    "GOLD": 3,
    "PLATINUM": 4,
    "EMERALD": 5,
    "DIAMOND": 6,
    "MASTER": 7,
    "GRANDMASTER": 8,
    "CHALLENGER": 9,
}

division = {
    "IV": 0,
    "III": 1,
    "II": 2,
    "I": 3,
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
    
    # sort the summoners
    # 1. tagLine
    # 2. gameName
    # 3. leaguePoints
    # 4. rank
    # 5. tier
    summoners.sort(key=lambda summoner: summoner["tagLine"])
    summoners.sort(key=lambda summoner: summoner["gameName"])
    summoners.sort(key=lambda summoner: summoner["leagueEntries"][league]["leaguePoints"], reverse=True)
    summoners.sort(key=lambda summoner: division[summoner["leagueEntries"][league]["rank"]], reverse=True)
    summoners.sort(key=lambda summoner: tiers[summoner["leagueEntries"][league]["tier"]], reverse=True)
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
    # Print the leaderboard
    # Rank | gameName#tagLine | tier | Division(rank) | LP | Wins | Losses | Winrate
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#")
    table.add_column("Summoner")
    table.add_column("Rank")
    table.add_column("LP")
    table.add_column("Games")
    table.add_column("Winrate")
    for summoner in summoners:
        league_entry = summoner["leagueEntries"][league]
        table.add_row(
            str(rank),
            f"{summoner['gameName']}#{summoner['tagLine']}",
            f"{league_entry['tier']} {league_entry['rank']}",
            str(league_entry["leaguePoints"]),
            str(league_entry["wins"] + league_entry["losses"]),
            f"{round(league_entry['wins'] / (league_entry['wins'] + league_entry['losses']) * 100, 2)}%"
        )
        rank += 1
    console.print(table)


if __name__ == "__main__":
    main()