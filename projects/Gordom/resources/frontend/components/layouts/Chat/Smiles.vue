<template lang="pug">
    div(class="absolute top-1/2 -translate-y-1/2 right-16" v-on-clickaway="closeMenu")
        div.relative()
            button(
                type="button"
                @click="isMenuOpen = !isMenuOpen"
                class="w-[36px] h-[36px] flex items-center transition-all duration-200 justify-center text-[#46464e] hover:text-[#7c75d9] focus:ring-0 focus:ring-inherit focus:outline-0"
            )
                <svg class="w-[20px] h-[20px]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
                </svg>
        Transition(
            enter-active-class="transition ease-out duration-100"
            enter-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
        )
                div(
                    v-if="isMenuOpen"
                    class="scroll absolute origin-bottom-right right-0 overflow-auto -top-[210px] h-[200px] mt-2 w-48 rounded-xl bg-[#44444c] shadow-[0px_4px_28px_rgba(0,0,0,0.08)]"
                )
                    div(v-for="item in smiles" :key="item.id" class="relative")
                        div(class="sticky left-0 top-0 pt-3 bg-[#44444c] z-[1] flex items-start justify-start before:absolute before:-bottom-[20px] before:left-0 before:w-full before:h-[20px] before:z-[1] before:pointer-events-none before:bg-gradient-to-b before:from-[#44444c] before:to-transparent")
                            div(class="w-full text-[#cfcde9] h-full flex items-center justify-start px-4 uppercase font-semibold text-xs") {{ item.group }}
                        div(class="w-full grid grid-cols-5 p-2")
                            a(v-for="item in item.items" :key="item.id" @click="isMenuOpen = false;" href="javascript:;" :data-keycode="item.key" class="w-full grid relative before:pt-[100%] rounded-md transition-all duration-200 hover:bg-[#575762]")
                                div(class="absolute left-0 top-0 pointer-events-none w-full h-full flex items-center justify-center")
                                    img(:src="require('@/images/smiles/' + item.group + '/' + item.image)" class="max-w-[20px]")

</template>

