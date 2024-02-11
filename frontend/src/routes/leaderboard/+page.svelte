<svelte:window bind:innerWidth bind:innerHeight />

<script lang="ts">
    import type { PageData } from './$types';
    import DataTable from "./data-table.svelte";
    import * as Tabs from "$lib/components/ui/tabs";
    import type { Summoner } from "$lib/types";
    import RuneterraTerrainMap from "$lib/assets/Runeterra_Terrain_map.webp";
    import { onMount } from 'svelte';

    let isLoading = true;

    onMount(() => {
        isLoading = false;
    });

    export let data: PageData;
    const summoners: Summoner[] = data.props.summoners;

    const backgroundImage = `url(${RuneterraTerrainMap})`;

    let selectedTab = 'solo';

    const imgDimensions = { x: 2048, y: 2048 };
    const imgCenterSolo = { x: 810, y: 860 };
    const imgCenterFlex = { x: 1140, y: 1360 };
    // const imgCenterFlex = { x: 1110, y: 860 };

    const zoomFactor = 1.2;
    $: backgroundSize = `${imgDimensions.x * zoomFactor}px ${imgDimensions.y * zoomFactor}px`;

    $: innerWidth = 1920
    $: innerHeight = 953

    $: offsetX = selectedTab === 'solo' ? (innerWidth / 2) - imgCenterSolo.x * zoomFactor : (innerWidth / 2) - imgCenterFlex.x * zoomFactor;
    $: offsetY = selectedTab === 'solo' ? (innerHeight / 2) - imgCenterSolo.y * zoomFactor : (innerHeight / 2) - imgCenterFlex.y * zoomFactor;

    $: backgroundPosition = `${offsetX}px ${offsetY}px`;
</script>



<div
    class="w-screen h-screen bg-no-repeat {isLoading ? '' : 'background-transition'}"
    style="background-image: {backgroundImage}; background-position: {backgroundPosition}; background-size: {backgroundSize};"
>
    <div class="container py-10 rounded bg-background/15">
        <Tabs.Root bind:value={selectedTab}>
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
</div>

<style>
    .background-transition {
        transition: background-position 2s ease, background-size 2s ease;
    }
</style>