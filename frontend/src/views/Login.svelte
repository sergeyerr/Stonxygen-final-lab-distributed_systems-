<script>
    import { onMount } from "svelte";
    import { link, navigate } from "svelte-routing";
    import { User, user } from "../../lib/user.js";
    import TextField from "smelte/src/components/TextField";
    import Snackbar from "smelte/src/components/Snackbar";
    import Button from "smelte/src/components/Button";

    onMount(() => {
        if ($user.login != null) {
            navigate("/");
        }
    });

    let name = "";
    let password = "";
    let showError = false;
    let error = null;

    function loginUser(e) {
        User.login(name, password)
            .then((u) => {
                $user = u;
                navigate("/");
            })
            .catch((e) => {
                error = e;
                showError = true;
            });
        e.preventDefault();
    }
</script>

<Snackbar color="alert" top value={showError}>
    {#if error != null}
        <p>
            {error.message}
            {#if error.code != null}
                {error.code}
            {/if}
        </p>
    {:else}
        <p>Actually everything seems fine</p>
    {/if}
</Snackbar>

<div class="m-auto w-1/3">
    <h4>Log in</h4>
    <form method="POST" on:submit={loginUser} class="mb-4">
        <TextField bind:value={name} dense label="Login" />
        <TextField
            bind:value={password}
            dense
            type="password"
            label="Password" />
        <Button type="submit" block>Log in</Button>
    </form>

    <p>
        Or
        <a
            use:link
            href="/signup"
            class="hover:underline text-secondary-300">flex up</a>
        to start flexing!
    </p>
</div>
