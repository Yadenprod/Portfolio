<template>
	<div class="centerblock">
		<main v-if="loaded && ocase" id="main" class="site-main page_battles" role="main">
			<h1><span></span>{{ocase.name}}<span></span></h1>
			<template v-if="!progress.hasResult">
				<div class="open_case flex">
					<div class="case_thumb">
						<img :src="ocase.caseImage" :alt="ocase.name">	
					</div>
					<div class="case_settings">
						<template v-if="isLogin">
							<div v-if="isDefaultCase" class="selection">
								<template v-if="progress.started || userData.balance >= ocase.finalPrice">
									<div class="case_price">
										{{ocase.finalPrice * count}}
									</div>
									<div class="title">
										Выбери количество открытий
									</div>
									<div class="checkboxes">
										<template v-for="index in [1,2,3,4,5,10]">
											<template v-if="userData.balance >= ocase.finalPrice * index">
												<input v-model="count" type="radio" class="custom-checkbox"  :id="'custom-' + index" :value="index">
													   <label :for="'custom-' + index">x{{index}}</label>
											</template>
										</template>
									</div>
								</template>
								<template v-else>
									<div class="info_item">
										<div class="info_title">
											У вас недостаточно средств для открытия кейса!
										</div>
										<p><a href="#" @click.prevent data-popup="addBalance">Пополнение баланса</a></p>						
									</div>
								</template>
							</div>
							<div v-else-if="isDepositCase" class="info_item">
								<div class="info_title">
									ЧТОБЫ ОТКРЫТЬ ЭТОТ КЕЙС ВАМ НЕОБХОДИМО
								</div>
								<p>
									<a href="#" @click.prevent data-popup="addBalance">Пополнение баланса</a> за последние {{depositTimeStr(ocase.deposit.checkDayCount)}} не менее, чем на <span>{{ocase.deposit.minForOpen}}</span>
									За последние {{depositTimeStr(ocase.deposit.checkDayCount)}} вы пополнили баланс на <span>{{ocase.deposit.daySum}}</span>
									Открывать этот кейс можно не более {{ocase.deposit.possibleCount}} раз за последние {{depositTimeStr(ocase.deposit.checkDayCount)}}
									Кейс открыт: {{ocase.deposit.openedCount}}
									<template v-if="!ocase.allowOpen && ocase.deposit.timeBeforeOpen > 0">
										<br>До следующей попытки осталось: {{formattedTime(ocase.deposit.timeBeforeOpen)}}
									</template>
								</p>
							</div>
							<template v-if="ocase.allowOpen && userData.balance >= ocase.finalPrice">
								<a href="#" @click.prevent="openCase()" class="btn-yellow ">ОТКРЫТЬ</a>
								<a href="#" @click.prevent="openCase(true)" class="gray_btn ">ОТКРЫТЬ БЫСТРО</a>
							</template>

						</template>
						<template v-else>
							<div class="info_item">
								<div class="info_title">
									Вы не авторизованны
								</div>
								<p><a href="/?login">Авторизоваться</a></p>							
							</div>
						</template>
					</div>
				</div>
			</template>
			<template v-else-if="!progress.fast && !wonItems">
				<div v-for="roulletItemsData in roulletItems" class="roulette_item">
					<div class="roulette_gun flex">
						<div class="roulette_items_wrap">
							<div class="roulette_items" :style="[{'transition-duration': roulletItemsData.duration + 's'}, {'left': '-' + roulletItemsData.left + '%'}]">
								 <div v-for="(item, index) in roulletItemsData.roullet" class="gun_item" :class="item.rarity">
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
			</template>
			<template v-else-if="wonItems">
				<div class="drop_items_wrap flex">
					<div v-for="item in wonItems" class="drop_item" :class="item.rarity">
						<div class="drop_thumb">
							<img :src="'https://steamcommunity-a.akamaihd.net/economy/image/' + item.image +'/300fx200f'" alt="">
							<a href="#" v-if="wonItems.length > 1 && !item.sold" @click.prevent="saleItem(item)" class="btn_sell abs">Продать за <span>{{item.price}}</span></a>
						</div>
						<div class="drop_subtitle" v-html="clearItemQuality(item.name)"></div>
					</div>
				</div>
				<div class="drop_item">
					<a href="#" @click.prevent="refreshPage" class="btn-yellow again">Попробовать еще</a>
					<a href="#" @click.prevent="saleAllItems" class="btn_sell">Продать за <span>{{totalPrice}}</span></a>
				</div>				
			</template>
			<h2><span></span>Содержимое <b>кейса</b><span></span></h2>
			<div class="container_1770">
				<div class="case_contents flex">						
					<div v-for="item in items" :class="item.rarity" class="gun_item">
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
		</main>
		<page-404 v-if="loaded && !ocase"></page-404>
	</div>
