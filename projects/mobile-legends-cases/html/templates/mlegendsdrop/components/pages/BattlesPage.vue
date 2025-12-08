<template>
	<div class="centerblock">
		<main id="main" class="site-main" role="main">
			<h1><span></span>СРАЖЕНИЯ <span></span></h1>
			<div class="container_1570 flex">
				<div class="sidebar">
					<div class="last_battle">
						<h4>Последнее сражение</h4>
						<div v-if="lastBattle && lastBattle.creator && lastBattle.participant && lastBattle.case" class="border">
							<div class="battle_results flex">
								<div class="first_player" :class="{'winner' : (lastBattle.winnerId == -1 || lastBattle.winnerId == lastBattle.creator.id)}">
									 <div class="played_gun">
										<img :src="'http://steamcommunity-a.akamaihd.net/economy/image/' + lastBattle.creator.drop.image" :alt="clearItemQuality(lastBattle.creator.drop.name)">
									</div>
									<div class="player">
										<img :src="lastBattle.creator.image" :alt="lastBattle.creator.name">
									</div>
									<p class="price_gun">{{lastBattle.creator.drop.price}}</p>
								</div>
								<div class="played_case">
									<img :src="lastBattle.case.image" :alt="lastBattle.case.name">
								</div>
								<div class="second_player" :class="{'winner' : (lastBattle.winnerId == -1 || lastBattle.winnerId == lastBattle.participant.id)}">
									 <div class="played_gun">
										<img :src="'http://steamcommunity-a.akamaihd.net/economy/image/' + lastBattle.participant.drop.image" :alt="clearItemQuality(lastBattle.participant.drop.name)">
									</div>
									<div class="player">
										<img :src="lastBattle.participant.image" :alt="lastBattle.participant.name">
									</div>
									<p class="price_gun">{{lastBattle.participant.drop.price}}</p>
								</div>
							</div>
						</div>
						<div v-if="userStats" class="border">
							<div class="my_battles">
								<div class="battle_statistics flex">
									<div class="victory">
										<div class="quantity">{{userStats.won.toLocaleString('ru-RU')}}</div>
										<p>Побед</p>
									</div>
									<div class="defeat">
										<div class="quantity">{{userStats.lost.toLocaleString('ru-RU')}}</div>
										<p>Поражений</p>
									</div>
									<div class="draws">
										<div class="quantity">{{userStats.draw.toLocaleString('ru-RU')}}</div>
										<p>Ничьих</p>
									</div>
								</div>
								<router-link to="/profile/" class="open_statistics">Мои батлы</router-link>
							</div>
						</div>
						<div v-if="stats" class="border">
							<div class="battle_information">
								<div class="total_battles">
									<div class="quantity">{{stats.active.toLocaleString('ru-RU')}}</div>
									<p>Активные батлы</p>
								</div>
								<div class="active_battles">
									<div class="quantity">{{stats.total.toLocaleString('ru-RU')}}</div>
									<p>Всего батлов</p>
								</div>
							</div>
						</div>
						<h4>Как это работает?</h4>
						<div class="border">
							<div class="who_is">
								<ol class="who_is__list">
									<li>Кликните “Создать” или
										присоединитесь к существующему
										сражению.
									</li>
									<li>Сражение начнется как только оба
										участника присоединились.
									</li>
									<li>Участник, получивший предмет
										дороже, забирает оба.
									</li>
								</ol>
							</div>
						</div>
					</div>
				</div>
				<div class="battles_list">
					<table class="table_price" style="border-collapse: collapse; width: 100%;">
						<thead>
							<tr>
								<td class="table_case">Кейс </td>
								<td class="table_battles">Активные сражения </td>
								<td class="table_price">Стоимость</td>
								<td class="table_actions">Действия</td>
							</tr>
						</thead>
						<tbody>
							<tr v-for="ocase in cases">
								<td class="table_case"><img :src="ocase.image" :alt="ocase.name"></td>
								<td class="table_battles"><p>{{ocase.active}}</p></td>
								<td class="table_price"><p>{{ocase.salePrice}}</p></td>
								<td class="table_actions">
									<template v-if="isLogin">
										<a href="#" v-if="ocase.active > 0" @click.prevent="joinBattle(ocase.caseId)" class="enter_battle green_btn btn">Войти</a>
										<a href="#" @click.prevent="createBattle(ocase.caseId)" class="add_battle blue_btn btn">Создать</a>
									</template>
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
				cases: false,
				caseTimeout: false,
				actionInProgress: false,
				stats: false,
				lastBattle: false,
				userStats: false,
				destroyed: false
			}),
		mounted() {
			Utils.setTitle("Сражение");
			this.getBattlesData(true);
			this.$centrifuge.subscribe("uptadeBattleList", (resp) => {
				if (resp.data.success) {
					this.cases = resp.data.cases;
					this.stats = resp.data.stats;
					this.lastBattle = resp.data.lastBattle;
				}
			});
			this.$eventBus.$on('centrifugeDisconnected', this.getBattlesData);
		},
		beforeDestroy() {
			this.destroyed = true;
			clearTimeout(this.caseTimeout);
			this.$eventBus.$off('centrifugeDisconnected', this.getBattlesData);
			this.$centrifuge.getSub("uptadeBattleList").unsubscribe();
		},
		methods: {
			getBattlesData(force = false) {
				if (!force && this.$centrifugeConnected) {
					return;
				}
				Utils.apiPostCall("/api/opencase/battle/cases/list/")
						.then(resp => {
							if (resp.data.success) {
								this.cases = resp.data.cases;
								this.stats = resp.data.stats;
								this.lastBattle = resp.data.lastBattle;
								if (resp.data.userStats) {
									this.userStats = resp.data.userStats;
								}
							}
							if (!this.destroyed) {
								this.statTimeout = setTimeout(() => {
									this.getBattlesData();
								}, 5000);
							}
						})
						.catch(err => {
							if (!this.destroyed) {
								this.statTimeout = setTimeout(() => {
									this.getBattlesData();
								}, 5000);
							}
						});
			},
			createBattle(caseId) {
				if (this.actionInProgress) {
					return;
				}
				this.actionInProgress = true;
				Utils.apiPostCall("/api/opencase/battle/create/" + caseId + "/")
						.then(resp => {
							if (resp.data.success) {
								this.$router.push("/battle/" + resp.data.id + "/");
							} else {
								Utils.userAlert('Возникла ошибка при создании игры', resp.data.error, 'warn');
							}
							this.actionInProgress = false;
						})
						.catch(err => {
							this.actionInProgress = false;
							Utils.userAlert('Возникла ошибка при создании игры', err.response.statusText, 'error');
						});
			},
			joinBattle(caseId) {
				if (this.actionInProgress) {
					return;
				}
				this.actionInProgress = true;
				Utils.apiPostCall("/api/opencase/battle/join/" + caseId + "/")
						.then(resp => {
							if (resp.data.success) {
								this.$router.push("/battle/" + resp.data.id + "/");
							} else {
								Utils.userAlert('Возникла ошибка при присоединении к игре', resp.data.error, 'warn');
							}
							this.actionInProgress = false;
						})
						.catch(err => {
							this.actionInProgress = false;
							Utils.userAlert('Возникла ошибка при присоединении к игре', err.response.statusText, 'error');
						});
			},
		},
		computed: {
			isLogin() {
				return this.$store.getters.isLogin;
			}
		}
	}
</script>