"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_components_modals_ChatRules_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/modals/ChatRules.vue?vue&type=script&lang=js&":
/*!*****************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/modals/ChatRules.vue?vue&type=script&lang=js& ***!
  \*****************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var vue2_teleport__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vue2-teleport */ "./node_modules/vue2-teleport/dist/teleport.esm.js");

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  components: {
    Teleport: vue2_teleport__WEBPACK_IMPORTED_MODULE_0__["default"]
  },
  methods: {
    beforeOpen: function beforeOpen() {
      document.body.classList.add('overflow-hidden');
    },
    beforeClose: function beforeClose() {
      document.body.classList.remove('overflow-hidden');
    }
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/modals/ChatRules.vue?vue&type=template&id=8897e5ec&lang=pug&":
/*!******************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/modals/ChatRules.vue?vue&type=template&id=8897e5ec&lang=pug& ***!
  \******************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* binding */ render),
/* harmony export */   "staticRenderFns": () => (/* binding */ staticRenderFns)
/* harmony export */ });
var render = function render() {
  var _vm = this,
    _c = _vm._self._c;
  return _c("Teleport", {
    attrs: {
      to: "#modals-container"
    }
  }, [_c("modal", {
    attrs: {
      name: "chat-rules",
      adaptive: true,
      width: "300",
      height: "auto"
    },
    on: {
      "before-open": _vm.beforeOpen,
      "before-close": _vm.beforeClose
    }
  }, [_c("div", {
    staticClass: "w-full relative flex flex-col"
  }, [_c("div", {
    staticClass: "px-6 pt-6 pb-4 flex items-center justify-between select-none"
  }, [_c("b", {
    staticClass: "text-white text-lg font-medium"
  }, [_vm._v("Правила чата")]), _c("a", {
    staticClass: "transition-all duration-200 w-[32px] h-[32px] text-grayLight rounded-lg hover:bg-[#3c3c46] flex items-center justify-center",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: function click($event) {
        return _vm.$modal.hide("chat-rules");
      }
    }
  }, [_c("svg", {
    staticClass: "w-[12px] h-[12x]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#close"
    }
  })])])]), _c("div", {
    staticClass: "px-6"
  }, [_c("div", {
    staticClass: "flex flex-col space-y-2 text-sm"
  }, [_c("p", [_vm._v("В чате запрещено:")]), _c("ul", {
    staticClass: "text-grayLight flex flex-col [&_li]:py-0.5"
  }, [_c("li", [_vm._v("спамить промокоды")]), _c("li", [_vm._v("попрошайничать")]), _c("li", [_vm._v("оскорблять администрацию")]), _c("li", [_vm._v("проявлять чрезмерную агрессию и негатив")]), _c("li", [_vm._v("обвинять администрацию сайта или сайт в обмане")]), _c("li", [_vm._v("упоминать другие проекты")]), _c("li", [_vm._v("отправлять сообщения с рекламой")])])])]), _c("div", {
    staticClass: "px-6 pt-6 pb-6 flex flex-col"
  }, [_c("div", {
    on: {
      click: function click($event) {
        return _vm.$modal.hide("chat-rules");
      }
    }
  }, [_c("Btn", {
    attrs: {
      text: "Все понятно",
      type: "button",
      classes: "bg-[#3c3c46] hover:bg-[#43434e] w-full",
      ico: null
    }
  })], 1)])])])], 1);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./resources/frontend/components/modals/ChatRules.vue":
/*!************************************************************!*\
  !*** ./resources/frontend/components/modals/ChatRules.vue ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _ChatRules_vue_vue_type_template_id_8897e5ec_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./ChatRules.vue?vue&type=template&id=8897e5ec&lang=pug& */ "./resources/frontend/components/modals/ChatRules.vue?vue&type=template&id=8897e5ec&lang=pug&");
/* harmony import */ var _ChatRules_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./ChatRules.vue?vue&type=script&lang=js& */ "./resources/frontend/components/modals/ChatRules.vue?vue&type=script&lang=js&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");





/* normalize component */
;
var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__["default"])(
  _ChatRules_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _ChatRules_vue_vue_type_template_id_8897e5ec_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _ChatRules_vue_vue_type_template_id_8897e5ec_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/components/modals/ChatRules.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/components/modals/ChatRules.vue?vue&type=script&lang=js&":
/*!*************************************************************************************!*\
  !*** ./resources/frontend/components/modals/ChatRules.vue?vue&type=script&lang=js& ***!
  \*************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_ChatRules_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./ChatRules.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/modals/ChatRules.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_ChatRules_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/components/modals/ChatRules.vue?vue&type=template&id=8897e5ec&lang=pug&":
/*!****************************************************************************************************!*\
  !*** ./resources/frontend/components/modals/ChatRules.vue?vue&type=template&id=8897e5ec&lang=pug& ***!
  \****************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_ChatRules_vue_vue_type_template_id_8897e5ec_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_ChatRules_vue_vue_type_template_id_8897e5ec_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_ChatRules_vue_vue_type_template_id_8897e5ec_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../../node_modules/pug-plain-loader/index.js!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./ChatRules.vue?vue&type=template&id=8897e5ec&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/modals/ChatRules.vue?vue&type=template&id=8897e5ec&lang=pug&");


/***/ })

}]);