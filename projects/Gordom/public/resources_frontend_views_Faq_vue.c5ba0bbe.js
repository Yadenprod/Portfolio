"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_views_Faq_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=script&lang=js&":
/*!***********************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=script&lang=js& ***!
  \***********************************************************************************************************************************************************************************************/
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
    },
    faq: function faq(event) {
      var items = document.querySelectorAll('.faq-item');
      for (var i = 0; i < items.length; i++) {
        items[i].classList.remove('active');
      }
      if (event.target.classList.contains('active')) {
        event.target.classList.remove('active');
      } else {
        event.target.classList.add('active');
      }
    }
  },
  mounted: function mounted() {
    this.preloaderDestroy();
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=template&id=98c92460&lang=pug&":
/*!************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=template&id=98c92460&lang=pug& ***!
  \************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
  })]), _c("span", [_vm._v("Помощь")])])]), _c("div", {
    staticClass: "faq w-full flex flex-col space-y-[20px]"
  }, [_c("div", {
    staticClass: "faq-item relative bg-[#202024] rounded-xl overflow-hidden"
  }, [_c("div", {
    staticClass: "faq-heading [&.active]:bg-[#26262b] [&.active]:text-white [&.active>i]:top-[3px] [&.active>i]:rotate-[225deg] flex items-center justify-between px-6 py-5 text-grayLight font-semibold transition-all cursor-pointer duration-200 hover:bg-[#26262b]",
    on: {
      click: _vm.faq
    }
  }, [_c("span", {
    staticClass: "pointer-events-none"
  }, [_vm._v("Не пришел вывод")]), _c("i", {
    staticClass: "relative inline-block w-2 h-2 border-r-2 border-b-2 border-current rotate-[45deg] transition-all duration-200"
  })]), _c("div", {
    staticClass: "faq-body px-6 py-6 flex relative space-y-4 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] hidden"
  }, [_c("p", [_vm._v("Вывод на QIWI осуществляется до 24 часов. Вывод на остальные платежные системы может занимать до 48 часов.")])])]), _c("div", {
    staticClass: "faq-item relative bg-[#202024] rounded-xl overflow-hidden"
  }, [_c("div", {
    staticClass: "faq-heading [&.active]:bg-[#26262b] [&.active]:text-white [&.active>i]:top-[3px] [&.active>i]:rotate-[225deg] flex items-center justify-between px-6 py-5 text-grayLight font-semibold transition-all cursor-pointer duration-200 hover:bg-[#26262b]",
    on: {
      click: _vm.faq
    }
  }, [_c("span", {
    staticClass: "pointer-events-none"
  }, [_vm._v("Как начать с вами сотрудничать? ")]), _c("i", {
    staticClass: "relative inline-block w-2 h-2 border-r-2 border-b-2 border-current rotate-[45deg] transition-all duration-200"
  })]), _c("div", {
    staticClass: "faq-body px-6 py-6 flex relative space-y-4 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] hidden"
  }, [_c("p", [_vm._v("Чтобы предложить нам сотрудничество, вы можете написать нам в лс группы VK.")])])]), _c("div", {
    staticClass: "faq-item relative bg-[#202024] rounded-xl overflow-hidden"
  }, [_c("div", {
    staticClass: "faq-heading [&.active]:bg-[#26262b] [&.active]:text-white [&.active>i]:top-[3px] [&.active>i]:rotate-[225deg] flex items-center justify-between px-6 py-5 text-grayLight font-semibold transition-all cursor-pointer duration-200 hover:bg-[#26262b]",
    on: {
      click: _vm.faq
    }
  }, [_c("span", {
    staticClass: "pointer-events-none"
  }, [_vm._v("Есть ли отыгрыш депозита?")]), _c("i", {
    staticClass: "pointer-events-none relative inline-block w-2 h-2 border-r-2 border-b-2 border-current rotate-[45deg] transition-all duration-200"
  })]), _c("div", {
    staticClass: "faq-body px-6 py-6 flex relative space-y-4 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] hidden"
  }, [_c("p", [_vm._v("Да, сумма любой вашей ставки учитывается при отыгрыше. Отыгрыш составляет x2 от депозита.")])])]), _c("div", {
    staticClass: "faq-item relative bg-[#202024] rounded-xl overflow-hidden"
  }, [_c("div", {
    staticClass: "faq-heading [&.active]:bg-[#26262b] [&.active]:text-white [&.active>i]:top-[3px] [&.active>i]:rotate-[225deg] flex items-center justify-between px-6 py-5 text-grayLight font-semibold transition-all cursor-pointer duration-200 hover:bg-[#26262b]",
    on: {
      click: _vm.faq
    }
  }, [_c("span", {
    staticClass: "pointer-events-none"
  }, [_vm._v("Как часто я могу брать бонусы и сколько я получу?")]), _c("i", {
    staticClass: "relative inline-block w-2 h-2 border-r-2 border-b-2 border-current rotate-[45deg] transition-all duration-200"
  })]), _c("div", {
    staticClass: "faq-body px-6 py-6 flex relative space-y-4 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] hidden"
  }, [_c("p", [_vm._v("Каждые 24 часа крутите бонусную рулетку и получайте от 1 до 100р на свой баланс")])])])])])]) : _vm._e()])], 1);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss&":
/*!***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss& ***!
  \***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/laravel-mix/node_modules/css-loader/dist/runtime/api.js */ "./node_modules/laravel-mix/node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);
// Imports

var ___CSS_LOADER_EXPORT___ = _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".faq .faq-heading.active + .faq-body {\n  display: block;\n}", ""]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss&":
/*!*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss& ***!
  \*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Faq_vue_vue_type_style_index_0_id_98c92460_lang_scss___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss& */ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss&");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Faq_vue_vue_type_style_index_0_id_98c92460_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Faq_vue_vue_type_style_index_0_id_98c92460_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./resources/frontend/views/Faq.vue":
