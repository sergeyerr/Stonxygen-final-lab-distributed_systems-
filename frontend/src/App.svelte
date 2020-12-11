<script>
	import { userPromise } from "../lib/user";
	import { fade } from 'svelte/transition';
	import Loading from './views/Loading.svelte';
	import Header from "./Header.svelte";
	import Suitcase from "./views/Suitcase.svelte";
	import Stocks from "./views/Stocks.svelte";
	import Main from "./views/Main.svelte";
	import News from "./views/News.svelte";
	import Login from "./views/Login.svelte";
	import Signup from "./views/Signup.svelte";
	import About from "./views/About.svelte";
	import Footer from "./Footer.svelte";
	import { Router, Route } from "svelte-routing";
</script>

<main class="flex min-h-screen">
	{#await userPromise}
		<Loading/>
	{:then}
		<div in:fade class="flex flex-col flex-grow">
			<div class="mb-8"><Header/></div>
			<div class="container flex flex-grow mx-auto mb-8">
				<Router>
					<Route path="/news">
						<News />
					</Route>
					<Route path="/suitcase">
						<Suitcase/>
					</Route>
					<Route path="/stocks">
						<Stocks/>
					</Route>
					<Route path="/login">
						<Login/>
					</Route>
					<Route path="/signup">
						<Signup/>
					</Route>
					<Route path="/about">
						<About/>
					</Route>
					<Route path="/">
						<Main />
					</Route>
				</Router>
			</div>
			<Footer />
		</div>
	{:catch error}
		<div class="m-auto text-center">
			<h3>{error.message}</h3>
			{#if error.code != null}
				<h4>{error.code}</h4>
			{/if}
		</div>
	{/await}
</main>
