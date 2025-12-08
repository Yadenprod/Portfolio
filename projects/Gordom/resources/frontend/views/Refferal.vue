<template lang="pug">
    div(class="flex flex-col")
        div(v-if="preloader" class="w-full py-12 flex items-center justify-center")
            Spin(:color="'text-white'")
        Transition(
            enter-active-class="transition-all duration-[200ms] ease-out"
            enter-class="opacity-0"
            enter-to-class="opacity-100"
        )
            div(v-if="!preloader" class="flex flex-col space-y-[50px] lg:space-y-[30px]")
                div(class="flex flex-col mt-[20px] space-y-[30px]")
                    div(class="flex items-center flex-wrap justify-between")
                        div(class="flex 2xl:-order-[1] items-center text-grayLight uppercase font-['Rubik'] font-medium text-sm space-x-2")
                            svg(class="w-[18px] h-[18px]")
                                use(xlink:href="images/symbols.svg#users")
                            span Партнерская программа
                    div(class="w-full flex-col rounded-xl space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex")
                        div(class="flex items-center justify-between gap-12")
                            div(class="w-full flex flex-col space-y-6")
                                span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Информация о рефералах
                                div(class="flex flex-col space-y-4")
                                    div(class="relative flex md:flex-col md:items-start md:space-y-4 md:gap-0 items-center gap-4")
                                        span(class="shrink-0 text-sm text-grayLight w-[30%] md:w-full") Ваша реферальная ссылка
                                        div(class="w-full")
                                            div(class="text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]")
                                                span {{ link }}
                                                //a(href="javascript:;" class="transition-all duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center") 
                                                    svg(class="w-[18px] h-[18px]")
                                                        use(xlink:href="images/symbols.svg#copy")

                                    div(class="relative flex md:flex-col md:items-start md:space-y-4 md:gap-0 items-center gap-4")
                                        span(class="shrink-0 text-sm text-grayLight w-[30%] md:w-full") Рефералов привлечено
                                        div(class="w-full")
                                            div(class="text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]")
                                                span {{ count }}

                                    div(class="relative flex md:flex-col md:items-start md:space-y-4 md:gap-0 items-center gap-4")
                                        span(class="shrink-0 text-sm text-grayLight w-[30%] md:w-full") Всего заработано
                                        div(class="w-full")
                                            div(class="text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]")
                                                span {{ profit }}

                            div(class="shrink-0 2xl:hidden")
                                img(src="@/images/refferal-banner.png")

                        div(class="flex flex-col")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Описание
                            div(class="flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline")
                                p Приглашай друзей и зарабатывай {{ percent }}% с их каждого пополнения.

</template> 

<script>
    import 'vue-range-slider/dist/vue-range-slider.css'
    export default {
        data() {
            return {
                preloader: true,
                sliderValue: 2.4,
                link: null,
                count: 0,
                profit: 0,
                percent: 0
            }
        },
        methods: {
            init() {
                this.$root.axios.post('/referral/get')
                .then(response => {
                    const {data} = response

                    this.preloader = false
                    this.percent = data.ref_percent,
                    this.count = data.ref_count
                    this.profit = data.ref_profit
                    this.link = data.link
                })
            },
        },
        mounted() {
            this.init();
        }
    }
</script>


<style lang="scss">
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
    .range-slider.disabled {
        opacity: 1;
    }
</style>