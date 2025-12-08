<template>
	<div class="main-header">
		<header>
			<div class="header_block flex">
				<router-link to="/" class="header__logo"></router-link>
				<div class="header__menu flex">
					<ul class="header__list list_left flex">
						<li><router-link to="/" active-class="active" class="header__link" exact>Главная</router-link><span></span><span></span><span></span></li>
						<li><router-link to="/contracts/" active-class="active" class="header__link" exact>Контракты</router-link><span></span><span></span><span></span></li>
						<li><router-link to="/upgrade/" active-class="active" class="header__link" exact>UpGrade</router-link><span></span><span></span><span></span></li>
						<li><router-link to="/battles/" active-class="active" class="header__link" exact>Battles</router-link><span></span><span></span><span></span></li>
					</ul>
					<ul class="header__list list_right flex">
						<li><router-link to="/livetrade/" active-class="active" class="header__link" exact>Трейды ботов</router-link><span></span><span></span><span></span></li>
						<li><router-link to="/top/" active-class="active" class="header__link" exact>ТОП Везунчиков</router-link><span></span><span></span><span></span></li>
					</ul>
				</div>
				<div class="header_contacts flex">
					<template v-if="hasUserData">
						<div v-if="userData.login" class="log_in flex">
							<div class="user_avatar">
								<router-link to="/profile/">
									<img :src="userData.image" :alt="userData.name">
								</router-link>
								<a href="/steamauth/logout/" class="log_out"><span></span><span></span></a>
							</div>
							<div class="user_information">
								<router-link to="/profile/" class="user_name" tag="div">{{userData.name}}</router-link>
								<div class="user_cash" data-popup="addBalance">{{userData.balance.toLocaleString('ru-RU')}}</div>
							</div>
						</div>
						<a v-else href="/?login" class="steam_log-in">Войти через <span>Steam</span></a>
					</template>
					<a :href="VK_URL" class="link_vk" target="_blank"></a>
				</div>
			</div>
		</header>
		<div class="header_roulette flex">
			<router-link :to="'/profile/'+goodItem.user_id+'/'" v-if="goodItem" class="chic_drop chic_drop-yellow flex" :class="[goodItem.rarity, goodItem.source_css_class]">
				<div class="chic_drop_description">
					<div class="chic_drop__title">Шикарный дроп</div>
					<div class="gun_name" v-html="clearItemQuality(goodItem.name)"></div>
				</div>
				<div class="gun_img">
					<img :src="goodItem.image" :alt="goodItem.alt_name">
				</div>
				<div class="dropped">
					<div class="dropped__case">
						<div class="case_image">
							<img v-if="goodItem.from > 0" :src="goodItem.source_img" :alt="goodItem.source_img_alt">
							<img v-else-if="goodItem.from == 0" src="/tpl/maybedrop/img/contract.png" alt="Контракт">
							<img v-else-if="goodItem.from == -1" src="/tpl/maybedrop/img/upgrade.png" alt="Апгрейд">
							<img v-else-if="goodItem.from == -2" src="/tpl/maybedrop/img/battle.png" alt="Батл">
						</div>
						<div class="case_name">{{goodItem.source_img_alt}}</div>
					</div>
					<div class="dropped_user">
						<div class="user_image"><img :src="goodItem.user_img" :alt="goodItem.user_name"></div>
						<div class="user_name">{{goodItem.user_name}}</div>
					</div>
				</div>
			</router-link>
			<div class="guns_block_roulette flex">
				<router-link :to="'/profile/'+item.user_id+'/'" v-for="item in droppedItems" :key="item.id" class="gun_item_roulette worth_blue" :class="[item.rarity, item.source_css_class]">
					<div class="gun_img">
						<img :src="item.image" :alt="item.alt_name">
					</div>
					<div class="gun_name" v-html="clearItemQuality(item.name)"></div>
					<div class="dropped">
						<div class="dropped__case">
							<div class="case_image">
								<img v-if="item.from > 0" :src="item.source_img" :alt="item.source_img_alt">
								<img v-else-if="item.from == 0" src="/tpl/maybedrop/img/contract.png" alt="Контракт">
								<img v-else-if="item.from == -1" src="/tpl/maybedrop/img/upgrade.png" alt="Апгрейд">
								<img v-else-if="item.from == -2" src="/tpl/maybedrop/img/battle.png" alt="Батл">
							</div>
							<div class="case_name">{{item.source_img_alt}}</div>
						</div>
						<div class="dropped_user">
							<div class="user_image"><img :src="item.user_img" :alt="item.user_name"></div>
							<div class="user_name">{{item.user_name}}</div>
						</div>
					</div>
				</router-link>
			</div>
		</div>
		<balance-popup></balance-popup>
	</div>
