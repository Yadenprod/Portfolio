<template>
	<div class="centerblock">
		<main id="main" class="site-main" role="main">
			<h1><span></span>up<b>grade</b><span></span></h1>
			<div class="container_1570 flex">
				<div class="object_upgrade">
					<div class="object_upgrade__block flex">
						<div class="item_left">
							<template v-if="useBalance">
								<div class="gun_item-none">
									<div class="cost">{{additionalBalance}}</div>
									<div class="price_slider">
										<range-slider
											@input="checkUpgradeStatus(true)"
											class="range"
											min="1"
											:max="userData.balance"
											step="1"
											:disabled="userData.balance < 1"
											v-model="additionalBalance">
									</range-slider>
								</div>
							</div>
						</template>
						<template v-else>
							<template v-if="itemForUpgrade">
								<div class="gun_item" :class="itemForUpgrade.rarity">
									<div class="gun_img">
										<img :src="itemForUpgrade.image" :alt="itemForUpgrade.imageAlt">
									</div>
									<div class="gun_name" v-html="clearItemQuality(itemForUpgrade.name)"></div>
									<a href="#" @click.prevent="clearForUpgrade" class="cross"><div class="cross_border"><span></span><span></span></div></a>
								</div>
								<div class="gun_price">
									Стоимость: <span>{{itemForUpgrade.price}}</span>
								</div>
							</template>
							<template v-else>
								<div class="gun_item-none">
									<img src="/tpl/maybedrop/img/gun_shadow_1.png" alt="">
									<p>Выберите скин для апгреда
										из списка ниже
									</p>
								</div>
							</template>
						</template>
					</div>
					<div class="item_center">
						<template v-if="wonItem && endState == 'success'">
							<div class="item_center-top result_upgrade">
								<img src="/tpl/maybedrop/img/well-icon.png" alt="">
								<div class="text">Апгрейд прошел удачно</div>
							</div>
							<div class="item_center-bottom">
								<a href="#" @click.prevent="refreshPage" class="btn_again">Попробовать еще раз</a>
								<a href="#" @click.prevent="saleItem" class="btn_sell">Продать за <span>{{wonItem.price}}</span></a>
							</div>
						</template>
						<template v-else-if="endState == 'fail'">
							<div class="item_center-top result_upgrade">
								<img src="/tpl/maybedrop/img/none_icon.png" alt="">
								<div class="text">Апгрейд завершился неудачей</div>
							</div>
							<div class="item_center-bottom">
								<a href="#" @click.prevent="refreshPage" class="btn_again no_right_margin">Попробовать еще раз</a>
							</div>
						</template>
						<div v-else-if="!upgradeAvail" class="item_center-top">
							<img src="/tpl/maybedrop/img/warning_icon.png" alt="">
							<div class="text">Не выбран предмет апгрейда</div>
						</div>
						<div v-else class="item_center-top chance_circle">
                            <div class="probability">
                                <div class="circle_block">
                                    <div class="chance_indicator" :style="{transform: 'rotate(' + upgradeRotate + 'deg)'}"></div>
                                    <div v-for="index in 44"  class="block_points" :class="{'filled' : (index + 35) % 45 <= upgradeFillSquareCount}">
										 <div class="square"></div>
                                    </div>
                                </div>
                                <div class="probability_percent">{{upgradePercent}}%</div>
                                <div class="text">успех апгрейда</div>
                            </div>
                        </div>
						<div v-if="!upgradeStarted" class="item_center-bottom">
							<label class="switch">
								<input @change="onUseBalanceChange" v-model="useBalance" type="checkbox">
								<span class="slider round"><span></span></span>
							</label>
							<a href="#" @click.prevent="startUpgrade" :class="{'upgrade_btn' : !upgradeAvail}" class="btn-yellow">АПГРЕЙД</a>
						</div>
					</div>
					<div class="item_right">
						<template v-if="itemToUpgrade">
							<div class="gun_item" :class="itemToUpgrade.rarity">
								<div class="gun_img">
									<img :src="itemToUpgrade.image" :alt="itemToUpgrade.imageAlt">
								</div>
								<div class="gun_name" v-html="clearItemQuality(itemToUpgrade.name)"></div>
								<a href="#" @click.prevent="clearToUpgrade" class="cross"><div class="cross_border"><span></span><span></span></div></a>
							</div>
							<div class="gun_price">
								Стоимость: <span>{{itemToUpgrade.price}}</span>
							</div>
						</template>
						<template v-else>
							<div class="gun_item-none">
								<img src="/tpl/maybedrop/img/gun_shadow_2.png" alt="">
								<p>Выберите скин для апгреда
									из списка ниже
								</p>
							</div>
						</template>
					</div>
				</div>
			</div>
			<template v-if="isLogin">
				<div class="my_object">
					<h4>Мои предметы</h4>
					<template v-if="userItems">
						<div class="my_object__block-border">
							<template v-if="useBalance">
								<div class="my_object__block my_object__block-none flex">
									<div class="information_block">
										<div class="none_object"><img src="/tpl/maybedrop/img/none_icon.png" alt=""></div>
										<div class="none_text">Используйте средства на аккаунте</div>
									</div>
								</div>
							</template>
							<template v-else-if="userItems.length <= 0">
								<div class="my_object__block my_object__block-none flex">
									<div class="information_block">
										<div class="none_object"><img src="/tpl/maybedrop/img/none_icon.png" alt=""></div>
										<div class="none_text">У вас нет предметов, используйте
											средства на аккаунте или откройте кейс</div>
										<router-link to="/" class="upgrade_btn">КЕЙСЫ</router-link>
									</div>
								</div>
							</template>
							<template v-else>
								<div class="my_object__block flex">
									<div v-for="item in userItems" :class="[item.rarity, {'gray-disabled' : item.selected}]" class="gun_item">
										 <div class="gun_img">
											<img :src="item.image" :alt="item.imageAlt">
										</div>
										<div class="gun_name" v-html="clearItemQuality(item.name)"></div>
										<div class="gun_description">Чёрный песок</div>
										<a href="#"  @click.prevent="selectForUpgrade(item)" class="cross"><div class="cross_border"><span></span><span></span></div></a>
									</div>
								</div>
							</template>
						</div>
					</template>
				</div>
				<div class="upgrade_block flex">
					<h4>Апгрейд</h4>
					<div class="filters">
						<div class="search flex">
							<div class=" search_form flex">
								<label class="search">
									<input v-model="allItems.search" @input="searchItems" placeholder="Быстрый поиск" type="search">
									<button type="submit"></button>
								</label>
								<button @click="changeOrder" class="price" :class="{'back' : !isAscOrder}">Стоимость</button>
								<label class="from_to">
									<input type="number" v-model="allItems.min" @input="searchItems" placeholder="От">
								</label>
								<label class="from_to">
									<input type="number" v-model="allItems.max" @input="searchItems" placeholder="До">
								</label>
							</div>
						</div>
					</div>
					<div class="items_block flex available_items" ref="itemsList" @scroll="itemListScroll">
						<div class="flex" ref="itemsListContent">
							<div v-for="item in allItems.list"  @click="selectToUpgrade(item)" class="gun_item" :class="[item.rarity, {'gray-disabled' : item.selected}]">
								 <div class="gun_img">
									<img :src="item.image" :alt="item.imageAlt">
								</div>
								<div class="gun_name" v-html="clearItemQuality(item.name)"></div>
								<div class="gun_cost">{{item.price}}</div>
							</div>
						</div>
					</div>
				</div>
			</template>
			<div class="upgrade_instruction flex">
				<div class="instruction_item">
					<div class="item_thumb"><img src="/tpl/maybedrop/img/instruction_item-1.png" alt=""></div>
					<div class="instruction_text">
						Выберите один из ваших скинов слева,
						чтобы обновить его и получить
						более дорогой
					</div>
				</div>
				<div class="instruction_item">
					<div class="item_thumb"><img src="/tpl/maybedrop/img/instruction_item-2.png" alt=""></div>
					<div class="instruction_text">
						Вы также можете использовать баланс
						вашего счета в качестве входных
						данных вместо скина
					</div>
				</div>
				<div class="instruction_item">
					<div class="item_thumb"><img src="/tpl/maybedrop/img/instruction_item-3.png" alt=""></div>
					<div class="instruction_text">
						Выберите скин справа
						до которого вы хотите выполнить
						апгрейд
					</div>
				</div>
				<div class="instruction_item">
					<div class="item_thumb"><img src="/tpl/maybedrop/img/instruction_item-4.png" alt=""></div>
					<div class="instruction_text">
						Вы увидите вероятность успешного
						апгрейда. В случае неудачи,
						вы теряете свой скин/баланс.
					</div>
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
</div>
</template>
<script>
	import RangeSlider from 'vue-range-slider';
	import 'vue-range-slider/dist/vue-range-slider.css';
	export default {
		components: {
			RangeSlider
		},
		data: () => ({
				userItems: false,
				itemForUpgrade: false,
				itemToUpgrade: false,
				upgradeStarted: false,
				upgradePercent: 0,
				upgradeRotate: 0,
				upgradeFillSquareCount: 0,
				upgradeAvail: false,
				wonItem: false,
				endState: '',
				additionalBalance: 0,
				isAscOrder: true,
				useBalance: false,
				allItems: {
					list: [],
					isLoading: false,
					page: 1,
					limit: 20,
					minPrice: 100,
					search: '',
					reset: true,
					hasMore: true,
					timeout: false,
					min: '',
					max: ''
				},
				destroyed: false,
				inAction: false
			}),
		mounted() {
			Utils.setTitle("Апгрейд");
			this.getPageData();
		},
		beforeDestroy() {
			this.destroyed = true;
		},
		methods: {
			getPageData() {
				Utils.apiPostCall("/api/user/availdrop/")
						.then(resp => {
							if (resp.data.success) {
								for (let i in resp.data.items) {
									resp.data.items[i].selected = false;
								}
								this.userItems = resp.data.items;
								this.getItems();
							}
						});
			},
			getItems() {
				if (!this.allItems.hasMore || this.allItems.isLoading) {
					return;
				}
				this.allItems.isLoading = true;
				let min = this.allItems.minPrice;
				if (this.allItems.min > 0) {
					min = Math.max(parseInt(this.allItems.min), this.allItems.minPrice);
				}
				let max = 0;
				if (this.allItems.max >= min) {
					max = parseInt(this.allItems.max);
				}
				Utils.apiPostCall("/api/opencase/upgrade/getavaillist/", {
					page: this.allItems.page,
					limit: this.allItems.limit,
					minprice: min,
					maxprice: max,
					search: this.allItems.search,
					order: this.isAscOrder ? 0 : 1
				})
						.then(resp => {
							if (resp.data.success) {
								this.allItems.page++;
								if (resp.data.items.length < this.allItems.limit) {
									this.allItems.hasMore = false;
								}
								for (let i in resp.data.items) {
									if (this.itemToUpgrade && this.itemToUpgrade.id == resp.data.items[i].id) {
										resp.data.items[i].selected = true;
									} else {
										resp.data.items[i].selected = false;
									}
									resp.data.items[i].imageAlt = resp.data.items[i].name;
									resp.data.items[i].name = resp.data.items[i].name.replace('StatTrak™', '<span class="stattrak-color">StatTrak™</span>')
								}
								if (this.allItems.reset) {
									this.$refs.itemsList.scrollTop = 0;
									this.allItems.reset = false;
									this.allItems.list = resp.data.items;
								} else {
									this.allItems.list = this.allItems.list.concat(resp.data.items);
								}
							}
							this.allItems.isLoading = false;
						})
						.catch(err => {
							this.allItems.isLoading = false;
						});
			},
			searchItems() {
				if (this.allItems.timeout) {
					clearTimeout(this.allItems.timeout);
				}
				this.allItems.timeout = setTimeout(() => {
					this.allItems.reset = true;
					this.allItems.hasMore = true;
					this.allItems.page = 1;
					this.getItems();
				}, 1000);
			},
			changeOrder() {
				this.isAscOrder = !this.isAscOrder;
				this.allItems.reset = true;
				this.allItems.hasMore = true;
				this.allItems.page = 1;
				this.getItems();
			},
			itemListScroll() {
				let list = this.$refs.itemsList;
				let content = this.$refs.itemsListContent;
				if (content.clientHeight - list.clientHeight - list.scrollTop < 50) {
					this.getItems();
				}
			},
			checkUpgradeStatus(checkToItems = false) {
				if (this.useBalance) {
					if (this.additionalBalance > 0) {
						if (checkToItems) {
							this.allItems.minPrice = Math.round(this.additionalBalance * 1.25);
							this.searchItems();
						}
						if (this.itemToUpgrade) {
							if (this.itemToUpgrade.price < Math.round(this.additionalBalance * 1.25)) {
								this.clearToUpgrade();
							} else {
								this.upgradePercent = Math.max(0.01, Math.min(75, (Math.round(this.additionalBalance / this.itemToUpgrade.price * 9300) / 100)));
								this.upgradeAvail = true;
								this.upgradeFillSquareCount = Math.floor(this.upgradePercent * 0.44);
								return;
							}
						}
					}
				} else if (this.itemForUpgrade && this.itemToUpgrade) {
					this.additionalBalance = 0;
					this.upgradePercent = Math.max(0.01, Math.min(75, (Math.round(this.itemForUpgrade.price / this.itemToUpgrade.price * 9300) / 100)));
					this.upgradeAvail = true;
					this.upgradeFillSquareCount = Math.floor(this.upgradePercent * 0.44);
					return;
				}

				this.upgradePercent = 0;
				this.upgradeFillSquareCount = 0;
				this.upgradeAvail = false;
			},
			onUseBalanceChange() {
				if (this.useBalance) {
					if (this.itemForUpgrade) {
						this.clearForUpgrade();
					}
				} else {
					this.additionalBalance = 0;
				}
				this.checkUpgradeStatus();
				this.allItems.reset = true;
				this.allItems.hasMore = true;
				this.allItems.page = 1;
				this.allItems.minPrice = 100;
				this.getItems();

			},
			selectForUpgrade(item) {
				if (this.upgradeStarted || item.selected) {
					return;
				}
				for (let i in this.userItems) {
					if (this.userItems[i].selected) {
						this.userItems[i].selected = false;
					}
				}
				item.selected = true;
				this.itemForUpgrade = item;
				this.allItems.reset = true;
				this.allItems.hasMore = true;
				this.allItems.page = 1;
				this.allItems.minPrice = item.price * 1.25;
				this.getItems();
				if (this.itemToUpgrade && this.itemToUpgrade.price < item.price * 1.25) {
					this.clearToUpgrade();
				}
				this.checkUpgradeStatus();
			},
			clearForUpgrade() {
				if (this.upgradeStarted) {
					return;
				}
				for (let i in this.userItems) {
					if (this.userItems[i].selected) {
						this.userItems[i].selected = false;
					}
				}
				this.itemForUpgrade = false;
				this.allItems.reset = true;
				this.allItems.hasMore = true;
				this.allItems.page = 1;
				this.allItems.minPrice = 100;
				this.getItems();
				this.checkUpgradeStatus();
			},
			selectToUpgrade(item) {
				if (this.upgradeStarted || item.selected) {
					return;
				}
				for (let i in this.allItems.list) {
					if (this.allItems.list[i].selected) {
						this.allItems.list[i].selected = false;
					}
				}
				item.selected = true;
				this.itemToUpgrade = item;
				this.checkUpgradeStatus();
			},
			clearToUpgrade() {
				if (this.upgradeStarted) {
					return;
				}
				for (let i in this.allItems.list) {
					if (this.allItems.list[i].selected) {
						this.allItems.list[i].selected = false;
					}
				}
				this.itemToUpgrade = false;
				this.checkUpgradeStatus();
			},
			startUpgrade() {
				if (this.upgradeStarted || !this.upgradeAvail || !this.useBalance && !this.itemForUpgrade || this.useBalance && this.additionalBalance < 1 || !this.itemToUpgrade) {
					return;
				}
				this.upgradeStarted = true;
				let params = {
					target: this.itemToUpgrade.id,
				};
				let addBalance = 0;
				if (this.useBalance) {
					params.balance = this.additionalBalance;
					addBalance = this.additionalBalance;
				} else {
					params.source = this.itemForUpgrade.id;
				}
				this.$store.commit('changeBalance', -addBalance);
				Utils.apiPostCall("/api/opencase/upgrade/", params)
						.then(resp => {
							if (resp.data.success) {
								this.startUpgradeAnimation(resp.data);
							} else {
								Utils.userAlert('Возникла ошибка при апгрейде', resp.data.error, 'warn');
								this.upgradeStarted = false;
								this.$store.commit('changeBalance', addBalance);
							}

						})
						.catch(err => {
							Utils.userAlert('Возникла ошибка при апгрейде', err.response.statusText, 'error');
							this.upgradeStarted = false;
							this.$store.commit('changeBalance', addBalance);
						});

			},
			startUpgradeAnimation(data) {
				this.upgradeRotate = 360 + data.percent * 360;
				setTimeout(() => {
					if (this.destroyed) {
						return;
					}
					if (data.won) {
						this.endState = 'success';
						data.item.name = data.item.name.replace('StatTrak™', '<span class="stattrak-color">StatTrak™</span>');
						this.wonItem = data.item;
						Utils.playSound("ItemReveal");
					} else {
						this.endState = 'fail';
					}
				}, 5000);
			},
			refreshPage() {
				Object.assign(this.$data, this.$options.data());
				this.getPageData();
			},
			saleItem() {
				if (this.inAction) {
					return;
				}
				this.inAction = true;
				Utils.apiPostCall("/api/opencase/sale/" + this.wonItem.ID + "/")
						.then(resp => {
							if (resp.data.success) {
								this.$store.commit('changeBalance', this.wonItem.price);
								this.refreshPage();
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
			toContractItem() {
				this.$router.push({name: "contracts", params: {selectedItemsIds: [parseInt(this.wonItem.ID)]}});
			},
		},
		computed: {
			isLogin() {
				return this.$store.getters.isLogin;
			},
			userData() {
				return this.$store.getters.userData;
			}
		}
	}
</script>