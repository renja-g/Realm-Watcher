<script lang="ts">
    export let iconId: number;
    export let gameName: string;
    export let tagLine: string;
    export let platform: string;

    function get_opgg_link(platform: string, gameName: string, tagLine: string) {
        return `https://www.op.gg/summoners/${platform}/${gameName}-${tagLine}`;
    }
</script>

{#if iconId || gameName && tagLine}
    <div class="flex items-center hover:underline">
        <a href={get_opgg_link(platform, gameName, tagLine)} target="_blank" class="flex items-center">
            {#if iconId}
                <img src={`https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/${iconId}.jpg`} alt="P" class="mr-2 h-7 w-7 text-muted-foreground rounded-lg" />
            {/if}
            {#if gameName && tagLine}
                <span class="whitespace-nowrap">{gameName}#{tagLine}</span>
            {/if}
        </a>
    </div>
{/if}    