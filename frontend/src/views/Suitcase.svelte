<script>
    import { link, navigate } from "svelte-routing";
    import Card from "smelte/src/components/Card";
    import Button from "smelte/src/components/Button";
    import Snackbar from "smelte/src/components/Snackbar";
    import { flip } from 'svelte/animate';
    import { onMount } from "svelte";
    import { user } from "../../lib/user.js";
    import { writable } from 'svelte/store';

    let showErrorMessage = false;
    let error = null;

    let knownStatistics = writable({});

    function sellStock(item) {
        $user.sellStock(item)
            .then(() => $user = $user)
            .catch(e => {
                error = e;
                showErrorMessage = true;
            })
    }

    function fetchStatistic(item) {
        if ($knownStatistics[item.code] != '...') {
            $knownStatistics[item.code] = '...';
            item.statistic()
                .then(response => {
                    s = parseFloat(response.statistic).toFixed(2)
                    $knownStatistics[item.code] = s;
                })
                .catch(e => {
                    $knownStatistics[item.code] = '?';
                    error = e;
                    showErrorMessage = true;
                })
        }
    }

    $: sortedStocks = (stocks =>
        stocks
            .slice()
            .sort((sA, sB) => sA.name <= sB.name ? -1 : 0)
    )($user.selectedStocks);

    onMount(() => {
        if ($user.name == null) {
            navigate("/signup");
        }
    });
</script>

<Snackbar color="alert" top bind:value={showErrorMessage}>
    <p>
        {error.message}
        {#if error.code != null}
            {error.code}
        {/if}
    </p>
</Snackbar>

<div class="flex mx-auto flex-col items-center">
    <h3 class="mx-auto">Suitcase</h3>
    <p class="mb-4">The <i>stonks</i> you bought end up here...</p>
    {#if $user.selectedStocks.length == 0}
        <div class="flex flex-col m-auto items-center">
            <div class="bg-orang bg-contain bg-center bg-no-repeat h-64 w-64" />
            <p>It appears yout suitcase is empty...</p>
            <p>
                You can buy some
                <i>stonks</i>
                over in the
                <a
                    use:link
                    class="text-secondary-300 hover:underline"
                    href="/stocks">
                    stonks
                </a>
                section!
            </p>
        </div>
    {:else}
        <div class="flex flex-wrap mx-32 justify-center my-auto">
            {#each sortedStocks as item (item.code)}
                <div animate:flip={{duration: 300}} on:mouseenter={fetchStatistic(item)}>
                    <Card.Card class="mb-4 mr-4">
                        <div slot="title">
                            <Card.Title title={item.code} subheader={item.organization}/>
                        </div>
                        <div slot="text" class="px-4 pb-0 pt-0 text-right">
                            <span class="mr-8">${item.price}</span>
                            <span>VAR
                                {#if $knownStatistics[item.code] == null}
                                    ?
                                {:else}
                                    {$knownStatistics[item.code]}
                                {/if}
                            </span>
                        </div>
                        <div slot="actions" class="flex justify-center">
                            <div class="p-2">
                                <Button
                                    text
                                    on:click={sellStock(item)}
                                    add="text-secondary-300">
                                    Sell
                                </Button>
                            </div>
                        </div>
                    </Card.Card>
                </div>
            {/each}
        </div>
        <p>Buy more
            <a use:link href="/stocks" class="hover:underline text-secondary-300">
                stonks
            </a>
        </p>
    {/if}
</div>
