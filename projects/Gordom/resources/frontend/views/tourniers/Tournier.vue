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
                    div(class="flex 2xl:-order-[1] items-center text-grayLight uppercase font-['Rubik'] font-medium text-sm space-x-2")
                        svg(class="w-[18px] h-[18px]")
                            use(xlink:href="images/symbols.svg#tourniers")
                        span Турниры 
                            | <b class="!font-medium text-violet">Игровой режим: wheel</b>
                    div(class="w-full flex-col rounded-xl space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex")
                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Информация
                            div(class="flex flex-col space-y-[20px]")
                                div(class="flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline")
                                    p При соблюдении условий турнира от суммы ставок будет начислено 10% в очки! Обновление рейтинга происходит раз в 10 минут!
                                div(class="w-full grid grid-cols-6 2xl:grid-cols-3 sm:!grid-cols-2 xs:flex xs:flex-col gap-3")
                                    .flex.flex-col.items-center(v-for="item in information" :key="item.index" class="bg-[#2c2c31] [&_b]:last:!text-red justify-center py-4 rounded-xl space-y-1")
                                        span(v-if="item.title" class="text-grayLight text-sm") {{ item.title }}
                                        b(class="text-white !font-medium font-['Rubik'] text-md") {{ item.value }}

                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Условия для участия в турнире
                            div(class="flex flex-col space-y-[20px]")
                                div(class="flex flex-col space-y-3 [&_p>span]:text-violet [&_p>em]:not-italic [&_p>em]:text-green [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline")
                                    p 1. Нужно пополнить баланс от <span>500.00 ₽</span> за последние 7 дней
                                    p 2. Ставки учитываются только из списка игр
                                    p 3. Ставки учитываются от <span>5.00 ₽</span>
                                    p 4. За каждую ставку будет начисленно <em>10%</em> в таблицу рейтинга

                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Список игр участвующие в турнире
                            div(class="flex flex-col space-y-[20px]")
                                ul(class="flex items-center w-fit space-x-2.5")
                                    li(v-for="item in games" :key="item.index" class="shrink-0 relative pointer-events-none flex w-[64px] h-[64px] rounded-xl bg-[#2c2c31] text-sm uppercase text-grayLight flex flex-col items-center justify-center space-y-0.5")
                                        b(class="relative z-[1]") {{ item.name }}
                                        svg(class="w-[32px] h-[32px] text-gray/[0.3] absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2")
                                            use(:xlink:href="'images/symbols.svg#' + item.ico")

                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Призовые места
                            div(
                                class="\
                                    flex flex-col space-y-[20px]\
                                    [&_div.table>div>div>div:first-child]:w-1/2 [&>div.table>div:first-child>div:first-child]:w-1/2\
                                    [&_div.table>div>div>div:nth-child(3)]:w-1/2 [&>div.table>div:first-child>div:nth-child(3)]:w-1/2\
                                    [&_div.table>div>div>div:nth-child(4)]:w-1/2 [&>div.table>div:first-child>div:nth-child(4)]:w-1/2\
                                    [&_div.table>div>div>div:nth-child(5)]:w-1/2 [&>div.table>div:first-child>div:nth-child(5)]:w-1/2\
                                    lg:[&_div.table>div>div>div:nth-child(2)]:w-1/2 lg:[&>div.table>div:first-child>div:nth-child(2)]:w-1/2\
                                    lg:[&_div.table>div>div>div:nth-child(3)]:hidden lg:[&>div.table>div:first-child>div:nth-child(3)]:hidden\
                                    lg:[&_div.table>div>div>div:nth-child(5)]:hidden lg:[&>div.table>div:first-child>div:nth-child(5)]:hidden\
                                    [&_div.table>div:last-child>div>div:first-child>div:first-child>svg]:hidden\
                                    [&_div.table>div:last-child>div:first-child>div:first-child>div:first-child>svg]:text-violet\
                                    [&_div.table>div:last-child>div:first-child>div:first-child>div:first-child]:text-violet\
                                    [&_div.table>div:last-child>div:first-child>div:first-child>div:first-child>svg]:w-[22px]\
                                    [&_div.table>div:last-child>div:first-child>div:first-child>div:first-child>svg]:h-[22px]\
                                    [&_div.table>div:last-child>div:first-child>div:first-child>div:first-child>svg]:block\
                                    [&_div.table>div:last-child>div:nth-child(2)>div:first-child>div:first-child>svg]:text-green\
                                    [&_div.table>div:last-child>div:nth-child(2)>div:first-child>div:first-child]:text-green\
                                    [&_div.table>div:last-child>div:nth-child(2)>div:first-child>div:first-child>svg]:w-[22px]\
                                    [&_div.table>div:last-child>div:nth-child(2)>div:first-child>div:first-child>svg]:h-[22px]\
                                    [&_div.table>div:last-child>div:nth-child(2)>div:first-child>div:first-child>svg]:block\
                                    [&_div.table>div:last-child>div:nth-child(3)>div:first-child>div:first-child>svg]:text-red\
                                    [&_div.table>div:last-child>div:nth-child(3)>div:first-child>div:first-child]:text-red\
                                    [&_div.table>div:last-child>div:nth-child(3)>div:first-child>div:first-child>svg]:w-[22px]\
                                    [&_div.table>div:last-child>div:nth-child(3)>div:first-child>div:first-child>svg]:h-[22px]\
                                    [&_div.table>div:last-child>div:nth-child(3)>div:first-child>div:first-child>svg]:block\
                                "
                            )
                                Table(:table="place")

