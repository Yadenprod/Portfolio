<template>
	<div class="centerblock">
		<main v-if="trades" id="main" class="site-main" role="main">
			<h1><span></span>Live-трейды<span></span></h1>
			<div class="trades_list">
				<table class="table_list" style="border-collapse: collapse; width: 100%;">
					<thead>
						<tr>
							<td class="table_user">Пользователь</td>
							<td class="table_item">Предмет</td>
							<td class="table_time">Время</td>
						</tr>
					</thead>
					<tbody>
						<tr v-for="item in trades">
							<td class="table_user">
					<router-link class="user_avatar" :to="'/profile/'+item.user.steamId+'/'">
								 <img :src="item.user.image" :alt="item.user.name">
					</router-link>
					<router-link class="nick_name" :to="'/profile/'+item.user.steamId+'/'">{{item.user.name}}</router-link>
					</td>
					<td class="table_item">
						<div class="gun_thumb">
							<img :src="item.image" :alt="clearItemQuality(item.name)">
						</div>
						<p v-html="clearItemQuality(item.name)"></p>
					</td>
					<td class="table_time">
						<p>
							{{item.timeDrop}}
						</p>
					</td>
					</tr>
					</tbody>
				</table>
			</div>
			<div class="pay_block flex">
				<div class="pay_item pay_item-mastercard"></div>
				<div class="pay_item pay_item-qiwi"></div>
				<div class="pay_item pay_item-visa"></div>
				<div class="pay_item pay_item-webmoney"></div>
				<div class="pay_item pay_item-yandex"></div>
			</div>
		</main>
	</div>
</template>
<script>
	export default {
		data: () => ({
				trades: false,
				hasMore: true,
				page: 0,
				inAction: false
			}),
		mounted() {
			Utils.setTitle("Live-трейды");
			this.getPageData();
		},
		methods: {
			getPageData() {
				if (this.inAction || !this.hasMore) {
					return;
				}
				this.inAction = true;
				Utils.apiPostCall("/api/livetrade/", {page: this.page})
						.then(resp => {
							if (resp.data.success) {
								this.page++;
								if (this.trades) {
									this.trades = this.trades.concat(resp.data.trades);
								} else {
									this.trades = resp.data.trades;
								}
								this.hasMore = resp.data.hasMore;
							}
							this.inAction = false;
						})
						.catch(err => {
							this.inAction = false;
						});
			}
		}
	}
</script>