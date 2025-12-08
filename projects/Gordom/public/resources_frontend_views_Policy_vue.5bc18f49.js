"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_views_Policy_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Policy.vue?vue&type=script&lang=js&":
/*!**************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Policy.vue?vue&type=script&lang=js& ***!
  \**************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  data: function data() {
    return {
      preloader: true
    };
  },
  methods: {
    preloaderDestroy: function preloaderDestroy() {
      var _this = this;
      setTimeout(function () {
        _this.preloader = false;
      }, 300);
    }
  },
  mounted: function mounted() {
    this.preloaderDestroy();
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Policy.vue?vue&type=template&id=77294f30&lang=pug&":
/*!***************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Policy.vue?vue&type=template&id=77294f30&lang=pug& ***!
  \***************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* binding */ render),
/* harmony export */   "staticRenderFns": () => (/* binding */ staticRenderFns)
/* harmony export */ });
var render = function render() {
  var _vm = this,
    _c = _vm._self._c;
  return _c("div", {
    staticClass: "flex flex-col"
  }, [_vm.preloader ? _c("div", {
    staticClass: "w-full py-12 flex items-center justify-center"
  }, [_c("Spin", {
    attrs: {
      color: "text-white"
    }
  })], 1) : _vm._e(), _c("Transition", {
    attrs: {
      "enter-active-class": "transition-all duration-[200ms] ease-out",
      "enter-class": "opacity-0",
      "enter-to-class": "opacity-100"
    }
  }, [!_vm.preloader ? _c("div", {
    staticClass: "flex flex-col space-y-[50px] lg:space-y-[30px]"
  }, [_c("div", {
    staticClass: "flex flex-col mt-[20px] space-y-[30px]"
  }, [_c("div", {
    staticClass: "flex items-center flex-wrap justify-between"
  }, [_c("div", {
    staticClass: "flex 2xl:-order-[1] items-center text-grayLight uppercase font-['Rubik'] font-medium text-sm space-x-2"
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#faq"
    }
  })]), _c("span", [_vm._v("Политика конфиденциальности")])])]), _c("div", {
    staticClass: "relative w-full p-[24px] bg-violet rounded-xl text-white/[0.8] text-sm space-y-3"
  }, [_c("p", [_vm._v("Пожалуйста, внимательно прочитайте эту Политику конфиденциальности перед использованием Treasure Casino. ")]), _c("p", [_vm._v("Мы предоставляем доступ к различным играм на нашей платформе. Пользуясь нашими сервисами, Вы доверяете нам свою информацию. Мы понимаем, что это большая ответственность, и прилагаем все усилия, чтобы защитить Ваши данные и дать Вам возможность управлять ими.")]), _c("p", [_vm._v("В этой Политике конфиденциальности описано, какую информацию мы собираем, с какой целью мы это делаем и как Вы можете обновлять, удалять свои данные и управлять ими.")])]), _c("div", {
    staticClass: "w-full flex-col rounded-xl space-y-[30px] p-[32px] bg-[#202024] relative z-[1] flex"
  }, [_c("div", {
    staticClass: "flex flex-col space-y-[20px]"
  }, [_c("span", {
    staticClass: "text-grayLight uppercase font-['Rubik'] font-medium text-sm"
  }, [_vm._v("Информация, которую мы собираем")]), _c("div", {
    staticClass: "flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline"
  }, [_c("p", [_vm._v("Виды персональной информации, которую мы собираем:")]), _c("p", [_vm._v("1. имя, игровой никнейм;"), _c("br"), _vm._v(" 2. адрес электронной почты;\n"), _c("br"), _vm._v(" 3. номер телефона;\n"), _c("br"), _vm._v(" 4. IP-адрес, браузер, ОС;\n"), _c("br"), _vm._v(" 5. номера кошельков, из которых были пополнения и выводы;\n"), _c("br"), _vm._v(" 6. если Вы создаете аккаунт через социальные сети (ВКонтакте, Facebook, Яндекс, Google, Steam, Twitch, Mail.ru, Reddit, Одноклассники), то, соответственно, мы будем хранить Ваше имя, фотографию профиля, ссылку на страницу в социальные сети.")])])]), _c("div", {
    staticClass: "flex flex-col space-y-[20px]"
  }, [_c("span", {
    staticClass: "text-grayLight uppercase font-['Rubik'] font-medium text-sm"
  }, [_vm._v("Как мы используем информацию, полученную от игроков")]), _c("div", {
    staticClass: "flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline"
  }, [_c("p", [_vm._v("Став игроком, или иным способом предоставив Treasure Casino персональную информацию, Вы соглашаетесь с тем, что мы собираем и используем Вашу персональную информацию для предоставления нами услуг."), _c("br"), _vm._v(" Вы соглашаетесь на предоставления номера телефона и/или адреса электронной почты третьей стороне для маркетинговых целей.\n"), _c("br"), _vm._v(" Вы соглашаетесь на предоставление ID игры, имени Вашего игрока, ставки, выигрышного коэффициента и выигрыша для публикации в наших социальных сетях.\n"), _c("br"), _vm._v(" Вы соглашаетесь с тем, что мы имеем право раскрывать вашу персональную информацию, но лишь с целью и в случаях, если такое требование выдвинуто государственными органами, в предусмотренном действующим законодательством порядке.")])])]), _c("div", {
    staticClass: "flex flex-col space-y-[20px]"
  }, [_c("span", {
    staticClass: "text-grayLight uppercase font-['Rubik'] font-medium text-sm"
  }, [_vm._v("Обращение с жалобами и применимое законодательство")]), _c("div", {
    staticClass: "flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline"
  }, [_c("p", [_vm._v("В случае возникновения споров и разногласий наше решение является окончательным и Вы с ним полностью согласны. Все споры и разногласия, возникающие из или в связи с настоящей политикой, разрешаются путем переговоров. Если невозможно достичь соглашения путем переговоров, споры, разногласия и претензии, вытекающие из настоящей политики, разрешаются в соответствии с действующим законодательством Нидерландских Антильских островов.ы соглашаетесь с тем, что мы имеем право раскрывать вашу персональную информацию, но лишь с целью и в случаях, если такое требование выдвинуто государственными органами, в предусмотренном действующим законодательством порядке.")]), _c("p", [_vm._v("Если у Вас есть какие-либо вопросы, запросы на доступ, или жалобы, связанные с обработкой, Вы можете обратиться к нашей команде поддержки клиентов с соответствующим запросом.")])])])])])]) : _vm._e()])], 1);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./resources/frontend/views/Policy.vue":
