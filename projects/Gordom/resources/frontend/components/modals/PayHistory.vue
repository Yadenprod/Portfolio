<template lang="pug">
    Teleport(to="#modals-container")
        modal(name="pay-history" :adaptive="true" width="780" height="auto" @before-open="beforeOpen" @before-close="beforeClose")
            div(class="w-full relative flex flex-col")
                div(class="flex items-center justify-between pl-2 pr-4 mb-2 xa:space-x-0")
                    ul(class="flex items-center space-x-2")
                        li 
                            a(href="javascript:;" 
                                class="relative text-sm xa:px-3 xa:text-xs text-grayLight font-semibold py-5 px-5 inline-block transition-all duration-200 hover:text-white before:absolute before:bottom-2 before:w-0 before:h-[3px] before:rounded-full before:bg-[#7c75d9] before:transition-all before:duration-200 [&.active]:before:w-[25px] [&.active]:text-white"
                                :class="currentTab === 'pay' ? 'active' : ''"
                                @click="currentTab = 'pay'"
                            ) Пополнения
                        li 
                            a(
                                href="javascript:;" 
                                class="relative text-sm xa:px-3 xa:text-xs text-grayLight font-semibold py-5 px-5 inline-block transition-all duration-200 hover:text-white before:absolute before:bottom-2 before:w-0 before:h-[3px] before:rounded-full before:bg-[#7c75d9] before:transition-all before:duration-200 [&.active]:before:w-[25px] [&.active]:text-white"
                                :class="currentTab === 'withdraw' ? 'active' : ''"
                                @click="currentTab = 'withdraw'"
                            ) Выводы

                    a(href="javascript:;" @click="$modal.hide('pay-history')" class="transition-all duration-200 w-[32px] h-[32px] text-grayLight rounded-lg hover:bg-[#3c3c46] flex items-center justify-center") 
                        svg(class="w-[12px] h-[12x]")
                            use(xlink:href="images/symbols.svg#close")

                div(class="px-5 pb-5 relative")
                    Transition(
                        enter-active-class="transition ease duration-200"
                        enter-class="-translate-x-[50px] opacity-0"
                        enter-to-class="-translate-x-[0px] opacity-100"
                    )
                        div(v-if="currentTab === 'pay'" class="relative") 
                            div(
                                class="\
                                    sm:overflow-auto\
                                    [&_div.table>div>div>div:first-child]:w-1/2 [&>div.table>div:first-child>div:first-child]:w-1/2\
                                    [&_div.table>div:last-child>div:nth-child(odd)]:bg-[#3A3A43]\
                                    [&_div.table>div:last-child>div:nth-child(even)]:bg-[#3A3A43]\
                                    md:[&_div.table]:text-xs\
                                    md:[&_div.table>div:last-child>div]:text-xs\
                                    [&_div.table>div:last-child]:space-y-2\
                                    sm:[&_div.table]:min-w-[780px]\
                                "
                            )
                                <div class="table w-full flex flex-col text-sm">
                                    <div class="flex items-center justify-between mb-4">
                                        <div class="w-full text-[#6a6a7a] font-semibold px-4">#</div>
                                        <div class="w-full text-[#6a6a7a] font-semibold px-4">Дата</div>
                                        <div class="w-full text-[#6a6a7a] font-semibold px-4">Сумма</div>
                                        <div class="w-full text-[#6a6a7a] font-semibold px-4">Статус</div>
                                    </div>
                                    <div class="flex flex-col">
                                        <div v-for="item in historyPay" class="flex py-4 odd:bg-[#2c2c31] items-center rounded-xl justify-between font-['Rubik'] font-medium text-sm">
                                            <div class="px-4 w-full">
                                                <span>{{ item.id }}</span>
                                            </div>
                                            <div class="px-4 w-full">
                                                <span>{{ $moment(item.created_at).format('lll') }}</span>
                                            </div>
                                            <div class="px-4 w-full">
                                                <span>{{ item.sum }} ₽</span>
                                            </div>
                                            <div class="px-4 w-full">
                                                <span>{{ item.status == 1 ? 'Оплачен' : 'Ожидает' }}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                    Transition(
                        enter-active-class="transition ease duration-200"
                        enter-class="-translate-x-[50px] opacity-0"
                        enter-to-class="-translate-x-[0px] opacity-100"
                    )
                        div(v-if="currentTab === 'withdraw'" class="relative") 
                            div(
                                class="\
                                    sm:overflow-auto\
                                    [&_div.table>div>div>div:first-child]:w-1/2 [&>div.table>div:first-child>div:first-child]:w-1/2\
                                    [&_div.table>div:last-child>div:nth-child(odd)]:bg-[#3A3A43]\
                                    [&_div.table>div:last-child>div:nth-child(even)]:bg-[#3A3A43]\
                                    md:[&_div.table]:text-xs\
                                    md:[&_div.table>div:last-child>div]:text-xs\
                                    [&_div.table>div:last-child]:space-y-2\
                                    sm:[&_div.table]:min-w-[780px]\
                                "
                            )
                                <div class="table w-full flex flex-col text-sm">
                                    <div class="flex items-center justify-between mb-4">
                                        <div class="w-full text-[#6a6a7a] font-semibold px-4">#</div>
                                        <div class="w-full text-[#6a6a7a] font-semibold px-4">Дата</div>
                                        <div class="w-full text-[#6a6a7a] font-semibold px-4">Система</div>
                                        <div class="w-full text-[#6a6a7a] font-semibold px-4">Реквизиты</div>
                                        <div class="w-full text-[#6a6a7a] font-semibold px-4">Сумма</div>
                                        <div class="w-full text-[#6a6a7a] font-semibold px-4">Статус</div>
                                    </div>
                                    <div class="flex flex-col">
                                        <div v-for="item in historyWithdraw" class="flex py-4 odd:bg-[#2c2c31] items-center rounded-xl justify-between font-['Rubik'] font-medium text-sm">
                                            <div class="px-4 w-full">
                                                <span>{{ item.id }}</span>
                                            </div>
                                            <div class="px-4 w-full">
                                                <span>{{ $moment(item.created_at).format('lll') }}</span>
                                            </div>
                                            <div class="px-4 w-full">
                                                <span>{{ item.system }}</span>
                                            </div>
                                            <div class="px-4 w-full">
                                                <span>{{ item.wallet }}</span>
                                            </div>
                                            <div class="px-4 w-full">
                                                <span>{{ item.sum }} ₽</span>
                                            </div>
                                            <div class="px-4 w-full">
                                                <span :class="getColorStatus(item.status)">{{ getTextStatus(item.status, item.reason) }} <span v-if="item.status == 0" class="text-[#fff] !cursor-pointer" @click="decline(item.id)">(отменить)</span></span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
