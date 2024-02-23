<script lang="ts">
    import { createTable, Render, Subscribe, createRender } from "svelte-headless-table";
    import {
        addHiddenColumns,
        addPagination,
        addSelectedRows,
        addSortBy,
        addTableFilter,
    } from "svelte-headless-table/plugins";
    import { readable } from "svelte/store";
    import * as Table from "$lib/components/ui/table";
    import { Button } from "$lib/components/ui/button";
    import type { Summoner } from "$lib/types";
    import DataTableColumnHeader from "./data-table-column-header.svelte";
    import DataTableSummonerCell from "./data-table-summoner-cell.svelte";
    import DataTableTierCell from "./data-table-tier-cell.svelte";
    import DataTablePagination from "./data-table-pagination.svelte";
    import DataTableRowActions from "./data-table-row-actions.svelte";


    export let leagueId: "420" | "440" = "420";
    export let data: Summoner[]

    // drop all summoners that are not in the league
    data = data.filter((summoner) => summoner.leagueEntries[leagueId]);

    // sort the summoners by their league
    // Tier > Rank > LP
    const tierOrder = {
    CHALLENGER: 1,
    GRANDMASTER: 2,
    MASTER: 3,
    DIAMOND: 4,
    EMERALD: 5,
    PLATINUM: 6,
    GOLD: 7,
    SILVER: 8,
    BRONZE: 9,
    IRON: 10,
    };

    const rankOrder = {
        I: 1,
        II: 2,
        III: 3,
        IV: 4,
    };

    data.sort((a, b) => {
        const aEntry = a.leagueEntries[leagueId];
        const bEntry = b.leagueEntries[leagueId];

        if (!aEntry || !bEntry) {
            return 0;
        }

        // sort by tier
        const aTierValue = tierOrder[aEntry.tier as keyof typeof tierOrder] || 0;
        const bTierValue = tierOrder[bEntry.tier as keyof typeof tierOrder] || 0;
        if (aTierValue !== bTierValue) {
            return aTierValue - bTierValue;
        }

        // sort by rank
        const aRankValue = rankOrder[aEntry.rank as keyof typeof rankOrder] || 0;
        const bRankValue = rankOrder[bEntry.rank as keyof typeof rankOrder] || 0;
        if (aRankValue !== bRankValue) {
            return aRankValue - bRankValue;
        }

        // sort by LP
        return bEntry.leaguePoints - aEntry.leaguePoints;
    });
    console.log(data);

    const table = createTable(readable(data), {
        select: addSelectedRows(),
        page: addPagination({
            initialPageSize: 10,
        }),
        sort: addSortBy({
            toggleOrder: ["asc", "desc", undefined],
        }),
        filter: addTableFilter({
            fn: ({ filterValue, value }) => {
                return value.toLowerCase().includes(filterValue.toLowerCase());
            },
        }),
        hide: addHiddenColumns(),
    });

    const isAdmin = true;

    const columns = table.createColumns([
        table.column({
            accessor: (row: Summoner) => {
                return {
                    iconId: row.profileIconId,
                    gameName: row.gameName,
                    tagLine: row.tagLine,
                    platform: row.platform,
                };
            },
            header: "Summoner",
            cell: ({ value }) => {
                return createRender(DataTableSummonerCell, {
                    iconId: value.iconId,
                    gameName: value.gameName,
                    tagLine: value.tagLine,
                    platform: value.platform,
                });
            },
            plugins: {
                sort: {
                    disable: true,
                },
            },
        }),
        table.column({
            accessor: (row: Summoner) => row.leagueEntries[leagueId]?.tier ?? "Unranked",
            header: "Tier",
            cell: ({ value }) => {
                return createRender(DataTableTierCell, { tier: value });
            },
            plugins: {
                sort: {
                    disable: true,
                },
            },
        }),
        table.column({
            accessor: (row: Summoner) => row.leagueEntries[leagueId]?.rank ?? "Unranked",
            header: "Rank",
            plugins: {
                sort: {
                    disable: true,
                },
            },
        }),
        table.column({
            accessor: (row: Summoner) => row.leagueEntries[leagueId]?.leaguePoints ?? "Unranked",
            header: "LP",
            plugins: {
                sort: {
                    disable: true,
                },
            },
        }),
        table.column({
            accessor: (row: Summoner) => {
                const wins = row.leagueEntries[leagueId]?.wins ?? 0;
                const losses = row.leagueEntries[leagueId]?.losses ?? 0;
                return wins + losses;
            },
            header: "Matches",
        }),
        table.column({
            accessor: (row: Summoner) => {
                const wins = row.leagueEntries[leagueId]?.wins ?? 0;
                const losses = row.leagueEntries[leagueId]?.losses ?? 0;
                const totalMatches = wins + losses;
                const winrate = totalMatches > 0 ? ((wins / totalMatches) * 100).toFixed(2) + '%' : "N/A";
                return winrate;
            },
            header: "Winrate"
        }),
        table.display({
            id: "actions",
            header: () => {
                return "";
            },
            cell: ({ row }) => {
                if (row.isData() && row.original) {
                    return createRender(DataTableRowActions, {
                        row: row.original,
                    });
                }
                return "";
            },
        }),
    ].filter(Boolean));

    const tableModel = table.createViewModel(columns);
    const { headerRows, pageRows, tableAttrs, tableBodyAttrs } = tableModel;

    const sortables = ["Matches", "Winrate"]
</script>


<div>
    <div class="rounded-md border">
        <Table.Root class="text-xl" {...$tableAttrs}>
            <Table.Header class="">
                {#each $headerRows as headerRow}
                <Subscribe rowAttrs="{headerRow.attrs()}">
                    <Table.Row>
                        {#each headerRow.cells as cell (cell.id)}
                        <Subscribe
                            attrs="{cell.attrs()}"
                            let:attrs
                            props="{cell.props()}"
                            let:props
                            >
                            <Table.Head {...attrs}>
                                {#if sortables.includes(cell.id)}
                                    <DataTableColumnHeader {props}
                                        ><Render
                                            of={cell.render()}
                                    /></DataTableColumnHeader
                                    >
                                {:else}
                                    <Render of="{cell.render()}" />
                                {/if}
                            </Table.Head>
                        </Subscribe>
                        {/each}
                    </Table.Row>
                </Subscribe>
                {/each}
            </Table.Header>
            <Table.Body {...$tableBodyAttrs}>
                {#each $pageRows as row (row.id)}
                <Subscribe rowAttrs="{row.attrs()}" let:rowAttrs>
                    <Table.Row {...rowAttrs}>
                        {#each row.cells as cell (cell.id)}
                        <Subscribe attrs="{cell.attrs()}" let:attrs>
                            <Table.Cell {...attrs}>
                                <Render of="{cell.render()}" />
                            </Table.Cell>
                        </Subscribe>
                        {/each}
                    </Table.Row>
                </Subscribe>
                {/each}
            </Table.Body>
        </Table.Root>
    </div>
    <DataTablePagination {tableModel}/>
</div>