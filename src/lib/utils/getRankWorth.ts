import type { matchLeague } from '$lib/types/types';

export function getLPWorth(league: matchLeague): number {
  const tierWorth: Record<string, number> = {
    IRON: 0,
    BRONZE: 400,
    SILVER: 800,
    GOLD: 1200,
    PLATINUM: 1600,
    EMERALD: 2000,
    DIAMOND: 2400,
    MASTER: 2800,
    GRANDMASTER: 2800,
    CHALLENGER: 2800
  };

  const rankWorth: Record<string, number> = {
    IV: 0,
    III: 100,
    II: 200,
    I: 300
  };

  return tierWorth[league.tier] + rankWorth[league.rank] + league.leaguePoints;
}
