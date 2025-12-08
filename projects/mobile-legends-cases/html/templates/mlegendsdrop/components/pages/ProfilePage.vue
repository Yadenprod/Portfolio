<template>
	<div class="centerblock">
		<main v-if="loaded && profile" id="main" class="site-main page_battles" role="main">
			<h1><span></span><div class="content">{{profile.name}}</div><span></span></h1>
			<div class="user_data flex">
				<div class="user_data__left">
					<ul class="action_information flex">
						<li>
							<div class="information_thumb"><img src="/tpl/maybedrop/img/pa_list-icon1.png" alt=""></div>
							<div class="information_name">Апгрейд</div>
							<div class="information_statistics flex">
								<div class="quantity quantity_successful">{{profile.counts.upgrade.won}}</div>
								<div class="quantity quantity_unsuccessful">{{profile.counts.upgrade.lost}}</div>
							</div>
						</li>
						<li>
							<div class="information_thumb"><img src="/tpl/maybedrop/img/pa_list-icon2.png" alt=""></div>
							<div class="information_name">Сражения</div>
							<div class="information_statistics flex">
								<div class="quantity quantity_victories">{{profile.counts.battle.won}}</div>
								<div class="quantity quantity_defeats">{{profile.counts.battle.lost}}</div>
								<div class="quantity quantity_drawes">{{profile.counts.battle.draw}}</div>
							</div>
						</li>
						<li>
							<div class="information_thumb"><img src="/tpl/maybedrop/img/pa_list-icon3.png" alt=""></div>
							<div class="information_name">Контракты</div>
							<div class="information_statistics">
								<div class="quantity quantity_contracts">{{profile.counts.contract}}</div>
							</div>
						</li>
						<li>
							<div class="information_thumb"><img src="/tpl/maybedrop/img/pa_list-icon4.png" alt=""></div>
							<div class="information_name">Кейсы</div>
							<div class="information_statistics">
								<div class="quantity quantity_cases">{{profile.counts.case}}</div>
							</div>
						</li>
					</ul>
				</div>
				<div class="user_data__center">
					<div class="user_id">ID #{{profile.id}}</div>
					<div class="user_information">
						<div class="user_thumb">
							<!--<div class="image"></div>-->
							<img :src="profile.image" :alt="profile.name">
						</div>
						<a v-if="!profile.isOther && userData" href="#" @click.prevent data-popup="addBalance" class=" btn-yellow user_balance">
							<div class="balance_number">
								{{userData.balance.toLocaleString('ru-RU')}}
							</div>
							<p>пополнение баланса</p>
						</a>
					</div>
					<template v-if="!profile.isOther">
						<div class="url_trade flex" @click="tradeLinkIsOpen = !tradeLinkIsOpen">
							<div class="reset_image"></div>
							<p>Trade-URL</p>
						</div>
						<div class="trade-link" :class="{'open' : tradeLinkIsOpen}">
							 <div class="trade-link__title">Найти ссылку можно <a :href="'http://steamcommunity.com/profiles/'+profile.steamId+'/tradeoffers/privacy#trade_offer_access_url/'" target="_blank">на сайте Steam</a></div>
							<div class="trade-link__form">
								<input class="trade-link__input success" v-model="profile.tradeLink" placeholder="https://steamcommunity.com/tradeoffer/new/?partner=1094534594&token=123456579">
								<button  @click="saveTradeUrl" class="trade-link__btn button button_main">Сохранить</button>
							</div>
						</div>
					</template>
				</div>
				<div class="user_data__right">
					<div class="profile_information flex">
						<div class="profile_information_item">
							<div class="information_thumb"><img src="/tpl/maybedrop/img/pa_list-icon-calendar.png" alt=""></div>
							<div class="information_name">На сайте</div>
							<div class="information_statistics">
								<div class="days">{{profile.timeFromReg}}</div>
							</div>
						</div>
						<a :href="'https://steamcommunity.com/profiles/'+profile.steamId+'/'" target="_blank"class="profile_information_item profile_steam">
							<div class="information_thumb"><img src="/tpl/maybedrop/img/pa_list-icon-steam.png" alt=""></div>
							<div class="information_name">Профиль в Steam</div>
						</a>
					</div>
					<div class="achievements flex">
						<div class="best_drop" v-if="profile.bestDrop">
							<div class="gun_item" :class="profile.bestDrop.rarity">
								<div class="gun_img">
									<img :src="profile.bestDrop.image" :alt="profile.bestDrop.imageAlt">
								</div>
								<div class="gun_name" v-html="clearItemQuality(profile.bestDrop.name)"></div>
							</div>
							<div class="best_drop__signature">Лучший дроп</div>
						</div>
						<router-link tag="div" :to="'/case/'+profile.favoriteCase.key+'/'"  class="best_case" v-if="profile.favoriteCase">
									 <div class="best_case__thumb">
								<img :src="profile.favoriteCase.image" :alt="profile.favoriteCase.name">
							</div>
							<div class="best_case__signature">Любимый кейс</div>
						</router-link>
					</div>
				</div>
			</div>

			<div class="container_1770">
				<div class="header_case_contents">
					<div class="header_top">
						<ul class="header_top__menu flex">
							<li><a :class="{'active' : activeItemsTab == 'items'}" @click.prevent="setActiveItemsTab('items')" href="#">Дропы</a></li>
							<li><a :class="{'active' : activeItemsTab == 'contracts'}" @click.prevent="setActiveItemsTab('contracts')" href="#">Контракты</a></li>
							<li><a :class="{'active' : activeItemsTab == 'battles'}" @click.prevent="setActiveItemsTab('battles')" href="#">Сражения</a></li>
						</ul>
					</div>
					<div v-if="this.activeItemsTab == 'items'" class="header_bottom flex">
						<template v-if="!profile.isOther">
							<a href="#"  @click.prevent="saleAllInit" class="btn-yellow sell">Продать все</a>
							<a href="#" @click.prevent="toggleOnlyNotSaled" class="gray_btn">
								<span v-if="isOnlyNotSaled">Доступные для продажи</span>
								<span v-else>Все</span>
							</a>
						</template>
						<div class="selection">
							<div class="checkboxes">
								<input type="radio" id="custom-1" class="custom-checkbox" @click="setItemsPriceFilter(0, 0)" :checked="isActiveItemsPriceFilter(0, 0)">
								<label for="custom-1">Все</label>
								<input type="radio" id="custom-2" class="custom-checkbox" @click="setItemsPriceFilter(0, 9)" :checked="isActiveItemsPriceFilter(0, 9)">
								<label for="custom-2">0-9P</label>
								<input type="radio" id="custom-3" class="custom-checkbox" @click="setItemsPriceFilter(10, 49)" :checked="isActiveItemsPriceFilter(10, 49)">
								<label for="custom-3">10-49P</label>
								<input type="radio" id="custom-4" class="custom-checkbox" @click="setItemsPriceFilter(50, 99)" :checked="isActiveItemsPriceFilter(50, 99)">
								<label for="custom-4">50-99P</label>
								<input type="radio" id="custom-5" class="custom-checkbox" @click="setItemsPriceFilter(100, 999)" :checked="isActiveItemsPriceFilter(100, 999)">
								<label for="custom-5">100-999P</label>
								<input type="radio" id="custom-6" class="custom-checkbox" @click="setItemsPriceFilter(1000, 0)" :checked="isActiveItemsPriceFilter(1000, 0)">
								<label for="custom-6">1000+P</label>
							</div>
						</div>
					</div>
				</div>
				<template v-if="this.activeItemsTab == 'items'" >
					<div class="case_contents flex">
						<template v-if="items.list && items.list.length > 0">
							<div v-for="item in items.list" class="gun_item" :class="[item.rarity, item.source_css_class]">
								 <div class="gun_img">
									<img :src="item.image" :alt="item.alt_name">
								</div>
								<div class="gun_name" v-html="item.name"></div>
								<template v-if="!profile.isOther && (item.status == 0 || item.status == 6)">
									<a href="#" class="gun_cost for_sale"  @click.prevent="saleItem(item)" title="Продать">{{item.price}}</a>
									<template v-if="item.withdrawable" >
										<a href="#" @click.prevent="withdrawItem(item)" class="withdraw">Запросить с маркета</a>
										<a href="#" @click.prevent="withdrawItem(item)" class="check_sold" title="Забрать"></a> 
									</template>
									<template v-else>
										<div class="check_in_stock"></div> 
									</template>							
								</template>
								<template v-else>
									<template v-if="profile.isOther && (item.status == 0 || item.status == 6)">
										<div class="gun_cost for_sale" title="Ожидает">{{item.price}}</div>
										<div class="check_sold" title="Ожидает"></div>
									</template>
									<template v-else-if="item.status == 1">
										<div class="gun_cost" title="Отправлен">{{item.price}}</div>
										<div class="check_in_stock" title="Отправлен"></div>
									</template>
									<template v-else-if="item.status == 2">
										<div class="gun_cost" title="Получен">{{item.price}}</div>
										<div class="check_in_stock" title="Получен"></div>
									</template>
									<template v-else-if="item.status == 3">
										<div class="gun_cost" title="Продан">{{item.price}}</div>
										<div class="check_in_stock" title="Продан"></div>
									</template>
									<template v-else-if="item.status == 4">
										<div class="gun_cost" title="Добавлен в контракт">{{item.price}}</div>
										<div class="check_in_stock" title="Добавлен в контракт"></div>
									</template>
									<template v-else-if="item.status == 5">
										<div class="gun_cost" title="Ошибка при отправке">{{item.price}}</div>
										<div class="check_in_stock" title="Ошибка при отправке"></div>
									</template>
									<template v-else-if="item.status == 10">
										<div class="gun_cost" title="Использован в апгрейд">{{item.price}}</div>
										<div class="check_in_stock" title="Использован в апгрейд"></div>
									</template>
								</template>
								<div class="dropped">
									<router-link tag="div" :to="item.source_link" class="dropped__case">
										<div class="case_image">
											<img v-if="item.from > 0" :src="item.source_img" :alt="item.source_img_alt">
											<img v-else-if="item.from == 0" src="/tpl/maybedrop/img/contract.png" alt="Контракт">
											<img v-else-if="item.from == -1" src="/tpl/maybedrop/img/upgrade.png" alt="Апгрейд">
											<img v-else-if="item.from == -2" src="/tpl/maybedrop/img/battle.png" alt="Сражение">
										</div>
										<div class="case_name">{{item.source_img_alt}}</div>
									</router-link>
									<div class="dropped_user"></div>
								</div>
							</div>
						</template>						
					</div>
					<template v-if="items.hasMore">
						<a href="#" @click.prevent="getItems" class="btn-yellow bold">
							<template v-if="items.isLoading">Загрузка...</template>
							<template v-else>Показать ещё</template>	
						</a>
					</template>
				</template>
				<template v-else-if="this.activeItemsTab == 'contracts'">
					<div class="contracts_contents flex">
						<template v-if="contracts.list && contracts.list.length > 0">
							<div v-for="contract in contracts.list" class="contracts_item flex">
								<div class="gun_item" :class="contract.rarity">
									<div class="gun_img">
										<img :src="contract.image" :alt="contract.alt_name">
									</div>
									<div class="gun_name" v-html="contract.name"></div>
									<div class="gun_cost">{{contract.price}}</div>
								</div>
								<div class="available_guns">
									<div class="gun_block flex">
										<div  v-for="item in contract.contract_items" class="gun_list">
											<img :src="item.image" :alt="item.alt_name">
										</div>
									</div>
									<div class="contract_sum">
										Стоимость контракта
										<span>
											{{contract.contract_price}}
										</span>
									</div>
								</div>
							</div>
						</template>
					</div>
					<template v-if="contracts.hasMore">
						<a href="#" @click.prevent="getContracts" class="btn-yellow bold">
							<template v-if="contracts.isLoading">Загрузка...</template>
							<template v-else>Показать ещё</template>	
						</a>
					</template>
				</template>
				<template v-else-if="this.activeItemsTab == 'battles'">
					<div class="battles_content flex">
						<template v-if="battles.list && battles.list.length > 0">
							<div v-for="battle in battles.list" class="border" v-if="battle.creator && battle.participant && battle.case">
								<div class="battle_results flex">
									<div class="first_player" :class="{'winner' : (battle.winnerId == -1 || battle.winnerId == battle.creator.id)}">
										 <div class="played_gun">
											<img :src="'http://steamcommunity-a.akamaihd.net/economy/image/' + battle.creator.drop.image" :alt="clearItemQuality(battle.creator.drop.name)">
										</div>
										<div class="player">
											<img :src="battle.creator.image" :alt="battle.creator.name">
										</div>
										<p class="price_gun">{{battle.creator.drop.price}}</p>
									</div>
									<div class="played_case">
										<img :src="battle.case.image" :alt="battle.case.name">
									</div>
									<div class="second_player" :class="{'winner' : (battle.winnerId == -1 || battle.winnerId == battle.participant.id)}">
										 <div class="played_gun">
											<img :src="'http://steamcommunity-a.akamaihd.net/economy/image/' + battle.participant.drop.image" :alt="clearItemQuality(battle.participant.drop.name)">
										</div>
										<div class="player">
											<img :src="battle.participant.image" :alt="battle.participant.name">
										</div>
										<p class="price_gun">{{battle.participant.drop.price}}</p>
									</div>
								</div>
							</div>
						</template>
					</div>
					<template v-if="battles.hasMore">
						<a href="#" @click.prevent="getBattles" class="btn-yellow bold">
							<template v-if="battles.isLoading">Загрузка...</template>
							<template v-else>Показать ещё</template>	
						</a>
					</template>
				</template>
			</div>
			<div class="pay_block flex">
				<div class="pay_item pay_item-mastercard"></div>
				<div class="pay_item pay_item-qiwi"></div>
				<div class="pay_item pay_item-visa"></div>
				<div class="pay_item pay_item-webmoney"></div>
				<div class="pay_item pay_item-yandex"></div>
			</div>
			<withdraw-analog-popup v-if="withdrowAnalogItemData" :withdrowAnalogItemData="withdrowAnalogItemData" @closeWithdrawAnalogModal="closeWithdrawAnalogModal"></withdraw-analog-popup>
			<sell-all-popup v-if="sellAllData" :sellData="sellAllData" @saleAll="saleAll" @closeSellAllModal="closeSellAllModal"></sell-all-popup>
		</main>
		<page-404 v-if="loaded && !profile"></page-404>
	</div>
