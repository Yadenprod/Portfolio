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
                            span Бонусы
                    div(class="w-full flex-col rounded-xl space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex")
                        div(class="flex flex-col space-y-[30px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Колесо ежедневных бонусов
                            form(class="flex flex-col space-y-3" @submit.prevent="roll()")
                                div(class="w-full flex flex-col items-center space-y-[30px]")
                                    img(src="@/images/logotype-small.svg" class="max-w-[75px]")
                                    p(class="uppercase text-grayLight text-sm font-medium text-center sm:text-xs [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline") Для получения бонуса, вы должны быть подписаны на нашу группу <a href="https://vk.com/TreasureCasino/" target="_blank">vk.com/TreasureCasino</a>
                                div(class="w-full relative h-[90px] overflow-hidden")
                                    div(class="w-[2px] h-[90%] bg-violet absolute left-1/2 -translate-x-1/2 z-[1] top-1/2 -translate-y-1/2")
                                    div(class="w-[1920px] absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-[64px]")
                                        ul(ref="bonusCarousel" class="flex items-center w-fit space-x-2.5" style="transform: translateX(410px);transition: 10s;")
                                            li(v-for="item in list" :key="item.index" class="shrink-0 pointer-events-none flex w-[64px] h-[64px] rounded-xl bg-[#2c2c31]  text-sm flex flex-col items-center justify-center space-y-0.5")
                                                b {{ item.sum }}
                                                span(class="text-gray") мон.
                                div(class="w-full flex justify-center")
                                    Btn(
                                        :text="'Получить'"
                                        :type="'button'"
                                        :theme="null"
                                        :ico="null"
                                    )

                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Как это работает?
                            div(class="flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline")
                                p Каждые 24 часа крутите бонусную рулетку и получайте от 1 до 100р на свой баланс
                        
                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Оставь отзыв и получи бонус
                            div(class="flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline")
                                p Отправьте в "Предложить новость" нашей группы <a href="https://vk.com/TreasureCasino/" target="_blank">vk.com/TreasureCasino</a> скриншот с крупным выигрышем (более 30000 монет) или большим коэффициентом (более х500) и получите бонус после публикации.
                                    | <br> Требования к посту:
                                    | <br> —  Скриншот должен быть хорошего качества. Не стоит фотографировать экран компьютера, воспользуйтесь встроенными средствами для создания скриншотов. 
                                    | <br> —  На скриншоте не должно быть информации, не относящейся к сайту. 
                                    | <br> —  На скриншоте должен быть виден результат игры. Предпочтение отдается скриншотам, где результат показан непосредственно на странице режима, а не в профиле. 
                                    | <br> —  При возможности, обрежьте скриншот, удалив из него элементы, относящиеся к браузеру или операционной системе (такие как меню "Пуск", верхняя панель браузера и прочее). 
                                    | <br> —  Подпись к скриншоту не должна содержать нецензурной лексики и оскорблений. В подпись не следует включать просьбу о бонусе.

                        div(class="flex flex-col space-y-[20px]")
                            span(class="text-grayLight uppercase font-['Rubik'] font-medium text-sm") Промокод
                            form(class="flex sm:flex-col sm:space-x-0 sm:space-y-3 sm:[&_button]:w-full items-stretch space-x-3" @submit.prevent="activate()")
                                div(class="relative")
                                    input(v-model="promo" type="text" placeholder="Введите промокод" class="border-0 sm:w-full sm:h-[52px] text-sm px-5 placeholder:text-gray focus:ring-0 focus:outline-0 h-full rounded-xl bg-[#1b1c20]")
                                Btn(
                                    :text="'Активировать'"
                                    :type="'button'"
                                    :theme="null"
                                    :ico="null"
                                )
</template> 

<script>
    export default {
        data() {
            return {
                isLoading: false,
                preloader: true,
                list: [
                    {
                        sum: 1
                    },
                    {
                        sum: 250
                    },
                    {
                        sum: 50
                    },
                    {
                        sum: 20
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 100
                    },
                    {
                        sum: 15
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 250
                    },
                    {
                        sum: 50
                    },
                    {
                        sum: 20
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 100
                    },
                    {
                        sum: 15
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 5
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },                    
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },                    
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },                    
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },                    
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },                    
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },                    
                    {
                        sum: 'changeMe'
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 1
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 40
                    },
                    {
                        sum: 30
                    },
                    {
                        sum: 10
                    },
                    {
                        sum: 1
                    },
                ],
                promo: ''
            }
        },
        methods: {
            preloaderDestroy() {
                setTimeout(() => {
                    this.preloader = false;
                }, 300);
            },
            roll() {
                this.$root.axios.post('/bonus/take', {
                    type: 'daily'
                })
                .then(response => {
                    const {data} = response

                    if(data.error) {
                        return this.$toastr.Add({
                            name: 'PromoToast',
                            title: 'Ошибка',
                            msg: data.message,
                            type: 'error',
                            defaultClassNames: ["animated", "zoomInUp"],
                            timeout: 3000,
                            progressbar: true,
                        })
                    }

                    this.list = this.list.map(item => 
                        item.sum == 'changeMe'
                            ? {sum: data.bonus}
                            : item
                    )
                    this.$refs['bonusCarousel'].style.marginLeft = '-7030px'

                    setTimeout(() => {
                        this.$toastr.Add({
                            name: 'PromoToast',
                            title: 'Успех',
                            msg: 'Бонус получен',
                            type: 'success',
                            defaultClassNames: ["animated", "zoomInUp"],
                            timeout: 3000,
                            progressbar: true,
                        })
                        this.$root.user.balance = data.balance
                    }, 10000)
                })
            },
            activate() {
                this.$root.axios.post('/promo/activate', {
                    code: this.promo
                })
                .then(response => {
                    const {data} = response

                    if(data.error) {
                        return this.$toastr.Add({
                            name: 'PromoToast',
                            title: 'Ошибка',
                            msg: data.message,
                            type: 'error',
                            defaultClassNames: ["animated", "zoomInUp"],
                            timeout: 3000,
                            progressbar: true,
                        })
                    }

                    this.$root.user.balance = data.balance

                    this.$toastr.Add({
                        name: 'PromoToast',
                        title: 'Успех',
                        msg: 'Промокод активирован!',
                        type: 'success',
                        defaultClassNames: ["animated", "zoomInUp"],
                        timeout: 3000,
                        progressbar: true,
                    })

                    this.promo = ''
                })
            }
        },
        mounted() {
            this.preloaderDestroy();
        }
    }
</script>
