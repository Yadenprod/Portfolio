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
                                use(xlink:href="images/symbols.svg#fair")
                            span Честная игра
                    div(class="w-full flex-col rounded-xl space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex")
                        div(class="flex items-center justify-between gap-12")
                            div(class="w-full flex flex-col space-y-6")
                                span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Результат игры <b class="text-violet">#5320361</b>
                                div(class="flex flex-col space-y-4")
                                    div(class="relative flex md:flex-col md:items-start md:space-y-4 items-center")
                                        span(class="shrink-0 text-sm text-grayLight w-[20%] md:w-full") Соль 1
                                        div(class="w-[80%] md:w-full")
                                            div(class="text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]")
                                                span(class="max-w-full whitespace-nowrap text-ellipsis overflow-hidden") 6OA1jt9g2c9eQx27flwnQ586
                                                a(href="javascript:;" class="transition-all shrink-0 duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center") 
                                                    svg(class="w-[18px] h-[18px]")
                                                        use(xlink:href="images/symbols.svg#copy")

                                    div(class="relative flex md:flex-col md:items-start md:space-y-4 items-center")
                                        span(class="shrink-0 text-sm text-grayLight w-[20%] md:w-full") Соль 2
                                        div(class="w-[80%] md:w-full")
                                            div(class="text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]")
                                                span(class="max-w-full whitespace-nowrap text-ellipsis overflow-hidden") QaAKPH8d7T2T2Oud285m6C9d
                                                a(href="javascript:;" class="transition-all shrink-0 duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center") 
                                                    svg(class="w-[18px] h-[18px]")
                                                        use(xlink:href="images/symbols.svg#copy")

                                    div(class="relative flex md:flex-col md:items-start md:space-y-4 items-center")
                                        span(class="shrink-0 text-sm text-grayLight w-[20%] md:w-full") Число игры:
                                        div(class="w-[80%] md:w-full")
                                            div(class="text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]")
                                                span(class="max-w-full whitespace-nowrap text-ellipsis overflow-hidden") 0.39326375111344614
                                                a(href="javascript:;" class="transition-all shrink-0 duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center") 
                                                    svg(class="w-[18px] h-[18px]")
                                                        use(xlink:href="images/symbols.svg#copy")

                                    div(class="relative flex md:flex-col md:items-start md:space-y-4 items-center")
                                        span(class="shrink-0 text-sm text-grayLight w-[20%] md:w-full") Хэш игры:
                                        div(class="w-[80%] md:w-full")
                                            div(class="text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]")
                                                span(class="max-w-full whitespace-nowrap text-ellipsis overflow-hidden") 2c05877a04ba24e25de4f912357e6181da8544c6c9eb2c5c7edf0d87
                                                a(href="javascript:;" class="transition-all shrink-0 duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center") 
                                                    svg(class="w-[18px] h-[18px]")
                                                        use(xlink:href="images/symbols.svg#copy")

                                    div(class="relative flex md:flex-col md:items-start md:space-y-4 items-center")
                                        span(class="shrink-0 text-sm text-grayLight w-[20%] md:w-full") Общая строка:
                                        div(class="w-[80%] md:w-full")
                                            div(class="text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]")
                                                span(class="max-w-full whitespace-nowrap text-ellipsis overflow-hidden") 6OA1jt9g2c9eQx27flwnQ5860.39326375111344614QaAKPH8d7T2T2Oud285m6C9d
                                                a(href="javascript:;" class="transition-all shrink-0 duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center") 
                                                    svg(class="w-[18px] h-[18px]")
                                                        use(xlink:href="images/symbols.svg#copy")

                            div(class="shrink-0 2xl:hidden")
                                img(src="@/images/fair.png")

                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Описание
                            div(class="flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline")
                                p "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
</template> 

<script>
    export default {
        data() {
            return {
                preloader: true,
                sliderValue: 2.4,
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
