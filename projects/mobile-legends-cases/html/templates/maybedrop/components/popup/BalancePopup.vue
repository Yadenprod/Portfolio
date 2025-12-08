<template>
	<div v-if="isLogin" id="addBalance" class="payments-refillblock">
		<div class="payments-block">
			<div class="pb-header">Пополнение баланса</div>
			<div class="inner-refill">
				<div class="inner-refill__tabs">
					<div class="inner-refill__tab-item active standart-tab ui-controller">Стандартный метод</div>
				</div>
				<div class="inner-refill__form">
					<form class="payments-form" name="payment" method="post" action="/deposite/uniform/" accept-charset="UTF-8">
						<div class="inner-refill__input inner-refill__input_promocode">
							<div class="pb-input payPromoCodeBlock">
								<div class="pb-inputdescr discount">{{promoMsg}}</div>
							</div>
							<input type="text" v-model="promocode" @input="checkPromo" name="ik_x_promo" placeholder="Промокод (при наличии)">
						</div>
						<div class="inner-refill__input inner-refill__input_amount">
							<input type="number" placeholder="500 рублей" name="amount">
						</div>
						<input type="submit" class="button inner-refill__btn inner-refill__btn_standart" value="Пополнение баланса">
					</form>
				</div>
			</div>
		</div>
		<div class="payments-footer">
			Баланс на сайте пополняется моментально, но если этого не произошло в течение часа, напишите нам на почту
			<a href="mailto:support@maybedrop.ru" class="payments-link">support@maybedrop.ru</a>,
			указав подробные данные платежа.
		</div>
		<div class="payments-logos payments-logos_is-ru">
			<div class="pay_item pay_item-mastercard"></div>
			<div class="pay_item pay_item-qiwi"></div>
			<div class="pay_item pay_item-visa"></div>
			<div class="pay_item pay_item-webmoney"></div>
			<div class="pay_item pay_item-yandex"></div>
		</div>
	</div>
</template>
<script>
	export default {
		data: () => ({
				promocode: '',
				promoMsg: '',
				promoTimeout: false
			}),
		mounted() {
			$(document).on('click', '[data-popup="addBalance"]', () => {
				$('#addBalance').addClass('open').addClass('animate');

				$(document).on('click', '#addBalance', (e) => {
						e.stopPropagation() 
				});
				$(document).on('click', 'body', () => {
					if ($('#addBalance').hasClass('open')) {
						$('#addBalance').removeClass('open').removeClass('animate');
						$(document).off('click', '#addBalance');
						$(document).off('click', 'body');
						return false;
					}
				});

				return false;
			});

		},
		beforeDestroy() {
			$(document).off('click', '[data-popup="addBalance"]');
		},
		methods: {
			checkPromo() {
				if (this.promoTimeout) {
					clearTimeout(this.promoTimeout);
				}
				this.promoMsg = '';
				if (this.promocode.length > 0) {
					this.promoTimeout = setTimeout(() => {
						Utils.apiPostCall("/api/percent/promo/check/", {promo: this.promocode})
								.then(resp => {
									if (resp.data.success) {
										this.promoMsg = resp.data.msg;
									} else {
										this.promoMsg = resp.data.error;
									}
								})
								.catch(err => {
									Utils.userAlert('Возникла ошибка при проверке промокода', err.response.statusText, 'error');
								});
					}, 1000);
				}
			}
		},
		computed: {
			isLogin() {
				return this.$store.getters.isLogin;
			}
		}
	}
</script>