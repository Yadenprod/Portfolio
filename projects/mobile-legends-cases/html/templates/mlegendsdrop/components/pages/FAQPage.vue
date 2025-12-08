<template>
	<div class="centerblock">
		<main id="main" class="site-main" role="main">
			<h1><span></span>FAQ<span></span></h1>
			<div class="faq_block">
				<div v-if="questions" v-for="(question, key) in questions" class="faq_item__border">
					<div @click="question.open = !question.open" class="faq_item" :class="{'open' : question.open}">
						<div class="faq_question" v-html="question.question"></div>
						<div class="faq_answer" v-html="question.answer"></div>
					</div>
				</div>
			</div>
			<div class="faq_warning">
				<img src="/tpl/maybedrop/img/warning_icon.png" alt="">
				<p>Если вы не нашли ответа на свой вопрос в данном разделе,
					то напишите на почту <a href="mailto:support@maybedrop.ru">support@maybedrop.ru</a></p>
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
	export default {
		data: () => ({
				questions: false
			}),
		mounted() {
			Utils.setTitle("FAQ");
			this.getPageData();
		},
		methods: {
			getPageData() {
				Utils.apiPostCall("/api/faq/")
						.then(resp => {
							if (resp.data.success) {
								for (let i in resp.data.questions) {
									resp.data.questions[i].open = false;
								}
								this.questions = resp.data.questions;
							}
						});
			}
		}
	}
</script>