<template>
    <div class="relative bg-[#202024] p-[1px] rounded-[16px]">
        <div v-if="isLoading" class="w-full py-12 flex items-center justify-center">
            <Spin :color="'text-white'" />
        </div>
        <div v-else>
            <div class="w-full relative z-[5] mt-[70px]">
                <div class="max-w-[1075px] px-[32px] ms:px-[16px] mx-auto relative flex flex-col space-y-[20px]">
                    <div class="flex sm:flex-col z-[2] sm:space-y-4 items-center justify-between relative -top-[30px]">
                        <div class="flex sm:w-full space-x-3 sm:space-x-0 sm:space-y-3 sm:flex-col">
                            <div class="relative sm:w-full">
                                <svg class="w-[16px] h-[16px] absolute left-4 top-1/2 -translate-y-1/2 text-[#696F96]"><use xlink:href="images/symbols.svg#search"></use></svg>
                                <input 
                                    type="text" 
                                    placeholder="Поиск" 
                                    class="sm:w-full placeholder:text-[#696F96] bg-[#2a2a2d] h-[48px] min-w-[240px] pl-[44px] focus:ring-0 focus:outline-none text-base font-semibold rounded-[14px] px-4" 
                                />
                            </div>
                        </div>
                            <div class="relative sm:w-full">
                            <div>
                                <button @click="providerShow = !providerShow" class="placeholder:text-[#696F96] bg-[#2a2a2d] sm:w-full w-[180px] justify-between text-[#696F96] transition-all duration-200 hover:text-[#545A81] h-[48px] flex items-center space-x-4 focus:ring-0 focus:outline-none text-base font-semibold rounded-[14px] px-5">
                                    <span class="pointer-events-none sm:max-w-[90%] max-w-[160px] whitespace-nowrap overflow-hidden text-ellipsis">
                                        Провайдеры
                                    </span> 
                                    <i class="rotate-45 border-r-2 border-b-2 w-[6px] h-[6px] border-current"/>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="max-w-[1075px] px-[32px] ms:px-[16px] py-6 mx-auto relative flex flex-col space-y-[30px]">
                <div class="grid grid-cols-4 2xl:grid-cols-3 sm:!grid-cols-2 gap-4">
                    <a v-for="item in 16" :key="item" href="/slot/7760" class="group transition-all duration-200 ease-out hover:scale-105 rounded-[17px] overflow-hidden shadow-[0px_3px_44px_rgba(0,0,0,0.05)] hover:shadow-[0px_3px_65px_rgba(0,0,0,0.1)] relative">
                        <svg class="w-[64px] h-[64px] absolute m-auto left-0 right-0 top-[70px] z-[1] play-button">
                            <use xlink:href="images/symbols.svg#play"></use>
                        </svg>
                        <div class="h-[200px] sm:!h-[120px] relative group-hover:blur-[3px]">
                            <div class="absolute z-[1] left-0 -bottom-[2px] w-full h-[20%] z-[1] bg-gradient-to-t from-white to-transparent"></div>
                            <div class="absolute z-[1] left-0 -bottom-[2px] w-full h-[20%] z-[1] bg-gradient-to-t from-white to-transparent"></div>
                            <img src="https://statict2.static-cdns.com/resources/sitepicstbs/slgames/game_img_2/GatesofOlympus.jpg" class="object-cover absolute left-0 top-0 w-full h-full" />
                        </div>
                        <div class="flex flex-col px-6 pb-5 space-y-1 bg-[#2c2c31] pt-[10px] z-[3]">
                            <b class="text-xl text-white !font-extrabold whitespace-nowrap overflow-hidden text-ellipsis">
                                Gates of Olympus
                            </b> 
                            <span class="text-sm font-semibold text-[#696F96]">
                                Pragmatic Play
                            </span>
                        </div>
                    </a>
                </div>
                <div class="flex justify-center w-full">
                    <div class="flex space-x-4 items-center">
                        <a
                            href="javascript:;"
                            class="h-[42px] px-6 rounded-full font-bold transition-all duration-200 hover:shadow-[0px_0px_0px_12px_rgba(86,79,232,0.12)] flex items-center justify-center text-white bg-gradient-to-r from-[#3265E8] to-[#8232E8]"
                        >
                            Загрузить ещё
                        </a>
                        <span class="text-[#696F96] text-sm font-semibold">1 из 23</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    components: {},
    data() {
        return {
            isLoading: true,
            providerShow: false,
            providers: ['Pragmatic', 'Amatic', 'PlaynGO'],
            search: '',
            provider: ''
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            setTimeout(() => {
                this.isLoading = false
            }, 200)
        }
    }
}
</script>

<style scoped>
.play-button {
    opacity: 0;
    transition: .4s
}
.group:hover .play-button {
    opacity: 1;
}
</style>