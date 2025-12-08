<template lang="pug">
    div(class="hidden lg:block fixed bottom-0 left-0 w-full bg-[#202024] z-[10]")
        div(class="w-full h-[68px] rounded-xl px-[16px] flex items-center justify-between")
            router-link(
                to="/" 
                :class="preloader ? 'loader !border-0' : ''"
                class="flex relative overflow-hidden before:opacity-[0.6] items-center justify-center w-[36px] h-[36px] bg-[#08b0fb] rounded-xl transition-all duration-200 text-white"
            )
                        Transition(
                            enter-active-class="transition ease-out duration-800"
                            enter-class="transform opacity-0 scale-90"
                            enter-to-class="transform opacity-100 scale-100"
                        )
                            <svg v-if="!preloader" class="w-[16px] h-[16px]"><use xlink:href="@/images/symbols.svg#home"></use></svg>

            nav(class="flex items-center space-x-4")
                li(v-for="item in games" :key="item.id" class="w-full flex items-center justify-center")
                    router-link(
                        :to="item.path" 
                        active-class="active" 
                        exact-active-class=""
                        :class="preloader ? 'loader !border-0' : ''"
                        class="flex relative overflow-hidden before:opacity-[0.08] items-center justify-center w-[44px] h-[44px] bg-[#2c2c31] rounded-xl border-2 border-transparent transition-all duration-200 hover:border-[#7c75d9] text-[#c1c8dc] hover:text-[#7c75d9] [&.active]:border-[#7c75d9] [&.active]:text-[#7c75d9]"
                    )
                        Transition(
                            enter-active-class="transition ease-out duration-800"
                            enter-class="transform opacity-0 scale-90"
                            enter-to-class="transform opacity-100 scale-100"
                        )
                            <svg v-if="!preloader" class="w-[20px] h-[20px]"><use :xlink:href="'../images/symbols.svg#' + item.ico"></use></svg>

            a(
                href="javascript:;" 
                :class="preloader ? 'loader !border-0' : ''"
                @click="chatInitState"
                class="flex relative overflow-hidden before:opacity-[0.6] items-center justify-center w-[36px] h-[36px] bg-violet hover:bg-violetHover rounded-xl transition-all duration-200 text-white"
            )
                        Transition(
                            enter-active-class="transition ease-out duration-800"
                            enter-class="transform opacity-0 scale-90"
                            enter-to-class="transform opacity-100 scale-100"
                        )
                            <svg v-if="!preloader" class="w-[16px] h-[16px]"><use xlink:href="@/images/symbols.svg#send"></use></svg>
                            
</template>

<script>
    export default {
        data () {
            return {
                preloader: true,
                games: [
                    {
                        id: 1,
                        path: '/dice',
                        ico: 'dice',
                    },
                    {
                        id: 2,
                        path: '/mines',
                        ico: 'mines',
                    },
                    {
                        id: 3,
                        path: '/wheel',
                        ico: 'wheel',
                    },
                    {
                        id: 4,
                        path: '/slots',
                        ico: 'slot'
                    }
                ]
            }
        },
        methods: {
            preloaderDestroy() {
                setTimeout(() => {
                    this.preloader = false;
                }, 800);
            },
            chatInitState() {
                if (this.chatOpen) {
                    this.$emit('chatInitState', false);
                } else {
                    this.$emit('chatInitState', true);
                }
            },
        },  
        mounted() {
            this.preloaderDestroy();
        }
    }
</script>
