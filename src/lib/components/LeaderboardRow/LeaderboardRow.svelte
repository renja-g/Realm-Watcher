<script lang="ts">
  import type { LeaderboardEntry, Match } from '$lib/types/types';

  const {
    index,
    entry
  }: {
    index: number;
    entry: LeaderboardEntry;
  } = $props();

  const iconUrl = `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/${entry.summoner.profileIconId}.jpg`;
  const tierIconUrl = `https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-mini-crests/${entry.league.tier.toLowerCase()}.svg`;
  const opggUrl = `https://www.op.gg/summoners/euw/${entry.summoner.gameName}-${entry.summoner.tagLine}`;


  function calcLPDiff(matches: Match[]): number {
    if (matches.length < 2) return 0;

    const tierWorth: Record<string, number> = {
      "IRON": 0,
      "BRONZE": 400,
      "SILVER": 800,
      "GOLD": 1200,
      "PLATINUM": 1600,
      "EMERALD": 2000,
      "DIAMOND": 2400,
      "MASTER": 2800,
      "GRANDMASTER": 2800,
      "CHALLENGER": 2800
    };

    const rankWorth: Record<string, number> = {
      "IV": 0,
      "III": 100,
      "II": 200,
      "I": 300
    };

    const firstMatch = matches[0];
    const compareMatch = matches[Math.min(4, matches.length - 1)]; // Get 5th match (index 4) or last available

    const currentWorth = tierWorth[firstMatch.league.tier] + rankWorth[firstMatch.league.rank] + firstMatch.league.leaguePoints;
    const previousWorth = tierWorth[compareMatch.league.tier] + rankWorth[compareMatch.league.rank] + compareMatch.league.leaguePoints;

    return currentWorth - previousWorth;
  }

  function calcKDA(matches: Match[]): number {
    const last10Matches = matches.slice(0, 10);
    const kda = last10Matches.reduce((acc, match) => {
      const kills = match.kills;
      const deaths = match.deaths;
      const assists = match.assists;

      return {
        kills: acc.kills + kills,
        deaths: acc.deaths + deaths,
        assists: acc.assists + assists
      };
    }, { kills: 0, deaths: 0, assists: 0 });

    return kda.deaths === 0 ? kda.kills + kda.assists : (kda.kills + kda.assists) / kda.deaths;
  }

  function getLastLpChange(matches: Match[]): { win: number | null; loss: number | null } {
    const tierWorth: Record<string, number> = {
      "IRON": 0,
      "BRONZE": 400,
      "SILVER": 800,
      "GOLD": 1200,
      "PLATINUM": 1600,
      "EMERALD": 2000,
      "DIAMOND": 2400,
      "MASTER": 2800,
      "GRANDMASTER": 2800,
      "CHALLENGER": 2800
    };

    const rankWorth: Record<string, number> = {
      "IV": 0,
      "III": 100,
      "II": 200,
      "I": 300
    };

    function getTotalLP(match: Match): number {
      return tierWorth[match.league.tier] + rankWorth[match.league.rank] + match.league.leaguePoints;
    }

    let lastWinLP = null;
    let lastLossLP = null;

    for (let i = 0; i < matches.length - 1; i++) {
      const currentMatch = matches[i];
      const nextMatch = matches[i + 1];
      
      const lpDiff = getTotalLP(currentMatch) - getTotalLP(nextMatch);

      if (currentMatch.win && lastWinLP === null) {
        lastWinLP = lpDiff;
      } else if (!currentMatch.win && lastLossLP === null) {
        lastLossLP = -lpDiff;
      }

      if (lastWinLP !== null && lastLossLP !== null) break;
    }

    return {
      win: lastWinLP,
      loss: lastLossLP
    };
  }

  const lpDiff = calcLPDiff(entry.matches);
  const kda = calcKDA(entry.matches);
  const lpChange = getLastLpChange(entry.matches);

  const winRate = (entry.league.wins / (entry.league.wins + entry.league.losses)) * 100;
  const winWidth = winRate * 0.6; // Scale factor for width
  const lossWidth = (100 - winRate) * 0.6; // Scale factor for width
</script>

<div class="grid grid-cols-12 items-center border-t border-gray-700 px-6 py-4">
  <!-- Rank Number -->
  <div class="col-span-1 font-bold">
    {index + 1}
  </div>

  <!-- Profile -->
  <div class="col-span-2 flex items-center">
    <img class="mr-4 h-11 w-11 rounded-full" src={iconUrl} alt="Profile Icon" />
    <div class="flex flex-col">
      <a  href={opggUrl}  target="_blank" rel="noopener noreferrer" class="font-semibold hover:underline">
        {entry.summoner.gameName}
      </a>
      <span class="text-sm text-gray-400">#{entry.summoner.tagLine}</span>
    </div>
  </div>

  <!-- Rank -->
  <div class="col-span-2 flex items-center">
    <img class="mr-2 h-8 w-8" src={tierIconUrl} alt="Rank Icon" />
    <span class="mr-2">{entry.league.tier}</span>
    <span class="mr-2">{entry.league.rank}</span>
    <span class="text-gray-400">{entry.league.leaguePoints}</span>
  </div>

  <!-- LP Diff -->
  <div class={`col-span-1 font-semibold text-center ${
    lpDiff > 0 ? 'text-green-500' : lpDiff < 0 ? 'text-red-500' : 'text-white'
  }`}>
    {lpDiff}
  </div>

  <!-- LP Diff -->
  <div class="col-span-1 text-center">
    <span class="text-green-500">{lpChange.win !== null ? `+${lpChange.win}` : '?'}</span>
    {' / '}
    <span class="text-red-500">{lpChange.loss !== null ? `-${lpChange.loss}` : '?'}</span>
  </div>

  <!-- KDA -->
  <div class="col-span-2 text-center">
    {kda.toFixed(2)}
  </div>

  <!-- Win Rate -->
  <div class="col-span-3">
    <div class="flex items-center justify-center">
      <div
        class="rounded-l bg-[#4B7AD8] px-2 py-0.3 text-sm font-semibold"
        style="width: {winWidth}%;"
      >
        {entry.league.wins}W
      </div>
      <div
        class="mr-2 rounded-r bg-[#DC5F61] px-2 py-0.3 text-right text-sm font-semibold"
        style="width: {lossWidth}%;"
      >
        {entry.league.losses}L
      </div>
      <div>{winRate.toFixed(1)}%</div>
    </div>
  </div>
</div>
