<template lang="pug">
    div(class="flex flex-col")
        div(v-if="preloader" class="w-full py-12 flex items-center justify-center")
            Spin(:color="'text-white'")
        Transition(
            enter-active-class="transition-all duration-[200ms] ease-out"
            enter-class="opacity-0"
            enter-to-class="opacity-100"
        )
            div(v-if="!preloader" class="flex items-center flex-col space-y-[50px] lg:space-y-[30px]")
                span(class="font-semibold") Нет активных турниров
</template> 

<script>
    export default {
        data() {
            return {
                preloader: true,
                tourniers: [
                    {
                        id: 0,
                        cost: 2000,
                        status: 0,
                        game: 'Wheel',
                        users: [
                            {
                                id: 0,
                                avatar: 'https://sun9-east.userapi.com/sun9-26/s/v1/ig2/XiQUJBodHmXrWOXGfbDpTsSLizMHjHB07nTAlTgNb4lphc2LmIKj9nw3UUwZpwtr3lllnma09VM3j71qwPvpJSjz.jpg?size=1280x853&quality=95&type=album',
                                username: 'Mart',
                                sum: 1200
                            },
                            {
                                id: 1,
                                avatar: 'https://sun1.userapi.com/sun1-23/s/v1/if1/mOOfH7McJx7iJmWOrmciD2UHTpMY9U5OABDGIi0mxQzY_pxzdQaOFJ3DiM9o-Nn1iINM5oDi.jpg?size=200x232&quality=96&crop=47,45,350,407&ava=1',
                                username: 'Lambo',
                                sum: 530
                            },
                            {
                                id: 2,
                                avatar: 'https://sun1.userapi.com/sun1-94/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                username: 'Владислав',
                                sum: 100
                            },
                        ]
                    },
                    {
                        id: 1,
                        cost: 750,
                        status: 0,
                        game: 'Mines',
                        users: [
                            {
                                id: 0,
                                avatar: 'https://sun9-east.userapi.com/sun9-26/s/v1/ig2/XiQUJBodHmXrWOXGfbDpTsSLizMHjHB07nTAlTgNb4lphc2LmIKj9nw3UUwZpwtr3lllnma09VM3j71qwPvpJSjz.jpg?size=1280x853&quality=95&type=album',
                                username: 'Mart',
                                sum: 1200
                            },
                            {
                                id: 1,
                                avatar: 'https://sun1.userapi.com/sun1-23/s/v1/if1/mOOfH7McJx7iJmWOrmciD2UHTpMY9U5OABDGIi0mxQzY_pxzdQaOFJ3DiM9o-Nn1iINM5oDi.jpg?size=200x232&quality=96&crop=47,45,350,407&ava=1',
                                username: 'Lambo',
                                sum: 530
                            },
                            {
                                id: 2,
                                avatar: 'https://sun1.userapi.com/sun1-94/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                username: 'Владислав',
                                sum: 100
                            },
                        ]
                    },
                    {
                        id: 2,
                        cost: 3000,
                        status: 1,
                        game: 'Wheel',
                        users: [
                            {
                                id: 0,
                                avatar: 'https://sun9-east.userapi.com/sun9-26/s/v1/ig2/XiQUJBodHmXrWOXGfbDpTsSLizMHjHB07nTAlTgNb4lphc2LmIKj9nw3UUwZpwtr3lllnma09VM3j71qwPvpJSjz.jpg?size=1280x853&quality=95&type=album',
                                username: 'Mart',
                                sum: 1200
                            },
                            {
                                id: 1,
                                avatar: 'https://sun1.userapi.com/sun1-23/s/v1/if1/mOOfH7McJx7iJmWOrmciD2UHTpMY9U5OABDGIi0mxQzY_pxzdQaOFJ3DiM9o-Nn1iINM5oDi.jpg?size=200x232&quality=96&crop=47,45,350,407&ava=1',
                                username: 'Lambo',
                                sum: 530
                            },
                            {
                                id: 2,
                                avatar: 'https://sun1.userapi.com/sun1-94/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                username: 'Владислав',
                                sum: 100
                            },
                        ]
                    },
                    {
                        id: 3,
                        cost: 1500,
                        status: 1,
                        game: 'Dice',
                        users: [
                            {
                                id: 0,
                                avatar: 'https://sun9-east.userapi.com/sun9-26/s/v1/ig2/XiQUJBodHmXrWOXGfbDpTsSLizMHjHB07nTAlTgNb4lphc2LmIKj9nw3UUwZpwtr3lllnma09VM3j71qwPvpJSjz.jpg?size=1280x853&quality=95&type=album',
                                username: 'Mart',
                                sum: 1200
                            },
                            {
                                id: 1,
                                avatar: 'https://sun1.userapi.com/sun1-23/s/v1/if1/mOOfH7McJx7iJmWOrmciD2UHTpMY9U5OABDGIi0mxQzY_pxzdQaOFJ3DiM9o-Nn1iINM5oDi.jpg?size=200x232&quality=96&crop=47,45,350,407&ava=1',
                                username: 'Lambo',
                                sum: 530
                            },
                            {
                                id: 2,
                                avatar: 'https://sun1.userapi.com/sun1-94/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                username: 'Владислав',
                                sum: 100
                            },
                        ]
                    },
                    {
                        id: 4,
                        cost: 1500,
                        status: 1,
                        game: 'Dice',
                        users: [
                            {
                                id: 0,
                                avatar: 'https://sun9-east.userapi.com/sun9-26/s/v1/ig2/XiQUJBodHmXrWOXGfbDpTsSLizMHjHB07nTAlTgNb4lphc2LmIKj9nw3UUwZpwtr3lllnma09VM3j71qwPvpJSjz.jpg?size=1280x853&quality=95&type=album',
                                username: 'Mart',
                                sum: 1200
                            },
                            {
                                id: 1,
                                avatar: 'https://sun1.userapi.com/sun1-23/s/v1/if1/mOOfH7McJx7iJmWOrmciD2UHTpMY9U5OABDGIi0mxQzY_pxzdQaOFJ3DiM9o-Nn1iINM5oDi.jpg?size=200x232&quality=96&crop=47,45,350,407&ava=1',
                                username: 'Lambo',
                                sum: 530
                            },
                            {
                                id: 2,
                                avatar: 'https://sun1.userapi.com/sun1-94/s/v1/ig2/e08xwS94vEmcSoPd4d2RBVp7jfcLeHDgVOt3T4F4cXHMkhqYjm0saqGA98AN2WJuaG8NAvWRA7_KJ0byGWylRT6g.jpg?size=1440x1920&quality=95&type=album',
                                username: 'Владислав',
                                sum: 100
                            },
                        ]
                    },
                ]
            }
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
