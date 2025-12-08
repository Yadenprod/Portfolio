<template lang="pug">
    Teleport(to="#modals-container")
        modal(name="pay" :adaptive="true" width="525" height="auto" @before-open="beforeOpen" @before-close="beforeClose")
            div(class="w-full relative flex flex-col")
                div(class="flex items-center justify-between pl-2 pr-4 mb-2")
                    ul(class="flex items-center space-x-2 xa:space-x-0")
                        li 
                            a(href="javascript:;" 
                                class="relative text-sm xa:px-3 xa:text-xs text-grayLight font-semibold py-5 px-5 inline-block transition-all duration-200 hover:text-white before:absolute before:bottom-2 before:w-0 before:h-[3px] before:rounded-full before:bg-[#7c75d9] before:transition-all before:duration-200 [&.active]:before:w-[25px] [&.active]:text-white"
                                :class="currentTab === 'pay' ? 'active' : ''"
                                @click="currentTab = 'pay'"
                            ) Пополнение
                        li 
                            a(
                                href="javascript:;" 
                                class="relative text-sm xa:px-3 xa:text-xs text-grayLight font-semibold py-5 px-5 inline-block transition-all duration-200 hover:text-white before:absolute before:bottom-2 before:w-0 before:h-[3px] before:rounded-full before:bg-[#7c75d9] before:transition-all before:duration-200 [&.active]:before:w-[25px] [&.active]:text-white"
                                :class="currentTab === 'withdraw' ? 'active' : ''"
                                @click="currentTab = 'withdraw'"
                            ) Вывод
                        li 
                            a(
                                href="javascript:;" 
                                class="relative text-sm xa:px-3 xa:text-xs text-grayLight font-semibold py-5 px-5 inline-block transition-all duration-200 hover:text-white before:absolute before:bottom-2 before:w-0 before:h-[3px] before:rounded-full before:bg-[#7c75d9] before:transition-all before:duration-200 [&.active]:before:w-[25px] [&.active]:text-white"
                                @click="showHistoryPay()"
                            ) История

                    a(href="javascript:;" @click="$modal.hide('pay')" class="transition-all duration-200 w-[32px] h-[32px] text-grayLight rounded-lg hover:bg-[#3c3c46] flex items-center justify-center") 
                        svg(class="w-[12px] h-[12x]")
                            use(xlink:href="images/symbols.svg#close")

                div(class="px-5 pb-5 relative")
                    Transition(
                        enter-active-class="transition ease duration-200"
                        enter-class="-translate-x-[50px] opacity-0"
                        enter-to-class="-translate-x-[0px] opacity-100"
                    )
                        div(v-if="currentTab === 'pay'" class="relative")
                            div(v-if="!currentPayTab" class="grid grid-cols-3 xa:grid-cols-2 gap-3 w-full")
                                a(v-for="item in payMethods" @click="payTabShow(item.name)" :key="item.id" href="javascript:;" class="rounded-xl h-[110px] justify-between p-4 flex flex-col items-start text-white font-bold px-4 py-4 bg-[#3A3A43] transition-all duration-200 hover:bg-[#42424E]")
                                    div(class="h-[60%] flex items-center")
                                        img(:src="require('@/images/methods/' + item.image)")
                                    span(class="pointer-events-none") {{ item.name }}
                            div(v-if="currentPayTab" class="relative w-full flex flex-col")
                                div(class="flex flex-col space-y-4")
                                    div(class="flex items-center text-sm text-grayLight")
                                        a(href="javascript:;" @click="currentPayTab = null" class="transition-all duration-200 py-2 h-[32px] hover:text-white text-grayLight flex items-center space-x-2") 
                                            svg(class="w-[18px] h-[18px] -rotate-[180deg]")
                                                use(xlink:href="images/symbols.svg#arrow")
                                            span(class="pointer-events-none") Вернуться назад
                                    div(class="flex flex-col space-y-4")
                                        div(class="flex items-center space-x-3 pointer-events-none")
                                            img(:src="currentPayTab === 'Qiwi' ? require('@/images/methods/qiwi.svg') : '' || currentPayTab === 'Visa' ? require('@/images/methods/visa.svg') : '' || currentPayTab === 'Mastercard' ? require('@/images/methods/mastercard.svg') : '' || currentPayTab === 'Mir' ? require('@/images/methods/mir.svg') : '' || currentPayTab === 'Yoomoney' ? require('@/images/methods/yoomoney.svg') : '' || currentPayTab === 'Freekassa' ? require('@/images/methods/freekassa.png') : ''")
                                            b {{ currentPayTab === 'Qiwi' ? 'Qiwi' : '' || currentPayTab === 'Visa' ? 'Visa' : '' || currentPayTab === 'Mastercard' ? 'Mastercard' : '' || currentPayTab === 'Mir' ? 'Mir' : '' || currentPayTab === 'Yoomoney' ? 'Yoomoney' : '' || currentPayTab === 'Freekassa' ? 'Freekassa' : ''}}
                                        input(v-model="code" type="text" placeholder="Промокод" class="font-['Rubik'] border-0 w-full h-[52px] text-sm px-5 placeholder:text-gray focus:ring-0 focus:outline-0 h-full rounded-xl bg-[#3A3A43]")
                                        div(class="flex items-center gap-3")
                                            input(type="text" v-model="sum" @input="onInputSumm" class="font-['Rubik'] border-0 w-full h-[52px] text-sm px-5 placeholder:text-gray focus:ring-0 focus:outline-0 h-full rounded-xl bg-[#3A3A43]")
                                            div(class="[&_button]:w-full" @click="createOrder")
                                                Btn(
                                                    :text="'Пополнить'"
                                                    :type="'button'"
                                                    :theme="null"
                                                    :ico="null"
                                                )

                    Transition(
                        enter-active-class="transition ease duration-200"
                        enter-class="-translate-x-[50px] opacity-0"
                        enter-to-class="-translate-x-[0px] opacity-100"
                    )
                        div(v-if="currentTab === 'withdraw'" class="relative")
                            div(v-if="!currentWithdrawTab" class="grid grid-cols-3 xa:grid-cols-2 gap-3 w-full")
                                a(v-for="item in withdrawMethods" @click="withdrawTabShow(item.name)" :key="item.id" href="javascript:;" class="rounded-xl h-[110px] justify-between p-4 flex flex-col items-start text-white font-bold px-4 py-4 bg-[#3A3A43] transition-all duration-200 hover:bg-[#42424E]")
                                    div(class="h-[60%] flex items-center")
                                        img(:src="require('@/images/methods/' + item.image)")
                                    span(class="pointer-events-none") {{ item.name }}
                            div(v-if="currentWithdrawTab" class="relative w-full flex flex-col")
                                div(class="flex flex-col space-y-4")
                                    div(class="flex items-center text-sm text-grayLight")
                                        a(href="javascript:;" @click="currentWithdrawTab = null" class="transition-all duration-200 py-2 h-[32px] hover:text-white text-grayLight flex items-center space-x-2") 
                                            svg(class="w-[18px] h-[18px] -rotate-[180deg]")
                                                use(xlink:href="images/symbols.svg#arrow")
                                            span(class="pointer-events-none") Вернуться назад
                                    div(class="flex flex-col space-y-4")
                                        div(class="flex items-center space-x-3 pointer-events-none")
                                            img(:src="currentWithdrawTab === 'Qiwi' ? require('@/images/methods/qiwi.svg') : '' || currentWithdrawTab === 'Visa' ? require('@/images/methods/visa.svg') : '' || currentWithdrawTab === 'Mastercard' ? require('@/images/methods/mastercard.svg') : '' || currentWithdrawTab === 'Mir' ? require('@/images/methods/mir.svg') : '' || currentWithdrawTab === 'Yoomoney' ? require('@/images/methods/yoomoney.svg') : '' || currentWithdrawTab === 'Freekassa' ? require('@/images/methods/freekassa.png') : ''")
                                            b {{ currentWithdrawTab === 'Qiwi' ? 'Qiwi' : '' || currentWithdrawTab === 'Visa' ? 'Visa' : '' || currentWithdrawTab === 'Mastercard' ? 'Mastercard' : '' || currentWithdrawTab === 'Mir' ? 'Mir' : '' || currentWithdrawTab === 'Yoomoney' ? 'Yoomoney' : '' || currentWithdrawTab === 'Freekassa' ? 'Freekassa' : ''}}
                                        div(class="flex flex-col space-y-4")
                                            input(v-model="wallet" type="text" placeholder="Кошелёк" class="font-['Rubik'] border-0 w-full h-[52px] text-sm px-5 placeholder:text-gray focus:ring-0 focus:outline-0 h-full rounded-xl bg-[#3A3A43]")
                                            div(class="flex items-center gap-3")
                                                input(type="text" v-model="sum" @input="onInputSumm" class="font-['Rubik'] border-0 w-full h-[52px] text-sm px-5 placeholder:text-gray focus:ring-0 focus:outline-0 h-full rounded-xl bg-[#3A3A43]")
                                                div(class="[&_button]:w-full" @click="createWithdraw")
                                                    Btn(
                                                        :text="'Вывести'"
                                                        :type="'button'"
                                                        :theme="null"
                                                        :ico="null"
                                                    )
        ModalPayHistory
