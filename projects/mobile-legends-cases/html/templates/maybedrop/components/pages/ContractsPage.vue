<template>
	<div class="centerblock">
		<main id="main" class="site-main" role="main">
			<h1><span></span>контракты <span></span></h1>
			<template v-if="!wonItem">
				<div class="contracts_block flex">
					<contract-place-elem v-for="index in 10" @removeFromContract="removeFromContract" :key="index" :index="index" :item="(usedItems.length < index ? false : usedItems[index - 1])"></contract-place-elem>
				</div>
				<div class="add_contracts">
					<div class="contracts__circle">
						<div class="contracts__circle-border">
							{{usedItems.length}}/10
							<span>мин. 3</span>
						</div>
					</div>
					<a href="#" @click.prevent="createContract" :class="{'gray-disabled' : usedItems.length < 3}" class="new_contract animation_light">Создать контракт</a>
					<div class="contracts__circle">
						<div class="contracts__circle-border">
							{{currentPrice}} Р
							<span>сумма</span>
						</div>
					</div>
				</div>
			</template>
			<template v-else>
				<div class="drop_items_wrap flex">
					<div class="drop_item">
						<div class="drop_thumb">
							<img :src="'https://steamcommunity-a.akamaihd.net/economy/image/' + wonItem.image +'/300fx200f'" alt="">
						</div>
						<div class="drop_subtitle" v-html="clearItemQuality(wonItem.name)"></div>
					</div>
				</div>
				<div class="drop_item">
					<a href="#" @click.prevent="refreshPage" class="btn-yellow again">Попробовать еще</a>
					<a href="#" @click.prevent="saleDroppedItem" class="btn_sell">Продать за <span>{{wonItem.price}}</span></a>
				</div>		
			</template>
			<template v-if="isLogin && !wonItem">
				<div class="available_items">
					<h2><span></span>доступные для контракта предметы <span></span></h2>
					<div class="available_block flex">
						<div v-for="item in userItems" @click="useForContract(item)" class="gun_item" :class="[item.rarity, {'gray-disabled' : item.used}]">
							 <div class="gun_img">
								<img :src="item.image" :alt="item.imageAlt">
							</div>
							<div class="gun_name" v-html="clearItemQuality(item.name)"></div>
							<div class="gun_cost">{{item.price}}</div>
						</div>
					</div>
				</div>
			</template>
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
	import ContractPlaceElem from '../elems/ContractPlaceElem';
	export default {
		components: {
			ContractPlaceElem
		},
		data: () => ({
				userItems: false,
				usedItems: [],
				inProgress: false,
				wonItem: false
			}),
		props: {
			selectedItemsIds: false
		},
		mounted() {
			Utils.setTitle("Контракты");
			this.getPageData();
		},
		methods: {
			getPageData() {
				Utils.apiPostCall("/api/user/availdrop/")
						.then(resp => {
							if (resp.data.success) {
								for (let i in resp.data.items) {
									if (this.selectedItemsIds && this.selectedItemsIds.includes(parseInt(resp.data.items[i].id)) && this.usedItems.length < 10) {
										resp.data.items[i].used = true;
										this.usedItems.push(resp.data.items[i]);
									} else {
										resp.data.items[i].used = false;
									}
								}
								this.userItems = resp.data.items;
							}
						});
			},
			useForContract(item) {
				if (!this.inProgress && !item.used) {
					if (this.usedItems.length < 10) {
						item.used = true;
						this.usedItems.push(item);
					}
				}
			},
			removeFromContract(index) {
				if (!this.inProgress && index < this.usedItems.length) {
					let item = this.usedItems[index];
					item.used = false;
					this.usedItems.splice(index, 1);
				}
			},
			createContract() {
				if (this.inProgress) {
					return;
				}
				if (this.usedItems.length >= 3 && this.currentPrice > 0) {
					this.inProgress = true;
					let contractItemsId = [];
					for (let i in this.usedItems) {
						contractItemsId.push(this.usedItems[i].id);
					}
					Utils.apiPostCall("/api/opencase/contracts/", {
						items: contractItemsId.join(';')
					})
							.then(resp => {
								if (resp.data.success) {
									resp.data.item.name = resp.data.item.name.replace('StatTrak™', '<span class="stattrak-color">StatTrak™</span>');
									this.wonItem = resp.data.item;
									Utils.playSound("ItemReveal");
								} else {
									Utils.userAlert('Ошибка при создание контракта', resp.data.error, 'warn');
								}
								this.inProgress = false;

							})
							.catch(err => {
								this.inProgress = false;
								Utils.userAlert('Ошибка при создание контракта', err.response.statusText, 'error');
							});
				} else {
					Utils.userAlert('Ошибка при создание контракта', 'Контракт не соответсвует условиям', 'warn')
				}
			},
			refreshPage() {
				Object.assign(this.$data, this.$options.data());
				this.getPageData();
			},
			saleDroppedItem() {
				if (this.inProgress) {
					return;
				}
				this.inProgress = true;
				Utils.apiPostCall("/api/opencase/sale/" + this.wonItem.ID + "/")
						.then(resp => {
							if (resp.data.success) {
								this.$store.commit('changeBalance', this.wonItem.price);
								this.refreshPage();
							} else {
								Utils.userAlert('Возникла ошибка при продаже предмета', resp.data.error, 'warn');
							}
							this.inProgress = false;
						})
						.catch(err => {
							Utils.userAlert('Возникла ошибка при продаже предмета', err.response.statusText, 'error');
							this.inProgress = false;
						});
			}
		},
		computed: {
			currentPrice() {
				let price = 0;
				for (let i in this.usedItems) {
					price += parseInt(this.usedItems[i].price);
				}
				return price;
			},
			isLogin() {
				return this.$store.getters.isLogin;
			}
		}
	}
</script>