<template lang="pug">
    .table(class="w-full flex flex-col text-sm")
        div(class="flex items-center justify-between mb-4")
            div(v-for="item in table.thead" :key="item.id" class="w-full text-[#6a6a7a] font-semibold px-4") {{ item.name }}
        div(class="flex flex-col")
            div(v-for="item in table.tbody" :key="item.id" class="flex py-4 odd:bg-[#2c2c31] items-center rounded-xl justify-between font-['Rubik'] font-medium text-sm")
                div(v-for="item in item.items" :key="item.id" class="px-4 w-full")
                    div(v-if="item.ico" class="flex space-x-2 items-center")
                        svg(class="w-[18px] h-[18px] text-grayLight") 
                            use(:xlink:href="'images/symbols.svg#' + item.ico")
                        span {{ item.icoText }}
                    div(v-if="item.user" class="flex space-x-3 items-center")
                        img(class="shrink-0 w-[32px] h-[32px] object-cover rounded-lg" :src="item.user.avatar")
                        span(class="lg:hidden") {{ item.user.username }}
                    span(v-if="!item.ico && !item.user") {{ item.value }}
</template>

<script>
    export default {
        props: {
            table: {
                type: Object,
                default: () => {}
            }
        }
    }
</script>
