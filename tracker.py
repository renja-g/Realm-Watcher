# A tracker that keeps the summoners.json file up to date
import os
import asyncio
import sys
from typing import Literal

from dotenv import load_dotenv
import orjson
from loguru import logger

from pulsefire.clients import RiotAPIClient
from pulsefire.ratelimiters import RiotAPIRateLimiter
from pulsefire.middlewares import (
    json_response_middleware,
    http_error_middleware,
    rate_limiter_middleware,
)

logger.info("Starting tracker...")

load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")


PLATFORM_TO_REGIONS = {
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


def has_summoner_changed(old_data: dict, new_data: dict) -> bool:
    return old_data != new_data


async def get_summoners():
    with open("summoners.json", "r") as f:
        summoners = orjson.loads(f.read())
    return summoners


async def get_league(client: RiotAPIClient, summoner: dict) -> dict | None:
    """Get the leagues of a summoner"""
    api_league_entries = await client.get_lol_league_v4_entries_by_summoner(
        region=summoner["platform"],
        summoner_id=summoner["summonerId"],
    )
    league_entries ={
        "420": None,
        "440": None,
    }
    if not api_league_entries:
        return league_entries
    for entry in api_league_entries:
        if entry["queueType"] == "RANKED_SOLO_5x5":
            entry.pop("summonerId")
            entry.pop("summonerName")
            league_entries["420"] = entry
        elif entry["queueType"] == "RANKED_FLEX_SR":
            entry.pop("summonerId")
            entry.pop("summonerName")
            league_entries["440"] = entry
    return league_entries


async def update_summoner_league(summoner: dict, league_entries: dict) -> dict:
    """
    Update the league of a summoner.
    """
    old_league_entries = summoner.get("leagueEntries", {})
    summoner["leagueEntries"] = league_entries
    if has_summoner_changed(old_league_entries, league_entries):
        logger.info(f"Summoner {summoner['gameName']}#{summoner['tagLine']} league entries updated.")
    return summoner


async def update_summoner(summoner: dict, client: RiotAPIClient) -> dict:
    """Updates the icon, level name etc"""
    old_summoner_data = summoner.copy()
    api_summoner = await client.get_lol_summoner_v4_by_puuid(
        region=summoner["platform"],
        puuid=summoner["puuid"],
    )
    api_summoner.pop("revisionDate")
    api_summoner.pop("accountId")
    api_summoner.pop("id")
    api_summoner.pop("puuid")
    summoner.update(api_summoner)
    
    api_summoner_account = await client.get_account_v1_by_puuid(
        region=PLATFORM_TO_REGIONS[summoner["platform"]],
        puuid=summoner["puuid"],
    )
    api_summoner_account.pop("puuid")
    summoner.update(api_summoner_account)

    if has_summoner_changed(old_summoner_data, summoner):
        logger.info(f"Summoner {summoner['gameName']}#{summoner['tagLine']} details updated.")
    return summoner

async def update_summoners(summoners: list[dict], client: RiotAPIClient) -> None:
    """
    Update the league of all summoners.
    """
    for summoner in summoners:
        league_entries = await get_league(client, summoner)
        summoner = await update_summoner_league(summoner, league_entries)
    
    with open("summoners.json", "w") as f:
        f.write(orjson.dumps(summoners, option=orjson.OPT_INDENT_2).decode())


async def main() -> None:
    while True:
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
            summoners = await get_summoners()
            await update_summoners(summoners, client)
            logger.info("Everything updated.")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
