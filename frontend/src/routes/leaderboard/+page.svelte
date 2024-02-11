<script lang="ts">
    import type { PageData } from './$types';
    import DataTable from "./data-table.svelte";
    import * as Tabs from "$lib/components/ui/tabs";
    import type { Summoner } from "$lib/types";

    export let data: PageData;

    const summoners: Summoner[] = data.props.summoners;
    // backend should be Runeterra_Terrain_map.webp
</script>


<div class="leaderboard-root container mx-auto py-10">
    <Tabs.Root value="solo">
        <Tabs.List class="flex">
            <Tabs.Trigger class="flex-1 justify-center" value="solo">Solo</Tabs.Trigger>
            <Tabs.Trigger class="flex-1 justify-center" value="flex">Flex</Tabs.Trigger>
        </Tabs.List>
        <Tabs.Content value="solo">
            <DataTable leagueId="420" data={summoners}/>
        </Tabs.Content>
        <Tabs.Content value="flex">
            <DataTable leagueId="440" data={summoners}/>
        </Tabs.Content>
    </Tabs.Root>
</div>