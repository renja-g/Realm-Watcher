import os

import orjson
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import Summoner, SummonerCreate

from pulsefire.clients import RiotAPIClient
from pulsefire.ratelimiters import RiotAPIRateLimiter
from pulsefire.middlewares import (
    json_response_middleware,
    http_error_middleware,
    rate_limiter_middleware,
)

from dotenv import load_dotenv

load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
RATELIMITER_HOST = os.getenv('RATELIMITER_HOST', 'localhost')
RATELIMITER_PORT = os.getenv('RATELIMITER_PORT', '12227')

ratelimiter_url = f'http://{RATELIMITER_HOST}:{RATELIMITER_PORT}'

app = FastAPI()

origins = [
    "*",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


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

platform_to_regions = {
    "br1": "americas",
    "eun1": "europe",
    "euw1": "europe",
    "jp1": "asia",
    "kr": "asia",
    "la1": "americas",
    "la2": "americas",
    "na1": "americas",
    "oc1": "sea",
    "tr1": "europe",
    "ru": "europe",
    "ph2": "sea",
    "sg2": "sea",
    "th2": "sea",
    "tw2": "sea",
    "vn2": "sea",
}


def platform_to_region(platform: str) -> str:
    '''Return the region correspondent to a given platform'''
    return platform_to_regions[platform]


async def add_summoner(game_name, tag_line, platform):
    with open("data/summoners.json", "r") as f:
        summoners = orjson.loads(f.read())
    if any(
        summoner["gameName"] == game_name
        and summoner["tagLine"] == tag_line
        and summoner["platform"] == platform
        for summoner in summoners
    ):
        print(f"Summoner {game_name}#{tag_line} already in the database.")
        return HTTPException(status_code=409, detail="Summoner already added.")

    async with RiotAPIClient(
        default_headers={"X-Riot-Token": RIOT_API_KEY},
        middlewares=[
            json_response_middleware(orjson.loads),
            http_error_middleware(3),
            rate_limiter_middleware(RiotAPIRateLimiter(
                proxy=ratelimiter_url,
            )),
        ]
    ) as client:
        account = await client.get_account_v1_by_riot_id(
            region=platform_to_region(platform), game_name=game_name, tag_line=tag_line
        )
        summoner = await client.get_lol_summoner_v4_by_puuid(
            region=platform, puuid=account["puuid"]
        )
        leagues = await client.get_lol_league_v4_entries_by_summoner(
            region="euw1", summoner_id=summoner["id"]
        )
        solo_queue_league = next(
            (league for league in leagues if league["queueType"] == "RANKED_SOLO_5x5"),
            None,
        )
        flex_queue_league = next(
            (league for league in leagues if league["queueType"] == "RANKED_FLEX_SR"),
            None,
        )
    if solo_queue_league:
        solo_queue_league.pop("summonerId", None)
        solo_queue_league.pop("summonerName", None)
    if flex_queue_league:
        flex_queue_league.pop("summonerId", None)
        flex_queue_league.pop("summonerName", None)

    enriched_summoner = {
        "gameName": game_name,
        "tagLine": tag_line,
        "summonerId": summoner["id"],
        "puuid": summoner["puuid"],
        "name": summoner["name"],
        "profileIconId": summoner["profileIconId"],
        "summonerLevel": summoner["summonerLevel"],
        "platform": platform,
        "leagueEntries": {
            "420": solo_queue_league,  # 420 is the queue id for solo queue | None if not ranked
            "440": flex_queue_league,  # 440 is the queue id for flex queue | None if not ranked
        },
    }

    summoners.append(enriched_summoner)
    with open("data/summoners.json", "w") as f:
        f.write(orjson.dumps(summoners, option=orjson.OPT_INDENT_2).decode())

    print(f"Summoner {game_name}#{tag_line} added to the database.")
    return enriched_summoner


def sort_by_name(summoners: list[dict]):
    """Sort summoners by tagLine, then by gameName."""
    summoners.sort(key=lambda summoner: summoner["tagLine"])
    summoners.sort(key=lambda summoner: summoner["gameName"])
    return summoners


# Endpoint to get summoners
@app.get("/summoners", response_model=list[Summoner])
def get_summoners():
    """Get a list of summoners, optionally sorted by solo or flex rank."""
    # Load summoners from JSON file
    summoners = []
    with open("data/summoners.json", "r") as f:
        summoners = orjson.loads(f.read())

    return sort_by_name(summoners)


# Endpoint to add a summone
@app.post("/summoners")
async def create_summoner(summoner: SummonerCreate):
    try:
        return await add_summoner(summoner.gameName, summoner.tagLine, summoner.platform)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to delete a summoner
@app.delete("/summoners/{summoner_puuid}")
def delete_summoner(summoner_puuid: str):
    """Delete a summoner by puuid."""
    # Load summoners from JSON file
    summoners = []
    with open("data/summoners.json", "r") as f:
        summoners = orjson.loads(f.read())

    # Remove the summoner with the given puuid
    summoners = [summoner for summoner in summoners if summoner["puuid"] != summoner_puuid]

    # Write the updated list of summoners to the JSON file
    with open("data/summoners.json", "w") as f:
        f.write(orjson.dumps(summoners, option=orjson.OPT_INDENT_2).decode())

    return {"message": "Summoner deleted successfully."}