<script lang="ts">
  import LeaderboardRow from '$lib/components/LeaderboardRow/LeaderboardRow.svelte';
  import LeaderboardSkeleton from '$lib/components/LeaderboardRow/LeaderboardSkeleton.svelte';
  import useFetchLeaderboard from '$lib/hooks/useFetchLeaderboard.svelte';
  import type { queueType } from '$lib/types/types';
  import { error } from '@sveltejs/kit';

  const tabs: { id: queueType; label: string }[] = [
    { id: 'RANKED_SOLO_5x5', label: 'RANKED SOLO/DUO' },
    { id: 'RANKED_FLEX_SR', label: 'RANKED FLEX 5v5' }
  ];

  let activeTab: queueType = $state('RANKED_SOLO_5x5');

  let entries = $derived(useFetchLeaderboard(activeTab));
</script>

<div class="min-h-screen bg-slate-900 px-20 py-8 text-white">
  <h1 class="mb-6 text-center text-4xl font-bold">Realm Watcher</h1>

  <!-- Tabs -->
  <div class="mb-1 flex justify-center border-b border-gray-700">
    {#each tabs as tab}
      <button
        class="relative px-8   py-2 {activeTab === tab.id
          ? 'text-white'
          : 'text-gray-400'} hover:text-white"
        onclick={() => (activeTab = tab.id)}
      >
        {tab.label}
        {#if activeTab === tab.id}
          <div class="absolute bottom-0 left-0 w-full">
            <div class="relative h-0.5 bg-blue-600">
              <div class="absolute inset-0 bg-blue-600 blur-sm"></div>
              <div class="bg-blue-5 00 absolute inset-0 opacity-50 blur-md"></div>
            </div>
          </div>
        {/if}
      </button>
    {/each}
  </div>

  <!-- Leaderboard Headers -->
  <div class="grid grid-cols-12 border-b-2 border-gray-700 px-6 py-2 text-sm text-gray-400">
    <div class="col-span-1">#</div>
    <div class="col-span-3">Profile</div>
    <div class="col-span-3">Rank</div>
    <div class="col-span-2">Last 5 Games</div>
    <div class="col-span-3">Win Rate</div>
  </div>

  <!-- Player Rows -->
  <div class="rounded-b-lg bg-slate-800">
    {#if entries.error}
      <div class="flex items-center justify-center py-10">
        <span class="text-red-500 text-lg">An error occurred while fetching the leaderboard. Please try again later.</span>
      </div>
    {:else if entries.isLoading}
      <LeaderboardSkeleton rows={10} />
    {:else}
      {#each entries.entries as entry, index}
        <LeaderboardRow {index} {entry} />
      {/each}
    {/if}
  </div>
</div>
