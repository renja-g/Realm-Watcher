from pydantic import BaseModel, ConfigDict, validator, GetJsonSchemaHandler
from pydantic_core import CoreSchema

from bson import ObjectId



class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, any]:
        return {"type": "string", "format": "ObjectId"}


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class UserResponse(BaseResponse):
    id: ObjectIdStr
    username: str


class SummonerResponse(BaseResponse):
    id: ObjectIdStr
    puuid: str

    game_name: str
    tag_line: str
    summoner_id: str
    name: str
    profile_icon_id: int
    summoner_level: int
    platform: str


class LeagueEntryResponse(BaseResponse):
    id: ObjectIdStr

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


class SummonerWithLeagueEntriesResponse(BaseResponse):
    summoner: SummonerResponse
    league_entries: list[LeagueEntryResponse]
