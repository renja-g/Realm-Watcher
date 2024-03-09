from aiohttp import ClientResponseError

from fastapi import APIRouter, Depends, HTTPException

from pulsefire.clients import RiotAPIClient

from app.api import deps
from app.models import Summoner, LeagueEntry, User
from app.schemas.requests import SummonerCreateRequest
from app.schemas.responses import SummonerResponse, SummonerWithLeagueEntriesResponse
from app.core.utils import platform_to_region, convert_keys

router = APIRouter()


@router.post("", response_model=SummonerWithLeagueEntriesResponse)
async def create_summoner(
    summoner_in: SummonerCreateRequest,
    current_user: User = Depends(deps.get_current_user),
    client: RiotAPIClient = Depends(deps.get_riot_client),
):
    summoner = await Summoner.find_one(
        Summoner.game_name == summoner_in.game_name,
        Summoner.tag_line == summoner_in.tag_line,
        Summoner.platform == summoner_in.platform
    )
    if summoner is not None:
        raise HTTPException(status_code=409, detail="Summoner already exists")

    try:
        account = await client.get_account_v1_by_riot_id(
            region=platform_to_region(summoner_in.platform), game_name=summoner_in.game_name, tag_line=summoner_in.tag_line
        )
    except ClientResponseError as e:
        if e.status == 404:
            raise HTTPException(status_code=404, detail="Summoner not found")
        elif e.status == 429:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        else:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    summoner = await client.get_lol_summoner_v4_by_puuid(
        region=summoner_in.platform, puuid=account["puuid"]
    )
    league_entries = await client.get_lol_league_v4_entries_by_summoner(
        region=summoner_in.platform, summoner_id=summoner["id"]
    )
    for league_entry in league_entries:
        league_entry.pop("summonerId", None)
        league_entry.pop("summonerName", None)
    
    summoner = Summoner(
        **convert_keys(summoner),
        game_name=account["gameName"],
        tag_line=account["tagLine"],
        platform=summoner_in.platform.lower(),
    )
    league_entries = [LeagueEntry(
        **convert_keys(league_entry),
        summoner=summoner
        ) for league_entry in league_entries]

    await summoner.insert()
    for league_entry in league_entries:
        await league_entry.insert()
    return SummonerWithLeagueEntriesResponse(
        summoner=summoner,
        league_entries=league_entries
    )


@router.get("/{puuid}", response_model=SummonerWithLeagueEntriesResponse)
async def get_summoners(
    puuid: str,
):
    summoner = await Summoner.find_one(Summoner.puuid == puuid, fetch_links=True)
    if summoner is None:
        raise HTTPException(status_code=404, detail="Summoner not found")
    return SummonerWithLeagueEntriesResponse(
        summoner=summoner,
        league_entries=summoner.league_entries
    )


@router.get("", response_model=list[SummonerWithLeagueEntriesResponse])
async def get_summoners():
    summoners = await Summoner.find_all(fetch_links=True).to_list()
    return [
        SummonerWithLeagueEntriesResponse(
            summoner=summoner,
            league_entries=summoner.league_entries
        ) for summoner in summoners
    ]


@router.delete("/{puuid}", response_model=SummonerResponse)
async def delete_summoner(
    puuid: str,
    current_user: User = Depends(deps.get_current_user),
):
    summoner = await Summoner.find_one(Summoner.puuid == puuid)
    if summoner is None:
        raise HTTPException(status_code=404, detail="Summoner not found")
    await summoner.delete()
    return SummonerResponse(**summoner.model_dump())
