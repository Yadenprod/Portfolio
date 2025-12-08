<template>
    <header class="flex lg:fixed lg:left-0 lg:top-0 lg:w-full lg:bg-[#1b1c20] relative items-center justify-between py-[10px] lg:px-[16px] z-[21]">
        <router-link to="/" active-class="" exact-active-class="" class="sm:w-[44px] overflow-hidden">
            <img src="@/images/logotype.svg" class="max-h-[44px] sm:max-w-fit">
        </router-link>
        <nav class="flex 2xl:hidden items-center space-x-12">
            <li 
                v-for="item in menu" 
                :key="item.id"
            >
                <router-link 
                    :to="item.path" 
                    active-class="active" 
                    exact-active-class="active"
                    class="
                        text-[#6a6a7a] text-sm font-semibold 
                        transition-all duration-200 
                        hover:text-[#c1c8dc] 
                        py-2 inline-block relative
                        font-['Manrope']
                        before:absolute before:-bottom-2 before:w-0 before:h-[3px] before:rounded-full before:bg-[#7c75d9]
                        before:transition-all before:duration-200
                        [&.active]:before:w-[25px]
                        [&.active]:text-white
                    "
                >
                    {{ item.name }}
                </router-link>
            </li>
        </nav>
        <div class="flex items-center">
            <div v-if="$root.user !== null" class="h-[48px] rounded-[12px] pl-4 pr-2 bg-[#2c2c31] flex items-center justify-between shadow-[0px_4px_28px_rgba(0,0,0,0.03)]">
                <div class="w-[140px] sm:w-[115px] h-full flex items-center space-x-3">
                    <img src="@/images/logotype-small.svg" class="max-w-[16px]" alt="">
                    <p class="flex items-center text-sm relative">
                        <Transition
                            enter-active-class="transition ease-out duration-100"
                            enter-class="transform opacity-0 scale-95"
                            enter-to-class="transform opacity-100 scale-100"
                            leave-active-class="transition ease-in duration-75"
                            leave-class="transform opacity-100 scale-100"
                            leave-to-class="transform opacity-0 scale-95"
                        >
                            <span v-if="!preloader" class="flex items-center font-['Rubik']">
                                <b>
                                    <IOdometer
                                        class="iOdometer"
                                        :value="$root.user.balance"
                                    />
                                </b>
                                <!-- <span class="text-[#757A8B] font-medium">.00</span> -->
                            </span>
                        </Transition>
                        <span v-if="preloader" class="relative w-[40px] h-[6px] h-full bg-[#3A3A40] rounded-sm loader overflow-hidden before:opacity-[0.1]"></span>
                    </p>
                </div>
                <a 
                    href="javascript:;"
                    @click="modalPay()"
                    class="flex w-[32px] h-[32px] items-center justify-center bg-[#3A3A40] rounded-lg transition-all duration-200 hover:bg-[#7C75D9] hover:!text-white"
                >
                    <svg class="w-[18px] h-[18px]"><use xlink:href="@/images/symbols.svg#plus"></use></svg>
                </a>
            </div>
            <div v-if="$root.user !== null" class="relative">
                <div 
                    class="relative"
                    v-on-clickaway="closeMenu"
                >
                    <div>
                        <span>
                            <button
                                @click="isMenuOpen = !isMenuOpen"
                                class="flex w-[48px] h-[48px] items-center justify-center text-[#4C4F5A] transition-all duration-200 hover:text-[#c5cbe0] focus:ring-0 focus:ring-inherit focus:outline-0"
                                type="button"
                            >
                                <svg class="w-[18px] h-[18px]"><use xlink:href="@/images/symbols.svg#more"></use></svg>
                            </button>
                        </span>
                    </div>
                    <Transition
                        enter-active-class="transition ease-out duration-100"
                        enter-class="transform opacity-0 scale-95"
                        enter-to-class="transform opacity-100 scale-100"
                        leave-active-class="transition ease-in duration-75"
                        leave-class="transform opacity-100 scale-100"
                        leave-to-class="transform opacity-0 scale-95"
                    >
                        <div
                            v-if="isMenuOpen"
                            class="absolute z-[1] origin-top-right right-0 mt-2 w-56 rounded-xl overflow-hidden bg-[#313136] flex flex-col shadow-[0px_4px_28px_rgba(0,0,0,0.08)]"
                        >   
                            <div class="p-4 bg-[#2d2d32] flex flex-col space-y-2">
                                <img 
                                    class="w-[32px] h-[32px] rounded-full" 
                                    :src="$root.user.avatar" 
                                    alt=""
                                >
                                <div class="w-full flex items-end justify-between">
                                    <div class="flex shrink-0 flex-col space-y-1">
                                        <b class="text-sm !font-medium max-w-[100px] whitespace-nowrap overflow-hidden text-ellipsis">{{ $root.user.login }}</b>
                                    </div>
                                    <p class="text-sm font-normal text-[#6a6a7a] max-w-[100px] font-['Rubik'] whitespace-nowrap overflow-hidden text-ellipsis">Id: {{ $root.user.id }}</p>
                                </div>
                            </div>
                            <div class="py-2">
                                <nav class="flex hidden 2xl:flex flex-col space-y-1">
                                    <li v-for="item in menuMobile" :key="item.id" @click="isMenuOpen = false">
                                        <router-link 
                                            :to="item.path"
                                            class="text-white font-['Manrope'] font-semibold flex items-center py-2 space-x-2 px-4 text-sm transition-all duration-200 hover:bg-[#3a3a40]"
                                            active-class=""
                                            exact-active-class=""
                                        >
                                            <svg class="w-[16px] h-[16px] text-[#c5cbe0]"><use :xlink:href="'../images/symbols.svg#' + item.ico"></use></svg>
                                            <span class="pointer-events-none">{{ item.name }}</span>
                                        </router-link>
                                    </li>
                                </nav>
                                <nav class="flex flex-col space-y-1">
                                    <li v-for="item in menuProfileDropdown" :key="item.id" @click="isMenuOpen = false || item.modal ? showModal(item.modal) : ''">
                                        <router-link 
                                            :to="item.path"
                                            class="text-white font-['Manrope'] font-semibold flex items-center py-2 space-x-2 px-4 text-sm transition-all duration-200 hover:bg-[#3a3a40]"
                                            active-class=""
                                            exact-active-class=""
                                        >
                                            <svg class="w-[16px] h-[16px] text-[#c5cbe0]"><use :xlink:href="'../images/symbols.svg#' + item.ico"></use></svg>
                                            <span class="pointer-events-none">{{ item.name }}</span>
                                        </router-link>
                                    </li>
                                </nav>
                            </div>
                        </div>
                    </Transition>
                </div>
            </div>
            <div v-if="$root.user == null" class="relative flex items-center space-x-2">
                <a href="javascript:;" @click="login()" class="font-['Rubik'] hover:bg-[#3A3A40] bg-[#2c2c31] whitespace-nowrap flex transition-all duration-200 items-center justify-center rounded-xl text-sm uppercase font-medium h-[52px] px-6 shadow-[0px_4px_35px_rgba(0,0,0,0.1)]">
                    Авторизация
                </a>
            </div>
        </div>
        <modalPay></modalPay>
        <modalSettings></modalSettings>
        <modalRegister></modalRegister>
        <modalLogin></modalLogin>
    </header>
</template>

<script>
    import IOdometer from 'vue-odometer';
    import 'odometer/themes/odometer-theme-default.css';

    export default {
        name: 'HeaderMain',
        data() {
            return {
                menu: [
                    {
                        id: 1,
                        name: 'Бонусы',
                        path: '/bonus',
                    },
                    {
                        id: 2,
                        name: 'Политика конфиденциальности',
                        path: '/policy',
                    },
                    {
                        id: 3,
                        name: 'FAQ',
                        path: '/faq',
                    },
                    {
                        id: 4,
                        name: 'Контакты',
                        path: '/contacts',
                    },
                ],
                menuProfileDropdown: [
                    {
                        id: 0,
                        name: 'Пригласить друзей',
                        ico: 'users',
                        path: '/refferal'
                    },
                    // {
                    //     id: 1,
                    //     name: 'Честная игра',
                    //     ico: 'fair',
                    //     path: '/provably-fair'
                    // },
                    // {
                    //     id: 2,
                    //     name: 'Профиль',
                    //     ico: 'user',
                    //     path: ''
                    // },
                    {
                        id: 4,
                        name: 'Выйти',
                        ico: 'logout',
                        path: '/logout'
                    },
                ],
                menuMobile: [
                    {
                        id: 1,
                        name: 'Бонусы',
                        ico: 'bonus',
                        path: '/bonus'
                    },
                    {
                        id: 2,
                        name: 'FAQ',
                        ico: 'faq',
                        path: '/faq'
                    },
                    {
                        id: 3,
                        name: 'Контакты',
                        ico: 'contacts',
                        path: '/contacts'
                    },
                ],
                isMenuOpen: false,
                preloader: true,
            }
        },
        components: {
            IOdometer,
            modalPay: () => import('@/components/modals/Pay.vue'),
            modalSettings: () => import('@/components/modals/Settings.vue'),
            modalLogin: () => import('@/components/modals/Login.vue'),
            modalRegister: () => import('@/components/modals/Register.vue'),
        },
        methods: {
            onCopy() {
                alert('1')
            },
            closeMenu() {
                this.isMenuOpen = false;
            },
            preloaderDestroy() {
                setTimeout(() => {
                    this.preloader = false;
                }, 800);
            },
            modalPay() {
                this.$modal.show('pay')
            },
            showModal(modal) {
                this.$modal.show(modal)
            },
            login() {
                location.href = '/auth/vkontakte'
            }
        },
        mounted() {
            this.preloaderDestroy();
        }
    }
</script>