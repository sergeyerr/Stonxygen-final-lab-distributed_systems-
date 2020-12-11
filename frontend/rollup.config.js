import svelte from 'rollup-plugin-svelte';
import commonjs from '@rollup/plugin-commonjs';
import resolve from '@rollup/plugin-node-resolve';
// import livereload from 'rollup-plugin-livereload';
import { terser } from 'rollup-plugin-terser';
import dev from 'rollup-plugin-dev'

const smelte = require("smelte/rollup-plugin-smelte");

const production = !process.env.ROLLUP_WATCH;

export default {
	input: 'src/main.js',
	output: {
		sourcemap: true,
		format: 'iife',
		name: 'app',
		file: 'public/build/bundle.js'
	},
	plugins: [
		svelte({
			compilerOptions: {
				// enable run-time checks when not in production
				dev: !production
			},
		}),

		smelte({
			purge: production,
			output: "public/build/global.css",
			postcss: [], // Your PostCSS plugins
			whitelist: [], // Array of classnames whitelisted from purging
			whitelistPatterns: [], // Same as above, but list of regexes
			tailwind: {
				theme: {
					extend: {
						backgroundImage: theme => ({
							'face': "url('../images/meme-man.png')",
							'tom': "url('../images/ching-chang-tom.gif')",
							'cubes': "url('../images/cubes.jpg')",
							'doge': "url('../images/doge.png')",
							'bounce': "url('../images/bounce.gif')",
							'orang': "url('../images/orang.png')"
						})
					}
				},
			},
		}),

		// If you have external dependencies installed from
		// npm, you'll most likely need these plugins. In
		// some cases you'll need additional configuration -
		// consult the documentation for details:
		// https://github.com/rollup/plugins/tree/master/packages/commonjs
		resolve({
			browser: true,
			dedupe: ['svelte']
		}),

		commonjs(),

		!production && dev({
			dirs: ['public'],
			proxy: { '/api/*': 'localhost:4567' },
			spa: 'public/index.html',
			port: 3000
		}),

		// If we're building for production (npm run build
		// instead of npm run dev), minify
		production && terser(),	
	],

	watch: {
		clearScreen: false
	}
};
