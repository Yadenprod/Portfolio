<template>
	<div class="centerblock">
		<main v-if="loaded && pageData"  id="main" class="site-main" role="main">
			<h3 v-html="pageData.pageTitle"></h3>
			<p v-html="pageData.content"></p>
		</main>
	</div>
</template>
<script>
	export default {
		data: () => ({
				loaded: false
			}),
		props: {
			pageData: {},
		},
		mounted() {
			Utils.setTitle(this.pageData.title);
			this.loaded = true;
		},
		watch: {
			$route(to, from) {
				Utils.setTitle(this.pageData.title);
			}

		}
	}
</script>