</template>
<script>
	export default {
		data: () => ({
				loaded: false,
				progress: {
					started: false,
					fast: false,
					hasResult: false
				},
				wonItems: false,
				ocase: false,
				items: false,
				roulletItems: [],
				initRoulletItems: false,
				destroyed: false,
				count: 1,
				inAction: false,
				clickInt: false,
				openTimeout: false,
				depositIntv: false
			}),
		mounted() {
			Utils.setTitle("Кейс");
			this.getPageData();
		},
		beforeDestroy() {
			this.destroyed = true;
			clearInterval(this.clickInt);
			clearInterval(this.depositIntv);
			clearTimeout(this.openTimeout);
		},
		methods: {
			getPageData() {
				Utils.apiPostCall("/api/case/" + this.$route.params.key + "/")
						.then(resp => {
							if (resp.data.success) {
								this.ocase = resp.data.case;
								this.items = resp.data.items;
								let roulletItems = Utils.repeatFillObjectArray(Utils.shuffle(resp.data.items.slice()), 50).splice(0, 50);
								let availQualities = [3, 4, 5, 6, 12];
								for (let i in roulletItems) {
									if (~availQualities.indexOf(parseInt(roulletItems[i].quality)) && Math.random() > 0.9) {
										roulletItems[i].stattrack = true;
									} else {
										roulletItems[i].stattrack = false;
									}
								}
								this.initRoulletItems = roulletItems;
								clearInterval(this.depositIntv);
								if (this.ocase.hasOwnProperty('deposit') && this.ocase.deposit.timeBeforeOpen > 0) {
									this.depositIntv = setInterval(() => {
										this.ocase.deposit.timeBeforeOpen--;
										if (this.ocase.deposit.timeBeforeOpen < 0) {
											clearInterval(this.depositIntv);
											this.refreshPage();
										}
									}, 1000);
								}
							}
							this.loaded = true;
						})
						.catch(err => {
							this.loaded = true;
						});
			},
			openCase(fast = false) {
				if (this.isDepositCase) {
					this.openDepositCase(fast);
				} else if (!this.progress.started) {
					this.progress.fast = fast;
					this.progress.started = true;
					let data = {
						count: this.count
					};
					if (fast) {
						data.fast = 1;
					} else {
						Utils.playSound("CaseOpen");
					}
					this.$store.commit('changeBalance', -this.ocase.finalPrice * this.count);
					Utils.apiPostCall("/api/opencase/open/multiply/" + this.ocase.id + "/", data)
							.then(resp => {
								if (resp.data.success) {
									this.progress.hasResult = true;
									this.startRoulettes(resp.data.items, fast);
								} else {
									Utils.userAlert('Возникла ошибка при открытии кейса', resp.data.error, 'warn');
									this.$store.commit('changeBalance', this.ocase.finalPrice * this.count);
									Object.assign(this.$data.progress, this.$options.data().progress);
								}
							})
							.catch(err => {
								Utils.userAlert('Возникла ошибка при открытии кейса', err.response.statusText, 'error');
								this.$store.commit('changeBalance', this.ocase.finalPrice * this.count);
								Object.assign(this.$data.progress, this.$options.data().progress);
							});
				}
			},
			startRoulettes(items, fast) {
				for (let i in items) {
					items[i].name = items[i].name.replace('StatTrak™', '<span class = "stattrak-color">StatTrak™</span>');
					items[i].sold = false;
				}
				if (fast) {
					this.wonItems = items;
					Utils.playSound("ItemReveal");
				} else {
					let blockWidth = 25;
					let startOffset = 50;
					let timeRoulett = 15;
					for (let i in items) {
						let winnerBlock = 25 + Math.floor(Math.random() * 10);
						let item = items[i];
						let roullet = Utils.shuffle(this.initRoulletItems.slice());
						roullet[winnerBlock] = {
							name: item.name,
							rarity: item.rarity,
							image: "http://steamcommunity-a.akamaihd.net/economy/image/" + item.image,
							stattrack: false
						};
						let left = blockWidth * (winnerBlock) - startOffset + 12.5;
						let roullettData = {roullet: roullet, duration: timeRoulett, left: 0};
						this.roulletItems.push(roullettData);
						setTimeout(() => {
							roullettData.left = left;
						}, 200);
					}

					let oldPos = 0;
					this.clickInt = setInterval(() => {
						let newPos = Math.floor(($('.roulette_items').position().left / $('.roulette_items').parent().width() * 100 - startOffset) / blockWidth);
						if (oldPos != newPos) {
							oldPos = newPos;
							Utils.playSound("CaseScroll");
						}
					}, 100);
					this.openTimeout = setTimeout(() => {
						this.wonItems = items;
						clearInterval(this.clickInt);
						Utils.playSound("ItemReveal");
					}, (timeRoulett + 1) * 1000);
				}
			},
			refreshPage() {
				Object.assign(this.$data, this.$options.data());
				this.getPageData();
			},
			saleItem(item) {
				if (item.sold || this.inAction) {
					return;
				}
				this.inAction = true;
				Utils.apiPostCall("/api/opencase/sale/" + item.ID + "/")
						.then(resp => {
							if (resp.data.success) {
								this.$store.commit('changeBalance', item.price);
								item.sold = true;
								let hasNoSold = false;
								for (let i in this.wonItems) {
									if (!this.wonItems[i].sold) {
										hasNoSold = true;
										break;
									}
								}
								if (!hasNoSold) {
									this.refreshPage();
								}
							} else {
								Utils.userAlert('Возникла ошибка при продаже предмета', resp.data.error, 'warn');
							}
							this.inAction = false;
						})
						.catch(err => {
							Utils.userAlert('Возникла ошибка при продаже предмета', err.response.statusText, 'error');
							this.inAction = false;
						});
			},
			saleAllItems() {
				if (this.inAction) {
					return;
				}
				this.inAction = true;
				let ids = [];
				if (this.wonItems) {
					for (let i in this.wonItems) {
						if (!this.wonItems[i].sold) {
							ids.push(parseInt(this.wonItems[i].ID));
						}
					}
				}
				Utils.apiPostCall("/api/opencase/sale/list/", {ids: ids})
						.then(resp => {
							if (resp.data.success) {
								this.$store.commit('setBalance', resp.data.balance);
								Utils.userAlert(resp.data.msg, '', 'success');
								this.refreshPage();
							} else {
								Utils.userAlert('Возникла ошибка при продаже предметов', resp.data.error, 'warn');
							}
							this.inAction = false;
						})
						.catch(err => {
							Utils.userAlert('Возникла ошибка при продаже предметов', err.response.statusText, 'error');
							this.inAction = false;
						});
			},
			openDepositCase(fast = false) {
				if (this.ocase.allowOpen && !this.progress.started) {
					this.progress.fast = fast;
					this.progress.started = true;
					let data = {};
					if (fast) {
						data.fast = 1;
					} else {
						Utils.playSound("CaseOpen");
					}
					Utils.apiPostCall("/api/opencase/open/" + this.ocase.id + "/", data)
							.then(resp => {
								if (resp.data.success) {
									this.progress.hasResult = true;
									this.startRoulettes([resp.data.item], fast);
								} else {
									Utils.userAlert('Возникла ошибка при открытии кейса', resp.data.error, 'warn');
									Object.assign(this.$data.progress, this.$options.data().progress);
								}
							})
							.catch(err => {
								Utils.userAlert('Возникла ошибка при открытии кейса', err.response.statusText, 'error');
								Object.assign(this.$data.progress, this.$options.data().progress);
							});
			}
			},
			depositTimeStr(count) {
				if (count == 1) {
					return '24 часа';
				} else {
					const cases = [2, 0, 1, 1, 1, 2];
					const daysNames = ['день', 'дня', 'дней'];
					let index = (count % 100 > 4 && count % 100 < 20) ? 2 : cases[(count % 10 < 5) ? (count % 10) : 5];
					return count + ' ' + daysNames[index];
				}
			},
			formattedTime(time) {
				let res = '';
				if (time > 86400) {
					res += parseInt(time / 86400) + 'д ';
					time %= 86400;
				}
				let h = parseInt(time / 3600);
				res += (h < 10 ? '0' : '') + h + ':';
				let m = parseInt(time / 60 % 60);
				res += (m < 10 ? '0' : '') + m + ':';
				let s = parseInt(time % 60);
				res += (s < 10 ? '0' : '') + s;
				return res;
			}
		},
		computed: {
			isDefaultCase() {
				return this.ocase.type == 0;
			},
			isDepositCase() {
				return this.ocase.type == 2;
			},
			totalPrice() {
				let price = 0;
				if (this.wonItems) {
					for (let i in this.wonItems) {
						if (!this.wonItems[i].sold) {
							price += this.wonItems[i].price;
						}
					}
				}
				return price;
			},
			userData() {
				return this.$store.getters.userData;
			},
			isLogin() {
				return this.$store.getters.isLogin;
			}
		},
		watch: {
			$route(to, from) {
				Object.assign(this.$data, this.$options.data());
				this.getPageData();
			}

		}
	}
</script>