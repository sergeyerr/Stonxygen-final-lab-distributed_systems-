<script>
    import { onMount } from 'svelte';
    import { link, navigate } from 'svelte-routing';
    import { User, user, userPromise } from '../../lib/user.js';
    import TextField from 'smelte/src/components/TextField';
    import Snackbar from 'smelte/src/components/Snackbar'
    import Button from 'smelte/src/components/Button';

    onMount(() => {
        if ($user.login != null) {
            navigate('/');
        }
    });

    let name = '';
    let password = '';
    let showErrorMessage = false;
    let error = null;

    function loginUser(e) {
        User.login(name, password)
            .then(u => {
                $user = u;
                navigate('/');
            })
            .catch(e => {
                error = e;
                showErrorMessage = true;
            });
        e.preventDefault();
    }
</script>

<Snackbar color="alert" top bind:value={showErrorMessage}>
    <p>
        {error.message}
        {#if error.code != null}
            {error.code}
        {/if}
    </p>
</Snackbar>

<div class="m-auto w-1/3">
    <h4>Log in</h4>
    <form method="POST" on:submit={loginUser} class="mb-4">
        
        <TextField bind:value={name} dense label="Login"/>
        <TextField bind:value={password} dense type="password"
            label="Password"/>
        <Button type="submit" block>Log in</Button>
    </form>

    <p>
        Or
        <a use:link href="/signup" class="hover:underline text-secondary-300">flex up</a>
        to start flexing!
    </p>
</div>
