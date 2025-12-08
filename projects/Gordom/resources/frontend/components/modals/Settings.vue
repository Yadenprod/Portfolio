<template lang="pug">
    Teleport(to="#modals-container")
        modal(name="settings" :adaptive="true" width="300" height="auto" @before-open="beforeOpen" @before-close="beforeClose")
            div(class="w-full relative flex flex-col")
                div(class="px-6 pt-6 pb-4 flex items-center justify-between select-none")
                    b(class="text-white text-lg font-medium") Настройки
                    a(href="javascript:;" @click="$modal.hide('settings')" class="transition-all duration-200 w-[32px] h-[32px] text-grayLight rounded-lg hover:bg-[#3c3c46] flex items-center justify-center") 
                        svg(class="w-[12px] h-[12x]")
                            use(xlink:href="images/symbols.svg#close")
                div(class="px-6 pb-6 flex flex-col space-y-[10px]")
                    div(class="flex flex-col")
                        ul.w-48.text-sm.font-medium.text-gray-900.rounded-lg
                            li.w-full.rounded-t-lg(class='')
                                .flex.items-center
                                    input#chat.w-4.h-4.text-violet.rounded(type='checkbox' value='' class='border-0 bg-[#44444e] focus:!ring-inherit focus:!shadow-none focus:!ring-0 focus:ring-offset-0 focus:!border-0 focus:!outline-none')
                                    label.py-3.ml-2.w-full.text-xs.font-medium(for='chat' class='cursor-pointer text-grayLight font-semibold') Невидимые игроки в чате
                    div(class="flex flex-col")
                        h3(class="mb-4 font-semibold text-grayLight text-sm") Изменить пароль
                        div(class="flex flex-col space-y-2.5")
                            input(placeholder="Введите текущий пароль" type="password" class="border-0 bg-[#3A3A43] h-[52px] px-5 rounded-xl text-sm font-medium placeholder:text-grayLight/[0.5] focus:ring-0 focus:outline-none focus:border-0")
                            input(placeholder="Введите новый пароль" type="password" class="border-0 bg-[#3A3A43] h-[52px] px-5 rounded-xl text-sm font-medium placeholder:text-grayLight/[0.5] focus:ring-0 focus:outline-none focus:border-0")
                            div(class="[&_button]:w-full")
                                Btn(
                                    :text="'Изменить пароль'"
                                    :type="'button'"
                                    :theme="null"
                                    :ico="null"
                                )
</template>

<style lang="css">
    [type=checkbox]:checked {
        background-image: url(data:image/svg+xml;charset=utf-8,%3Csvg viewBox='0 0 16 16' fill='%23fff' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M12.207 4.793a1 1 0 0 1 0 1.414l-5 5a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L6.5 9.086l4.293-4.293a1 1 0 0 1 1.414 0z'/%3E%3C/svg%3E);
    }
    [type=checkbox]:checked, [type=radio]:checked {
        background-color: currentColor;
        background-position: 50%;
        background-repeat: no-repeat;
        background-size: 100% 100%;
        border-color: transparent;
    }
    [type=checkbox], [type=radio] {
        print-color-adjust: exact;
        --tw-shadow: 0 0 #0000;
        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;
        background-origin: border-box;
        display: inline-block;
        flex-shrink: 0;
        height: 1rem;
        padding: 0;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        vertical-align: middle;
        width: 1rem;
    }
</style>

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
