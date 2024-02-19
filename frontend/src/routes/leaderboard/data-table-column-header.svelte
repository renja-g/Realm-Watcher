<script lang="ts">
    import { MoveDown, MoveUp, ArrowUpDown } from 'lucide-svelte';
    import { cn } from "$lib/utils";
    import { Button } from "$lib/components/ui/button";

    let className: string | undefined | null = undefined;
    export { className as class };
    export let props: {
        select: never;
        sort: {
            order: "desc" | "asc" | undefined;
            toggle: (event: Event) => void;
            disabled: boolean;
        };
        filter: never;
    };
</script>

{#if !props.sort.disabled}
    <div class={cn("flex items-center", className)}>
        <Button
            variant="ghost"
            class="-ml-3 text-xl data:[props.sort.order]:bg-accent"
            on:click={props.sort.toggle}
        >
            <slot />
            {#if props.sort.order === "desc"}
                <MoveDown class="ml-2 h-6 w-6" />
            {:else if props.sort.order === "asc"}
                <MoveUp class="ml-2 h-6 w-6" />
            {:else}
                <ArrowUpDown class="ml-2 h-6 w-6" />
            {/if}
        </Button>
    </div>
{:else}
    <slot />
{/if}