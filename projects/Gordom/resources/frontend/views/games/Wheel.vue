<template lang="pug">
    div(class="flex flex-col")
        div(v-if="preloader" class="w-full py-12 flex items-center justify-center")
            Spin(:color="'text-white'")
        Transition(
            enter-active-class="transition-all duration-[200ms] ease-out"
            enter-class="opacity-0"
            enter-to-class="opacity-100"
        )
            div(:class="[preloader ? 'invisible' : '']" class="flex flex-col space-y-[50px] lg:space-y-[30px]")
                div(class="flex flex-col -space-y-[20px]")
                    div(class="w-full flex items-center justify-center gap-6")
                        div(class="shrink-0 relative select-none")
                            div(class="absolute left-0 -top-[5px] w-full h-full flex items-center justify-center z-[1]")
                                span(class="font-['Deftone'] text-grayLight text-4xl tracking-[1px]") Wheel
                            img(src="@/images/game.png")
                    div(class="relative w-full flex flex-col min-h-[50px] overflow-hidden rounded-xl")
                        div(class="w-full flex-col mt-[50px] space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex items-center justify-between")
                            div(class="flex md:flex-col md:space-y-[30px] sm:!space-y-[20px] w-full items-center justify-between")
                                div(class="w-[calc(100%_-_300px)] md:w-full flex flex-col space-y-5 relative")
                                    div(class="h-[344px] relative")
                                        div(class="absolute flex left-1/2 -translate-x-1/2 -translate-y-[65%] top-0 w-[772px] h-[772px]")
                                            div(class="absolute flex items-end justify-center left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[85%] h-[85%] rounded-full overflow-hidden pointer-events-none")
                                                div(class="absolute left-0 top-0 w-full h-full flex items-end justify-center pb-[20%] md:pb-[15%]")
                                                    div(class="flex flex-col items-center space-y-2")
                                                        span(class="text-grayLight text-sm font-semibold") До начала игры
                                                        b(class="text-violet text-3xl font-['Rubik'] !font-semibold") {{ wheelTimer }}
                                            img(src="@/images/games/wheel/wheel1.png" ref="wheel" class="wheel-preview absolute left-0 top-0 w-full h-full object-cover")
                                            img(src="@/images/games/wheel/cursor.svg" class="absolute left-1/2 -translate-x-1/2 -bottom-[50px]")
                                    div(class="relative w-full overflow-hidden before:absolute before:right-0 before:h-full before:top-0 before:w-[150px] before:bg-gradient-to-r before:to-[#202024] before:from-transparent before:z-[1]")
                                        div(class="flex items-center space-x-3")
                                            div(v-for="(item, key) in history" :key="key" :class="item.x === 2 ? 'x2' : '' || item.x === 3 ? 'x3' : '' || item.x === 5 ? 'x5' : '' || item.x === 10 ? 'x10' : '' || item.x === 20 ? 'x20' : '' || item.x === 100 ? 'x100' : ''" class="[&.x2]:!text-[#bec5da] [&.x3]:!text-[#44c276] [&.x5]:!text-[#f08929] [&.x10]:!text-[#f24841] [&.x20]:!text-[#d92c9f] [&.x100]:!text-[#7c75d9] min-w-[44px] min-h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs select-none") {{ 'x' + item.x }}
                                div(class="w-[220px] md:w-full flex flex-col shrink-0 space-y-6")
                                    img(src="@/images/logotype.svg" class="max-h-[48px] md:hidden")
                                    div(class="w-full flex flex-col items-center space-y-[30px] md:hidden")
                                        p(class="uppercase text-grayLight text-sm font-medium text-center sm:text-xs") Забери самый <br> крупный джекпот
                                        img(src="@/images/logotype-small.svg" class="max-w-[75px]")
                                    div(class="flex flex-col space-y-4")
                                        b(class="text-grayLight !font-semibold text-sm") Ваша ставка:
                                        div(class="flex flex-col")
                                            div(class="flex items-center justify-between md:justify-start md:space-x-3")
                                                a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="maxBet") Max 
                                                a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="minBet") Min 
                                                a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="xBet") X2 
                                                a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="dBet") 1/2
                                        input(v-model="betSum" @input="onInputSumm" class="text-sm font-['Rubik'] bg-[#1b1c20] py-3 px-4 rounded-xl placeholder:text-gray text-white focus:border-0 focus:placeholder:opacity-0 focus:outline-0" placeholder="Введите сумму")

                            Bets(:list="bets" @play="play")

                        img(src="@/images/game-top-bar.svg" class="absolute top-0 left-1/2 -translate-x-1/2 max-w-fit")

                        
                GamesBlock