</template>

<script>
    import Teleport from 'vue2-teleport';
    export default {
        data() {
            return {
                currentTab: 'pay',
                currentPayTab: null,
                currentWithdrawTab: null,
                historyTab: 'pay',
                max: 25000,
                sum: 300,
                wallet: '',
                code: '',
                payMethods: [
                    // {
                    //     id: 0,
                    //     name: 'Qiwi',
                    //     image: 'qiwi.svg'
                    // },
                    {
                        id: 5,
                        name: 'Freekassa',
                        image: 'freekassa.png'
                    },
                ],
                withdrawMethods: [
                    {
                        id: 0,
                        name: 'Visa',
                        image: 'visa.svg'
                    },
                    {
                        id: 1,
                        name: 'Qiwi',
                        image: 'qiwi.svg'
                    },
                    {
                        id: 5,
                        name: 'Freekassa',
                        image: 'freekassa.png'
                    },
                ],
            }
        },
        components: {
            Teleport,
            ModalPayHistory: () => import('@/components/modals/PayHistory.vue'),
        },
        methods: {
            beforeOpen() {
                document.body.classList.add('overflow-hidden')
            },
            beforeClose() {
                document.body.classList.remove('overflow-hidden')
            },
            createOrder() {
                this.$root.axios.post('/payment/create', {
                    system: this.currentPayTab,
                    amount: this.sum,
                    code: this.code
                })
                .then(response => {
                    const {data} = response

                    if(data.error) {
                        return this.$toastr.Add({
                            name: 'BetMinesToast',
                            title: 'Ошибка',
                            msg: data.message,
                            type: 'error',
                            timeout: 3000,
                            progressbar: true,
                        })
                    }

                    location.href = data.url
                })
            },
            createWithdraw() {
                this.$root.axios.post('/withdraw/create', {
                    system: this.currentWithdrawTab,
                    sum: this.sum,
                    wallet: this.wallet
                })
                .then(response => {
                    const {data} = response

                    if(data.error) {
                        return this.$toastr.Add({
                            name: 'BetMinesToast',
                            title: 'Ошибка',
                            msg: data.message,
                            type: 'error',
                            timeout: 3000,
                            progressbar: true,
                        })
                    }

                    this.$toastr.Add({
                        name: 'BetMinesToast',
                        title: 'Успешно',
                        msg: 'Заявка на вывод создана',
                        type: 'success',
                        timeout: 3000,
                        progressbar: true,
                    })

                    this.$root.user.balance = data.balance
                })
            },
            payTabShow(name) {
                this.currentPayTab = name
            },
            withdrawTabShow(name) {
                this.currentWithdrawTab = name
            },
            onInputSumm({ target }) {
                const val = target.value
                const newVal = `${Math.min(this.max, Math.max(0, val.slice(-10000) | 0))}`

                if (val !== newVal) {
                    target.value = newVal
                    target.dispatchEvent(new Event('input'))
                }
                if (val === '') {
                    target.value = ''
                    target.dispatchEvent(new Event('input'))
                }
            },
            showHistoryPay() {
                this.$modal.hide('pay')
                this.$modal.show('pay-history')
            }
        },
        watch: {
            currentTab(newValue) {
                this.currentPayTab = null
                this.currentWithdrawTab = null
            }
        }
    }
</script>
