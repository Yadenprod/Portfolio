<template lang="pug">
    Teleport(to="#modals-container")
        modal(name="modal-register" :adaptive="true" width="300" height="auto" @before-open="beforeOpen" @before-close="beforeClose")
            div(class="w-full relative flex flex-col")
                div(class="px-6 pt-6 pb-4 flex items-center flex-col justify-between select-none space-y-2")
                    b(class="text-white text-lg font-medium") Регистрация
                    p(class="text-xs text-grayLight font-semibold [&_a]:text-violet hover:[&_a]:underline") Уже есть аккаунт? <a href="javascript:;" @click="loginModal()">Войдите</a>
                div(class="px-6 pb-6 flex flex-col space-y-2.5")
                    div(class="flex flex-col")
                        input(placeholder="Введите логин" type="text" class="border-0 bg-[#3A3A43] h-[52px] px-5 rounded-xl text-sm font-medium placeholder:text-grayLight/[0.5] focus:ring-0 focus:outline-none focus:border-0")
                    div(class="flex flex-col")
                        input(placeholder="Введите пароль" type="password" class="border-0 bg-[#3A3A43] h-[52px] px-5 rounded-xl text-sm font-medium placeholder:text-grayLight/[0.5] focus:ring-0 focus:outline-none focus:border-0")
                    div(class="flex flex-col")
                        input(placeholder="Повторите пароль" type="password" class="border-0 bg-[#3A3A43] h-[52px] px-5 rounded-xl text-sm font-medium placeholder:text-grayLight/[0.5] focus:ring-0 focus:outline-none focus:border-0")
                    div(class="[&_button]:w-full")
                            Btn(
                                :text="'Зарегистрироваться'"
                                :type="'button'"
                                :theme="null"
                                :ico="null"
                            )
                div(class="px-6 flex items-center justify-center pb-6")
                    a(href="javascript:;" class="shrink-0 flex w-[48px] h-[48px] rounded-xl bg-[#3A3A43] hover:bg-[#43434d] transition-all duration-200 text-sm flex items-center justify-center")
                        <svg class="w-[20px] h-[20px]" viewBox="0 0 32 18" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M31.247 1.25c.237-.705 0-1.218-1.05-1.218h-3.491c-.881 0-1.288.448-1.525.929 0 0-1.797 4.1-4.305 6.758-.813.769-1.186 1.025-1.626 1.025-.238 0-.543-.256-.543-.961V1.217c0-.833-.27-1.217-1.016-1.217H12.2c-.543 0-.882.384-.882.769 0 .8 1.254.993 1.39 3.235v4.868c0 1.057-.203 1.249-.644 1.249-1.186 0-4.067-4.132-5.795-8.84C5.93.352 5.592 0 4.71 0H1.187C.17 0 0 .448 0 .929c0 .865 1.186 5.22 5.524 10.986 2.88 3.94 6.982 6.053 10.676 6.053 2.236 0 2.508-.48 2.508-1.281v-2.979c0-.96.203-1.12.915-1.12.508 0 1.423.255 3.49 2.145C25.485 16.975 25.893 18 27.214 18h3.49c1.017 0 1.492-.48 1.22-1.41-.304-.928-1.456-2.273-2.948-3.875-.813-.896-2.033-1.89-2.406-2.37-.508-.64-.373-.897 0-1.473-.034 0 4.236-5.701 4.677-7.623z" fill="currentColor"></path></svg>
</template>

<script>
    import Teleport from 'vue2-teleport';
    export default {
        components: {
            Teleport,
        },
        methods: {
            beforeOpen() {
                document.body.classList.add('overflow-hidden')
            },
            beforeClose() {
                document.body.classList.remove('overflow-hidden')
            },
            loginModal() {
                this.$modal.hide('modal-register')
                this.$modal.show('modal-login')
            },
        }
    }
</script>