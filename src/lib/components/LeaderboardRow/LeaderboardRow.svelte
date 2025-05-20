<script lang="ts">
  import type { LeaderboardEntry, Match } from '$lib/types/types';
  import { capitalize } from '$lib/utils/capitalize';

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

    const firstMatch = matches[0];
    const compareMatch = matches[Math.min(4, matches.length - 1)]; // Get 5th match (index 4) or last available

    const currentWorth =
      tierWorth[firstMatch.league.tier] +
      rankWorth[firstMatch.league.rank] +
      firstMatch.league.leaguePoints;
    const previousWorth =
      tierWorth[compareMatch.league.tier] +
      rankWorth[compareMatch.league.rank] +
      compareMatch.league.leaguePoints;

    return currentWorth - previousWorth;
  }

  function calcKDA(matches: Match[]): number {
    const last10Matches = matches.filter((x) => !x.remake).slice(0, 10);
    const kda = last10Matches.reduce(
      (acc, match) => {
        const kills = match.kills;
        const deaths = match.deaths;
        const assists = match.assists;

        return {
          kills: acc.kills + kills,
          deaths: acc.deaths + deaths,
          assists: acc.assists + assists
        };
      },
      { kills: 0, deaths: 0, assists: 0 }
    );

    return kda.deaths === 0 ? kda.kills + kda.assists : (kda.kills + kda.assists) / kda.deaths;
  }

  function getLastLpChange(matches: Match[]): { win: number | null; loss: number | null } {
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

    function getTotalLP(match: Match): number {
      return (
        tierWorth[match.league.tier] + rankWorth[match.league.rank] + match.league.leaguePoints
      );
    }

    let lastWinLP = null;
    let lastLossLP = null;

    for (let i = 0; i < matches.length - 1; i++) {
      const currentMatch = matches[i];
      const nextMatch = matches[i + 1];

      // Don't count remakes
      if (currentMatch.remake || nextMatch.remake) continue;

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

  function getStreak(matches: Match[]): { type: 'win' | 'loss'; amount: number } {
    let last: boolean | undefined;
    let amount: number = 1;
    for (let i = 0; i < matches.length; i++) {
      const match = matches[i];

      if (match.remake) continue;

      if (last === undefined) {
        last = match.win;
        continue;
      }

      if (last !== match.win) break;
      amount++;
    }

    return {
      type: last ? 'win' : 'loss',
      amount
    };
  }

  const lpDiff = calcLPDiff(entry.matches);
  const kda = calcKDA(entry.matches);
  const lpChange = getLastLpChange(entry.matches);
  const streak = getStreak(entry.matches);
  const showStreak = streak.amount >= 3;

  const winRate = (entry.league.wins / (entry.league.wins + entry.league.losses)) * 100;
  const winWidth = winRate * 0.6; // Scale factor for width
  const lossWidth = (100 - winRate) * 0.6; // Scale factor for width
</script>

<div class="grid grid-cols-12 items-center gap-8 border-t border-gray-700 px-6 py-4">
  <!-- Rank Number -->
  <div class="col-span-1 font-bold">
    {index + 1}
  </div>

  <!-- Profile -->
  <div class={`col-span-2 -ml-8 flex items-center`}>
    <img
      class={`mr-4 h-11 w-11 rounded-full ${entry.league.inactive ? 'grayscale' : ''}`}
      src={iconUrl}
      alt="Profile Icon"
    />
    <div class="flex flex-col">
      <a
        href={opggUrl}
        target="_blank"
        rel="noopener noreferrer"
        class={`font-semibold hover:underline ${entry.league.inactive ? 'italic' : ''}`}
      >
        {entry.summoner.gameName}
      </a>
      <span class="text-sm text-gray-400">#{entry.summoner.tagLine}</span>
    </div>
    {#if showStreak}
      <div
        class={`mx-4 flex items-center gap-2 rounded-md px-2 py-1 text-sm ${streak.type === 'win' ? 'bg-orange-500' : 'bg-blue-600 brightness-75'}`}
      >
        {streak.amount}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 448 512"
          class={`w-[0.875rem] fill-white`}
        >
          <!--!Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.-->
          <path
            d="M159.3 5.4c7.8-7.3 19.9-7.2 27.7 .1c27.6 25.9 53.5 53.8 77.7 84c11-14.4 23.5-30.1 37-42.9c7.9-7.4 20.1-7.4 28 .1c34.6 33 63.9 76.6 84.5 118c20.3 40.8 33.8 82.5 33.8 111.9C448 404.2 348.2 512 224 512C98.4 512 0 404.1 0 276.5c0-38.4 17.8-85.3 45.4-131.7C73.3 97.7 112.7 48.6 159.3 5.4zM225.7 416c25.3 0 47.7-7 68.8-21c42.1-29.4 53.4-88.2 28.1-134.4c-4.5-9-16-9.6-22.5-2l-25.2 29.3c-6.6 7.6-18.5 7.4-24.7-.5c-16.5-21-46-58.5-62.8-79.8c-6.3-8-18.3-8.1-24.7-.1c-33.8 42.5-50.8 69.3-50.8 99.4C112 375.4 162.6 416 225.7 416z"
          />
        </svg>
      </div>
    {/if}
  </div>

  <!-- Rank -->
  <div class="col-span-3 flex items-center">
    <img class="mr-2 h-8 w-8" src={tierIconUrl} alt="Rank Icon" />
    <span class={`mr-2 ${entry.league.inactive ? 'italic text-gray-300' : ''}`}>
      {capitalize(entry.league.tier)}</span
    >
    <span class={`mr-2 ${entry.league.inactive ? 'italic text-gray-300' : ''}`}
      >{entry.league.rank}</span
    >
    <span class="text-sm text-gray-400">{entry.league.leaguePoints} LP</span>
  </div>

  <!-- LP Diff -->
  <div
    class={`col-span-1 font-semibold ${
      lpDiff > 0 ? 'text-win' : lpDiff < 0 ? 'text-loss' : 'text-white'
    }`}
  >
    {lpDiff}
  </div>

  <!-- LP Diff -->
  <div class="col-span-1">
    <span class="text-win">{lpChange.win !== null ? `+${lpChange.win}` : '+?'}</span>
    {' / '}
    <span class="text-loss">{lpChange.loss !== null ? `-${lpChange.loss}` : '-?'}</span>
  </div>

  <!-- KDA -->
  <div class="col-span-1">
    {kda.toFixed(2)}
  </div>

  <!-- Win Rate -->
  <div class="col-span-3">
    <div class="flex items-center">
      <div class="py-0.3 bg-win rounded-l px-2 text-sm font-semibold" style="width: {winWidth}%;">
        {entry.league.wins}W
      </div>
      <div
        class="py-0.3 bg-loss mr-2 rounded-r px-2 text-right text-sm font-semibold"
        style="width: {lossWidth}%;"
      >
        {entry.league.losses}L
      </div>
      <div>{winRate.toFixed(1)}%</div>
    </div>
  </div>
</div>
