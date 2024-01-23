import enum

import orjson
from fastapi import FastAPI

from schemas import Summoner


app = FastAPI()


# Define tier and division ranking constants
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

# Define an enum for sort options
class SortBy(str, enum.Enum):
    solo = "solo"
    flex = "flex"


# Utility functions to sort summoners
def sort_summoners(summoners: list[dict], league_key: str):
    """Sort summoners by specified league rank, unranked at the bottom."""
    unranked = [s for s in summoners if s["leagueEntries"][league_key] is None]
    ranked = [s for s in summoners if s["leagueEntries"][league_key] is not None]

    # Sort ranked summoners
    ranked.sort(key=lambda summoner: summoner["tagLine"])
    ranked.sort(key=lambda summoner: summoner["gameName"])
    ranked.sort(key=lambda summoner: summoner["leagueEntries"][league_key]["leaguePoints"], reverse=True)
    ranked.sort(key=lambda summoner: division[summoner["leagueEntries"][league_key]["rank"]], reverse=True)
    ranked.sort(key=lambda summoner: tiers[summoner["leagueEntries"][league_key]["tier"]], reverse=True)

    # Sort unranked summoners
    unranked.sort(key=lambda summoner: summoner["tagLine"])
    unranked.sort(key=lambda summoner: summoner["gameName"])

    return ranked + unranked


def sort_by_name(summoners: list[dict]):
    """Sort summoners by tagLine, then by gameName."""
    summoners.sort(key=lambda summoner: summoner["tagLine"])
    summoners.sort(key=lambda summoner: summoner["gameName"])
    return summoners


# Endpoint to get summoners
@app.get("/summoners", response_model=list[Summoner])
def get_summoners(sort_by: SortBy = None):
    """Get a list of summoners, optionally sorted by solo or flex rank."""
    # Load summoners from JSON file
    summoners = []
    with open("data/summoners.json", "r") as f:
        summoners = orjson.loads(f.read())

    # Sort summoners based on the requested sort option
    match sort_by:
        case SortBy.solo:
            return sort_summoners(summoners, "420")
        case SortBy.flex:
            return sort_summoners(summoners, "440")
        case None:
            return sort_by_name(summoners)
