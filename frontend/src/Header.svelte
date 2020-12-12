<script>
    import { links } from 'svelte-routing';
    import { user } from '../lib/user.js';

    console.debug('App started!');
</script>

<div class="flex px-8 items-center">
    <nav class="flex justify-between w-1/5" use:links>
        <a href="/stocks" class="my-auto hover:underline">stonks</a>
        <a href="/news" class="my-auto hover:underline">news</a>
        <a href="/about" class="my-auto hover:underline">about</a>
    </nav>
    <div class="flex text-center w-3/5" use:links>
        <a href="." class="bg-blue-500 text-white rounded-b-2xl mx-auto px-32">
            <h4>Stonxygen</h4>
        </a>
    </div>
    <div class="flex justify-end w-1/5" use:links>
        <div class="flex items-center">
            {#if $user.name == null}
                <a href="/login" class="hover:underline mr-8">flex in</a>
                <a href="/signup" class="hover:underline">flex up</a>
            {:else}
                <a on:click={() => { $user = $user.logout() }}
                    href="/" class="hover:underline mr-4">
                    flex out
                </a>
                <a href="/suitcase" class="hover:underline mr-2">{$user.name}</a>
                <div class="w-8 h-8 rounded-full bg-face bg-contain bg-center"/>
            {/if}
        </div>
    </div>
</div>
