import Vue from 'vue'
import App from './components/Layout.vue'
import '../css/app.css'
import './fonts/Deftone/styles.css'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.use(VueAxios, axios)

// plugins
import SmoothScrollbar from 'vue-smooth-scrollbar'
Vue.use(SmoothScrollbar)

import { directive as onClickaway } from 'vue-clickaway'
Vue.directive('on-clickaway', onClickaway)

import VModal from 'vue-js-modal'
Vue.use(VModal)

import VueClipboard from 'vue-clipboard2'
Vue.use(VueClipboard)

import RangeSlider from 'vue-range-slider'
Vue.component('RangeSlider', RangeSlider)

import VueToastr from "vue-toastr";
Vue.use(VueToastr, {
  defaultTimeout: 3000,
  defaultClassNames: ['animate-[slideUpScale_0.2s_ease]'],
  defaultPosition: "toast-top-center"
});

import VueSocketIO from 'vue-socket.io'
let port = '8443';

Vue.use(new VueSocketIO({
    connection: `${window.location.protocol}//${window.location.hostname}:${port}`
}));

//components
import Spin from '@/components/ui/Spin.vue'
Vue.component('Spin', Spin)

// Button (опции при вызове компонента):
// :text="''" (Текст самой кнопки)
// :type="''" (Тип кнопки: link - ссылка(<router-link></router-link>), button - кнопка (<button type="submit"></button>))
// :path="''" (Url ссылки)
// :theme="null" (Цвет кнопки: null - цвет по умолчанию (фиолетовый), red - красный, green - зеленый, gray - серый )
// :ico="''" (Иконка в кнопку: иконки хранятся в images/symbols.svg, просто указываем здесь её id, например: games)
import Btn from '@/components/ui/Button.vue'
Vue.component('Btn', Btn)

const moment = require('moment')
require('moment/locale/ru')

Vue.use(require('vue-moment'), {
    moment
})

Vue.config.productionTip = false

new Vue({
    router,
    methods: {
        init() {
            this.$root.axios.post('/user/init')
            .then(response => {
                const {data} = response

                if(data.user) {
                    this.user = data.user
                }
            })
        }
    },
    mounted() {
        this.init()
    },
    data() {
        return {
            user: null
        }
    },
    render: h => h(App)
})
.$mount('#app')
