import { nullable, z } from "zod";

const N420Schema = z.object({
    leagueId: z.string(),
    queueType: z.string(),
    tier: z.string(),
    rank: z.string(),
    leaguePoints: z.number(),
    wins: z.number(),
    losses: z.number(),
    veteran: z.boolean(),
    inactive: z.boolean(),
    freshBlood: z.boolean(),
    hotStreak: z.boolean(),
});

const N440Schema = z.object({
    leagueId: z.string(),
    queueType: z.string(),
    tier: z.string(),
    rank: z.string(),
    leaguePoints: z.number(),
    wins: z.number(),
    losses: z.number(),
    veteran: z.boolean(),
    inactive: z.boolean(),
    freshBlood: z.boolean(),
    hotStreak: z.boolean(),
});

const LeagueEntriesSchema = z.object({
    "420": N420Schema.optional().nullable(),
    "440": N440Schema.optional().nullable(),
});

export const summonerSchema = z.object({
    gameName: z.string(),
    tagLine: z.string(),
    summonerId: z.string(),
    puuid: z.string(),
    name: z.string(),
    profileIconId: z.number(),
    summonerLevel: z.number(),
    platform: z.string(),
    leagueEntries: LeagueEntriesSchema,
});

// Infer the Summoner type from the schema
export type Summoner = z.infer<typeof summonerSchema>;
