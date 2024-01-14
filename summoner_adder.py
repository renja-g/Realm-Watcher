import os
import asyncio
import sys
from typing import Literal

from dotenv import load_dotenv
import orjson

from pulsefire.clients import RiotAPIClient
from pulsefire.ratelimiters import RiotAPIRateLimiter
from pulsefire.middlewares import (
    json_response_middleware,
    http_error_middleware,
    rate_limiter_middleware,
)


load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")


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
    with open("summoners.json", "r") as f:
        summoners = orjson.loads(f.read())
    if any(
        summoner["gameName"] == game_name
        and summoner["tagLine"] == tag_line
        and summoner["platform"] == platform
        for summoner in summoners
    ):
        print(f"Summoner {game_name}#{tag_line} already in the database.")
        sys.exit(1)
    
    async with RiotAPIClient(
        default_headers={"X-Riot-Token": RIOT_API_KEY},
        middlewares=[
            json_response_middleware(orjson.loads),
            http_error_middleware(3),
            rate_limiter_middleware(RiotAPIRateLimiter(
                proxy="http://127.0.0.1:12227"
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
    with open("summoners.json", "w") as f:
        f.write(orjson.dumps(summoners, option=orjson.OPT_INDENT_2).decode())

    print(f"Summoner {game_name}#{tag_line} added to the database.")


# Run the event loop
if __name__ == "__main__":
    input_args = sys.argv[1:]
    if len(input_args) != 3:
        print("Usage: python summoner_adder.py <name> <tag_line> <platform>")
        print("If there is a space in the name, surround it with quotes.")
        sys.exit(1)
    asyncio.run(add_summoner(*input_args))
'''
Ayato, 11235, euw1
WeingottBachus, EUW, euw1
Killer Fisch, 1111, euw1
Ethereal Peace, EUW, euw1
ique, ique1, euw1
bubble, 1608, euw1
'''