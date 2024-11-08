<script lang="ts">
  import type { LeaderboardEntry } from '$lib/types/types';

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


  // Random Sample Data -53 - - 54
  const lpChange = Math.floor(Math.random() * 107) - 54;

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
  <div class="col-span-3 flex items-center">
    <img class="mr-4 h-11 w-11 rounded-full" src={iconUrl} alt="Profile Icon" />
    <div class="flex flex-col">
      <a  href={opggUrl}  target="_blank" rel="noopener noreferrer" class="font-semibold hover:underline">
        {entry.summoner.gameName}
      </a>
      <span class="text-sm text-gray-400">#{entry.summoner.tagLine}</span>
    </div>
  </div>

  <!-- Rank -->
  <div class="col-span-3 flex items-center">
    <img class="mr-2 h-8 w-8" src={tierIconUrl} alt="Rank Icon" />
    <span class=" mr-2">{entry.league.tier}</span>
    <span class=" mr-2">{entry.league.rank}</span>
    <span class="text-gray-400">{entry.league.leaguePoints}</span>
  </div>

  <!-- Last 5 Games -->
  <div class={`col-span-2 font-semibold ${lpChange >= 0 ? 'text-green-500' : 'text-red-500'}`}>
    {lpChange}
  </div>

  <!-- Win Rate -->
  <div class="col-span-3">
    <div class="flex items-center">
      <div
        class="rounded-l bg-blue-500 px-2 py-1 text-sm font-semibold"
        style="width: {winWidth}%;"
      >
        {entry.league.wins}W
      </div>
      <div
        class="mr-2 rounded-r bg-red-500 px-2 py-1 text-right text-sm font-semibold"
        style="width: {lossWidth}%;"
      >
        {entry.league.losses}L
      </div>
      <div>{winRate.toFixed(1)}%</div>
    </div>
  </div>
</div>
