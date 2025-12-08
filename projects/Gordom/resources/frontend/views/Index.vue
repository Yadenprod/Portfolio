<template lang="pug">
    div(class="flex flex-col")
        div(v-if="preloader" class="w-full py-12 flex items-center justify-center")
            Spin(:color="'text-white'")
        Transition(
            enter-active-class="transition-all duration-[200ms] ease-out"
            enter-class="opacity-0"
            enter-to-class="opacity-100"
        )
            div(v-if="!preloader" class="flex flex-col space-y-[30px]")
                div(class="flex w-full items-stretch justify-between gap-6")
                    .shrink-0(class="xl:hidden w-[25%] flex flex-col py-6 justify-between space-y-6")
                        div(
                            class="\
                                flex flex-col [&_h1]:font-['Rubik'] [&_h1]:text-[26px] [&_h1>span]:text-[#7c75d9]\
                                font-semibold text-[#cfcde9] [&_p]:text-sm [&_p]:text-[#cfcde9] [&_p]:leading-[180%]\
                                space-y-2\
                            "
                        )
                            h1 <span>TREASURE</span> Casino
                            p Уникальные игры с выводом денег <br> и с большым шансом на победу
                        div(class="flex flex-col space-y-2")
                            span(class="text-sm text-gray font-semibold") Сейчас играют:
                            div(class="flex items-center space-x-3 font-['Rubik']")
                                span(class="flex relative h-2 w-2")
                                    span(class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green opacity-75")
                                    span(class="relative inline-flex rounded-full h-2 w-2 bg-green")
                                b(class="font-medium text-lg") {{ online }}
                    div(class="w-full grid before:pt-[30%] xl:before:pt-[40%] sm:before:!pt-[70%] relative rounded-2xl overflow-hidden")
                        div(class="absolute left-0 top-0 w-full h-full flex items-center xl:justify-center justify-start z-[1]")
                            div(class="pl-20 xl:pl-0 flex flex-col items-center space-y-6")
                                div(class="flex flex-col items-center space-y-1")
                                    div(class="uppercase text-6xl font-['Rubik'] xl:text-5xl sm:!text-4xl font-medium select-none text-white leading-[100%]") Турниры
                                    p(class="text-sm font-semibold text-grayLight") стань первым среди лучших
                                Btn(
                                    :text="'Забери джекпот'"
                                    :type="'link'"
                                    :path="'/tourniers'"
                                    :theme="null"
                                    :ico="null"
                                )
                        div(class="absolute left-0 top-0 w-full h-full")
                            img(src="@/images/banner.png" class="absolute left-0 top-0 w-full h-full object-cover")
                    
                div(class="w-full flex flex-col space-y-[50px] lg:space-y-[30px]")
                    div(class="flex flex-col")
                        div(class="flex items-center justify-between mb-[30px] lg:mb-[20px]")
                            div(class="flex items-center text-grayLight uppercase font-['Rubik'] font-medium text-sm space-x-2")
                                svg(class="w-[18px] h-[18px]")
                                    use(xlink:href="images/symbols.svg#games")
                                span Наши игры
                        CardGame(:games="games")

                    GamesBlock
</template>

<script>
    export default {
        name: 'Index',
        components: {
            'CardGame': () => import('@/components/pages/index/CardGame.vue'),
            Table: () => import('@/components/ui/Table.vue'),
            GamesBlock: () => import('@/components/layouts/Elements/GamesBlock.vue'),
            Stats: () => import('@/components/layouts/Elements/Stats.vue'),
        },
        data() {
            return {
                preloader: true,
                games: [
                    {
                        id: 1,
                        name: 'Dice',
                        path: '/dice',
                        image: 'dice_prev.png',
                    },
                    {
                        id: 2,
                        name: 'Mines',
                        path: '/mines',
                        image: 'mines_prev.png',
                    },
                    {
                        id: 3,
                        name: 'Wheel',
                        path: '/wheel',
                        image: 'wheel_prev.png',
                    },
                    {
                        id: 4,
                        name: 'Slots',
                        path: '/slots',
                        image: 'slots_prev.png',
                    },
                    // {
                    //     id: 5,
                    //     name: null,
                    //     path: null,
                    //     image: 'none_prev.png',
                    // },
                ],
                online: 0
            }
        },  
        mounted() {
            this.preloaderDestroy();
            this.$socket.emit('getOnline')
        },
        methods: {
            preloaderDestroy() {
                setTimeout(() => {
                    this.preloader = false;
                }, 300);
            }
        },
        sockets: {
            online(data) {
                this.online = data
            }
        }
    }
</script>
