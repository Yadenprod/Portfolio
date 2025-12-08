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
                                use(xlink:href="images/symbols.svg#faq")
                            span Помощь
                    .faq(class="w-full flex flex-col space-y-[20px]")
                        .faq-item(class="relative bg-[#202024] rounded-xl overflow-hidden")
                            .faq-heading(v-on:click="faq" class="[&.active]:bg-[#26262b] [&.active]:text-white [&.active>i]:top-[3px] [&.active>i]:rotate-[225deg] flex items-center justify-between px-6 py-5 text-grayLight font-semibold transition-all cursor-pointer duration-200 hover:bg-[#26262b]")
                                span(class="pointer-events-none") Не пришел вывод
                                i(class="relative inline-block w-2 h-2 border-r-2 border-b-2 border-current rotate-[45deg] transition-all duration-200")
                            .faq-body(class="px-6 py-6 flex relative space-y-4 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] hidden")
                                p Вывод на QIWI осуществляется до 24 часов. Вывод на остальные платежные системы может занимать до 48 часов.
                                
                        .faq-item(class="relative bg-[#202024] rounded-xl overflow-hidden")
                            .faq-heading(v-on:click="faq" class="[&.active]:bg-[#26262b] [&.active]:text-white [&.active>i]:top-[3px] [&.active>i]:rotate-[225deg] flex items-center justify-between px-6 py-5 text-grayLight font-semibold transition-all cursor-pointer duration-200 hover:bg-[#26262b]")
                                span(class="pointer-events-none") Как начать с вами сотрудничать? 
                                i(class="relative inline-block w-2 h-2 border-r-2 border-b-2 border-current rotate-[45deg] transition-all duration-200")
                            .faq-body(class="px-6 py-6 flex relative space-y-4 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] hidden")
                                p Чтобы предложить нам сотрудничество, вы можете написать нам в лс группы VK.
                        
                        .faq-item(class="relative bg-[#202024] rounded-xl overflow-hidden")
                            .faq-heading(v-on:click="faq" class="[&.active]:bg-[#26262b] [&.active]:text-white [&.active>i]:top-[3px] [&.active>i]:rotate-[225deg] flex items-center justify-between px-6 py-5 text-grayLight font-semibold transition-all cursor-pointer duration-200 hover:bg-[#26262b]")
                                span(class="pointer-events-none") Есть ли отыгрыш депозита?
                                i(class="pointer-events-none relative inline-block w-2 h-2 border-r-2 border-b-2 border-current rotate-[45deg] transition-all duration-200")
                            .faq-body(class="px-6 py-6 flex relative space-y-4 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] hidden")
                                p Да, сумма любой вашей ставки учитывается при отыгрыше. Отыгрыш составляет x2 от депозита.
                        
                        .faq-item(class="relative bg-[#202024] rounded-xl overflow-hidden")
                            .faq-heading(v-on:click="faq" class="[&.active]:bg-[#26262b] [&.active]:text-white [&.active>i]:top-[3px] [&.active>i]:rotate-[225deg] flex items-center justify-between px-6 py-5 text-grayLight font-semibold transition-all cursor-pointer duration-200 hover:bg-[#26262b]")
                                span(class="pointer-events-none") Как часто я могу брать бонусы и сколько я получу?
                                i(class="relative inline-block w-2 h-2 border-r-2 border-b-2 border-current rotate-[45deg] transition-all duration-200")
                            .faq-body(class="px-6 py-6 flex relative space-y-4 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] hidden")
                                p Каждые 24 часа крутите бонусную рулетку и получайте от 1 до 100р на свой баланс

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
            faq: function (event) {
                var items = document.querySelectorAll('.faq-item')
                for (var i = 0; i < items.length; i++) {
                    items[i].classList.remove('active')
                }
                if (event.target.classList.contains('active')) {
                    event.target.classList.remove('active')
                } else {
                    event.target.classList.add('active')
                }
            }
        },
        mounted() {
            this.preloaderDestroy();
        }
    }
</script>


<style lang="scss">
    .faq {
        .faq-heading {
            &.active + .faq-body {
                display: block;
            }
        }
    }
</style>
