import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
	plugins: [sveltekit()],
	preview: {allowedHosts: ["ebisu.cc.gatech.edu"]},

	test: {
		include: ['src/**/*.{test,spec}.{js,ts}']
	}
});
