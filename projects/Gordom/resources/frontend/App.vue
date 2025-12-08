<template lang="pug">
  div(id="app")
    LeftPanel
    main(class="pl-[118px] pt-[16px] transition-all duration-200 pb-[50px] lg:pl-0 lg:pr-0 lg:pb-[86px]" :class="chatOpen ? 'pr-[318px]' : 'pr-[52px]'")
        div(class="max-w-[1232px] 2xl:max-w-[925px] px-[16px] mx-auto")
            HeaderMain
            div(class="layout pt-[20px] lg:pt-[55px]")
                <router-view/>
    Chat(@chatInitState="chatInitState" :chatOpen="chatOpen")
    MobileMenu(@chatInitState="chatInitState" :chatOpen="chatOpen")
    img(src="@/images/background.png" class="absolute -z-[1] left-0 top-0 w-full h-full object-cover")
</template>

<script>
  export default {
    name: 'App',
    components: {
      'LeftPanel': () => import('@/components/layouts/LeftPanel/LeftPanel.vue'),
      'HeaderMain': () => import('@/components/layouts/Header/Header.vue'),
      'Chat': () => import('@/components/layouts/Chat/Chat.vue'),
      'MobileMenu': () => import('@/components/layouts/Mobile/Menu.vue'),
    },
    data() {
      return {
        chatOpen: true,
      }
    },
    methods: {
      chatInitState(value) {
        this.chatOpen = value
        if (value) {
          localStorage.removeItem('chat')
        } else {
          localStorage.setItem('chat', 'closed')
        }
      }
    },
    mounted() {
      if (localStorage.getItem('chat') === 'closed') {
        this.chatOpen = false
      } else {
        localStorage.removeItem('chat')
      }
    }
  }
</script>

<style lang="scss">
  ::-webkit-scrollbar {
      width: 0;
  }
  .loader:before {
      content: '';
      display: block;
      position: absolute;
      left: -150px;
      top: 0;
      height: 100%;
      width: 150px;
      background: linear-gradient(to right, transparent 0%, rgba(#fff, 1) 60%, transparent 100%);
      -webkit-animation: load 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      animation: load 1s cubic-bezier(0.4, 0, 0.2, 1) infinite;
  }
  @keyframes load {
      from {
          left: -150px;
      }
      to   {
          left: 100%;
      }
  }
</style>
