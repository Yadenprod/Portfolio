<template lang="pug">
    div(class="relative grid grid-cols-6 2xl:grid-cols-4 md:!grid-cols-3 md:gap-2 sm:flex sm:flex-col sm:gap-0 sm:space-y-3 gap-4 w-full")
        div(v-for="item in list" :key="item.id" class="relative flex flex-col space-y-3")
            button(type="submit" @click="play(item.color);" :class="item.x === 2 ? 'bg-[#2c2c31] hover:bg-[#3A3A40] text-grayLight ' : '' || item.x === 3 ? 'bg-green hover:bg-greenHover text-white' : '' || item.x === 5 ? 'bg-[#f08929] hover:bg-[#fd9739] text-white' : '' || item.x === 10 ? 'bg-red hover:bg-redHover text-white' : '' || item.x === 20 ? 'bg-[#d92c9f] hover:bg-[#e43fad] text-white' : '' || item.x === 100 ? 'bg-violet hover:bg-violetHover text-white' : ''" class="justify-between flex items-center h-[58px] px-5 rounded-xl text-sm transition-all duration-200 focus:ring-0 focus:border-0 focus:outline-0")
                span(class="font-semibold pointer-events-none") Ставка
                b(class="text-lg font-['Rubik'] pointer-events-none") {{ 'x' + item.x }}
            div(class="flex flex-col space-y-2 text-grayLight text-sm font-semibold")
                div(class="flex items-center justify-between bg-[#1b1c20] py-2.5 px-4 rounded-lg")
                    div(class="flex items-center space-x-2")
                        svg(class="w-[16px] h-[16px]")
                            use(xlink:href="images/symbols.svg#users")
                        span {{ item.users.length }}
                    div(class="flex items-center space-x-2")
                        img(src="@/images/logotype-small.svg" class="max-w-[16px]")
                        span {{ parseFloat( getBank(item.x) ).toFixed(2) }}
                div(class="flex flex-col space-y-2.5 2xl:hidden")
                    div(v-for="item in item.users" :key="item.id" class="gap-[10px] flex items-center justify-between bg-[#1b1c20] py-2.5 px-4 rounded-lg")
                        span(class="max-w-full whitespace-nowrap text-ellipsis overflow-hidden") {{ item.username }}
                        div(class="shrink-0 flex items-center space-x-2")
                            img(src="@/images/logotype-small.svg" class="max-w-[16px]")
                            span {{ item.bet }}
</template>

<script>
    export default {
        props: {
            list: {
                type: Array,
                default: () => {}
            }
        },
        methods: {
            play(color) {
                this.$emit('play', color)
            },
            getBank(x) {
                const item = this.list.find(el => el.x === x)
                const bets = item.users.map(el => el.bet);

                if(!bets.length) return 0

                return bets.reduce((total, amount) => total + parseFloat(amount))
            }
        },
    }
</script>
