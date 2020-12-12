<script>
    import { link } from 'svelte-routing';
    import Snackbar from "smelte/src/components/Snackbar";
    import Button from 'smelte/src/components/Button';
    import TextField from 'smelte/src/components/TextField';
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';
    import { User, user } from '../../lib/user';

    let name = '';
    let password = '';
    let password2 = '';
    let showError = false;
    let error = null;

    function signupUser(e) {
        e.preventDefault();
        if (password !== password2) {
            error = new Error('Passwords do not match!');
            showError = true;
            return;
        }

        if ($user.name == null) {
            User.signup(name, password)
                .then(u => {
                    $user = u;
                    navigate('/');
                })
                .catch(e => {
                    error = e;
                    showError = true;
                })
        } else {
            navigate('/');
        }
    }

    onMount(() => {
        if (user.name != null) {
            navigate('/');
        }
    })
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
    <h4>Sign up</h4>
    <form on:submit={signupUser} target="/" class="mb-4">
        <TextField bind:value={name} dense label="Name"/>
        <TextField bind:value={password} type="password" dense label="Password"/>
        <TextField bind:value={password2} type="password" 
            dense label="Confirm password"/>
        <Button block>Sign up</Button>
    </form>
    <p>
        Or
        <a use:link href="/login" class="hover:underline text-secondary-300">flex in</a>
        if you are flexxxing already...
    </p>
</div>
