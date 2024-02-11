<script lang="ts">
    export let tier: string;
    let lowerCaseTier: string;
    $: lowerCaseTier = tier.toLowerCase();
</script>

{#if tier}
    <div class="flex w-[100px] items-center">
        <img src={`https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-mini-crests/${lowerCaseTier}.svg`} alt={tier.toUpperCase()} class="mr-2 h-7 w-7 text-muted-foreground" />
    </div>
{/if}