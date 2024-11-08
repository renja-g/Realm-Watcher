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

export interface LeaderboardEntry {
    _id: string;
    summoner: Summoner;
    league: League;
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