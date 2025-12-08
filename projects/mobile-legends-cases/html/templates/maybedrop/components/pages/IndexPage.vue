<template>
	<div class="centerblock">
		<main v-if="casesData" id="main" class="site-main" role="main">
			<div class="main_banner">
				<div class="main_parallax"></div>
				<div class="bullets_parallax"></div>
				<img class="conter_left revealator-once revealator-slideright" src="/tpl/maybedrop/img/conter_left.png" alt="">
				<img class="conter_right revealator-once revealator-slideleft" src="/tpl/maybedrop/img/conter_right.png" alt="">
				<div class="text_block">
					<h1>ОТКРЫВАЙ <span>КЕЙСЫ</span></h1>
					<div class="subtitle">counter strike: global offensive</div>
					<ul v-if="stats" class="banner_list flex">
						<li class="user">{{stats.today_online.toLocaleString('ru-RU')}} пользоваелей сегодня</li>
						<li class="contract">{{stats.today_count_create_contracts.toLocaleString('ru-RU')}} Создано контрактов</li>
						<li class="case">{{stats.today_count_open_case.toLocaleString('ru-RU')}} Открыто кейсов</li>
					</ul>
				</div>
				<div class="case_images">
					<img class="base_layer" src="/tpl/maybedrop/img/case.png" alt="">
					<img class="shadow" src="/tpl/maybedrop/img/shadow.png" alt="">
					<img class="ray-1" src="/tpl/maybedrop/img/ray-1.png" alt="">
					<img class="ray-2" src="/tpl/maybedrop/img/ray-2.png" alt="">
					<img class="ray-3" src="/tpl/maybedrop/img/ray-3.png" alt="">
					<img class="ray-4" src="/tpl/maybedrop/img/ray-4.png" alt="">
					<img class="ray-5" src="/tpl/maybedrop/img/ray-5.png" alt="">
					<div class="arrow_24">
						<img class="num_24" src="/tpl/maybedrop/img/24.png" alt="">
						<img class="arrow" src="/tpl/maybedrop/img/arrow.png" alt="">
					</div>
				</div>
				<div v-if="stats" class="main_icons_block flex">
					<router-link to="/" class="icons_item">
						<div class="icon_image"><img src="/tpl/maybedrop/img/main_icon-1.png" alt=""></div>
						<div class="icon_information">
							<div class="icon_title">Кейсы</div>
							<div class="icon_quantity">{{stats.count_open_case.toLocaleString('ru-RU')}}</div>
						</div>
					</router-link>
					<router-link to="/contracts/" class="icons_item">
						<div class="icon_image"><img src="/tpl/maybedrop/img/main_icon-2.png" alt=""></div>
						<div class="icon_information">
							<div class="icon_title">Контракты</div>
							<div class="icon_quantity">{{stats.count_create_contracts.toLocaleString('ru-RU')}}</div>
						</div>
					</router-link>
					<router-link to="/upgrade/" class="icons_item">
						<div class="icon_image"><img src="/tpl/maybedrop/img/main_icon-4.png" alt=""></div>
						<div class="icon_information">
							<div class="icon_title">Апгрейд</div>
							<div class="icon_quantity">{{stats.count_upgrade.toLocaleString('ru-RU')}}</div>
						</div>
					</router-link>
					<router-link to="/battles/" class="icons_item">
						<div class="icon_image"><img src="/tpl/maybedrop/img/main_icon-5.png" alt=""></div>
						<div class="icon_information">
							<div class="icon_title">Сражения</div>
							<div class="icon_quantity">{{stats.count_battles.toLocaleString('ru-RU')}}</div>
						</div>
					</router-link>
					<router-link to="/top/" class="icons_item">
						<div class="icon_image"><img src="/tpl/maybedrop/img/main_icon-6.png" alt=""></div>
						<div class="icon_information">
							<div class="icon_title">Пользователи</div>
							<div class="icon_quantity">{{stats.count_reg_users.toLocaleString('ru-RU')}}</div>
						</div>
					</router-link>
					<router-link to="/top/" class="icons_item">
						<div class="icon_image"><img src="/tpl/maybedrop/img/main_icon-7.png" alt=""></div>
						<div class="icon_information">
							<div class="icon_title">Онлайн</div>
							<div class="icon_quantity">{{stats.online.toLocaleString('ru-RU')}}</div>
						</div>
					</router-link>
				</div>
			</div>
			<div class="advantages">
				<img class="conter_right-2" src="/tpl/maybedrop/img/conter_right-2.png" alt="">
				<img class="bullet" src="/tpl/maybedrop/img/bullet_in_advantages.png" alt="">
				<div class="items_block flex">
					<div class="item">
						<div class="item_thumb"><img src="/tpl/maybedrop/img/advantages_item-1.png" alt=""></div>
						<h4>ТОПовый шмот</h4>
					</div>
					<div class="item">
						<div class="item_thumb"><img src="/tpl/maybedrop/img/advantages_item-2.png" alt=""></div>
						<h4>частые подарки</h4>
					</div>
					<div class="item">
						<div class="item_thumb"><img src="/tpl/maybedrop/img/advantages_item-3.png" alt=""></div>
						<h4>честно и прозрачно</h4>
					</div>
				</div>
			</div>
			<div class="popular_cases">
				<div class="form_block">
					<div class="search flex">
						<form @submit.prevent>
							<input v-model="research" placeholder="Название кейса" type="search">
							<button type="submit"></button>
						</form>
						<div class="selection">
							<div class="checkboxes">
								<input v-model="priceCheckbox[0]" :true-value="{min: 1, max: 19}" :false-value="{}" type="checkbox" class="custom-checkbox" id="custom-1" name="custom" value="yes">
									   <label for="custom-1">1 - 19P</label>
								<input v-model="priceCheckbox[1]" :true-value="{min: 20, max: 49}" :false-value="{}" type="checkbox" class="custom-checkbox" id="custom-2" name="custom" value="yes">
									   <label for="custom-2">20 - 49P</label>
								<input v-model="priceCheckbox[2]" :true-value="{min: 50, max: 99}" :false-value="{}" type="checkbox" class="custom-checkbox" id="custom-3" name="custom" value="yes">
									   <label for="custom-3">50 - 99P</label>
								<input v-model="priceCheckbox[3]" :true-value="{min: 100, max: -1}" :false-value="{}" type="checkbox" class="custom-checkbox" id="custom-4" name="custom" value="yes">
									   <label for="custom-4">100+P</label>
							</div>
						</div>
					</div>
				</div>
			</div>
			<template v-if="casesData">
				<div v-for="caseData in casesData" v-if="allowCategoryOutput(caseData.cases)" class="limited_edition">
					<h2><span></span>{{caseData.name}}<span></span></h2>
					<div class="cases_block flex">
						<div class="border_item" v-for="ocase in caseData.cases" v-if="allowCaseOutput(ocase)" :key="ocase.id" >
							<router-link :to="'/case/'+ocase.key+'/'" class="cases_item">
								<div class="item_thumb"><img :src="ocase.caseImage" :alt="ocase.name"></div>
								<div class="price">{{ocase.salePrice}} <span>руб</span></div>
							</router-link>
						</div>
					</div>
				</div>
			</template>
			<div class="live_reviews">
				<div class="reviews_block">
					<div id="vk_groups"></div>
				</div>
			</div>
		</main>
	</div>
