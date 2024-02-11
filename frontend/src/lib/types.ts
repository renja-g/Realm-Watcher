export type Summoner = {
    gameName: string
    tagLine: string
    summonerId: string
    puuid: string
    name: string
    profileIconId: number
    summonerLevel: number
    platform: string
    leagueEntries: LeagueEntries
}

export interface LeagueEntries {
    "420"?: N420
    "440"?: N440
}

export interface N420 {
    leagueId: string
    queueType: string
    tier: string
    rank: string
    leaguePoints: number
    wins: number
    losses: number
    veteran: boolean
    inactive: boolean
    freshBlood: boolean
    hotStreak: boolean
}

export interface N440 {
    leagueId: string
    queueType: string
    tier: string
    rank: string
    leaguePoints: number
    wins: number
    losses: number
    veteran: boolean
    inactive: boolean
    freshBlood: boolean
    hotStreak: boolean
}
