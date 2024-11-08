import type { LeaderboardEntry, queueType } from '$lib/types/types';


class LeaderboardResponse {
    entries: LeaderboardEntry[] = $state([]);
    error: unknown = $state(undefined);
    isLoading: boolean = $state(true);
}

export default function useFetchLeaderboard(queueType: queueType) {
    const resp = new LeaderboardResponse();

  async function fetchData() {
    resp.isLoading = true;
    try {
      const response = await fetch(`https://rw.renja.dev/leaderboard?queue_type=${queueType}`);
      resp.entries = await response.json() as LeaderboardEntry[];
      resp.error = undefined;
    } catch (err) {
      resp.error = err;
      resp.entries = [];
    }
    resp.isLoading = false;
  }

  fetchData();
  return resp;
}