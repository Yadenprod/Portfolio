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
                div(class="flex flex-col -space-y-[20px]")
                    div(class="w-full flex items-center justify-center gap-6")
                        div(class="shrink-0 relative select-none")
                            div(class="absolute left-0 -top-[5px] w-full h-full flex items-center justify-center z-[1]")
                                span(class="font-['Deftone'] text-grayLight text-4xl tracking-[1px]") Dice
                            img(src="@/images/game.png")
                    div(class="relative w-full min-h-[50px] overflow-hidden rounded-xl")
                        div(class="w-full md:flex-col mt-[50px] md:space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex items-center justify-between")
                            div(class="w-[calc(100%_-_300px)] md:w-full flex flex-col space-y-5")
                                div(class="w-full flex flex-col items-center space-y-[30px]")
                                    img(src="@/images/logotype-small.svg" class="max-w-[75px]")
                                    p(class="uppercase text-grayLight text-sm font-medium text-center sm:text-xs") Угадай число и увеличь свой депозит!
                                div(class="relative flex flex-col space-y-3")
                                    div(class="flex items-center text-sm text-gray justify-between font-medium font-['Rubik'] [&_span]:w-[28px] [&_span]:text-center")
                                        span 0
                                        span 30
                                        span 50
                                        span 70
                                        span 100
                                    div(class="flex relative flex-col bg-[#2c2c31] px-4 py-5 rounded-xl")
                                        .range__slider_wrap
                                            range-slider(
                                                class="\
                                                    !w-full [&_span.range-slider-rail]:bg-red [&_span.range-slider-fill]:bg-green\
                                                    [&_span.range-slider-knob]:!rounded-[10px] [&_span.range-slider-knob]:w-[28px] [&_span.range-slider-knob]:h-[28px]\
                                                    [&_span.range-slider-knob]:!border-0 [&_span.range-slider-knob]:bg-violet\
                                                    [&_span.range-slider-knob]:cursor-pointer [&_span.range-slider-knob]:hover:bg-violetHover\
                                                "
                                                min="1"
                                                max="95"
                                                step="1"
                                                v-model="sliderValue"
                                            )
                                        div(
                                            class="picker" 
                                            ref="dicePicker" 
                                            :class="[{'invisible': !showPicker},{'win': isWin},{'lose': !isWin} ]"
                                        )
                                div(class="relative w-full overflow-hidden before:absolute before:right-0 before:h-full before:top-0 before:w-[150px] before:bg-gradient-to-r before:to-[#202024] before:from-transparent before:z-[1]")
                                    div(class="flex items-center space-x-3")
                                        div(v-for="item in history" :key="item.id" :class="item.win ? 'text-green' : 'text-red'" class="min-w-[44px] min-h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs select-none") {{ item.percent }}
                            form(class="w-[220px] md:w-full flex flex-col shrink-0 space-y-6" @submit.prevent="play();")
                                div(class="flex flex-col space-y-4")
                                    div(class="w-full flex items-center justify-between text-sm bg-[#1b1c20] py-3 px-4 rounded-xl text-gray")
                                        span(class="font-semibold") Коэффициент:
                                        b(class="uppercase font-['Rubik'] !font-medium text-grayLight text-base") x{{ parseFloat(100 / sliderValue).toFixed(2) }}
                                    div(class="w-full flex items-center justify-between text-sm bg-[#1b1c20] py-3 px-4 rounded-xl text-gray")
                                        span(class="font-semibold") Шанс:
                                        b(class="uppercase font-['Rubik'] !font-medium text-grayLight text-base") {{ sliderValue + '%' }}
                                div(class="flex flex-col space-y-4" )
                                    b(class="text-grayLight !font-semibold text-sm") Ваша ставка:
                                    div(class="flex flex-col")
                                        div(class="flex items-center justify-between md:justify-start md:space-x-3")
                                            a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="maxBet") Max 
                                            a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="minBet") Min 
                                            a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="xBet") X2 
                                            a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="dBet") 1/2
                                    input(v-model="betSum" @input="onInputSumm" class="text-sm font-['Rubik'] bg-[#1b1c20] py-3 px-4 rounded-xl placeholder:text-gray text-white focus:border-0 focus:placeholder:opacity-0 focus:outline-0" placeholder="Введите сумму")
                                    div(class="[&_button]:w-full")
                                       Btn(
                                            :text="isLoading ? 'Бросаем кости..' : 'Играть'"
                                            :type="'button'"
                                            :theme="null"
                                            :ico="'play'"
                                            :class="betSum ? '' : 'opacity-[0.3] cursor-not-allowed pointer-events-none'"
                                        )
                        img(src="@/images/game-top-bar.svg" class="absolute top-0 left-1/2 -translate-x-1/2 max-w-fit")
                        
                GamesBlock
