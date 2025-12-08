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
                    div(class="flex items-center flex-wrap justify-between")
                        div(class="flex 2xl:-order-[1] items-center text-grayLight uppercase font-['Rubik'] font-medium text-sm space-x-2")
                            svg(class="w-[18px] h-[18px]")
                                use(xlink:href="images/symbols.svg#users")
                            span Контакты
                    div(class="relative w-full p-[24px] bg-violet rounded-xl text-white/[0.8] text-sm space-y-3 [&_a]:underline hover:[&_a]:no-underline")
                        p Группа ВКонтакте: <a href="https://vk.com/treasure" target="_blank">https://vk.com/treasure</a>
                        p Группа Телеграм: <a href="https://t.me/treasure" target="_blank">https://t.me/treasure</a>
                        p Группа Дискорд: <a href="https://discord.gg/treasure" target="_blank">https://discord.gg/treasure</a>

</template> 

<script>
    export default {
        data() {
            return {
                preloader: true,
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
