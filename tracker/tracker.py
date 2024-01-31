import os
import asyncio
from typing import Optional, Dict, List

# External libraries
from dotenv import load_dotenv
import orjson
from loguru import logger

# pulsefire modules
from pulsefire.clients import RiotAPIClient
from pulsefire.ratelimiters import RiotAPIRateLimiter
from pulsefire.middlewares import json_response_middleware, http_error_middleware, rate_limiter_middleware


# Load environment variables
load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
RATELIMITER_HOST = os.getenv('RATELIMITER_HOST', 'localhost')
RATELIMITER_PORT = os.getenv('RATELIMITER_PORT', '12227')

ratelimiter_url = f'http://{RATELIMITER_HOST}:{RATELIMITER_PORT}'

# Mapping of platforms to their respective regions
PLATFORM_TO_REGIONS = {
    "br1": "americas", "eun1": "europe", "euw1": "europe", "jp1": "asia", "kr": "asia",
    "la1": "americas", "la2": "americas", "na1": "americas", "oc1": "sea", "tr1": "europe",
    "ru": "europe", "ph2": "sea", "sg2": "sea", "th2": "sea", "tw2": "sea", "vn2": "sea",
}


logger.info("Starting tracker...")


# Function definitions
def has_summoner_changed(old_data: Dict, new_data: Dict) -> bool:
    """Check if the summoner's data has changed."""
    return old_data != new_data


async def get_summoners() -> Optional[List[Dict]]:
    """Read and load summoner data from a JSON file."""
    try:
        with open("data/summoners.json", "r") as f:
            summoners = orjson.loads(f.read())
        return summoners
    except Exception as e:
        logger.error(f"Failed to read summoners.json: {e}")
        return None


async def get_league(client: RiotAPIClient, summoner: Dict) -> Dict[str, Optional[Dict]]:
    """Get the league details for a summoner."""
    api_league_entries = await client.get_lol_league_v4_entries_by_summoner(
        region=summoner["platform"],
        summoner_id=summoner["summonerId"],
    )
    league_entries = {"420": None, "440": None}
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


async def update_summoner_league(summoner: Dict, league_entries: Dict) -> Dict:
    """Update the league details of a summoner."""
    old_league_entries = summoner.get("leagueEntries", {})
    summoner["leagueEntries"] = league_entries
    if has_summoner_changed(old_league_entries, league_entries):
        logger.info(f"Summoner {summoner['gameName']}#{summoner['tagLine']} league entries updated.")
    return summoner


async def update_summoner_details(summoner: Dict, client: RiotAPIClient) -> Dict:
    """Fetch and update the summoner's details from the API."""
    old_summoner_data = summoner.copy()
    try:
        api_summoner = await client.get_lol_summoner_v4_by_puuid(
            region=summoner["platform"],
            puuid=summoner["puuid"],
        )
        api_summoner.pop("revisionDate")
        api_summoner.pop("accountId")
        api_summoner.pop("id")
        api_summoner.pop("puuid")
        summoner.update(api_summoner)
    except Exception as e:
        logger.error(f"Failed to get summoner {summoner['gameName']}#{summoner['tagLine']} details: {e}")

    try:    
        api_summoner_account = await client.get_account_v1_by_puuid(
            region=PLATFORM_TO_REGIONS[summoner["platform"]],
            puuid=summoner["puuid"],
        )
        api_summoner_account.pop("puuid")
        summoner.update(api_summoner_account)
    except Exception as e:
        logger.error(f"Failed to get summoner {summoner['gameName']}#{summoner['tagLine']} account details: {e}")

    if has_summoner_changed(old_summoner_data, summoner):
        logger.info(f"Summoner {summoner['gameName']}#{summoner['tagLine']} details updated.")
    return summoner

async def update_summoner(summoner: Dict, client: RiotAPIClient) -> None:
    """Update details for a summoner."""
    league_entries = await get_league(client, summoner)
    summoner = await update_summoner_league(summoner, league_entries)
    summoner = await update_summoner_details(summoner, client)
    return summoner


async def update_all_summoners(summoners: List[Dict], client: RiotAPIClient) -> None:
    """Update details for all summoners."""
    if summoners is None:
        logger.error("No summoners to update.")
        return
    
    tasks = []
    for summoner in summoners:
        tasks.append(update_summoner(summoner, client))
    summoners = await asyncio.gather(*tasks)

    try:
        with open("data/summoners.json", "w") as f:
            f.write(orjson.dumps(summoners, option=orjson.OPT_INDENT_2).decode())
    except Exception as e:
        logger.error(f"Failed to write summoners.json: {e}")


async def main() -> None:
    """Main function to orchestrate the updating of summoners."""
    while True:
        try:
            async with RiotAPIClient(
                    default_headers={"X-Riot-Token": RIOT_API_KEY},
                    middlewares=[
                        json_response_middleware(orjson.loads),
                        http_error_middleware(3),
                        rate_limiter_middleware(RiotAPIRateLimiter(
                            proxy=ratelimiter_url
                        )),
                    ]
                ) as client:
                summoners = await get_summoners()
                await update_all_summoners(summoners, client)
                logger.info("Everything up to date.")
                await asyncio.sleep(20)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