</template>

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

    .picker.win {
        &::before {
            background: #43c175;
        }
    }

    .picker.lose {
        &::before {
            background: #c90e0e;
        }
    }

    .picker {
        width: 16px;
        height: 16px;

        position: absolute;
        top: 4px;
        left: 100%;

        transition: .15s ease-in;
        transform: translateX(-8px);

        border-radius: 100%;
        border: 3px solid white;

        &::before {
            content: "";

            width: 10px;
            height: 10px;

            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);

            border-radius: 100%;

            z-index: 2;
        }

        &::after {
            content: "";

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

<script>
    import 'vue-range-slider/dist/vue-range-slider.css'
    export default {
        name: 'Dice',
        data() {
            return {
                isLoading: false,
                preloader: true,
                sliderValue: 50,
                betSum: 1,
                maxBetSum: 10000,
                minBetSum: 1,
                history: [],
                isWin: false,
                showPicker: false,
                interval: null
            }
        },
        components: {
            Table: () => import('@/components/ui/Table.vue'),
            GamesBlock: () => import('@/components/layouts/Elements/GamesBlock.vue'),
            Stats: () => import('@/components/layouts/Elements/Stats.vue'),
        },
        mounted() {
            this.preloaderDestroy();
        },
        methods: {
            preloaderDestroy() {
                setTimeout(() => {
                    this.preloader = false;
                }, 300);
            },
            play() {
                this.isLoading = true
                this.$root.axios.post('/dice/bet', {
                    amount: this.betSum,
                    chance: this.sliderValue
                })
                .then(response => {
                    const {data} = response
                    this.showPicker = true
                    this.isLoading = false

                    if('error' in data) {
                        return this.$toastr.Add({
                            name: 'BetWheelToast',
                            title: 'Ошибка',
                            msg: data.message,
                            type: 'error',
                            defaultClassNames: ["animated", "zoomInUp"],
                            timeout: 3000,
                            progressbar: true,
                        })
                    }

                    this.isWin = data.status
                    this.history.unshift({
                        id: new Date() / 1,
                        percent: data.number,
                        win: data.status
                    })

                    clearTimeout(this.timeout)
                    this.timeout = setTimeout(() => {
                        this.showPicker = false
                        this.$refs['dicePicker'].style.left = '0%'
                    }, 5000)
                    
                    this.$refs['dicePicker'].style.left = (data.number + 1) + '%'
                    this.$root.user.balance = data.balance
                })
            },
            maxBet () {
                this.betSum = this.maxBetSum
            },
            minBet () {
                this.betSum = this.minBetSum
            },
            xBet () {
                if (this.betSum <= this.maxBetSum) {
                    this.betSum = this.betSum * 2
                }
                if (this.betSum >= this.maxBetSum) {
                    this.betSum = this.maxBetSum
                }
            },
            dBet () {
                if (this.betSum < 1) {
                    return false
                }
                this.betSum = (this.betSum / 2).toFixed()
            },
            onInputSumm({ target }) {
                const val = target.value
                const newVal = `${Math.min(this.maxBetSum, Math.max(0, val.slice(-10000) | 0))}`

                if (val !== newVal) {
                    target.value = newVal
                    target.dispatchEvent(new Event('input'))
                }
                if (val === '') {
                    target.value = ''
                    target.dispatchEvent(new Event('input'))
                }
            },
            getNumber(number, one, two, five) {
                let n = Math.abs(number);
                n %= 100;
                if (n >= 5 && n <= 20) {
                    return five;
                }
                n %= 10;
                if (n === 1) {
                    return one;
                }
                if (n >= 2 && n <= 4) {
                    return two;
                }
                return five;
            }
        },
        watch: {
            history() {
                if(this.history.length >= 25) {
                    this.history.pop()
                }
            }
        }
    }
</script>
