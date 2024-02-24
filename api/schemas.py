from enum import Enum
from pydantic import BaseModel


class TierEnum(str, Enum):
    CHALLENGER = 'CHALLENGER'
    GRANDMASTER = 'GRANDMASTER'
    MASTER = 'MASTER'
    DIAMOND = 'DIAMOND'
    EMERALD = 'EMERALD'
    PLATINUM = 'PLATINUM'
    GOLD = 'GOLD'
    SILVER = 'SILVER'
    BRONZE = 'BRONZE'
    IRON = 'IRON'

class RankEnum(str, Enum):
    I = 'I'
    II = 'II'
    III = 'III'
    IV = 'IV'


# Define the schema
class LeagueEntry(BaseModel):
    leagueId: str
    queueType: str
    tier: TierEnum
    rank: RankEnum
    leaguePoints: int
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    freshBlood: bool
    hotStreak: bool

class Summoner(BaseModel):
    gameName: str
    tagLine: str
    summonerId: str
    puuid: str
    name: str
    profileIconId: int
    summonerLevel: int
    platform: str
    leagueEntries: dict[str, LeagueEntry | None]


class SummonerCreate(BaseModel):
    gameName: str
    tagLine: str
    platform: str