</template>

<script>
    import Teleport from 'vue2-teleport';
    export default {
        data() {
            return {
                currentTab: 'pay',
                historyPay: [],
                historyWithdraw: []
            }
        },
        components: {
            Teleport,
            Table: () => import('@/components/ui/Table.vue')
        },
        methods: {
            initPayments() {
                this.$root.axios.post('/payment/init')
                .then(response => {
                    const {data} = response

                    this.historyPay = data.payments
                })
            },
            initWithdraws() {
                this.$root.axios.post('/withdraw/init')
                .then(response => {
                    const {data} = response

                    this.historyWithdraw = data.withdraws
                })
            },
            decline(id) {
                this.$root.axios.post('/withdraw/decline', {
                    id
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

                    this.historyWithdraw = this.historyWithdraw.map(item => 
                        item.id !== id
                            ? item
                            : {...item, status: 2}
                    )
                    
                    this.$root.user.balance = data.balance
                })
            },
            getColorStatus(status) {
                if(status == 0) {
                    return 'text-[#ff8f05]'
                }
                
                if(status == 1) {
                    return 'text-[#0db53a]'
                }

                if(status == 2) {
                    return 'text-[#ff3705]'
                }
            },
            getTextStatus(status, reason) {
                if(status == 0) {
                    return 'Ожидание'
                }

                if(status == 1) {
                    return 'Выполнено'
                }

                if(status == 2) {
                    return !reason ? 'Отменено' : reason
                }

                if(status == 3) {
                    return 'Обработка'
                }
            },
            beforeOpen() {
                document.body.classList.add('overflow-hidden')
                this.initPayments()
                this.initWithdraws()
            },
            beforeClose() {
                document.body.classList.remove('overflow-hidden')
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
        },
    }
</script>