/*!*********************************************!*\
  !*** ./resources/frontend/views/Policy.vue ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Policy_vue_vue_type_template_id_77294f30_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Policy.vue?vue&type=template&id=77294f30&lang=pug& */ "./resources/frontend/views/Policy.vue?vue&type=template&id=77294f30&lang=pug&");
/* harmony import */ var _Policy_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Policy.vue?vue&type=script&lang=js& */ "./resources/frontend/views/Policy.vue?vue&type=script&lang=js&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");





/* normalize component */
;
var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__["default"])(
  _Policy_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Policy_vue_vue_type_template_id_77294f30_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Policy_vue_vue_type_template_id_77294f30_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/views/Policy.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/views/Policy.vue?vue&type=script&lang=js&":
/*!**********************************************************************!*\
  !*** ./resources/frontend/views/Policy.vue?vue&type=script&lang=js& ***!
  \**********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Policy_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Policy.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Policy.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Policy_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/views/Policy.vue?vue&type=template&id=77294f30&lang=pug&":
/*!*************************************************************************************!*\
  !*** ./resources/frontend/views/Policy.vue?vue&type=template&id=77294f30&lang=pug& ***!
  \*************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Policy_vue_vue_type_template_id_77294f30_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Policy_vue_vue_type_template_id_77294f30_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Policy_vue_vue_type_template_id_77294f30_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../node_modules/pug-plain-loader/index.js!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Policy.vue?vue&type=template&id=77294f30&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Policy.vue?vue&type=template&id=77294f30&lang=pug&");


/***/ })

}]);