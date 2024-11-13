<script lang="ts">
  const { rows = 10 } = $props();
</script>

{#each Array(rows) as _}
  <div class="grid grid-cols-12 items-center border-t border-gray-800 px-6 py-4">
    <!-- Rank Number -->
    <div class="col-span-1">
      <div class="h-5 w-5 rounded bg-slate-700"></div>
    </div>

    <!-- Profile -->
    <div class="col-span-2 flex items-center">
      <div class="mr-4 h-11 w-11 rounded-full bg-slate-700"></div>
      <div class="flex flex-col gap-1.5">
        <div class="h-5 w-24 rounded bg-slate-700"></div>
        <div class="h-4 w-12 rounded bg-slate-700"></div>
      </div>
    </div>

    <!-- Rank -->
    <div class="col-span-2 flex items-center justify-center">
      <div class="mr-2 h-8 w-8 rounded bg-slate-700"></div>
      <div class="h-5 w-24 rounded bg-slate-700"></div>
    </div>

    <!-- LP +/- -->
    <div class="col-span-2 flex justify-center">
      <div class="h-5 w-16 rounded bg-slate-700"></div>
    </div>

    <!-- LP Diff -->
    <div class="col-span-2 flex justify-center">
      <div class="h-5 w-8 rounded bg-slate-700"></div>
    </div>

    <!-- KDA -->
    <div class="col-span-1 flex justify-center">
      <div class="h-5 w-12 rounded bg-slate-700"></div>
    </div>

    <!-- Win Rate -->
    <div class="col-span-2 flex justify-center">
      <div class="flex items-center gap-1">
        <div class="h-7 w-44 rounded bg-slate-700"></div>
        <div class="ml-2 h-5 w-12 rounded bg-slate-700"></div>
      </div>
    </div>
  </div>
{/each}
