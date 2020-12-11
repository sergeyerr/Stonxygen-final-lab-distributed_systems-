<script>
    import { link } from 'svelte-routing';
    import Snackbar from 'smelte/src/components/Snackbar';
    import Button from 'smelte/src/components/Button';
    import TextField from 'smelte/src/components/TextField';
    import { onMount } from 'svelte';
    import { navigate } from 'svelte-routing';
    import { User, user } from '../../lib/user';

    let name = '';
    let password = '';
    let passwordConfirmation = '';
    let showErrorMessage = false;
    let errorMessage = '';

    function signupUser(e) {
        e.preventDefault();
        if ($user.name == null) {
            User.signup(name, password)
                .then(u => {
                    $user = u;
                    navigate('/');
                })
                .catch(error => {
                    errorMessage = error.message;
                    showErrorMessage = true;
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

<div class="m-auto w-1/3">
    <h4>Sign up</h4>
    <form on:submit={signupUser} class="mb-4">
        <TextField bind:value={name} dense label="Name"/>
        <TextField bind:value={password} dense label="Password"/>
        <TextField bind:value={passwordConfirmation} dense label="Confirm password"/>
        <Button block>Sign up</Button>
    </form>
    <p>
        Or
        <a use:link href="/login" class="hover:underline text-secondary-300">flex in</a>
        if you are flexxxing already...
    </p>
    <Snackbar color="alert" top bind:value={showErrorMessage}>
        <p>{errorMessage}</p>
    </Snackbar>
</div>
