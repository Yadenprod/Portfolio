<template lang="pug">
    div(class="h-full overflow-auto space-y-3" ref="chatScroll")
        div(
            v-for="item in messages" 
            :key="item.id" 
            class="w-full bg-[#2c2c31] p-3 flex items-start justify-between rounded-xl"
        )
            div(
                class="shrink-0 w-[40px] h-[40px] overflow-hidden top-0.5 relative rounded-xl"
                :class="item.role === 'youtuber' ? 'border-2 border-[#f24841]' : '' || item.role === 'moderator' ? 'border-2 border-[#44c276]' : ''"
            )
                img(
                    class="absolute left-0 top-0 w-full h-full object-cover"
                    :src="item.user.avatar"
                )
            div(class="w-full flex flex-col py-1 pl-3.5 pr-1.5 relative space-y-1")
                div(class="flex items-center justify-between")
                    b(
                        class="text-xs text-[#cfcde9] max-w-[120px] overflow-hidden text-ellipsis whitespace-nowrap" 
                        :class="item.role === 'admin' ? '!text-[#7c75d9]' : '' || item.role === 'youtuber' ? '!text-[#f24841]' : '' || item.role === 'moderator' ? '!text-[#44c276]' : ''"
                    ) {{ item.user.nickname }}
                    div.message__props(class="flex items-center grow justify-end")
                        span.message__time(class="text-xs text-[#46464e] font-bold") {{ item.date }}
                        div.message__actions(class="flex items-center justify-between" v-if="$root.user !== null && ($root.user.is_admin || $root.user.is_moderator)")
                            span.message__action(@click="deleteMessage(item.id)" class="flex w-[32px] h-[32px] items-center text-xs justify-center bg-[#3A3A40] rounded transition-all duration-200 hover:bg-[#7C75D9] hover:!text-white")
                                svg(class="w-[12px] h-[12x]")
                                    use(xlink:href="@/images/symbols.svg#close")
                            span.message__action(class="flex w-[32px] h-[32px] items-center text-xs justify-center bg-[#3A3A40] rounded transition-all duration-200 hover:bg-[#7C75D9] hover:!text-white" @click="modalBan(item.id)") !
                div(
                    class="text-xs text-[#6a6a7a] font-medium [&_p]:leading-[160%]"
                    :class="item.role === 'admin' ? '!text-[#cfcde9]' : '' || item.role === 'youtuber' ? '!text-[#cfcde9]' : '' || item.role === 'moderator' ? '!text-[#cfcde9]' : ''"
                )
                    p(v-html="item.message")
        modalBan(:user_id="selectedUser")
</template>

<script>
    export default {
        props: {
            messages: {
                type: Array,
                default: () => {}
            },
        },
        data() {
            return {
                selectedUser: null
            }
        },
        components: {
            modalBan: () => import('@/components/modals/Ban.vue'),
        },
        methods: {
            selectMessage(id) {
                const message = this.messages.find(item => item.id == id)
                this.selectedUser = message.user.id
            },
            modalBan(id) {
                this.$modal.show("modal-ban")
                this.selectMessage(id)
            },
            deleteMessage(id) {
                this.$root.axios.post('/chat/delete', {
                    id
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
                        msg: 'Сообщение удалено',
                        type: 'success',
                        defaultClassNames: ["animated", "zoomInUp"],
                        timeout: 3000,
                        progressbar: true,
                    })
                })
            }
        },
        updated () {
            this.$nextTick(() => {
                const scrollbar = this.$refs.chatScroll
                scrollbar.scrollTop = scrollbar.scrollHeight
            })
        },
        mounted() {
            this.$nextTick(() => {
                const scrollbar = this.$refs.chatScroll
                scrollbar.scrollTop = scrollbar.scrollHeight
            }) 
        }
    }
</script>

<style lang="scss">
.message__props {
    &:hover {
        > .message__time {
            display: none;
        }

        > .message__actions {
            display: flex;
        }
    }
}

.message__actions {
    display: none;
    column-gap: 6px;
}

.message__action {
    width: 16px;
    height: 16px;

    display: flex;
    align-items: center;
    justify-content: center;

    text-align: center;

    padding: 4px;

    cursor: pointer !important;

    &:hover {
        color: lighten(#46464e, 10%);

        background: #46464e;
    }
}
</style>