</template>
<script>
	export default {
		data: () => ({
				casesData: false,
				animInterval: false,
				animIndex: 0,
				research: '',
				priceCheckbox: [],
				stats: false,
				statsInProgress: false,
				statTimeout: false,
				destroyed: false
			}),
		mounted() {
			this.animInterval = setInterval(() => {
				this.animIndex++;
				if (this.animIndex % 5 == 0) {
					$('.shadow').toggleClass("hovered");
				}
				if (this.animIndex % 6 == 0) {
					$('.ray-2').toggleClass("hovered");
				}
				if (this.animIndex % 7 == 0) {
					$('.ray-3').toggleClass("hovered");
				}
				if (this.animIndex % 10 == 0) {
					$('.arrow').toggleClass("rotate");
				}
				if (this.animIndex % 5 == 0) {
					$('.instruction_item .item_thumb img').toggleClass("img_shadow");
				}
			}, 100);
			$(document).on('mousemove', 'body', (e) => {
				let x = e.clientX / window.innerWidth;
				let y = e.clientY / window.innerHeight;
				if ($('.bullets_parallax').length > 0) {
					$('.bullets_parallax').css('transform', 'translate(-' + x * 50 + 'px, -' + y * 50 + 'px)');
				}
				if ($('.main_parallax').length > 0) {
					$('.main_parallax').css('transform', 'translate(-' + x * 20 + 'px, -' + y * 20 + 'px)');
				}
				if ($('.advantages_bullet').length > 0) {
					$('.advantages_bullet').css('transform', 'translate(-' + x * 20 + 'px, -' + y * 20 + 'px)');
				}
			});
			VK.Widgets.Group("vk_groups", {mode: 3, width: "auto", height: "186", no_cover: 0}, 198007059);
			Utils.setTitle("");
			this.getPageData();
			this.getStats(true);
			this.$centrifuge.subscribe("updateStats", (resp) => {
				if (resp.data.success) {
					this.stats = resp.data;
				}
			});
			this.$eventBus.$on('centrifugeDisconnected', this.getStats);
		},
		beforeDestroy() {
			this.destroyed = true;
			$(document).off('mousemove', 'body');
			clearInterval(this.animInterval);
			clearTimeout(this.statTimeout);
			this.$eventBus.$off('centrifugeDisconnected', this.getStats);
			this.$centrifuge.getSub("updateStats").unsubscribe();
		},
		methods: {
			getStats(force = false) {
				if (!force && this.$centrifugeConnected || this.statsInProgress) {
					return;
				}
				this.statsInProgress = true;
				Utils.apiPostCall("/api/opencase/getstat/")
						.then(resp => {
							if (resp.data.success) {
								this.stats = resp.data;
							}
							this.statsInProgress = false;
							if (!this.destroyed) {
								this.statTimeout = setTimeout(() => {
									this.getStats();
								}, 10000);
							}
						})
						.catch(err => {
							this.statsInProgress = false;
							if (!this.destroyed) {
								this.statTimeout = setTimeout(() => {
									this.getStats();
								}, 10000);
							}
						});
			},
			getPageData() {
				Utils.apiPostCall("/api/casesbycategory/")
						.then(resp => {
							this.casesData = resp.data.casesData;
						});
			},
			allowCategoryOutput(cases) {
				if (cases.length <= 0) {
					return false;
				}
				for (let i in cases) {
					let allowedPrice = false;
					let hasActiveCheckBox = false;
					for (let j in this.priceCheckbox) {
						if (this.priceCheckbox[j].hasOwnProperty('min') && this.priceCheckbox[j].hasOwnProperty('max')) {
							hasActiveCheckBox = true;
							if (cases[i].salePrice >= this.priceCheckbox[j].min && (this.priceCheckbox[j].max <= 0 || cases[i].salePrice <= this.priceCheckbox[j].max)) {
								allowedPrice = true;
								break;
							}
						}
					}
					if (hasActiveCheckBox && !allowedPrice) {
						continue;
					}
					if ((cases[i].type == 0 || cases[i].type == 2) && (this.research.length <= 0 || cases[i].name.toLowerCase().indexOf(this.research) !== -1)) {
						return true;
					}
				}
				return false;
			},
			allowCaseOutput(ocase) {
				let allowedPrice = false;
				let hasActiveCheckBox = false;
				for (let i in this.priceCheckbox) {
					if (this.priceCheckbox[i].hasOwnProperty('min') && this.priceCheckbox[i].hasOwnProperty('max')) {
						hasActiveCheckBox = true;
						if (ocase.salePrice >= this.priceCheckbox[i].min && (this.priceCheckbox[i].max <= 0 || ocase.salePrice <= this.priceCheckbox[i].max)) {
							allowedPrice = true;
							break;
						}
					}
				}
				if (hasActiveCheckBox && !allowedPrice) {
					return false;
				}
				return (ocase.type == 0 || ocase.type == 2) && (this.research.length <= 0 || ocase.name.toLowerCase().indexOf(this.research) !== -1);
			}
		}
	}
</script>