<template>
	<div v-if="isLogin && sellData" id="sellAllDrops" class="modal-window">
		<div class="title">
			Продажа предметов
		</div>
		<div class="info">
			Предметы: <span>{{sellData.count.toLocaleString('ru-RU')}}</span><br>
			Продать за <span>{{sellData.price.toLocaleString('ru-RU')}}</span> Р?
		</div>		
		<div class="btns-wrap">
			<button class="modal-btn" @click="sellAll">Продать</button>
			<button class="modal-btn empty" @click="close">Отмена</button>
		</div>
	</div>
</template>
<script>
	export default {
		props: {
			sellData: false
		},
		mounted() {
			$(document).on('click', '#sellAllDrops', () => {
				return false;
			});
			$(document).on('click', 'body', () => {
				this.$emit('closeSellAllModal');
				return false;
			});
		},
		beforeDestroy() {
			$(document).off('click', '#sellAllDrops');
			$(document).off('click', 'body');
		},
		methods: {
			close() {
				this.$emit('closeSellAllModal');
			},
			sellAll() {
				this.$emit('saleAll');
			}
		},
		computed: {
			isLogin() {
				return this.$store.getters.isLogin;
			}
		}
	}
</script>