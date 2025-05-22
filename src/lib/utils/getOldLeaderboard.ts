import { PUBLIC_COMPARISON_DAYS } from '$env/static/public';
import type { LeaderboardResponse } from '$lib/hooks/useFetchLeaderboard.svelte';
import { getLPWorth } from './getRankWorth';

export function getOldLeaderboard(entries: LeaderboardResponse): Record<string, number> {
  if (entries.error || entries.isLoading) return {};

  const gameMustBeOlderThan = Date.now() - parseInt(PUBLIC_COMPARISON_DAYS) * 24 * 60 * 60 * 1000;

  const players: { puuid: string; lp: number }[] = [];

  entries.entries.forEach((entry) => {
    const player = entry.summoner.puuid;
    let lp = getLPWorth(entry.league);

    for (let i = 0; i < entry.matches.length; i++) {
      const match = entry.matches[i];
      lp = getLPWorth(match.league);

      // we want the LP x days ago. Thats why we need the LP of the first game after the timestamp
      if (match.gameEndTimestamp < gameMustBeOlderThan) {
        break;
      }
    }

    players.push({
      puuid: player,
      lp
    });
  });

  players.sort((a, b) => b.lp - a.lp);

  const result: Record<string, number> = {};
  players.forEach((player, i) => {
    result[player.puuid] = i ;
  });

  return result;
}
