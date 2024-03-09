<script lang="ts">
    import { MoreHorizontal } from 'lucide-svelte';
    import { Button } from "$lib/components/ui/button";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    import { summonerSchema, type Summoner } from "$lib/schemas";

    export let row: Summoner;
<<<<<<< HEAD
    const task = summonerSchema.parse(row);
</script>

<DropdownMenu.Root>
    <DropdownMenu.Trigger asChild let:builder>
        <Button
            variant="ghost"
            builders={[builder]}
            class="flex h-8 w-8 p-0 data-[state=open]:bg-muted"
        >
            <MoreHorizontal class="h-4 w-4" />
            <span class="sr-only">Open menu</span>
        </Button>
    </DropdownMenu.Trigger>
    <DropdownMenu.Content class="w-[160px]" align="end">
        <DropdownMenu.Item>Delete</DropdownMenu.Item>
    </DropdownMenu.Content>
</DropdownMenu.Root>
=======
    const summoner = summonerSchema.parse(row);

    let form: HTMLFormElement;

    function handleSubmit() {
        form.submit();
    }
</script>

<form id="myForm" method="POST" bind:this={form}>
    <input type="hidden" name="puuid" value={summoner.puuid} />
    <DropdownMenu.Root>
        <DropdownMenu.Trigger asChild let:builder>
            <Button
                variant="ghost"
                builders={[builder]}
                class="flex h-8 w-8 p-0 data-[state=open]:bg-muted"
            >
                <MoreHorizontal class="h-4 w-4" />
                <span class="sr-only">Open menu</span>
            </Button>
        </DropdownMenu.Trigger>
        <DropdownMenu.Content class="w-[160px]" align="end">
            <DropdownMenu.Item on:click={handleSubmit}>Delete</DropdownMenu.Item>
        </DropdownMenu.Content>
    </DropdownMenu.Root>
</form>
>>>>>>> ce910cf1fbe58f1f86ae36ea5afb0130e64d8f56
