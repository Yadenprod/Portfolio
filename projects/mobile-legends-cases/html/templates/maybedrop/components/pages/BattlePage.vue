<template>
	<div class="centerblock">
		<main v-if="loaded && battle" id="main" class="site-main page_battles" role="main">
			<h1 class="title_white"><span></span>сражения <span></span></h1>
            <div class="main_fight">
                <h3 class="search_opponent" v-if="battle.status == 0">Поиск противника</h3>
                <h3 class="search_opponent" v-else-if="battle.status == 1">Сражение в процессе</h3>
                <h3 class="search_opponent" v-else-if="battle.status == 2">Результаты</h3>
                <div class="fight_block flex">
                    <div class="creator" :class="{'winner' : battle.creator && battle.status == 2 && (winnerId == -1 || winnerId == battle.creator.id)}">
						 <div class="creator_block">
							<template v-if="battle.creator">
								<div class="player_avatar"><img :src="battle.creator.image" alt="battle.creator.name"></div>
								<div class="player_name">{{battle.creator.name}}</div>
							</template>
							<template v-else>
								<div class="player_avatar"></div>
								<div class="player_name">Ожидание</div>
							</template>
                            <div class="signature">Создатель</div>
                        </div>
						<div v-if="battle.status == 2 && battle.creator && battle.creator.drop" class="player_item">
                            <div class="gun_image">
								<img :src="'http://steamcommunity-a.akamaihd.net/economy/image/' + battle.creator.drop.image" :alt="clearItemQuality(battle.creator.drop.name)">
							</div>
                            <div class="gun_price">{{battle.creator.drop.price}}</div>
                            <div v-if="isLogin && (userData.id == winnerId || winnerId == -1 && userData.id == battle.creator.id) && battle.creator.drop.droppedItem && (battle.creator.drop.droppedItem.status == 0 || battle.creator.drop.droppedItem.status == 6)" class="actions flex">
                                <a href="#" @click.prevent="withdrawItem(battle.creator.drop.droppedItem)" class="pick_up green_btn btn">Забрать</a>
                                <a href="#" @click.prevent="saleItem(battle.creator.drop.droppedItem)" class="sell red_btn btn">Продать</a>
                            </div>
                        </div>
                    </div>
                    <div class="case_block">
                        <div class="case_thumb">
                            <img :src="battle.case.image" :alt="battle.case.name">	
                        </div>
                        <div class="case_name">{{battle.case.name}}</div>
                        <div class="case_price">{{battle.price}}</div>
						<template v-if="battle.status == 2">
							<a href="#" @click.prevent="repeatBattle" class="btn_again animation_light">Попробовать еще</a>
							<router-link to="/battles/" class="back_list">< Вернуться к списку сражений</router-link>
						</template>
						<template v-else-if="isLogin && battle.creator && battle.creator.id == userData.id && battle.status == 0">
							<a href="#" @click.prevent="cancelBattle" class="btn_again animation_light">Отменить сражение</a>
						</template>
                    </div>
                    <div class="opponent" :class="{'winner' : battle.participant && battle.status == 2 && (winnerId == -1 || winnerId == battle.participant.id)}">
						 <div class="opponent_block">
							<template v-if="battle.participant">
								<div class="player_avatar"><img :src="battle.participant.image" alt="battle.participant.name"></div>
								<div class="player_name">{{battle.participant.name}}</div>
							</template>
							<template v-else>
								<div class="player_avatar"></div>
								<div class="player_name">Ожидание</div>
							</template>
                            <div class="signature">Противник</div>
                        </div>
						<div v-if="battle.status == 2 && battle.participant && battle.participant.drop" class="player_item">
                            <div class="gun_image">
								<img :src="'http://steamcommunity-a.akamaihd.net/economy/image/' + battle.participant.drop.image" :alt="clearItemQuality(battle.participant.drop.name)">
							</div>
                            <div class="gun_price">{{battle.participant.drop.price}}</div>
							<div v-if="isLogin && (userData.id == winnerId || winnerId == -1 && userData.id == battle.participant.id) && battle.participant.drop.droppedItem && (battle.participant.drop.droppedItem.status == 0 || battle.participant.drop.droppedItem.status == 6)" class="actions flex">
                                <a href="#" @click.prevent="withdrawItem(battle.participant.drop.droppedItem)" class="pick_up green_btn btn">Забрать</a>
                                <a href="#" @click.prevent="saleItem(battle.participant.drop.droppedItem)" class="sell red_btn btn">Продать</a>
                            </div>
                        </div>
                    </div>
                </div>
				<div v-if="battle.status == 1" class="roulette_block flex">
					<div v-if="battle.creator.casedrop && battle.creator.roullettData" class="roulette_player_wrap">
						<div class="roulette_player flex" :style="[{'transition-duration': battle.creator.roullettData.duration + 's'}, {'left': '-' + battle.creator.roullettData.left + '%'}]">
							 <div v-for="item in battle.creator.casedrop" class="gun_item" :class="item.rarity">
								<div class="gun_img"><img :src="item.image" :alt="clearItemQuality(item.name)"></div>
								<div class="gun_name">
									<span class="stattrak-color" v-if="item.stattrack">StatTrak™</span>
									<span v-html="clearItemQuality(item.name)"></span>
								</div>
							</div>
						</div>
					</div>
					<div v-if="battle.participant.casedrop && battle.participant.roullettData" class="roulette_player_wrap">
						<div class="roulette_player flex" :style="[{'transition-duration': battle.participant.roullettData.duration + 's'}, {'left': '-' + battle.participant.roullettData.left + '%'}]">
							 <div v-for="item in battle.participant.casedrop" class="gun_item" :class="item.rarity">
								<div class="gun_img"><img :src="item.image" :alt="clearItemQuality(item.name)"></div>
								<div class="gun_name">
									<span class="stattrak-color" v-if="item.stattrack">StatTrak™</span>
									<span v-html="clearItemQuality(item.name)"></span>
								</div>
							</div>
						</div>
					</div>
				</div>
            </div>
			<h2><span></span>Содержимое <b>кейса</b><span></span></h2>
			<div class="container_1770">
				<div class="case_contents flex">
					<div v-for="item in battle.case.items" class="gun_item" :class="item.rarity">
						<div class="gun_img"><img :src="item.image" :alt="clearItemQuality(item.name)"></div>
						<div class="gun_name" v-html="clearItemQuality(item.name)"></div>
					</div>
				</div>
			</div>
			<div class="pay_block flex">
				<div class="pay_item pay_item-mastercard"></div>
				<div class="pay_item pay_item-qiwi"></div>
				<div class="pay_item pay_item-visa"></div>
				<div class="pay_item pay_item-webmoney"></div>
				<div class="pay_item pay_item-yandex"></div>
			</div>
			<withdraw-analog-popup v-if="withdrowAnalogItemData" :withdrowAnalogItemData="withdrowAnalogItemData" @closeWithdrawAnalogModal="closeWithdrawAnalogModal"></withdraw-analog-popup>
		</main>
		<page-404 v-if="loaded && !battle"></page-404>
	</div>
