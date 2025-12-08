<template>
    <div class="max-w-[1075px] px-[32px] sm:px-[16px] py-6 mx-auto relative flex flex-col space-y-[30px]">
        <div class="w-full py-12 flex items-center justify-center" v-if="preloader">
            <Spin :color="'text-white'"/>
        </div>
        <div class="flex flex-col space-y-[25px]" :class="[preloader ? 'invisible' : '']">
            <div class="flex relative flex-wrap items-center justify-center w-full">
                <a href="javascript:;" @click="$router.push('/slots')" class="sm:relative absolute left-0 flex items-center h-[36px] rounded-[14px] overflow-hidden transition-all duration-200 text-white bg-[#696f96]">
                    <div class="font-bold pointer-events-none flex items-center h-full border-2 border-[#696f96] rounded-[14px] px-[14px] pointer-events-none space-x-1.5 text-current">
                        <span class="z-[2]">Назад к слотам</span>
                    </div>
                    <div class="gradient absolute transition-all duration-200 opacity-0 -left-[2px] z-[1] -top-[2px] w-[calc(100%_+_2px)] h-[calc(100%_+_2px)] bg-gradient-to-r from-[#3265E8] to-[#8232E8]"></div>
                </a>

                <div class="flex sm:w-full sm:mb-[20px] sm:-order-[1] flex-col items-center text-center space-y-1.5">
                    <b class="text-4xl !font-extrabold sm:text-2xl">{{ title }}</b> 
                    <span class="text-base text-[#696F96] font-semibold">{{ provider }}</span>
                </div>

                <a href="javascript:;" @click="fullscreen" class="sm:relative absolute transition-all duration-200 hover:bg-[#696f96] hover:shadow-[0px_3px_22px_rgba(0,0,0,0.05)] rounded-full hover:text-white right-0 w-[48px] h-[48px] text-[#696F96] flex items-center justify-center">
                    <svg class="w-[18px] h-[18px]"><use xlink:href="@/images/symbols.svg#resize"></use></svg>
                </a>
            </div>
            <iframe 
                id="slot" 
                frameborder="0" 
                width="100%" 
                height="100%" 
                class="w-full relative grid before:pt-[55%] sp:before:pt-[80%] bg-black rounded-[32px] overflow-hidden slotGame" 
                src=""
            />
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            preloader: true,
            title: '',
            provider: ''
        }
    },
    methods: {
        init() {
            this.$root.axios.post('/slots/loadGame', {
                id: this.$route.params.id
            })
            .then(response => {
                const {data} = response
                this.preloader = false

                if(data.error) {
                    this.$router.push('/slots')
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

                this.title = data.info.title
                this.provider = data.info.provider
                document.getElementsByTagName("iframe")[0].src = data.url;
            })
        },
        fullscreen() {
            document.getElementsByTagName("iframe")[0].requestFullscreen();
        }
    },
    mounted() {
        this.init()
    }
}
</script>

<style>
.slotGame {
    aspect-ratio: 1280/720;
}
</style>