</template>
<script>
	import WithdrawAnalogPopup from '../popup/WithdrawAnalogPopup';
	import SellAllPopup from '../popup/SellAllPopup';
	export default {
		components: {
			WithdrawAnalogPopup,
			SellAllPopup
		},
		data: () => ({
				loaded: false,
				profile: false,
				activeItemsTab: "items",
				savingTradeLinkStatus: 0,
				promocodeInput: "",
				usingPromocodeStatus: 0,
				itemActionInProgress: false,
				tradeLinkIsOpen: false,
				withdrowAnalogItemData: false,
				sellAllData: false,
				items: {
					list: false,
					page: 0,
					hasMore: true,
					isLoading: false,
					min: 0,
					max: 0,
					onlyNotSaled: false
				},
				contracts: {
					list: false,
					page: 0,
					hasMore: true,
					isLoading: false,
					min: 0,
					max: 0,
					onlyNotSaled: false
				},
				battles: {
					list: false,
					page: 0,
					hasMore: true,
					isLoading: false,
				}
			}),
		props: {
			pageData: {},
		},
		mounted() {
			Utils.setTitle('Профиль');
			this.getPageData();

		},
		methods: {
			getPageData() {
				let url = "/api/user/profile/";
				if (this.$route.params.steamId) {
					url += this.$route.params.steamId + "/";
				}
				Utils.apiPostCall(url)
						.then(resp => {
							if (resp.data.success) {
								this.profile = resp.data.profile;
								this.getItems();
							}
							this.loaded = true;
						})
						.catch(err => {
							this.loaded = true;
						});
			},
			getItems() {
				if (this.items.isLoading) {
					return;
				}
				this.items.isLoading = true;
				Utils.apiPostCall("/api/opencase/getuserdrops/", {
					user_id: this.profile.id,
					page: this.items.page,
					min: this.items.min,
					max: this.items.max,
					notSaled: (this.items.onlyNotSaled ? 1 : 0)
				})
						.then(resp => {
							if (resp.data.success) {
								this.items.page++;
								if (this.items.list) {
									this.items.list = this.items.list.concat(resp.data.items);
								} else {
									this.items.list = resp.data.items;
								}
							} else if (!this.items.list) {
								this.items.list = [];
							}
							this.items.hasMore = !resp.data.not_items;
							this.items.isLoading = false;
						})
						.catch(err => {
							this.items.isLoading = false;
						});
			},
			getContracts() {
				if (this.contracts.isLoading) {
					return;
				}
				this.contracts.isLoading = true;
				Utils.apiPostCall("/api/opencase/getusercontracts/", {
					user_id: this.profile.id,
					page: this.contracts.page,
					min: this.contracts.min,
					max: this.contracts.max,
					notSaled: (this.contracts.onlyNotSaled ? 1 : 0)
				})
						.then(resp => {
							if (resp.data.success) {
								this.contracts.page++;
								if (this.contracts.list) {
									this.contracts.list = this.contracts.list.concat(resp.data.items);
								} else {
									this.contracts.list = resp.data.items;
								}
							} else if (!this.contracts.list) {
								this.contracts.list = [];
							}
							this.contracts.hasMore = !resp.data.not_items;
							this.contracts.isLoading = false;
						})
						.catch(err => {
							this.contracts.isLoading = false;
						});
			},
			getBattles() {
				if (this.battles.isLoading) {
					return;
				}
				this.battles.isLoading = true;
				Utils.apiPostCall("/api/opencase/getuserbattles/", {
					user_id: this.profile.id,
					page: this.battles.page
				})
						.then(resp => {
							if (resp.data.success) {
								this.battles.page++;
								if (this.battles.list) {
									this.battles.list = this.battles.list.concat(resp.data.items);
								} else {
									this.battles.list = resp.data.items;
								}
							} else if (!this.battles.list) {
								this.battles.list = [];
							}
							this.battles.hasMore = !resp.data.not_items;
							this.battles.isLoading = false;
						})
						.catch(err => {
							this.battles.isLoading = false;
						});
			},
			saveTradeUrl() {
				if (this.savingTradeLinkStatus == 1) {
					return;
				}
				this.savingTradeLinkStatus = 1;
				Utils.apiPostCall("/api/opencase/savesettings/", {
					url: this.profile.tradeLink
				})
						.then(resp => {
							if (resp.data.success) {
								this.savingTradeLinkStatus = 2;
								Utils.userAlert('Ссылка успешно сохранена', '', 'success');
							} else {
								this.savingTradeLinkStatus = 3;
								Utils.userAlert('Возникла ошибка при сохранение ссылки', resp.data.error, 'warn');
							}

						})
						.catch(err => {
							this.savingTradeLinkStatus = 3;
							Utils.userAlert('Возникла ошибка при сохранение ссылки', err.response.statusText, 'error');
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
			closeSellAllModal() {
				this.sellAllData = false;
			},
			setActiveItemsTab(tab, hard = false) {
				if (hard || this.activeItemsTab != tab) {
					this.activeItemsTab = tab;
					if (tab == 'items' && !this.items.list) {
						this.getItems();
					} else if (tab == 'contracts' && !this.contracts.list) {
						this.getContracts();
					} else if (tab == 'battles' && !this.battles.list) {
						this.getBattles();
					}
			}
			},
			setItemsPriceFilter(min, max) {
				let data = this.getActiveItemsTabData();
				if (data.min != min || data.max != max) {
					data.list = false;
					data.page = 0;
					data.hasMore = true;
					data.min = min;
					data.max = max;
					this.setActiveItemsTab(this.activeItemsTab, true);
				}
			},
			isActiveItemsPriceFilter(min, max) {
				let data = this.getActiveItemsTabData();
				return data.min == min && data.max == max;
			},
			getActiveItemsTabData() {
				if (this.activeItemsTab == 'items') {
					return this.items;
				} else if (this.activeItemsTab == 'contracts') {
					return this.contracts;
				} else if (this.activeItemsTab == 'battles') {
					return this.battles;
				}
			},
			toggleOnlyNotSaled() {
				let data = this.getActiveItemsTabData();
				data.onlyNotSaled = !data.onlyNotSaled;
				data.list = false;
				data.page = 0;
				data.hasMore = true;
				this.setActiveItemsTab(this.activeItemsTab, true);
			},
			saleAllInit() {
				if (this.itemActionInProgress) {
					return;
				}
				this.itemActionInProgress = true;
				Utils.apiPostCall("/api/opencase/sale/all/info/")
						.then(resp => {
							if (resp.data.success) {
								this.sellAllData = resp.data.data;
							} else {
								Utils.userAlert('Возникла ошибка при продаже предметов', resp.data.error, 'warn');
							}
							this.itemActionInProgress = false;
						})
						.catch(err => {
							this.itemActionInProgress = false;
							Utils.userAlert('Возникла ошибка при продаже предметов', err.response.statusText, 'error');
						});
			},
			saleAll() {
				if (this.itemActionInProgress) {
					return;
				}
				this.sellAllData = false;
				this.itemActionInProgress = true;
				Utils.apiPostCall("/api/opencase/sale/all/")
						.then(resp => {
							if (resp.data.success) {
								this.items.list = false;
								this.items.page = 0;
								this.items.hasMore = true;
								this.contracts.list = false;
								this.contracts.page = 0;
								this.contracts.hasMore = true;
								this.battles.list = false;
								this.battles.page = 0;
								this.battles.hasMore = true;
								this.setActiveItemsTab(this.activeItemsTab, true);
								this.$store.commit('setBalance', resp.data.balance);
								Utils.userAlert(resp.data.msg, '', 'success');
							} else {
								Utils.userAlert('Возникла ошибка при продаже предметов', resp.data.error, 'warn');
							}
							this.itemActionInProgress = false;
						})
						.catch(err => {
							this.itemActionInProgress = false;
							Utils.userAlert('Возникла ошибка при продаже предметов', err.response.statusText, 'error');
						});
			}
		},
		computed: {
			isOnlyNotSaled() {
				let data = this.getActiveItemsTabData();
				return !data.onlyNotSaled;
			},
			userData() {
				return this.$store.getters.userData;
			},
		},
		watch: {
			$route(to, from) {
				Object.assign(this.$data, this.$options.data());
				this.getPageData();
			}

		}
	}
</script>