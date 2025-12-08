<template>
	<div class="centerblock">
		<main id="main" class="site-main" role="main">
			<h1><span></span>топ пользователей<span></span></h1>
			<div class="container_1570 drop_top">
				<h2>топ по дропу</h2>
				<ul class="time_interval_list flex">
					<li @click="setTopDropTimeLimit(3600)" :class="{'active' : topDropTimeLimit == 3600}">за час</li>
					<li @click="setTopDropTimeLimit(86400)" :class="{'active' : topDropTimeLimit == 86400}">за день</li>
					<li @click="setTopDropTimeLimit(86400 * 7)" :class="{'active' : topDropTimeLimit == 86400 * 7}">за неделю</li>
					<li @click="setTopDropTimeLimit(86400 * 30)" :class="{'active' : topDropTimeLimit == 86400 * 30}">за месяц</li>
					<li @click="setTopDropTimeLimit(86400 * 182)" :class="{'active' : topDropTimeLimit == 86400 * 182}">за полгода</li>
					<li @click="setTopDropTimeLimit(86400 * 365)" :class="{'active' : topDropTimeLimit == 86400 * 365}">за год</li>
					<li @click="setTopDropTimeLimit(0)" :class="{'active' : topDropTimeLimit == 0}">за все время</li>
				</ul>
				<div v-if="topDrop && topDrop.length > 0" class="drop_block flex">
					<div v-for="(item, topPos) in topDrop" class="drop_item" :class="item.rarity">
						<div class="top_place"><span>{{topPos + 1}}</span>место</div>
						<div class="border">
							<div class="item_thumb">
								<img :src="item.image" :alt="clearItemQuality(item.name)">
								<div class="drop_signature flex">
									<div class="drop_signature-left">
										<div class="gun_name" v-html="clearItemQuality(item.name)"></div>
									</div>
									<div class="drop_signature-right">
										<router-link :to="'/profile/' + item.user.steam_id + '/'" class="user_icon">
											<img :src="item.user.image" :alt="item.user.name">
										</router-link>
									</div>
								</div>
							</div>
							<div class="price">{{item.price}} <span>руб</span></div>
						</div>
					</div>
				</div>
			</div>
			<div v-if="topProfit && topProfit.length > 0" class="container_1570 earnings_top">
				<h2>топ по заработку</h2>
				<div class="earnings_block flex">
					<div v-for="(user, topPos) in topProfit.slice(0,3)" class="border">
						<div class="earnings_item">
							<div class="earnings_user">
								<div class="user_thumb">
									<div class="number">№<span>{{(topPos + 1)}}</span></div>
									<img :src="user.image" :alt="user.name">
								</div>
								<div class="user_name">{{user.name}}</div>
							</div>
							<div class="earnings_information">
								<div class="opened_cases">
									Кейсов открыл
									<p>{{user.cases}}</p>
								</div>
								<div class="earnings">
									Прибыль
									<p>{{user.profit.toLocaleString('ru-RU')}}</p>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="trades_list">
					<table class="table_list" style="border-collapse: collapse; width: 100%;">
						<thead>
							<tr>
								<td class="table_place">Место</td>
								<td class="table_user">Пользователь</td>
								<td class="table_cases">Кейсы</td>
								<td class="table_profit">Профит</td>
							</tr>
						</thead>
						<tbody>
							<tr v-for="(user, topPos) in topProfit">
								<td class="table_place">
									<p>{{(topPos + 1)}}</p>
								</td>
								<td class="table_user">
						<router-link :to="'/profile/' + user.steam_id + '/'" class="user_avatar">
							<img :src="user.image" :alt="user.name">
						</router-link>
						</td>
						<td class="table_cases">
							<p>{{user.cases}}</p>
						</td>
						<td class="table_profit">
							<p>
								{{user.profit.toLocaleString('ru-RU')}}
							</p>
						</td>
						</tr>
						</tbody>
					</table>
				</div>
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
				topProfit: false,
				topDrop: false,
				topDropTimeLimit: 3600,
				inAction: false,
			}),
		mounted() {
			Utils.setTitle("Топ");
			this.getTopDrop();
			this.getTopProfit();
		},
		methods: {
			getTopProfit() {
				Utils.apiPostCall("/api/user/top/")
						.then(resp => {
							if (resp.data.success) {
								this.topProfit = resp.data.top;
							}
						});
			},
			getTopDrop() {
				if (this.inAction) {
					return;
				}
				this.inAction = true;
				Utils.apiPostCall("/api/user/top/drop/", {limit: 4, timeLimit: this.topDropTimeLimit})
						.then(resp => {
							if (resp.data.success) {
								this.topDrop = resp.data.top;
							}
							this.inAction = false;
						})
						.catch(err => {
							this.inAction = false;
						});
			},
			setTopDropTimeLimit(timeLimit) {
				if (timeLimit == this.topDropTimeLimit || this.inAction) {
					return;
				}
				this.topDropTimeLimit = timeLimit;
				this.getTopDrop();
			}
		}
	}
</script>