<template>
	<footer>
		<div class="container_1370 flex">
			<nav class="footer__menu">
				<ul class="footer__list flex">
					<li><router-link to="/" class="header__link">Главная</router-link></li>
					<li><router-link to="/contracts/" class="header__link">Контракты</router-link></li>
					<li><router-link to="/faq/" class="header__link">FAQ</router-link></li>
					<li><a :href="VK_URL" target="_blank" class="header__link">Отзывы</a></li>
					<li><router-link to="/upgrade/" class="header__link">UpGrade</router-link></li>
					<li><router-link to="/battles/" class="header__link">Battles</router-link></li>
					<li><router-link to="/livetrade/" class="header__link">Live-трейды</router-link></li>
					<li><router-link to="/top/" class="header__link">Топ пользователей</router-link></li>
				</ul>
			</nav>
			<a href="index.html" class="footer__logo"></a>
			<div class="left_footer flex" :class="{'flex-end' : hasUserData && userData.login}">				
				 <a v-if="hasUserData && !userData.login" href="/?login" class="steam_log-in">Войти через <span>Steam</span></a>
				<a :href="VK_URL" class="link_vk" target="_blank"></a>
			</div>
		</div>
	</footer>
</template>
<script>
	export default {
		computed: {
			userData() {
				return this.$store.getters.userData;
			},
			hasUserData() {
				return this.$store.getters.hasUserData;
			}
		}
	}
</script>