</template>

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
</style>

<script>
    import 'vue-range-slider/dist/vue-range-slider.css'
    export default {
        name: 'Dice',
        data() {
            return {
                wheelTimer: '00:20',
                preloader: true,
                sliderValue: 50,
                betSum: 1,
                minBetSum: 1,
                maxBetSum: 100000,
                rotate: 0,
                history: [],
                bets: [
                    {
                        id: 0,
                        x: 2,
                        color: 'black',
                        users: [],
                    },
                    {
                        id: 1,
                        x: 3,
                        color: 'green',
                        users: [],
                    },
                    {
                        id: 2,
                        x: 5,
                        color: 'orange',
                        users: [],
                    },
                    {
                        id: 3,
                        x: 10,
                        color: 'red',
                        users: [],
                    },
                    {
                        id: 4,
                        x: 20,
                        color: 'pink',
                        users: [],
                    },
                    {
                        id: 5,
                        x: 100,
                        color: 'violet',
                        users: [],
                    },
                ]
            }
        },
        components: {
            Table: () => import('@/components/ui/Table.vue'),
            Bets: () => import('@/components/pages/games/wheel/Bets.vue'),
            GamesBlock: () => import('@/components/layouts/Elements/GamesBlock.vue'),
            Stats: () => import('@/components/layouts/Elements/Stats.vue'),
        },
        mounted() {
            this.init();
            this.$socket.emit('getWheelState')
        },
        methods: {
            init() {
                this.$root.axios.post('/wheel/init')
                .then(response => {
                    const {data} = response

                    this.bets.forEach((el, key) => {
                        this.bets[key].users = []
                    })

                    data.bets.map(bet => {
                        const { id } = this.bets.find(el => el.color == bet.color)

                        this.bets[id].users.push({
                            username: bet.username,
                            bet: bet.sum
                        })
                    })

                    data.history.forEach(item => {
                        this.history.push(this.getXByColor(item.winner_color))
                    })

                    this.preloader = false
                })
            },
            updateBalance() {
                this.$root.axios.post('/user/updateBalance')
                .then(response => {
                    const {data} = response

                    if(!data.balance) return
                    
                    this.$root.user.balance = data.balance
                })
            },
            maxBet () {
                this.betSum = this.$root?.user?.balance || 0
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
                if (this.betSum <= 1) {
                    return false
                }
                this.betSum = (this.betSum / 2).toFixed()
            },
            onInputSumm({ target }) {
                const val = target.value
            },
            play(color) {
                this.$root.axios.post('/wheel/bet', {
                    amount: this.betSum,
                    color
                })
                .then(response => {
                    const {data} = response

                    if(data.error) {
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

                    this.$root.user.balance = data.balance
                })
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
            },
            getXByColor(color) {
                const X = {
                    black: 2,
                    green: 3,
                    orange: 5,
                    red: 10,
                    pink: 20,
                    violet: 100
                }

                return {
                    id: this.history.length + 1,
                    x: X[color]
                }
            }
        },
        sockets: {
            wheelTimer(data) {
                var sec = (data.seconds >= 10) ? data.seconds : `0${data.seconds}`;
                var timer = `00:${sec}`
                this.wheelTimer = timer
            },
            wheelBets(data) {
                this.bets.forEach((el, key) => {
                    this.bets[key].users = []
                })

                data.bets.map(bet => {
                    const { id } = this.bets.find(el => el.color == bet.color)

                    this.bets[id].users.push({
                        username: bet.username,
                        bet: bet.sum
                    })
                })
            },
            wheelHistory(data) {
                this.updateBalance()

                this.bets.forEach((el, key) => {
                    this.bets[key].users = []
                })

                if(this.history.length >= 20) {
                    this.history.pop()
                }

                this.history.unshift(this.getXByColor(data.color))
            },
            wheelSpin(data) {
                this.wheelTimer = '00:20'

                var deg = data.position;
                this.rotate += deg + (360 * 6) - (this.rotate % 360)

                this.$refs['wheel'].style.transition = `all ${data.timer}s cubic-bezier(0, 0.49, 0, 1) -7ms`;
                this.$refs['wheel'].style.transform =  `rotate(${this.rotate}deg)`
            },
        }
    }
</script>
