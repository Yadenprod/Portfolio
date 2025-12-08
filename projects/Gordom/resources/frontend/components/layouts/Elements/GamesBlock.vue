<template lang="pug">
    div(class="flex flex-col")
        div(class="flex items-center flex-wrap justify-around mb-[10px] lg:mb-[20px]")
            div(class="flex 2xl:-order-[1] items-center text-grayLight uppercase font-['Rubik'] font-medium text-sm space-x-2")
                svg(class="w-[18px] h-[18px]")
                    use(xlink:href="images/symbols.svg#games")
                span Прошедшие игры
                
            div(class="flex lg:hidden items-center 2xl:w-full 2xl:justify-center 2xl:space-x-4 justify-between")
                a(href="javascript:;" @click="historyTab = 'all'" :class="historyTab === 'all' ? 'text-violet' : ''" class="flex items-center py-4 px-2 text-sm font-semibold space-x-2 text-gray transition-all duration-200 hover:text-violet")
                    i(class="w-2 pointer-events-none h-2 rounded-full bg-current")
                    span(class="pointer-events-none") Все ставки
                a(href="javascript:;" @click="historyTab = 'my'" :class="historyTab === 'my' ? 'text-violet' : ''" class="hidden flex items-center py-4 px-2 text-sm font-semibold space-x-2 text-gray transition-all duration-200 hover:text-violet")
                    i(class="w-2 pointer-events-none h-2 rounded-full bg-current")
                    span(class="pointer-events-none") Мои ставки
                a(href="javascript:;" @click="historyTab = 'tourniers'" :class="historyTab === 'tourniers' ? 'text-violet' : ''" class="hidden flex items-center py-4 px-2 text-sm font-semibold space-x-2 text-gray transition-all duration-200 hover:text-violet")
                    i(class="w-2 pointer-events-none h-2 rounded-full bg-current")
                    span(class="pointer-events-none") Турниры
                

        div(
            class="bg-[#202024] p-5 sm:p-4 rounded-2xl"
        )
            Transition(
                enter-active-class="transition-all ease-out duration-200"
                enter-class="opacity-0"
                enter-to-class="opacity-100"
            )
                div(
                    v-if="historyTab === 'all'" 
                    class="\
                        [&_div.table>div>div>div:first-child]:w-1/2 [&>div.table>div:first-child>div:first-child]:w-1/2\
                        [&_div.table>div>div>div:nth-child(3)]:w-1/2 [&>div.table>div:first-child>div:nth-child(3)]:w-1/2\
                        [&_div.table>div>div>div:nth-child(4)]:w-1/2 [&>div.table>div:first-child>div:nth-child(4)]:w-1/2\
                        [&_div.table>div>div>div:nth-child(5)]:w-1/2 [&>div.table>div:first-child>div:nth-child(5)]:w-1/2\
                        lg:[&_div.table>div>div>div:nth-child(2)]:w-1/2 lg:[&>div.table>div:first-child>div:nth-child(2)]:w-1/2\
                        lg:[&_div.table>div>div>div:nth-child(3)]:hidden lg:[&>div.table>div:first-child>div:nth-child(3)]:hidden\
                        lg:[&_div.table>div>div>div:nth-child(4)]:hidden lg:[&>div.table>div:first-child>div:nth-child(4)]:hidden\
                    "
                )
                    Table(:table="historyAll")

            Transition(
                enter-active-class="transition-all ease-out duration-200"
                enter-class="opacity-0"
                enter-to-class="opacity-100"
            )
                div(
                    v-if="historyTab === 'my'"
                    class="\
                        [&_div.table>div>div>div:first-child]:w-1/2 [&>div.table>div:first-child>div:first-child]:w-1/2\
                        [&_div.table>div>div>div:nth-child(3)]:w-1/2 [&>div.table>div:first-child>div:nth-child(3)]:w-1/2\
                        [&_div.table>div>div>div:nth-child(4)]:w-1/2 [&>div.table>div:first-child>div:nth-child(4)]:w-1/2\
                        [&_div.table>div>div>div:nth-child(5)]:w-1/2 [&>div.table>div:first-child>div:nth-child(5)]:w-1/2\
                        lg:[&_div.table>div>div>div:nth-child(2)]:w-1/2 lg:[&>div.table>div:first-child>div:nth-child(2)]:w-1/2\
                        lg:[&_div.table>div>div>div:nth-child(3)]:hidden lg:[&>div.table>div:first-child>div:nth-child(3)]:hidden\
                        lg:[&_div.table>div>div>div:nth-child(4)]:hidden lg:[&>div.table>div:first-child>div:nth-child(4)]:hidden\
                    "
                )
                    Table(:table="historyMy")

            Transition(
                enter-active-class="transition-all ease-out duration-200"
                enter-class="opacity-0"
                enter-to-class="opacity-100"
            )
                div(
                    v-if="historyTab === 'tourniers'"
                    class="\
                        [&_div.table>div>div>div:first-child]:w-1/2 [&>div.table>div:first-child>div:first-child]:w-1/2\
                        [&_div.table>div>div>div:nth-child(3)]:w-1/2 [&>div.table>div:first-child>div:nth-child(3)]:w-1/2\
                        [&_div.table>div>div>div:nth-child(4)]:w-1/2 [&>div.table>div:first-child>div:nth-child(4)]:w-1/2\
                        [&_div.table>div>div>div:nth-child(5)]:w-1/2 [&>div.table>div:first-child>div:nth-child(5)]:w-1/2\
                        lg:[&_div.table>div>div>div:nth-child(2)]:w-1/2 lg:[&>div.table>div:first-child>div:nth-child(2)]:w-1/2\
                        lg:[&_div.table>div>div>div:nth-child(3)]:hidden lg:[&>div.table>div:first-child>div:nth-child(3)]:hidden\
                        lg:[&_div.table>div>div>div:nth-child(4)]:hidden lg:[&>div.table>div:first-child>div:nth-child(4)]:hidden\
                    "
                )
                    Table(:table="historyTourniers")
</template>

<script>
    export default {
        data() {
            return {
                historyTab: 'all',
                historyAll: {
                    thead: [
                        {
                            id: 1,
                            name: 'Игра',
                        },
                        {
                            id: 2,
                            name: 'Игрок',
                        },
                        {
                            id: 3,
                            name: 'Время',
                            width: '50'
                        },
                        {
                            id: 4,
                            name: 'Ставка',
                        },
                        {
                            id: 5,
                            name: 'Выигрыш',
                        },
                    ],
                    tbody: []
                },
            }
        },
        mounted() {
            this.$socket.emit('getGamesHistory')
        },
        sockets: {
            newGame(data) {
                if(this.historyAll.tbody.length >= 15) {
                    this.historyAll.tbody.pop()
                }

                let item = {
                    items: data
                }
                this.historyAll.tbody.unshift(item)
            },
            gamesHistory(data) {
                let list = []

                data.forEach(el => {
                    let item = {
                        items: el.item
                    }
                    list.push(item)
                })

                this.historyAll.tbody = list
            },
        },
        components: {
            'CardGame': () => import('@/components/pages/index/CardGame.vue'),
            Table: () => import('@/components/ui/Table.vue'),
        }
    }
</script>