<script>
    export default {
        name: 'Chat',
        data() {
            return {
                isMenuOpen: false,
                smiles: [
                    {
                        id: 1,
                        group: 'Эмоции',
                        items: [
                            {
                                id: 1,
                                key: '',
                                group: 'emotions',
                                image: '1.png',
                            },
                            {
                                id: 2,
                                key: '',
                                group: 'emotions',
                                image: '2.png',
                            },
                            {
                                id: 3,
                                key: '',
                                group: 'emotions',
                                image: '3.png',
                            },
                            {
                                id: 4,
                                key: '',
                                group: 'emotions',
                                image: '4.png',
                            },
                            {
                                id: 5,
                                key: '',
                                group: 'emotions',
                                image: '5.png',
                            },
                            {
                                id: 6,
                                key: '',
                                group: 'emotions',
                                image: '6.png',
                            },
                            {
                                id: 7,
                                key: '',
                                group: 'emotions',
                                image: '7.png',
                            },
                            {
                                id: 8,
                                key: '',
                                group: 'emotions',
                                image: '8.png',
                            },
                            {
                                id: 9,
                                key: '',
                                group: 'emotions',
                                image: '9.png',
                            },
                            {
                                id: 10,
                                key: '',
                                group: 'emotions',
                                image: '10.png',
                            },
                            {
                                id: 11,
                                key: '',
                                group: 'emotions',
                                image: '11.png',
                            },
                            {
                                id: 12,
                                key: '',
                                group: 'emotions',
                                image: '12.png',
                            },
                            {
                                id: 13,
                                key: '',
                                group: 'emotions',
                                image: '13.png',
                            },
                            {
                                id: 14,
                                key: '',
                                group: 'emotions',
                                image: '14.png',
                            },
                            {
                                id: 15,
                                key: '',
                                group: 'emotions',
                                image: '15.png',
                            },
                            {
                                id: 16,
                                key: '',
                                group: 'emotions',
                                image: '16.png',
                            },
                            {
                                id: 17,
                                key: '',
                                group: 'emotions',
                                image: '17.png',
                            },
                            {
                                id: 18,
                                key: '',
                                group: 'emotions',
                                image: '18.png',
                            },
                            {
                                id: 19,
                                key: '',
                                group: 'emotions',
                                image: '19.png',
                            },
                            {
                                id: 20,
                                key: '',
                                group: 'emotions',
                                image: '20.png',
                            },
                            {
                                id: 21,
                                key: '',
                                group: 'emotions',
                                image: '21.png',
                            },
                            {
                                id: 22,
                                key: '',
                                group: 'emotions',
                                image: '22.png',
                            },
                            {
                                id: 23,
                                key: '',
                                group: 'emotions',
                                image: '23.png',
                            },
                            {
                                id: 24,
                                key: '',
                                group: 'emotions',
                                image: '24.png',
                            },
                            {
                                id: 25,
                                key: '',
                                group: 'emotions',
                                image: '25.png',
                            },
                            {
                                id: 26,
                                key: '',
                                group: 'emotions',
                                image: '26.png',
                            },
                            {
                                id: 27,
                                key: '',
                                group: 'emotions',
                                image: '27.png',
                            },
                            {
                                id: 28,
                                key: '',
                                group: 'emotions',
                                image: '28.png',
                            },
                            {
                                id: 29,
                                key: '',
                                group: 'emotions',
                                image: '29.png',
                            },
                            {
                                id: 30,
                                key: '',
                                group: 'emotions',
                                image: '30.png',
                            },
                        ]
                    },
                    {
                        id: 2,
                        group: 'Действие',
                        items: [
                            {
                                id: 1,
                                key: '',
                                group: 'actions',
                                image: '1.png',
                            },
                            {
                                id: 2,
                                key: '',
                                group: 'actions',
                                image: '2.png',
                            },
                            {
                                id: 3,
                                key: '',
                                group: 'actions',
                                image: '3.png',
                            },
                            {
                                id: 4,
                                key: '',
                                group: 'actions',
                                image: '4.png',
                            },
                            {
                                id: 5,
                                key: '',
                                group: 'actions',
                                image: '5.png',
                            },
                            {
                                id: 6,
                                key: '',
                                group: 'actions',
                                image: '6.png',
                            },
                            {
                                id: 7,
                                key: '',
                                group: 'actions',
                                image: '7.png',
                            },
                            {
                                id: 8,
                                key: '',
                                group: 'actions',
                                image: '8.png',
                            },
                            {
                                id: 9,
                                key: '',
                                group: 'actions',
                                image: '9.png',
                            },
                            {
                                id: 10,
                                key: '',
                                group: 'actions',
                                image: '10.png',
                            },
                            {
                                id: 11,
                                key: '',
                                group: 'actions',
                                image: '11.png',
                            },
                            {
                                id: 12,
                                key: '',
                                group: 'actions',
                                image: '12.png',
                            },
                            {
                                id: 13,
                                key: '',
                                group: 'actions',
                                image: '13.png',
                            },
                            {
                                id: 14,
                                key: '',
                                group: 'actions',
                                image: '14.png',
                            },
                            {
                                id: 15,
                                key: '',
                                group: 'actions',
                                image: '15.png',
                            },
                            {
                                id: 16,
                                key: '',
                                group: 'actions',
                                image: '16.png',
                            },
                            {
                                id: 17,
                                key: '',
                                group: 'actions',
                                image: '17.png',
                            },
                            {
                                id: 18,
                                key: '',
                                group: 'actions',
                                image: '18.png',
                            },
                            {
                                id: 19,
                                key: '',
                                group: 'actions',
                                image: '19.png',
                            },
                            {
                                id: 20,
                                key: '',
                                group: 'actions',
                                image: '20.png',
                            },
                            {
                                id: 21,
                                key: '',
                                group: 'actions',
                                image: '21.png',
                            },
                            {
                                id: 22,
                                key: '',
                                group: 'actions',
                                image: '22.png',
                            },
                            {
                                id: 23,
                                key: '',
                                group: 'actions',
                                image: '23.png',
                            },
                            {
                                id: 24,
                                key: '',
                                group: 'actions',
                                image: '24.png',
                            },
                            {
                                id: 25,
                                key: '',
                                group: 'actions',
                                image: '25.png',
                            },
                            {
                                id: 26,
                                key: '',
                                group: 'actions',
                                image: '26.png',
                            },
                            {
                                id: 27,
                                key: '',
                                group: 'actions',
                                image: '27.png',
                            },
                            {
                                id: 28,
                                key: '',
                                group: 'actions',
                                image: '28.png',
                            },
                            {
                                id: 29,
                                key: '',
                                group: 'actions',
                                image: '29.png',
                            },
                            {
                                id: 30,
                                key: '',
                                group: 'actions',
                                image: '30.png',
                            },
                        ]
                    },
                    {
                        id: 3,
                        group: 'Символы',
                        items: [
                            {
                                id: 1,
                                key: '',
                                group: 'symbols',
                                image: '1.png',
                            },
                            {
                                id: 2,
                                key: '',
                                group: 'symbols',
                                image: '2.png',
                            },
                            {
                                id: 3,
                                key: '',
                                group: 'symbols',
                                image: '3.png',
                            },
                            {
                                id: 4,
                                key: '',
                                group: 'symbols',
                                image: '4.png',
                            },
                            {
                                id: 5,
                                key: '',
                                group: 'symbols',
                                image: '5.png',
                            },
                            {
                                id: 6,
                                key: '',
                                group: 'symbols',
                                image: '6.png',
                            },
                            {
                                id: 7,
                                key: '',
                                group: 'symbols',
                                image: '7.png',
                            },
                            {
                                id: 8,
                                key: '',
                                group: 'symbols',
                                image: '8.png',
                            },
                            {
                                id: 9,
                                key: '',
                                group: 'symbols',
                                image: '9.png',
                            },
                            {
                                id: 10,
                                key: '',
                                group: 'symbols',
                                image: '10.png',
                            },
                            {
                                id: 11,
                                key: '',
                                group: 'symbols',
                                image: '11.png',
                            },
                            {
                                id: 12,
                                key: '',
                                group: 'symbols',
                                image: '12.png',
                            },
                            {
                                id: 13,
                                key: '',
                                group: 'symbols',
                                image: '13.png',
                            },
                            {
                                id: 14,
                                key: '',
                                group: 'symbols',
                                image: '14.png',
                            },
                            {
                                id: 15,
                                key: '',
                                group: 'symbols',
                                image: '15.png',
                            },
                            {
                                id: 16,
                                key: '',
                                group: 'symbols',
                                image: '16.png',
                            },
                            {
                                id: 17,
                                key: '',
                                group: 'symbols',
                                image: '17.png',
                            },
                            {
                                id: 18,
                                key: '',
                                group: 'symbols',
                                image: '18.png',
                            },
                            {
                                id: 19,
                                key: '',
                                group: 'symbols',
                                image: '19.png',
                            },
                            {
                                id: 20,
                                key: '',
                                group: 'symbols',
                                image: '20.png',
                            },
                            {
                                id: 21,
                                key: '',
                                group: 'symbols',
                                image: '21.png',
                            },
                            {
                                id: 22,
                                key: '',
                                group: 'symbols',
                                image: '22.png',
                            },
                            {
                                id: 23,
                                key: '',
                                group: 'symbols',
                                image: '23.png',
                            },
                            {
                                id: 24,
                                key: '',
                                group: 'symbols',
                                image: '24.png',
                            },
                            {
                                id: 25,
                                key: '',
                                group: 'symbols',
                                image: '25.png',
                            },
                            {
                                id: 26,
                                key: '',
                                group: 'symbols',
                                image: '26.png',
                            },
                            {
                                id: 27,
                                key: '',
                                group: 'symbols',
                                image: '27.png',
                            },
                            {
                                id: 28,
                                key: '',
                                group: 'symbols',
                                image: '28.png',
                            },
                            {
                                id: 29,
                                key: '',
                                group: 'symbols',
                                image: '29.png',
                            },
                            {
                                id: 30,
                                key: '',
                                group: 'symbols',
                                image: '30.png',
                            },
                        ]
                    },
                ]
            }
        },
        methods: {
            closeMenu() {
                this.isMenuOpen = false;
            },
        },
    }
</script>
