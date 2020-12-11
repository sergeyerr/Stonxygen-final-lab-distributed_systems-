<script>
    import Stock from "../../lib/stock.js";
    import ProgressCircular from 'smelte/src/components/ProgressCircular';
    import Snackbar from "smelte/src/components/Snackbar";
    import { user } from "../../lib/user.js";
    import { navigate, link } from "svelte-routing";
    import List from "smelte/src/components/List";
    import Button from "smelte/src/components/Button";
    import Icon from "smelte/src/components/Icon";
    import { onMount } from "svelte";
    import { fade } from 'svelte/transition';

    let items = [];
    let itemsPromise = null;
    let showErrorMessage = false;
    let error = null;

    function grabStock(stock) {
        if ($user.name != null) {
            $user.buyStock(stock)
                .then(() => {
                    $user = $user;
                })
                .catch(e => {
                    error = e;
                    showErrorMessage = true;
                })
            return true;
        } else {
            navigate('/signup');
            return false;
        }
    }

    function reloadStocks() {
        itemsPromise = Stock.allAvailable()
            .then(stocks => {
                items = stocks.map(s => ({
                    icon: "work",
                    stock: s
                }));
            })
    }
    
    onMount(() => {
        reloadStocks();
    })
</script>

<Snackbar color="alert" top bind:value={showErrorMessage}>
    <p>
        {error.message}
        {#if error.code != null}
            {error.code}
        {/if}
    </p>
</Snackbar>

<div class="flex flex-col m-auto w-1/2">
    <div class="text-center">
        <h3>Stonks</h3>
        <p>Below are all the <i>stonks</i> available for selection...</p>
    </div>

    {#await itemsPromise}
        <div class="mx-auto"><ProgressCircular/></div>
    {:then}
        <div in:fade class="flex flex-col">
            <List {items}>
                <li slot="item" let:item>
                    <div
                        class="cursor-pointer p-4 flex justify-between
                            items-center hover:bg-gray-200">
                        <div>
                            <Icon class="mr-4">work</Icon>
                            <div>{item.stock.code}</div>
                        </div>
                        <div class="my-auto">{item.stock.organization}</div>
    
                        <div class="flex items-center">
                            {#if !$user.selectedStocks.map((s) => s.code).includes(item.stock.code)}
                                <Button
                                    small flat outlined
                                    add="w-32 h-8"
                                    on:click={grabStock(item.stock)}>
                                    ${item.stock.price}
                                </Button>
                            {:else}
                                <Button small flat outlined add="w-32"
                                on:click={() => navigate("/suitcase")}>
                                    View in Suitcase
                                </Button>
                            {/if}
                        </div>
                    </div>
                </li>
            </List>
        </div>
    {:catch error}
        <p in:fade class="mx-auto mb-4">
            No actual <i>stonks</i>, just an error message:
            "{error.message}"
        </p>
        <div in:fade class="w-64 mx-auto">
            <Button block on:click={reloadStocks}>Retry</Button>
        </div>
    {/await}
</div>
