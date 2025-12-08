<template>
    <div class="fixed lg:-translate-x-[100%] transition-all duration-200 left-0 top-0 pl-[16px] py-[16px] h-full">
        <div class="scroll relative flex flex-col h-full w-[96px] bg-[#202024] rounded-xl overflow-auto pb-[16px]">
            <router-link to="/" active-class="" exact-active-class="" class="min-h-[84px] w-full mb-2 flex items-center justify-center py-[18px] [&_img]:hover:scale-105">
                <div v-if="preloader" class="w-[48px] h-[48px] bg-[#35353c] loader mask-logotype before:opacity-[0.08]"></div>
                <Transition 
                    enter-active-class="transition ease-out duration-600"
                    enter-class="transform opacity-0 scale-90"
                    enter-to-class="transform opacity-100 scale-100"
                >
                    <img v-if="!preloader" src="@/images/logotype-small.svg" class="max-w-[48px] transition-all duration-200" alt="">
                </Transition>
            </router-link>
            <nav class="w-full space-y-4">
                <li v-for="item in games" :key="item.id" class="w-full flex items-center justify-center">
                    <router-link 
                        :to="item.path" 
                        active-class="active" 
                        exact-active-class=""
                        :class="preloader ? 'loader !border-0' : ''"
                        class="flex relative overflow-hidden before:opacity-[0.08] items-center justify-center w-[62px] h-[62px] bg-[#2c2c31] rounded-xl border-2 border-transparent transition-all duration-200 hover:border-[#7c75d9] text-[#c1c8dc] hover:text-[#7c75d9] [&.active]:border-[#7c75d9] [&.active]:text-[#7c75d9]"
                    >
                        <Transition 
                            enter-active-class="transition ease-out duration-800"
                            enter-class="transform opacity-0 scale-90"
                            enter-to-class="transform opacity-100 scale-100"
                        >
                            <svg v-if="!preloader" class="w-[28px] h-[28px]"><use :xlink:href="'../images/symbols.svg#' + item.ico"></use></svg>
                        </Transition>
                    </router-link>
                </li>
            </nav>
        </div>
    </div>
</template>

<style>
    .mask-logotype {
        mask-image: url('@/images/logotype-small.svg');
        mask-size: cover;
    }
</style>

<script>
    export default {
        name: 'leftPanel',
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
                        ico: 'slot',
                    },
                ]
            }
        },
        methods: {
            preloaderDestroy() {
                setTimeout(() => {
                    this.preloader = false;
                }, 800);
            }
        },  
        mounted() {
            this.preloaderDestroy();
        }
    }
</script>
