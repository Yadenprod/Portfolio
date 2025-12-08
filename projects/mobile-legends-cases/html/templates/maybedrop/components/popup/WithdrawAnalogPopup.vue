<template>
	<div v-if="isLogin && withdrowAnalogItemData" id="withdrawAnalog" class="modal-window widthdrow-modal">
		<div class="title">
			Вывод предмета
		</div>
		<div class="info">
			К сожалению в данный момент мы не смогли подобрать нужный лот для покупки. Вместо него мы можем предложить вам следующий предмет.<br>
			<span v-if="withdrowAnalogItemData.balance > 0">Дополнительно вам на баланс начислится {{withdrowAnalogItemData.balance}} Р</span>
		</div>		
		<div class="item-wrap">
			<div class="gun_item" :class="withdrowAnalogItemData.analog.rarity">
				<div class="gun_img">
					<img :src="withdrowAnalogItemData.analog.image" :alt="withdrowAnalogItemData.analog.name">
				</div> 
				<div class="gun_name" v-html="statTrackName(withdrowAnalogItemData.analog.name)"></div> 
				<div class="gun_cost">{{withdrowAnalogItemData.analog.price}}</div>
			</div>
		</div>
		<div class="btns-wrap">
			<button class="modal-btn" @click="withdrawItem">Забрать</button>
			<button class="modal-btn empty" @click="close">Отмена</button>
		</div>
	</div>
</template>
<script>
	export default {
		props: {
			withdrowAnalogItemData: false
		},
		data: () => ({
				itemActionInProgress: false
			}),
		mounted() {
			$(document).on('click', '#withdrawAnalog', () => {
				return false;
			});
			$(document).on('click', 'body', () => {
				this.$emit('closeWithdrawAnalogModal');
				return false;
			});
		},
		beforeDestroy() {
			$(document).off('click', '#withdrawAnalog');
			$(document).off('click', 'body');
		},
		methods: {
			close() {
				this.$emit('closeWithdrawAnalogModal');
			},
			statTrackName(name) {
				return name.replace('StatTrak™', '<span class = "stattrak-color">StatTrak™</span>');
			},
			withdrawItem() {
				let item = this.withdrowAnalogItemData.item;
				if (this.itemActionInProgress || item.disable) {
					return;
				}
				this.itemActionInProgress = true;
				this.$set(item, 'disable', true);
				let balance = this.withdrowAnalogItemData.balance;
				Utils.apiPostCall("/api/opencase/withdraw/analogs/" + item.id + "/", {analog: this.withdrowAnalogItemData.analog.id})
						.then(resp => {
							if (resp.data.success) {
								item.status = 1;
								if (balance > 0) {
									this.$store.commit('changeBalance', balance);
								}
								Utils.userAlert(resp.data.msg, '', 'success');
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
				this.close();
			}
		},
		computed: {
			isLogin() {
				return this.$store.getters.isLogin;
			}
		}
	}
</script>