/*!******************************************!*\
  !*** ./resources/frontend/views/Faq.vue ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Faq_vue_vue_type_template_id_98c92460_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Faq.vue?vue&type=template&id=98c92460&lang=pug& */ "./resources/frontend/views/Faq.vue?vue&type=template&id=98c92460&lang=pug&");
/* harmony import */ var _Faq_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Faq.vue?vue&type=script&lang=js& */ "./resources/frontend/views/Faq.vue?vue&type=script&lang=js&");
/* harmony import */ var _Faq_vue_vue_type_style_index_0_id_98c92460_lang_scss___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss& */ "./resources/frontend/views/Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");



;


/* normalize component */

var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__["default"])(
  _Faq_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Faq_vue_vue_type_template_id_98c92460_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Faq_vue_vue_type_template_id_98c92460_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/views/Faq.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/views/Faq.vue?vue&type=script&lang=js&":
/*!*******************************************************************!*\
  !*** ./resources/frontend/views/Faq.vue?vue&type=script&lang=js& ***!
  \*******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Faq_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Faq.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Faq_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/views/Faq.vue?vue&type=template&id=98c92460&lang=pug&":
/*!**********************************************************************************!*\
  !*** ./resources/frontend/views/Faq.vue?vue&type=template&id=98c92460&lang=pug& ***!
  \**********************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Faq_vue_vue_type_template_id_98c92460_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Faq_vue_vue_type_template_id_98c92460_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Faq_vue_vue_type_template_id_98c92460_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../node_modules/pug-plain-loader/index.js!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Faq.vue?vue&type=template&id=98c92460&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=template&id=98c92460&lang=pug&");


/***/ }),

/***/ "./resources/frontend/views/Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss&":
/*!****************************************************************************************!*\
  !*** ./resources/frontend/views/Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss& ***!
  \****************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _node_modules_style_loader_dist_cjs_js_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Faq_vue_vue_type_style_index_0_id_98c92460_lang_scss___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/style-loader/dist/cjs.js!../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss& */ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Faq.vue?vue&type=style&index=0&id=98c92460&lang=scss&");


/***/ })

}]);