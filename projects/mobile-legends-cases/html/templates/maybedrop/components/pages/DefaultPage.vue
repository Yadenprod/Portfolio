<template>
	<div class="centerblock">
		<main v-if="loaded && pageData"  id="main" class="site-main" role="main">
			<h3 v-html="pageData.pageTitle"></h3>
			<p v-html="pageData.content"></p>
		</main>
		<page-404 v-if="loaded && !pageData"></page-404>
	</div>
</template>
<script>
	export default {
		data: () => ({
				pageData: false,
				loaded: false
			}),
		mounted() {
			this.getPageData();
		},
		methods: {
			getPageData() {
				this.pageData = false;
				this.loaded = false;
				Utils.apiPostCall("/api/page/", {
					url: this.$router.currentRoute.path
				})
						.then(resp => {
							this.loaded = true;
							if (resp.data.success) {
								this.pageData = resp.data.page;
								Utils.setTitle(this.pageData.title);
							} else {
								Utils.setTitle("Страница не найдена");
							}
						})
						.catch(err => {
							this.loaded = true;
							Utils.setTitle("Страница не найдена");
						});
			}
		},
		watch: {
			$route(to, from) {
				this.getPageData();
			}

		}
	}
</script>