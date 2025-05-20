/*
{
  "_id": "6732029b02ee4fb97e0a2343",
  "summoner": {
    "_id": "6732029b02ee4fb97e0a2343",
    "gameName": "Leo5000Twitch",
    "tagLine": "EUW",
    "platform": "euw1",
    "accountId": "zpOye2fHWr7wihaoTT8OMqKnc515CT6Q1v-ERVqIs3OBqg4",
    "puuid": "nhStND8Vo_D0mrcchTaU3VoGtFN7CK95i0iwUoTEZ7nFU1bEbCelc8BiuUUVlt25_yJKcKaNCZ0JKw",
    "profileIconId": 3589,
    "revisionDate": 1731341552183,
    "summonerLevel": 423,
    "summonerId": "JMmq8GBApwtP3SpJKGTQkq2GL4BXl0Mw7yuLxIZl06fx5uxM"
  },
  "league": {
    "_id": "673203dca983b6c3c7d8a8a9",
    "ref_summoner": "6732029b02ee4fb97e0a2343",
    "queueType": "RANKED_SOLO_5x5",
    "freshBlood": true,
    "hotStreak": false,
    "inactive": false,
    "leagueId": "7a75c2c0-ff7b-4e0a-9524-fc5ac660210a",
    "leaguePoints": 0,
    "losses": 57,
    "rank": "IV",
    "summonerId": "JMmq8GBApwtP3SpJKGTQkq2GL4BXl0Mw7yuLxIZl06fx5uxM",
    "tier": "EMERALD",
    "veteran": false,
    "wins": 67
  },
  "matches": [
    {
      "matchId": "EUW1_7182909051",
      "gameEndTimestamp": 1731338828252,
      "championName": "Akshan",
      "win": true,
      "kills": 2,
      "deaths": 2,
      "assists": 4,
      "teamPosition": "BOTTOM",
      "individualPosition": "BOTTOM",
      "league": {
        "leaguePoints": 19,
        "tier": "EMERALD",
        "rank": "IV"
      }
    },
    {
      "matchId": "EUW1_7182960493",
      "gameEndTimestamp": 1731341550568,
      "championName": "Skarner",
      "win": false,
      "kills": 6,
      "deaths": 10,
      "assists": 23,
      "teamPosition": "JUNGLE",
      "individualPosition": "JUNGLE",
      "league": {
        "leaguePoints": 0,
        "tier": "EMERALD",
        "rank": "IV"
      }
    }
  ]
}
*/

export interface Summoner {
    _id: string;
    gameName: string;
    tagLine: string;
    platform: string;
    accountId: string;
    puuid: string;
    profileIconId: number;
    revisionDate: number;
    summonerLevel: number;
    summonerId: string;
}

export interface League {
    _id: string;
    ref_summoner: string;
    queueType: string;
    freshBlood: boolean;
    hotStreak: boolean;
    inactive: boolean;
    leagueId: string;
    leaguePoints: number;
    losses: number;
    rank: string;
    summonerId: string;
    tier: string;
    veteran: boolean;
    wins: number;
}

export interface matchLeague {
    leaguePoints: number;
    tier: string;
    rank: string;
}

export interface Match {
    _id: string;
    matchId: string;
    gameEndTimestamp: number;
    // championName: string;
    championId: number;
    remake: boolean;
    win: boolean;
    kills: number;
    deaths: number;
    assists: number;
    teamPosition: string;
    individualPosition: string;
    league: matchLeague;
}

export interface LeaderboardEntry {
    _id: string;
    summoner: Summoner;
    league: League;
    matches: Match[];
}

export type queueType = "RANKED_SOLO_5x5" | "RANKED_FLEX_SR";


export interface Tab {
    id: string;
    label: string;
}

export interface Player {
    position: number;
    name: string;
    tag: string;
    rank: string;
    lp: number;
    lpChange: number;
    wins: number;
    losses: number;
    winRate: number;
    avatar: string;
}