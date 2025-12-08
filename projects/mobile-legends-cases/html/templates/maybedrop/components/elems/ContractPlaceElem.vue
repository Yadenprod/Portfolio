<template>
	<a href="#" @click.prevent class="contract_item">
		<div class="number_contract">
			<template v-if="item">
				<div  class="gun_image">
					<img :src="item.image" :alt="clearItemQuality(item.name)">
					<div class="close" @click="removeFromContract"><span></span><span></span></div>
					<div class="gun_price">
						{{item.price}}
					</div>
					<div class="gun_name" v-html="clearItemQuality(item.name)"></div>
				</div>
			</template>
			<template v-else>
				{{index}}
			</template>
		</div>
	</a>
</template>
<script>
	export default {
		props: {
			index: 0,
			item: false
		},
		methods: {
			removeFromContract() {
				this.$emit('removeFromContract', this.index - 1);
			},
		}
	}
</script>