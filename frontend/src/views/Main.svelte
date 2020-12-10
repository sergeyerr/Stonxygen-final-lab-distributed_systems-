<script>
    import { links } from 'svelte-routing';
</script>


<div class="flex m-auto justify-between w-1/2">
    <div class="bg-face bg-center bg-contain bg-no-repeat w-64 h-64"></div>
    <div class="flex flex-col items-end">
        <h2>Flexing away...</h2>
        <ul use:links class="text-lg">
            <li><a href="/stocks" class="hover:underline">stonks</a></li>
            <li><a href="/news" class="hover:underline">news</a></li>
            <li><a href="/about" class="hover:underline">about</a></li>
        </ul>
    </div>
</div>
