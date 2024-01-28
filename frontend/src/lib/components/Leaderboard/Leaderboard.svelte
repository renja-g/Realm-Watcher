<script>
    import { onMount } from 'svelte';

    let page = "flex";
    let summoners = [];
    let isLoading = false;

    onMount(async () => {
        await showLeaderboard('solo');
    });

    async function fetchData(sortBy) {
        isLoading = true;
        const response = await fetch(`https://lb-api.renja.dev/summoners?sort_by=${sortBy}`);
        const data = await response.json();
        isLoading = false;
        return data;
    }

    async function showLeaderboard(queueType) {
        if (page === queueType) return;
        page = queueType;
        summoners = await fetchData(queueType);
    }

    async function showSolo() {
        await showLeaderboard("solo");
    }

    async function showFlex() {
        await showLeaderboard("flex");
    }

    function getQueueData(summoner, queueType) {
        const queueId = queueType === "solo" ? "420" : "440";
        return summoner.leagueEntries[queueId];
    }

    function getIconUrl(summoner) {
        return `https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/${summoner.profileIconId}.jpg`;
    }

    function getTierUrl(queueData) {
        return `https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-mini-crests/${queueData.tier.toLowerCase()}.svg`;
    }

    function calculateWinRate(queueData) {
        return ((queueData.wins / (queueData.wins + queueData.losses) * 100).toFixed(0)) + '%';
    }

    function getDisplayName(summoner, queueData) {
        return summoner.gameName + (queueData.hotStreak ? " 🔥" : "");
    }

    function getUGG(summoner) {
        return `https://u.gg/lol/profile/${summoner.platform}/${summoner.gameName}-${summoner.tagLine}`;
    }

    function getOPGG(summoner) {
        return `https://op.gg/summoners/${summoner.platform}/${summoner.gameName}-${summoner.tagLine}`;
    }
</script>

<div class="leaderboard-container">
    <div class="button-container">
        <button on:click={showSolo}>Show Solo</button>
        <button on:click={showFlex}>Show Flex</button>
    </div>
    {#if isLoading}
        <p></p> <!-- Loading indicator -->
    {:else}
        <table>
            <tr>
                <th>Summoner</th>
                <th>Tier</th>
                <th>Rank</th>
                <th>LP</th>
                <th>Matches</th>
                <th>Winrate</th>
            </tr>
            {#each summoners as summoner}
                {#if getQueueData(summoner, page)}
                    <tr>
                        <td>
                            <a class="name" href={getUGG(summoner)} target="_blank">
                                <img src={getIconUrl(summoner)} alt="Icon" class="icon-img">
                                {getDisplayName(summoner, getQueueData(summoner, page))}
                            </a>
                        </td>
                        <td>
                            <img src={getTierUrl(getQueueData(summoner, page))} alt="Icon" class="icon-img">
                        </td>
                        <td>{getQueueData(summoner, page).rank}</td>
                        <td>{getQueueData(summoner, page).leaguePoints}</td>
                        <td>{getQueueData(summoner, page).wins + getQueueData(summoner, page).losses}</td>
                        <td>{calculateWinRate(getQueueData(summoner, page))}</td>
                    </tr>
                {/if}
            {/each}
        </table>
    {/if}
</div>

<style>
    :root {
        --background-color: #0e0e10;
        --text-color: #DDEEF2;
        --main-font: 'Roboto', sans-serif;
        --border-color: rgba(0, 0, 0, 0.5);
        --box-background: rgb(0, 0, 0, 0.2);
        --container-background: rgb(0, 0, 0, 0);
    }

    .leaderboard-container {
        width: 80%;
        margin: 20px auto;
        background: var(--container-background);
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px var(--border-color);
        color: var(--text-color);
        font-family: var(--main-font);
        font-size: 30px;
    }

    .button-container {
        text-align: center;
        margin-bottom: 20px;
    }

    .button-container button {
        padding: 10px 20px;
        cursor: pointer;
        background-color: rgba(0, 0, 0, 0.7);
        color: var(--text-color);
        border: none;
        border-radius: 8px;
        font-size: 30px;
        font-weight: bold;
        margin: 0 10px;
        transition: background-color 0.3s;
    }

    .button-container button:hover {
        background-color: rgba(0, 0, 0, 0.2);
    }

    table {
        width: 100%;
        border-collapse: collapse;
        color: var(--text-color);
    }

    th, td {
        text-align: left;
        padding: 12px;
        border: 1px solid var(--border-color);
        border-right: 0;
        border-left: 0;
        background: var(--box-background);
    }

    th {
        background-color: rgb(0, 0, 0, 0.6);
    }

    tr:nth-child(even) {
        background-color: rgb(0, 0, 0, 0.3);
    }

    .icon-img {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin-right: 10px;
        vertical-align: middle;
    }

    .name {
        color: var(--text-color);
        text-decoration: none;
        transition: color 0.3s;
        margin-left: 10px;
    }

    .name:hover {
        color: rgba(255, 255, 255, 0.4);
    }
</style>
