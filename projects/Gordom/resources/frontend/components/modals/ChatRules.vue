<template lang="pug">
    Teleport(to="#modals-container")
        modal(name="chat-rules" :adaptive="true" width="300" height="auto" @before-open="beforeOpen" @before-close="beforeClose")
            div(class="w-full relative flex flex-col")
                div(class="px-6 pt-6 pb-4 flex items-center justify-between select-none")
                    b(class="text-white text-lg font-medium") Правила чата
                    a(href="javascript:;" @click="$modal.hide('chat-rules')" class="transition-all duration-200 w-[32px] h-[32px] text-grayLight rounded-lg hover:bg-[#3c3c46] flex items-center justify-center") 
                        svg(class="w-[12px] h-[12x]")
                            use(xlink:href="images/symbols.svg#close")
                div(class="px-6")
                    div(class="flex flex-col space-y-2 text-sm")
                        p В чате запрещено:
                        ul(class="text-grayLight flex flex-col [&_li]:py-0.5")
                            li спамить промокоды
                            li попрошайничать
                            li оскорблять администрацию
                            li проявлять чрезмерную агрессию и негатив
                            li обвинять администрацию сайта или сайт в обмане
                            li упоминать другие проекты
                            li отправлять сообщения с рекламой
                div(class="px-6 pt-6 pb-6 flex flex-col")
                    div(@click="$modal.hide('chat-rules')")
                        Btn(
                            :text="'Все понятно'"
                            :type="'button'"
                            :classes="'bg-[#3c3c46] hover:bg-[#43434e] w-full'"
                            :ico="null"
                        )
</template>

<script>
    import Teleport from 'vue2-teleport';
    export default {
        components: {
            Teleport
        },
        methods: {
            beforeOpen() {
                document.body.classList.add('overflow-hidden')
            },
            beforeClose() {
                document.body.classList.remove('overflow-hidden')
            },
        }
    }
</script>
