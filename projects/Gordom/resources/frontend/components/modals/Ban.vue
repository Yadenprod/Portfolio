<template lang="pug">
    Teleport(to="#modals-container")
        modal(name="modal-ban" :adaptive="true" width="300" height="auto" @before-open="beforeOpen" @before-close="beforeClose")
            div(class="w-full relative flex flex-col")
                div(class="px-6 pt-6 pb-4 flex items-center justify-between select-none")
                    b(class="text-white text-lg font-medium") Блокировка
                    a(href="javascript:;" @click="$modal.hide('modal-ban')" class="transition-all duration-200 w-[32px] h-[32px] text-grayLight rounded-lg hover:bg-[#3c3c46] flex items-center justify-center") 
                        svg(class="w-[12px] h-[12x]")
                            use(xlink:href="images/symbols.svg#close")
                div(class="px-6 pb-6")
                    div(class="flex flex-col")
                        div(class="flex flex-col space-y-2.5")
                            input(v-model="reason" placeholder="Причина блокировки" type="text" class="border-0 bg-[#3A3A43] h-[52px] px-5 rounded-xl text-sm font-medium placeholder:text-grayLight/[0.5] focus:ring-0 focus:outline-none focus:border-0")
                            input(v-model="time" placeholder="Срок блокировки (в минутах)" type="text" class="border-0 bg-[#3A3A43] h-[52px] px-5 rounded-xl text-sm font-medium placeholder:text-grayLight/[0.5] focus:ring-0 focus:outline-none focus:border-0")
                            div(class="[&_button]:w-full" @click="ban")
                                Btn(
                                    :text="'Заблокировать'"
                                    :type="'button'"
                                    :theme="null"
                                    :ico="null"
                                )
</template>

<script>
    import Teleport from 'vue2-teleport';
    export default {
        props: ['user_id'],
        components: {
            Teleport
        },
        data() {
            return {
                reason: null,
                time: null
            }
        },
        methods: {
            beforeOpen() {
                document.body.classList.add('overflow-hidden')
            },
            beforeClose() {
                document.body.classList.remove('overflow-hidden')
            },
            ban() {
                this.$root.axios.post('/chat/ban', {
                    user_id: this.user_id,
                    time: this.time,
                    reason: this.reason
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
                    
                    this.$toastr.Add({
                        name: 'PromoToast',
                        title: 'Успех',
                        msg: 'Пользователь заблокирован',
                        type: 'success',
                        defaultClassNames: ["animated", "zoomInUp"],
                        timeout: 3000,
                        progressbar: true,
                    })

                    this.$modal.hide('modal-ban')
                    this.time = ''
                    this.reason = ''
                })
            }
        }
    }
</script>