</template>
<script>
	import WithdrawAnalogPopup from '../popup/WithdrawAnalogPopup';
	export default {
		components: {
			WithdrawAnalogPopup
		},
		data: () => ({
				loaded: false,
				destroyed: false,
				battle: false,
				actionInProgress: false,
				checkTimeout: false,
				clickInt: false,
				winnerId: false,
				itemActionInProgress: false,
				withdrowAnalogItemData: false,
				centrifugeSubscribed: false
			}),
		mounted() {
			Utils.setTitle("Сражение");
			this.getPageData();
		},
		beforeDestroy() {
			this.centrifugeUnsubscribe();
			if (this.isLogin && this.battle.creator && this.battle.creator.id == this.userData.id && this.battle.status == 0) {
				this.cancelBattle(false);
			}
			this.destroyed = true;
			clearTimeout(this.checkTimeout);
			clearInterval(this.clickInt);
		},
		methods: {
			centrifugeUnsubscribe() {
				if (this.centrifugeSubscribed && this.battle && this.battle.id) {
					this.$eventBus.$off('centrifugeDisconnected', this.startBattleCheck);
					this.$centrifuge.getSub("uptadeBattle" + this.battle.id).unsubscribe();
					this.centrifugeSubscribed = false;
				}
			},
			getPageData() {
				Utils.apiPostCall("/api/opencase/battle/" + this.$route.params.id + "/")
						.then(resp => {
							if (resp.data.success) {
								this.battle = resp.data.battle;
								this.winnerId = resp.data.battle.winnerId;
								if (this.battle.status == 0 || this.battle.status == 1) {
									if (this.battle.status == 1 && resp.data.result) {
										this.checkTimeout = setTimeout(() => {
											this.applyBattleResult(resp.data.result);
										}, 3000);
									} else {
										this.startBattleCheck();
										this.$centrifuge.subscribe("uptadeBattle" + this.battle.id, (resp) => {
											if (resp.data.success) {
												this.battle.status = parseInt(resp.data.status);
												switch (this.battle.status) {
													case 0:
													case 1:
														this.battle.creator = resp.data.creator;
														this.battle.participant = resp.data.participant;
														if (resp.data.winnerId) {
															this.winnerId = resp.data.winnerId;
														}
														if (resp.data.result) {
															this.checkTimeout = setTimeout(() => {
																this.applyBattleResult(resp.data.result);
															}, 3000);
															this.centrifugeUnsubscribe();
														}
														break;
													case 2:
														this.centrifugeUnsubscribe();
														Object.assign(this.$data, this.$options.data());
														this.getPageData();
														return;
													case 3:
														this.centrifugeUnsubscribe();
														Utils.userAlert('Игра была отменена', '', 'warn');
														this.$router.push("/battles/");
														return;
												}
											}
										});
										this.$eventBus.$on('centrifugeDisconnected', this.startBattleCheck);
										this.centrifugeSubscribed = true;
									}

								}
							}
							this.loaded = true;
						})
						.catch(err => {
							this.loaded = true;
						});
			},
			statTrack(val) {
				return val.replace('StatTrak™', '<span class = "stattrak-color">StatTrak™</span>');
			},
			cancelBattle(showMessage = true) {
				if (this.actionInProgress) {
					return;
				}
				this.actionInProgress = true;
				Utils.apiPostCall("/api/opencase/battle/cancel/" + this.battle.id + "/")
						.then(resp => {
							if (resp.data.success) {
								if (showMessage) {
									Utils.userAlert('Игра успешно отменена', '', 'success');
									this.$router.push("/battles/");
								}
								this.battle.status = 3;
							} else {
								if (showMessage) {
									Utils.userAlert('Возникла ошибка при отмене игры', resp.data.error, 'warn');
								}
							}
							this.actionInProgress = false;
						})
						.catch(err => {
							this.actionInProgress = false;
							if (showMessage) {
								Utils.userAlert('Возникла ошибка при отмене игры', err.response.statusText, 'error');
							}
						});
			},
			startBattleCheck() {
				if (this.battle.status != 0 || this.$centrifugeConnected || this.actionInProgress) {
					return;
				}
				this.actionInProgress = true;
				let needRepeat = true;
				Utils.apiPostCall("/api/opencase/checkbattle/" + this.battle.id + "/")
						.then(resp => {
							if (resp.data.success) {
								this.battle.status = parseInt(resp.data.status);
								switch (this.battle.status) {
									case 0:
									case 1:
										this.battle.creator = resp.data.creator;
										this.battle.participant = resp.data.participant;
										if (resp.data.winnerId) {
											this.winnerId = resp.data.winnerId;
										}
										if (resp.data.result) {
											this.applyBattleResult(resp.data.result);
											needRepeat = false;
											this.centrifugeUnsubscribe();
										}
										break;
									case 2:
										needRepeat = false;
										this.centrifugeUnsubscribe();
										Object.assign(this.$data, this.$options.data());
										this.getPageData();
										return;
									case 3:
										needRepeat = false;
										this.centrifugeUnsubscribe();
										Utils.userAlert('Игра была отменена', '', 'warn');
										this.$router.push("/battles/");
										return;
								}
							}
							this.actionInProgress = false;
							if (needRepeat && !this.destroyed) {
								this.checkTimeout = setTimeout(() => {
									this.startBattleCheck();
								}, 5000);
							}
						})
						.catch(err => {
							this.actionInProgress = false;
							if (needRepeat && this.destroyed) {
								this.checkTimeout = setTimeout(() => {
									this.startBattleCheck();
								}, 5000);
							}
						});
			},
			updateBattleUsers(users) {
				if (this.battle.users != users.length) {
					for (let newId in users) {
						let user = users[newId];
						let hasUser = false;
						for (let oldId in this.battle.users) {
							if (this.battle.users[oldId].id == user.id) {
								hasUser = true;
								break;
							}
						}
						if (!hasUser) {
							this.battle.users.push(user);
						}
					}
				}
			},
			applyBattleResult(result) {
				let casedrop = Utils.repeatFillObjectArray(this.battle.case.items, 50);
				let availQualities = [3, 4, 5, 6, 12];
				for (let i in casedrop) {
					if (~availQualities.indexOf(parseInt(casedrop[i].rarity)) && Math.random() > 0.9) {
						casedrop[i].stattrack = true;
					} else {
						casedrop[i].stattrack = false;
					}
				}
				this.$set(this.battle.creator, 'casedrop', Utils.shuffle(casedrop.slice()));
				this.$set(this.battle.participant, 'casedrop', Utils.shuffle(casedrop.slice()));

				let blockWidth = 32.9;
				let startOffset = 50;
				let timeRoulett = 15;
				for (let i = 0; i < result.length; i++) {
					let user;
					if (result[i].userId == this.battle.creator.id) {
						user = this.battle.creator;
					} else if (result[i].userId == this.battle.participant.id) {
						user = this.battle.participant;
					} else {
						continue;
					}
					let winnerBlock = 25 + Math.floor(Math.random() * 10);
					let item = result[i].drop;
					let roullet = user.casedrop;
					roullet[winnerBlock] = {
						name: item.name,
						rarity: item.rarity,
						image: "http://steamcommunity-a.akamaihd.net/economy/image/" + item.image,
						stattrack: false
					};
					let left = blockWidth * (winnerBlock) - startOffset + 16.45;
					this.$set(user, 'roullettData', {duration: timeRoulett, left: 0});
					setTimeout(() => {
						user.roullettData.left = left;
					}, 200);
				}
				let oldPos = 0;
				this.clickInt = setInterval(() => {
					let newPos = Math.floor(($('.roulette_player').position().left / $('.roulette_player').parent().width() * 100 - startOffset) / blockWidth);
					if (oldPos != newPos) {
						oldPos = newPos;
						Utils.playSound("CaseScroll");
					}
				}, 100);
				setTimeout(() => {
					this.battle.status = 2;
					clearInterval(this.clickInt);
					Utils.playSound("ItemReveal");
				}, (timeRoulett + 1) * 1000);
				return;

			},
			repeatBattle() {
				if (this.actionInProgress) {
					return;
				}
				this.actionInProgress = true;
				Utils.apiPostCall("/api/opencase/battle/repeat/" + this.battle.case.caseId + "/")
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
			saleItem(item) {
				if (this.itemActionInProgress || item.disable) {
					return;
				}
				this.itemActionInProgress = true;
				this.$set(item, 'disable', true);
				Utils.apiPostCall("/api/opencase/sale/" + item.id + "/")
						.then(resp => {
							if (resp.data.success) {
								item.status = 3;
								this.$store.commit('changeBalance', resp.data.price);
								Utils.userAlert(resp.data.msg, '', 'success');
							} else {
								Utils.userAlert('Возникла ошибка при продаже предмета', resp.data.error, 'warn');
							}
							this.itemActionInProgress = false;
							this.$set(item, 'disable', false);
						})
						.catch(err => {
							this.itemActionInProgress = false;
							this.$set(item, 'disable', false);
							Utils.userAlert('Возникла ошибка при продаже предмета', err.response.statusText, 'error');
						});
			},
			withdrawItem(item) {
				if (this.itemActionInProgress || item.disable) {
					return;
				}
				this.itemActionInProgress = true;
				this.$set(item, 'disable', true);
				Utils.apiPostCall("/api/opencase/withdraw/analogs/" + item.id + "/")
						.then(resp => {
							if (resp.data.success) {
								if (resp.data.analog) {
									this.withdrowAnalogItemData = {
										analog: resp.data.analog,
										balance: resp.data.addBalance,
										item: item
									};
								} else {
									item.status = 1;
									Utils.userAlert(resp.data.msg, '', 'success');
								}
							} else {
								Utils.userAlert('Возникла ошибка при отправке предмета', resp.data.error, 'warn');
							}
							this.itemActionInProgress = false;
							this.$set(item, 'disable', false);
						})
						.catch(err => {
							this.itemActionInProgress = false;
							this.$set(item, 'disable', false);
							Utils.userAlert('Возникла ошибка при отправке предмета', err.response.statusText, 'error');
						});
			},
			closeWithdrawAnalogModal() {
				this.withdrowAnalogItemData = false;
			},
		},
		computed: {
			userData() {
				return this.$store.getters.userData;
			},
			isLogin() {
				return this.$store.getters.isLogin;
			}
		},
		watch: {
			$route(to, from) {
				clearTimeout(this.checkTimeout);
				clearInterval(this.clickInt);
				Object.assign(this.$data, this.$options.data());
				this.getPageData();
			}

		}
	}
</script>