</template> 

<script>
    export default {
        data() {
            return {
                preloader: true,
                information: [
                    {
                        title: 'Призовой фонд',
                        value: 1024560
                    },
                    {
                        title: 'Призовых мест',
                        value: 3
                    },
                    {
                        title: 'Кол-во участников',
                        value: 126
                    },
                    {
                        title: 'Игровой период',
                        value: '08.11 - 08.14'
                    },
                    {
                        title: 'Осталось времени',
                        value: '01:05:27:54'
                    },
                    {
                        value: 'Завершен',
                    },
                ],
                games: [
                    {
                        name: 'Wheel',
                        ico: 'wheel'
                    },
                    {
                        name: 'Mines',
                        ico: 'mines'
                    },
                    {
                        name: 'Dice',
                        ico: 'dice'
                    },
                ],
                place: {
                    thead: [
                        {
                            id: 0,
                            name: 'Место'
                        },
                        {
                            id: 1,
                            name: 'Игрок'
                        },
                        {
                            id: 2,
                            name: 'Баллы'
                        },
                        {
                            id: 3,
                            name: 'Приз'
                        },
                        {
                            id: 4,
                            name: 'Рейтинг'
                        },
                    ],
                    tbody: [
                        {
                            id: 0,
                            items: [
                                {
                                    id: 0,
                                    ico: 'place',
                                    icoText: 1
                                },
                                {
                                    id: 1,
                                    user: {
                                        avatar: 'https://sun9-east.userapi.com/sun9-43/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                        username: 'Владислав Леонов'
                                    }
                                },
                                {
                                    id: 2,
                                    value: 589.30
                                },
                                {
                                    id: 3,
                                    value: 1200 + ' ₽'
                                },
                                {
                                    id: 4,
                                    value: 0
                                },
                            ]
                        },
                        {
                            id: 1,
                            items: [
                                {
                                    id: 0,
                                    ico: 'place',
                                    icoText: 2
                                },
                                {
                                    id: 1,
                                    user: {
                                        avatar: 'https://sun9-east.userapi.com/sun9-43/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                        username: 'Владислав Леонов'
                                    }
                                },
                                {
                                    id: 2,
                                    value: 589.30
                                },
                                {
                                    id: 3,
                                    value: 1200 + ' ₽'
                                },
                                {
                                    id: 4,
                                    value: 0
                                },
                            ]
                        },
                        {
                            id: 2,
                            items: [
                                {
                                    id: 0,
                                    ico: 'place',
                                    icoText: 3
                                },
                                {
                                    id: 1,
                                    user: {
                                        avatar: 'https://sun9-east.userapi.com/sun9-43/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                        username: 'Владислав Леонов'
                                    }
                                },
                                {
                                    id: 2,
                                    value: 589.30
                                },
                                {
                                    id: 3,
                                    value: 1200 + ' ₽'
                                },
                                {
                                    id: 4,
                                    value: 0
                                },
                            ]
                        },
                        {
                            id: 3,
                            items: [
                                {
                                    id: 0,
                                    ico: 'place',
                                    icoText: 4
                                },
                                {
                                    id: 1,
                                    user: {
                                        avatar: 'https://sun9-east.userapi.com/sun9-43/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                        username: 'Владислав Леонов'
                                    }
                                },
                                {
                                    id: 2,
                                    value: 589.30
                                },
                                {
                                    id: 3,
                                    value: 1200 + ' ₽'
                                },
                                {
                                    id: 4,
                                    value: 0
                                },
                            ]
                        },
                        {
                            id: 4,
                            items: [
                                {
                                    id: 0,
                                    ico: 'place',
                                    icoText: 5
                                },
                                {
                                    id: 1,
                                    user: {
                                        avatar: 'https://sun9-east.userapi.com/sun9-43/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                        username: 'Владислав Леонов'
                                    }
                                },
                                {
                                    id: 2,
                                    value: 589.30
                                },
                                {
                                    id: 3,
                                    value: 1200 + ' ₽'
                                },
                                {
                                    id: 4,
                                    value: 0
                                },
                            ]
                        },
                        {
                            id: 5,
                            items: [
                                {
                                    id: 0,
                                    ico: 'place',
                                    icoText: 6
                                },
                                {
                                    id: 1,
                                    user: {
                                        avatar: 'https://sun9-east.userapi.com/sun9-43/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                        username: 'Владислав Леонов'
                                    }
                                },
                                {
                                    id: 2,
                                    value: 589.30
                                },
                                {
                                    id: 3,
                                    value: 1200 + ' ₽'
                                },
                                {
                                    id: 4,
                                    value: 0
                                },
                            ]
                        },
                        {
                            id: 6,
                            items: [
                                {
                                    id: 0,
                                    ico: 'place',
                                    icoText: 7
                                },
                                {
                                    id: 1,
                                    user: {
                                        avatar: 'https://sun9-east.userapi.com/sun9-43/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                        username: 'Владислав Леонов'
                                    }
                                },
                                {
                                    id: 2,
                                    value: 589.30
                                },
                                {
                                    id: 3,
                                    value: 1200 + ' ₽'
                                },
                                {
                                    id: 4,
                                    value: 0
                                },
                            ]
                        },
                    ]
                }
            }
        },
        components: {
            Table: () => import('@/components/ui/Table.vue'),
        },
        methods: {
            preloaderDestroy() {
                setTimeout(() => {
                    this.preloader = false;
                }, 300);
            },
        },
        mounted() {
            this.preloaderDestroy();
        }
    }
</script>
