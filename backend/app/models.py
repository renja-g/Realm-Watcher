import pymongo
from pydantic import Field

from beanie import Document, Link, BackLink

# User is only used for the admin login
class User(Document):
    username: str = Field(..., unique=True)
    hashed_password: str

    class Settings:
        name = "user"
        indexes = [
            [
                ("username", pymongo.TEXT),
            ]
        ]


# A summoner can have multiple league entries or none at all
# A league entry is linked to a summoner
class Summoner(Document):
    game_name: str
    name: str
    platform: str
    profile_icon_id: int
    puuid: str
    summoner_id: str
    summoner_level: int
    tag_line: str

    league_entries: list[BackLink["LeagueEntry"]] = Field(original_field="summoner")

    class Settings:
        name = "summoner"
        indexes = [
            ("puuid", pymongo.TEXT),
            [
                ("game_name", pymongo.TEXT),
                ("tag_line", pymongo.TEXT),
                ("platform", pymongo.TEXT),
            ],

        ]


class LeagueEntry(Document):
    league_id: str
    queue_type: str
    tier: str
    rank: str
    league_points: int
    wins: int
    losses: int
    veteran: bool
    inactive: bool
    fresh_blood: bool
    hot_streak: bool

    summoner: Link[Summoner]

    class Settings:
        name = "league_entry"
        indexes = [
            [
                ("tier", pymongo.TEXT),
                ("rank", pymongo.TEXT),
                ("league_points", pymongo.TEXT),
            ]
        ]


__all_models__ = [
    User,
    Summoner,
    LeagueEntry
]