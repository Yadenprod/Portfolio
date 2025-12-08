<template lang="pug">
    div(class="fixed right-0 top-0 h-full lg:h-[calc(100%_-_67px)] pr-[16px] py-[16px] transition-all duration-200 lg:p-0 lg:translate-x-[0%] lg:z-[20] lg:left-0 lg:top-[67px] lg:right-inherit" :class="chatOpen ? '' : 'translate-x-[100%] lg:translate-x-[0%] lg:hidden'")
        a(v-if="!chatOpen" href="javascript:;" @click="chatInitState" class="lg:hidden absolute -left-[56px] top-[16px] w-[36px] h-[36px] rounded-[12px] bg-[#7c75d9] flex items-center justify-center transition-all duration-200 hover:bg-[#6962c1]")
            svg(class="w-[18px] h-[18px] rotate-[180deg]")
                use(xlink:href="@/images/symbols.svg#arrow") 
        div(class="relative overflow-hidden flex flex-col lg:w-full lg:rounded-none justify-between w-[300px] gap-6 h-full bg-[#202024] lg:px-4 px-6 rounded-xl pb-6 lg:pb-4")
            div(class="pt-6 lg:pt-4 flex items-center justify-between")
                div(class="flex flex-col space-y-1")
                    b(class="text-[#cfcde9] text-sm") Online чат
                    a(href="javascript:;" @click="modalRules()" class="text-[#46464e] text-sm font-semibold transition-all duration-200 hover:text-[#7c75d9]") Правила чата
                a(href="javascript:;" @click="chatInitState" class="w-[36px] h-[36px] rounded-[12px] bg-[#7c75d9] flex items-center justify-center transition-all duration-200 hover:bg-[#6962c1]")
                    svg(class="w-[18px] h-[18px]")
                        use(xlink:href="@/images/symbols.svg#arrow")
            div(class="w-full h-[calc(100%_-_185px)]" :class="preloader ? 'flex items-center justify-center' : ''")
                Spin(v-if="preloader" :color="'#cfcde9'")
                Transition(
                    enter-active-class="transition ease-out duration-800"
                    enter-class="transform opacity-0 scale-95"
                    enter-to-class="transform opacity-100 scale-100"
                )
                    div(v-if="!preloader" class="w-full h-full [&_div.scroll-content]:space-y-3 [&_div.scrollbar-track]:bg-transparent [&_div.scrollbar-thumb]:bg-[#5d5d6a]/[0.5]")
                        Message(:messages="messages")
            form(class="h-[70px] shrink-0 rounded-xl w-full bg-[#1b1c20]" @submit.prevent="addMessage()")
                div(class="w-full h-full relative")
                    input(v-model="msg" type="text" class="w-full h-full pl-6 pr-28 font-semibold bg-transparent border-0 focus:ring-0 focus:ring-inherit focus:outline-0 text-sm")
                    button(type="submit" class="absolute cursor-pointer right-5 top-1/2 -translate-y-1/2 w-[36px] h-[36px] rounded-[12px] bg-[#7c75d9] flex items-center justify-center transition-all duration-200 hover:bg-[#6962c1] focus:ring-0 focus:outline-0")
                        svg(class="w-[18px] h-[18px] pointer-events-none")
                            use(xlink:href="@/images/symbols.svg#send") 
        ModalChatRules

</template>

<script>
    export default {
        name: 'Chat',
        components: {
            Message: () => import('./Message.vue'),
            ModalChatRules: () => import('@/components/modals/ChatRules.vue')
        },
        data() {
            return {
                messages: [],
                msg: '',
                preloader: true,
                width: 0,
            }
        },
        props: {
            chatOpen: {
                type: Boolean,
                default: () => {}
            }
        },
        methods: {
            init() {
                this.$root.axios.post('/chat/init')
                .then(response => {
                    const {data} = response
                    
                    let messages = [];
                    data.forEach(message => {
                        messages.push({
                            id: message.id,
                            user: {
                                id: message.user_id,
                                avatar: message.avatar,
                                nickname: message.login
                            },
                            role: message.role,
                            date: message.time,
                            message: message.text,
                        })
                    })

                    this.preloader = false
                    this.messages = messages.reverse()
                })
            },
            chatInitState() {
                if (this.chatOpen) {
                    this.$emit('chatInitState', false);
                } else {
                    this.$emit('chatInitState', true);
                }
            },
            updateWidth() {
                this.width = window.innerWidth;
                if (window.innerWidth <= 1075) {
                    this.$emit('chatInitState', false)
                }
            },
            modalRules() {
                this.$modal.show('chat-rules')
            },
            addMessage() {
                this.$root.axios.post('/chat/send', {
                    message: this.msg
                })
                .then(response => {
                    const {data} = response

                    if(data.error) {
                        return this.$toastr.Add({
                            name: 'chatSendMsg',
                            title: 'Ошибка',
                            msg: data.message,
                            type: 'error',
                            defaultClassNames: ["animated", "zoomInUp"],
                            timeout: 3000,
                            progressbar: true,
                        })
                    }

                    this.msg = ''
                })
            },
        },
        mounted() {
            this.init();
            if (window.innerWidth <= 1075) {
                this.$emit('chatInitState', false)
            }
        },
        created() {
            window.addEventListener('resize', this.updateWidth);
        },
        sockets: {
            'chat.message' (data) {
                this.messages.push({
                    id: data.id,
                    user: {
                        id: data.user_id,
                        avatar: data.avatar,
                        nickname: data.login
                    },
                    date: data.time,
                    role: data.role,
                    message: data.text
                });
            },
            'chat.delete' (data) {
                this.messages = this.messages.filter(item => item.id !== data.id)
            }
        },
        watch: {
            '$route' (to, from) {
                if (window.innerWidth <= 1075) {
                    this.$emit('chatInitState', false)
                }
            }
        }
    }
</script>
