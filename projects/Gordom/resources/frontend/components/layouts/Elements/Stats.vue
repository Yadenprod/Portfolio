<template lang="pug">
    div(class="flex flex-col")
        div(class="flex items-center flex-wrap justify-between mb-[30px] lg:mb-[20px]")
            div(class="flex items-center text-grayLight uppercase font-['Rubik'] font-medium text-sm space-x-2")
                svg(class="w-[18px] h-[18px]")
                    use(xlink:href="images/symbols.svg#chart")
                span Статистика
        div(class="w-full grid grid-cols-4 2xl:grid-cols-2 sm:!grid-cols-1 gap-6")
            div(class="w-full grid relative 2xl:before:pt-[30%] xl:before:pt-[40%] md:before:!pt-[50%] before:pt-[50%] overflow-hidden rounded-2xl")
                div(class="flex items-center justify-center p-6 absolute left-0 top-0 w-full h-full z-[1]")
                    div(class="w-full flex flex-col items-center text-sm space-y-5")
                        b(class="font-medium text-grayLight") Игр за сегодня
                        div(class="w-full h-[52px] bg-[#1B1C20] rounded-xl flex items-center justify-center")
                            b(class="text-lg text-white") 1 024 323
                img(src="@/images/stats/stats1.png" class="absolute left-0 top-0 w-full h-full object-cover")
                
            div(class="w-full grid relative 2xl:before:pt-[30%] xl:before:pt-[40%] md:before:!pt-[50%] before:pt-[50%] overflow-hidden rounded-2xl")
                div(class="flex items-center justify-center p-6 absolute left-0 top-0 w-full h-full z-[1]")
                    div(class="w-full flex flex-col items-center text-sm space-y-5")
                        b(class="font-medium text-grayLight") Наибольший выигрыш
                        div(class="w-full h-[52px] bg-[#1B1C20] rounded-xl flex items-center justify-between px-3")
                            div(class="flex items-center space-x-3 text-xs font-semibold")
                                img(class="w-[32px] h-[32px] object-cover rounded-lg" src="https://sun9-east.userapi.com/sun9-22/s/v1/ig2/zq-9uttmMfIn0dFnjNN9rwBPrauU9N1DQrYHhiGZJ9Do2BbqTDuQZlnI8dPYoTkmHauXEY-6XZ5wlfCkjFJtA20U.jpg?size=1080x1080&quality=95&type=album")
                                span(class="max-w-[90px] whitespace-nowrap text-ellipsis overflow-hidden") Владислав Одинцов
                            b(class="text-violet text-xs") 1024.00
                img(src="@/images/stats/stats2.png" class="absolute left-0 top-0 w-full h-full object-cover")

            div(class="w-full grid relative 2xl:before:pt-[30%] xl:before:pt-[40%] md:before:!pt-[50%] before:pt-[50%] overflow-hidden rounded-2xl")
                div(class="flex items-center justify-center p-6 absolute left-0 top-0 w-full h-full z-[1]")
                    div(class="w-full flex flex-col items-center text-sm space-y-5")
                        b(class="font-medium text-grayLight") Счастливчик за сегодня
                        div(class="w-full h-[52px] bg-[#1B1C20] rounded-xl flex items-center justify-between px-3")
                            div(class="flex items-center space-x-3 text-xs font-semibold")
                                img(class="w-[32px] h-[32px] object-cover rounded-lg" src="https://sun9-east.userapi.com/sun9-22/s/v1/ig2/zq-9uttmMfIn0dFnjNN9rwBPrauU9N1DQrYHhiGZJ9Do2BbqTDuQZlnI8dPYoTkmHauXEY-6XZ5wlfCkjFJtA20U.jpg?size=1080x1080&quality=95&type=album")
                                span(class="max-w-[90px] whitespace-nowrap text-ellipsis overflow-hidden") Владислав Одинцов
                            b(class="text-violet text-xs") 1024.00
                img(src="@/images/stats/stats3.png" class="absolute left-0 top-0 w-full h-full object-cover")

            div(class="w-full grid relative 2xl:before:pt-[30%] xl:before:pt-[40%] md:before:!pt-[50%] before:pt-[50%] overflow-hidden rounded-2xl")
                div(class="flex items-center justify-center p-6 absolute left-0 top-0 w-full h-full z-[1]")
                    div(class="w-full flex flex-col items-center text-sm space-y-5")
                        b(class="font-medium text-grayLight") Сейчас играют
                        div(class="w-full h-[52px] bg-[#1B1C20] rounded-xl flex items-center justify-center")
                            b(class="text-lg text-white") 1 024 323
                img(src="@/images/stats/stats4.png" class="absolute left-0 top-0 w-full h-full object-cover")
</template>
