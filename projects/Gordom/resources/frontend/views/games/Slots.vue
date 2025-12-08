<template lang="pug">
    div(class="flex flex-col rounded-xl")
        //div(v-if="preloader" class="w-full py-12 flex items-center justify-center")
            //Spin(:color="'text-white'")
        Transition(
            enter-active-class="transition-all duration-[200ms] ease-out"
            enter-class="opacity-0"
            enter-to-class="opacity-100"
        )
            div(class="flex flex-col space-y-[50px] lg:space-y-[30px] rounded-xl")
                div(class="flex flex-col -space-y-[20px]")
                    div(class="relative w-full min-h-[50px] overflow-hidden rounded-xl")
                        div(class="w-full mt-[50px] md:space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1]")
                        
                          div(class="w-full mb-12 sm:flex-col gap-4 flex items-center justify-between")
                            label(for="search" class="md:w-full md:max-w-none max-w-[234px] relative")
                              svg(class="w-[24px] h-[24px] absolute top-1/2 text-gray -translate-y-1/2 left-3.5")
                                use(href="images/symbols.svg#search")
                              
                              input(v-model="search" placeholder="Поиск" type="text" name="search" id="search" class="border-0 bg-[#3A3A43] h-[52px] w-full px-5 pl-12 rounded-xl text-sm font-medium placeholder:text-grayLight/[0.5] focus:ring-0 focus:outline-none focus:border-0")

                            div(class="md:w-full relative" v-on-clickaway="closeProviderDropdown")
                              div(@click="isProviderDropdownOpen = !isProviderDropdownOpen" class="md:max-w-none max-w-[234px] relative bg-[#313136] h-[52px] px-5 rounded-xl flex items-center justify-between cursor-pointer")
                                p(class="text-sm pointer-events-none font-medium select-none text-grayLight/[0.5] mr-6") Провайдеры
                                
                                i(class="text-gray inline-block w-2 h-2 border-r-2 border-b-2 border-current rotate-[45deg] transition-all duration-200" :class="isProviderDropdownOpen ? ['rotate-[225deg]'] : ''")
                              
                              Transition(enter-active-class="transition ease-out duration-100" enter-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95")
                                div(v-if="isProviderDropdownOpen" class="absolute w-full z-[1] p-2 origin-top-right right-0 mt-2 bg-[#313136] rounded-xl flex flex-col gap-1 shadow-[0px_4px_28px_rgba(0,0,0,0.08)]")
                                  // Вариант с input 👇
                                  // label(class="relative px-3.5 py-2 rounded-md overflow-hidden select-none text-sm transition-colors text-gray cursor-pointer hover:bg-[#3A3A43] hover:text-white" for="pragmatic")
                                  //   input(type="checkbox" id="pragmatic" class="absolute cursor-pointer top-0 left-0 !w-full !h-full")
                                  //   p Pragmatic
                                  // label(class="relative px-3.5 py-2 rounded-md overflow-hidden select-none text-sm transition-colors text-gray cursor-pointer hover:bg-[#3A3A43] hover:text-white" for="Netent")
                                  //   input(type="checkbox" id="Netent" class="absolute cursor-pointer top-0 left-0 !w-full !h-full")
                                  //   p Netent
                                  // label(class="relative px-3.5 py-2 rounded-md overflow-hidden select-none text-sm transition-colors text-gray cursor-pointer hover:bg-[#3A3A43] hover:text-white" for="Amatic")
                                  //   input(type="checkbox" id="Amatic" class="absolute cursor-pointer top-0 left-0 !w-full !h-full")
                                  //   p Amatic
                                  // Вариант с div 👇
                                  div(class="px-3.5 py-2 rounded-md select-none text-sm transition-colors text-gray cursor-pointer hover:bg-[#3A3A43] hover:text-white" v-for="provider in providers" :class="[activeProvider == provider.type ? 'bg-[#3A3A43] !text-white' : '']" @click="activeProvider = provider.type") {{ provider.title }}
                                  //div(class="px-3.5 py-2 rounded-md select-none text-sm transition-colors text-gray cursor-pointer hover:bg-[#3A3A43] hover:text-white") Amatic

                          div(v-if="preloader" class="w-full py-12 flex items-center justify-center")
                            Spin(:color="'text-white'")

                          div(v-if="!preloader" class="grid grid-cols-5 2xl:grid-cols-3 sm:!grid-cols-2 gap-3.5")
                            SlotCard(v-for="(item, id) in slots" :data="item" :key="id")
                          
                          div(class="block text-center m-[25px]" v-if="!preloader && !slots.length")
                            span Не найдено
                          div(v-if="!preloader && page !== total_page" class="flex justify-center w-full mt-[30px]")
                            div(class="flex space-x-4 items-center")
                              a(@click="loadMore" href="javascript:;" class="h-[42px] px-6 rounded-full font-bold transition-all duration-200 hover:shadow-[0px_0px_0px_12px_rgba(86,79,232,0.12)] flex items-center justify-center text-white bg-gradient-to-r from-[#6a6a7a] to-[#6a6a7a]") 
                                | <svg v-if="buttonLoader" class="animate-spin mr-3 h-5 w-5 text-white !m-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> {{ !buttonLoader ? 'Загрузить ещё' : '' }}
                              span(class="text-[#696F96] text-sm font-semibold") {{ page }} из {{ total_page }}
</template>

<script>
import 'vue-range-slider/dist/vue-range-slider.css'
export default {
	name: 'Slots',
	data() {
		return {
			isProviderDropdownOpen: false,
			preloader: true,
            activeProvider: '',
            buttonLoader: false,
			providers: [
                { title: 'Все провайдеры', type: '' },
                { title: 'pragmatic', type: 'pragmatic' },
                { title: 'netent', type: 'netent' },
                { title: 'amatic', type: 'amatic' },
            ],
			slots: [],
            timeout: null,
            search: null,
            page: 1,
            total_page: 0
		}
	},
	components: {
		SlotCard: () => import('@/components/pages/games/slots/SlotCard.vue'),
	},
	mounted() {
		this.init()
	},
	methods: {
		init(page) {
            this.buttonLoader = true
            this.$root.axios.post('/slots/init', {
                page: page || this.page,
                search: this.search,
                provider: this.activeProvider
            })
            .then(response => {
                const {data} = response

                this.slots.push(...data.data)
                this.preloader = false
                this.total_page = data.last_page
                this.page = data.current_page
                this.buttonLoader = false
            })
            .catch(err => {
                this.buttonLoader = false

                this.$toastr.Add({
                    name: 'BetMinesToast',
                    title: 'Ошибка',
                    msg: 'При получении списка произошла ошибка',
                    type: 'error',
                    timeout: 3000,
                    progressbar: true,
                })
            })
        },
        loadMore() {
            if(this.buttonLoader) return;
            this.init(this.page + 1)
        },
		closeProviderDropdown() {
			this.isProviderDropdownOpen = false
		},
	},
    watch: {
        search() {
            clearTimeout(this.timeout)
            this.timeout = setTimeout(() => {
                this.slots = []
                this.preloader = true
                this.init(1)
            }, 500)
        },
        activeProvider() {
            this.slots = []
            this.preloader = true
            this.init(1)
        }
    }
}
</script>

<style lang="scss" scoped>
input[type='checkbox'] {
	&:checked {
		opacity: 10%;
	}
}
</style>

<style lang="scss">
.range__slider_wrap {
	position: relative;
}

.range-slider {
	padding: 0;
}

.range-slider-knob {
	&:before {
		content: '';
		position: absolute;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
		width: 16px;
		height: 16px;
		background: url('@/images/star.svg') no-repeat center center / contain;
	}
}

.picker {
	width: 16px;
	height: 16px;

	position: absolute;
	top: -10px;
	left: 100%;

	transform: translateX(-8px);

	border-radius: 100%;
	border: 3px solid white;

	&::before {
		content: '';

		width: 10px;
		height: 10px;

		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);

		border-radius: 100%;
		background: #43c175;

		z-index: 2;
	}

	&::after {
		content: '';

		width: 6px;
		height: 6px;

		position: absolute;
		bottom: -4px;
		left: 50%;
		transform: translateX(-50%) rotate(45deg);

		background: white;
		z-index: 1;
	}
}
</style>