<script lang="ts">
    import { CircleHelp } from 'lucide-svelte';

    const { text, class: className } = $props<{ text: string; class?: string }>();
</script>

<div class="group relative inline-block">
    <CircleHelp class="{className} ml-1 cursor-help text-gray-400" />
    <div class="pointer-events-none absolute bottom-full left-1/2 mb-2 -translate-x-1/2 opacity-0 transition-opacity group-hover:opacity-100">
        <div class="whitespace-nowrap rounded bg-gray-800 px-2 py-1 text-sm text-white">
            {text}
            <!-- Arrow -->
            <div class="absolute left-1/2 top-full -translate-x-1/2 border-4 border-transparent border-t-gray-800"></div>
        </div>
    </div>
</div>