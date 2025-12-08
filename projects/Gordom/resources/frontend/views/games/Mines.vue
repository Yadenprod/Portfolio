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
                                span(class="font-['Deftone'] text-grayLight text-4xl tracking-[1px]") Mines
                            img(src="@/images/game.png")
                    div(class="relative w-full min-h-[50px] overflow-hidden rounded-xl")
                        div(class="w-full mt-[50px] space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex flex-col items-center justify-between")
                            div(class="w-full flex md:flex-col items-center justify-between")
                                div(class="w-[calc(100%_-_280px)] md:w-full flex md:flex-col items-stretch md:items-center justify-between md:justify-center")
                                    div.flex.items-center.justify-center(class="2xl:hidden")
                                        img(src="@/images/games/mines/bg.png")
                                    div(class="flex items-center flex-col md:order-[1] md:flex-row justify-between py-6 gap-6")
                                        div(class="flex flex-col items-center text-grayLight font-['Rubik'] font-medium space-y-4")
                                            div(class="w-[64px] h-[64px] sm:w-[48px] sm:h-[48px] sm:rounded-xl flex items-center justify-center rounded-2xl bg-violet")
                                                img(src="@/images/logotype-small.svg" class="max-w-[32px] sm:max-w-[22px]")
                                            span {{ 25 - bomb }}
                                        div(class="flex flex-col items-center text-grayLight font-['Rubik'] font-medium space-y-4")
                                            div(class="w-[64px] h-[64px] sm:w-[48px] sm:h-[48px] sm:rounded-xl text-[#d5daea] flex items-center justify-center rounded-2xl bg-red")
                                                svg(class="w-[32px] h-[32px] sm:w-[22px] sm:h-[22px]")
                                                    use(xlink:href="images/symbols.svg#mines")
                                            span {{ bomb }}
                                    div(class="grid gap-[calc(64px_*_0.125)] grid-cols-[repeat(5,_64px)] grid-rows-[repeat(5,_64px)] sm:grid-cols-[repeat(5,_48px)] sm:grid-rows-[repeat(5,_48px)]")
                                        div(
                                            v-for="(item, key) in mines" 
                                            :key="item.id" 
                                            @click="openMine(key + 1)" 
                                            :class="['opacity-40',{ '!opacity-100 pointer-events-none': opened.indexOf(key + 1) !== -1 },{ 'hover:scale-105': item.status === null }, {'pointer-events-none': !game.isStart}]" 
                                            class="overflow-hidden relative bg-[#2c2c31] flex items-center justify-center rounded-xl cursor-pointer transition-all duration-200"
                                        )
                                            div(v-if="item.status === 'won'" class="w-full h-full flex items-center justify-center bg-violet")
                                                img(src="@/images/logotype-small.svg" class="max-w-[32px] sm:max-w-[22px]")
                                            div(v-if="item.status === 'lose'" class="text-[#d5daea] w-full h-full flex items-center justify-center bg-red")
                                                svg(class="w-[32px] h-[32px] sm:w-[22px] sm:h-[22px]")
                                                        use(xlink:href="images/symbols.svg#mines")


                                form(class="w-[220px] md:w-full flex flex-col shrink-0 space-y-6" @submit.prevent="preventDefault")
                                    div(class="flex flex-col space-y-4")
                                        b(class="text-grayLight !font-semibold text-sm") Количество бомб:
                                        div(class="flex flex-col")
                                            div(class="flex items-center justify-between md:justify-start md:space-x-3")
                                                a(href="javascript:;" @click="bomb = 3" :class="bomb === 3 ? '!border-violet text-violet hover:bg-[#2c2c31]' : ''" class="w-[44px] h-[44px] bg-[#2c2c31] border-2 border-transparent flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]") 3 
                                                a(href="javascript:;" @click="bomb = 5" :class="bomb === 5 ? '!border-violet text-violet hover:bg-[#2c2c31]' : ''" class="w-[44px] h-[44px] bg-[#2c2c31] border-2 border-transparent flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]") 5 
                                                a(href="javascript:;" @click="bomb = 10" :class="bomb === 10 ? '!border-violet text-violet hover:bg-[#2c2c31]' : ''" class="w-[44px] h-[44px] bg-[#2c2c31] border-2 border-transparent flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]") 10 
                                                a(href="javascript:;" @click="bomb = 24" :class="bomb === 24 ? '!border-violet text-violet hover:bg-[#2c2c31]' : ''" class="w-[44px] h-[44px] bg-[#2c2c31] border-2 border-transparent flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]") 24
                                    div(class="flex flex-col space-y-4")
                                        b(class="text-grayLight !font-semibold text-sm") Ваша ставка:
                                        div(class="flex flex-col")
                                            div(class="flex items-center justify-between md:justify-start md:space-x-3")
                                                a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="maxBet") Max 
                                                a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="minBet") Min 
                                                a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="xBet") X2 
                                                a(href="javascript:;" class="w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]" @click="dBet") 1/2
                                        input(v-model="betSum" @input="onInputSumm" class="text-sm font-['Rubik'] bg-[#1b1c20] py-3 px-4 rounded-xl placeholder:text-gray text-white focus:border-0 focus:placeholder:opacity-0 focus:outline-0" placeholder="Введите сумму")
                                        div(class="[&_button]:w-full")

                                            button(
                                                v-if="!game.isStart"
                                                class="font-['Rubik'] whitespace-nowrap focus:ring-0 focus:ring-inherit focus:outline-0 focus:border-0 flex transition-all duration-200 items-center justify-center rounded-xl text-sm uppercase font-medium h-[52px] px-6 shadow-[0px_4px_35px_rgba(0,0,0,0.1)] hover:bg-violetHover bg-violet" 
                                                @click="startGame"
                                            )       
                                                svg(class="w-[18px] h-[18px] text-current mr-2")
                                                    use(xlink:href="images/symbols.svg#play")
                                                | Играть         

                                            button(
                                                v-if="game.isStart"
                                                class="hidden font-['Rubik'] whitespace-nowrap focus:ring-0 focus:ring-inherit focus:outline-0 focus:border-0 flex transition-all duration-200 items-center justify-center rounded-xl text-sm uppercase font-medium h-[52px] px-6 shadow-[0px_4px_35px_rgba(0,0,0,0.1)] hover:bg-grayHover bg-gray" 
                                                @click="autoSelect"
                                            )  Автовыбор

                                            button(
                                                v-if="game.isStart"
                                                class="font-['Rubik'] whitespace-nowrap focus:ring-0 focus:ring-inherit focus:outline-0 focus:border-0 flex transition-all duration-200 items-center justify-center rounded-xl text-sm uppercase font-medium h-[52px] px-6 shadow-[0px_4px_35px_rgba(0,0,0,0.1)] hover:bg-violetHover bg-violet" 
                                                @click="catchMines"
                                            ) Забрать {{parseFloat(game.win).toFixed(2)}}

                            div(class="w-full relative flex items-center justify-between gap-5")
                                a(href="javascript:;" class="shrink-0 flex items-center justify-center text-violet w-[32px] h-[32px] rounded-lg bg-[#2c2c31] transition-all duration-200 hover:bg-violet hover:text-white" @click="controlledSwiper.slidePrev()") 
                                    svg(class="w-[20px] h-[20px] -rotate-[180deg]")
                                        use(xlink:href="images/symbols.svg#arrow")
                                swiper(
                                    :key="bomb"
                                    :freeMode="true"
                                    :slides-per-view="'auto'"
                                    :spaceBetween="16"
                                    @swiper="onSwiper"
                                )
                                    swiper-slide(v-for="(item, id) in coefs[bomb - 1]" :key="item.id" class="!w-auto") 
                                        div(class="w-[64px] h-[64px] flex flex-col justify-center items-center bg-[#2c2c31] rounded-xl")
                                            b(class="text-grayLight font-['Rubik'] !font-medium text-sm") {{ 'x' + parseFloat(item).toFixed(2) }}
                                            span(class="text-gray font-semibold text-sm") {{ id + 1 + ' hit' }}
                                a(href="javascript:;" class="shrink-0 flex items-center justify-center text-violet w-[32px] h-[32px] rounded-lg bg-[#2c2c31] transition-all duration-200 hover:bg-violet hover:text-white" @click="controlledSwiper.slideNext()") 
                                    svg(class="w-[20px] h-[20px]")
                                        use(xlink:href="images/symbols.svg#arrow")
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
    import { SwiperCore, Swiper, SwiperSlide } from 'swiper-vue2'
    import 'swiper/swiper-bundle.css'
    import { getEmptyArr } from '@/utils/getEmptyArr'

    export default {
        name: 'Mines',
        data() {
            return {
                preloader: true,
                sliderValue: 50,
                betSum: 1,
                maxBetSum: 10000,
                minBetSum: 1,
                bomb: 3,
                mines: [],
                chances: [],
                game: {
                    isStart: false,
                    win: 0
                },
                opened: [],
                controlledSwiper: null, 
                coefs: [
                    [],
                    [1.09,1.19,1.3,1.43,1.58,1.75,1.96,2.21,2.5,2.86,3.3,3.85,4.55,5.45,6.67,8.33,10.71,14.29,20,30,50,100,300],
                    [1.14,1.3,1.49,1.73,2.02,2.37,2.82,3.38,4.11,5.05,6.32,8.04,10.45,13.94,19.17,27.38,41.07,65.71,115,230,575,2300],
                    [1.19,1.43,1.73,2.11,2.61,3.26,4.13,5.32,6.95,9.27,12.64,17.69,25.56,38.33,60.24,100.4,180.71,361.43,843.33,2530,12650],
                    [1.25,1.58,2.02,2.61,3.43,4.57,6.2,8.59,12.16,17.69,26.54,41.28,67.08,115,210.83,421.67,948.75,2530,8855,53130],
                    [1.32,1.75,2.37,3.26,4.57,6.53,9.54,14.31,22.12,35.38,58.97,103.21,191.67,383.33,843.33,2108.33],
                    [1.39,1.96,2.82,4.13,6.2,9.54,15.1,24.72,42.02,74.7,140.06,280.13,606.94,1456.67,4005.83,13352.78],
                    [1.47,2.21,3.38,5.32,8.59,14.31,24.72,44.49,84.04,168.08,360.16,840.38,2185,6555,24035,120175,1081575],
                    [1.56,2.5,4.11,6.95,12.16,22.12,42.02,84.04,178.58,408.19,1020.47,2857.31,9286.25,37145,204297.5,2042975],
                    [1.67,2.86,5.05,9.27,17.69,35.38,74.7,168.08,408.19,1088.5,3265.49,11429.23,49526.67,297160,3268760],
                    [1.79,3.3,6.32,12.64,26.54,58.97,140.06,360.16,1020.47,3265.49,12245.6,57146.15,371450,4457400],
                    [1.92,3.85,8.04,17.69,41.28,103.21,280.13,840.38,2857.31,11429.23,57146.15,400023.08,5200300],
                    [2.08,4.55,10.45,25.56,67.08,191.67,606.94,2185,9286.25,49526.67,371450,5200300],
                    [2.27,5.45,13.94,38.33,115,383.33,1456.67,6555,37145,297160,4457400],
                    [2.5,6.67,19.17,60.24,210.83,843.33,4005.83,24035,204297.5,3268760],
                    [2.78,8.33,27.38,100.4,421.67,2108.33,13352.78,120175,2042975],
                    [3.13,10.71,41.07,180.71,948.75,6325,60087.5,1081575],
                    [3.57,14.29,65.71,361.43,2530,25300,480700],
                    [4.17,20,115,843.33,8855,177100],
                    [5,30,230,2530,53130],
                    [6.25,50,575,12650],
                    [8.33,100,2300],
                    [12.5,300],
                    [25]
                ],
            }
        },
        components: {
            Table: () => import('@/components/ui/Table.vue'),
            GamesBlock: () => import('@/components/layouts/Elements/GamesBlock.vue'),
            Stats: () => import('@/components/layouts/Elements/Stats.vue'),
            Swiper,
            SwiperSlide
        },
        mounted() {
            this.mines = getEmptyArr(25, {status: false})
            this.init()
        },
        methods: {
            init() {
                this.$root.axios.post('/mines/init')
                .then(response => {
                    const {data} = response;
                    this.preloader = false;

                    if(typeof data.click !== 'undefined') {
                        this.game.isStart = true;
                        this.betSum = data.amount;
                        this.bomb = data.bombs;
                        this.opened = data.click;
                        this.game.win = data.total;

                        this.mines = this.mines.map((item, index) =>
                            data.click.indexOf(index + 1) !== - 1
                                ? { ...item, status: 'won' }
                                : item
                        )
                    }
                })
            },
            startGame() {
                this.$root.axios.post('/mines/start', {
                    amount: this.betSum,
                    bombs: this.bomb
                })
                .then(response => {
                    const {data} = response

                    if(data.error) {
                        return this.$toastr.Add({
                            name: 'BetMinesToast',
                            title: 'Ошибка',
                            msg: data.message,
                            type: 'error',
                            timeout: 3000,
                            progressbar: true,
                        })
                    }

                    this.mines = getEmptyArr(25, {status: false})
                    this.opened = []

                    this.$root.user.balance = data.balance;
                    this.game.isStart = true;
                    this.game.win = 0;

                    this.$toastr.Add({
                        name: 'BetMinesToast',
                        title: 'Успешно',
                        msg: data.message,
                        type: 'success',
                        timeout: 3000,
                        progressbar: true,
                    })
                })
            },
            openMine(index) {
                this.$root.axios.post('/mines/open', {
                    path: index
                })
                .then(response => {
                    const {data} = response

                    if(data.error) {
                        return this.$toastr.Add({
                            name: 'BetMinesToast',
                            title: 'Ошибка',
                            msg: data.message,
                            type: 'error',
                            timeout: 3000,
                            progressbar: true,
                        })
                    }

                    this.opened.push(index);

                    if(data.continue) { // win - continue
                        this.game.win = data.total;
                        this.mines = this.mines.map(item => 
                            item.id === index - 1
                                ? { ...item, status: 'won'}
                                : item
                        )
                    } else {
                        this.game.isStart = false
                        this.mines = this.mines.map((item, index) =>
                            data.bombs.indexOf(index + 1) !== - 1
                                ? { ...item, status: 'lose' }
                                : { ...item, status: 'won' }
                        )
                    }

                    if(data.instwin) {
                        this.game.isStart = false
                        this.mines = getEmptyArr(25, {status: false})
                        this.opened = []
                        this.$root.user.balance = data.instwin.balance;
                    }
                })
            },
            catchMines() {
                this.$root.axios.post('/mines/take')
                .then(response => {
                    const {data} = response;
                    
                    if(data.error) {
                        return this.$toastr.Add({
                            name: 'BetMinesToast',
                            title: 'Ошибка',
                            msg: data.message,
                            type: 'error',
                            timeout: 3000,
                            progressbar: true,
                        })
                    }

                    this.$root.user.balance = data.balance;
                    this.game.isStart = false;
                    this.mines = getEmptyArr(25, { status: null });
                    this.opened = [];

                    this.$toastr.Add({
                        name: 'BetMinesToast',
                        title: 'Успешно',
                        msg: 'Вы забрали ' + data.total + ' руб.',
                        type: 'success',
                        timeout: 3000,
                        progressbar: true,
                    })
                })
            },
            autoSelect() {
                var noActive = document.querySelectorAll('.opacity-40:not(.!opacity-100)')
                noActive[Math.floor(Math.random() * noActive.length)].click();
                this.autoBtn.isLoading = true;
            },
            preventDefault(e) {
                e.preventDefault();
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
            },
            onSwiper(swiper) {
                this.controlledSwiper = swiper
            },
        }
    }
</script>
