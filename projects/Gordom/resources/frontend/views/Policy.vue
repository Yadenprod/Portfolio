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
                            span Политика конфиденциальности
                    div(class="relative w-full p-[24px] bg-violet rounded-xl text-white/[0.8] text-sm space-y-3")
                        p Пожалуйста, внимательно прочитайте эту Политику конфиденциальности перед использованием Treasure Casino. 
                        p Мы предоставляем доступ к различным играм на нашей платформе. Пользуясь нашими сервисами, Вы доверяете нам свою информацию. Мы понимаем, что это большая ответственность, и прилагаем все усилия, чтобы защитить Ваши данные и дать Вам возможность управлять ими.
                        p В этой Политике конфиденциальности описано, какую информацию мы собираем, с какой целью мы это делаем и как Вы можете обновлять, удалять свои данные и управлять ими.
                    div(class="w-full flex-col rounded-xl space-y-[30px] p-[32px] bg-[#202024] relative z-[1] flex")
                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Информация, которую мы собираем
                            div(class="flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline")
                                p Виды персональной информации, которую мы собираем:
                                p 1. имя, игровой никнейм;
                                    | <br> 2. адрес электронной почты;
                                    | <br> 3. номер телефона;
                                    | <br> 4. IP-адрес, браузер, ОС;
                                    | <br> 5. номера кошельков, из которых были пополнения и выводы;
                                    | <br> 6. если Вы создаете аккаунт через социальные сети (ВКонтакте, Facebook, Яндекс, Google, Steam, Twitch, Mail.ru, Reddit, Одноклассники), то, соответственно, мы будем хранить Ваше имя, фотографию профиля, ссылку на страницу в социальные сети.
                        
                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Как мы используем информацию, полученную от игроков
                            div(class="flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline")
                                p Став игроком, или иным способом предоставив Treasure Casino персональную информацию, Вы соглашаетесь с тем, что мы собираем и используем Вашу персональную информацию для предоставления нами услуг.
                                    | <br> Вы соглашаетесь на предоставления номера телефона и/или адреса электронной почты третьей стороне для маркетинговых целей.
                                    | <br> Вы соглашаетесь на предоставление ID игры, имени Вашего игрока, ставки, выигрышного коэффициента и выигрыша для публикации в наших социальных сетях.
                                    | <br> Вы соглашаетесь с тем, что мы имеем право раскрывать вашу персональную информацию, но лишь с целью и в случаях, если такое требование выдвинуто государственными органами, в предусмотренном действующим законодательством порядке.

                                    
                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Обращение с жалобами и применимое законодательство
                            div(class="flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline")
                                p В случае возникновения споров и разногласий наше решение является окончательным и Вы с ним полностью согласны. Все споры и разногласия, возникающие из или в связи с настоящей политикой, разрешаются путем переговоров. Если невозможно достичь соглашения путем переговоров, споры, разногласия и претензии, вытекающие из настоящей политики, разрешаются в соответствии с действующим законодательством Нидерландских Антильских островов.ы соглашаетесь с тем, что мы имеем право раскрывать вашу персональную информацию, но лишь с целью и в случаях, если такое требование выдвинуто государственными органами, в предусмотренном действующим законодательством порядке.
                                p Если у Вас есть какие-либо вопросы, запросы на доступ, или жалобы, связанные с обработкой, Вы можете обратиться к нашей команде поддержки клиентов с соответствующим запросом.


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