</template>
<script>
	import BalancePopup from '../popup/BalancePopup';
	export default {
		components: {
			BalancePopup
		},
		data: () => ({
				droppedItems: [],
				droppedItemsInprogress: false,
				droppedItemsTimeout: false,
				goodItem: false,
				destroyed: false
			}),
		mounted() {
			this.getDroppedItems(true);
			this.$centrifuge.subscribe("addDroppedItem", (resp) => {
				if (resp.data.success) {
					this.addNewDroppedItems(resp.data.items);
				}
			});
			this.$eventBus.$on('centrifugeDisconnected', this.getDroppedItems);
		},
		beforeDestroy() {
			this.destroyed = true;
			clearTimeout(this.droppedItemsTimeout);
			this.$eventBus.$off('centrifugeDisconnected', this.getDroppedItems);
			this.$centrifuge.getSub("addDroppedItem").unsubscribe();
		},
		methods: {
			addNewDroppedItems(items) {
				if (this.droppedItems.length <= 0) {
					this.droppedItems = items;
				} else {
					for (let i = 0; i < items.length; i++) {
						let find = false;
						for (let j = 0; j < this.droppedItems.length; j++) {
							if (this.droppedItems[j].id == items[i].id) {
								find = true;
								break;
							}
						}
						if (!find) {
							if (!items[i].waittime) {
								items[i].waittime = 0;
							}
							if (items[i].waittime) {
								setTimeout(() => {
									this.droppedItems.unshift(items[i]);
									if (items[i].price >= 1000) {
										this.goodItem = items[i];
									}
								}, items[i].waittime * 1000);
							} else {
								this.droppedItems.unshift(items[i]);
								if (items[i].price >= 1000) {
									this.goodItem = items[i];
								}
							}
						}

					}
					this.droppedItems.splice(100, this.droppedItems.length);
				}
			},
			getDroppedItems(force = false) {
				if (!force && this.$centrifugeConnected || this.droppedItemsInprogress) {
					return;
				}
				let params = {};
				if (this.droppedItems.length > 0) {
					params.lastupdate = this.droppedItems[0].time;
				}
				this.droppedItemsInprogress = true;
				Utils.apiPostCall("/api/opencase/getnewdrop/", params)
						.then(resp => {
							if (resp.data.success) {
								this.addNewDroppedItems(resp.data.items);
								if (resp.data.goodItem) {
									this.goodItem = resp.data.goodItem;
								}
							}
							this.droppedItemsInprogress = false;
							if (!this.destroyed) {
								this.droppedItemsTimeout = setTimeout(() => {
									this.getDroppedItems();
								}, 6000);
							}
						})
						.catch(err => {
							this.droppedItemsInprogress = false;
							if (!this.destroyed) {
								this.droppedItemsTimeout = setTimeout(() => {
									this.getDroppedItems();
								}, 6000);
							}
						});
			}
		},
		computed: {
			userData() {
				return this.$store.getters.userData;
			},
			hasUserData() {
				return this.$store.getters.hasUserData;
			}
		},
		watch: {
			$route(to, from) {
				this.$store.dispatch('getUserData');
			}

		}
	}
</script>
