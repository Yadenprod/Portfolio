"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_views_games_SlotGame_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=script&lang=js&":
/*!**********************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=script&lang=js& ***!
  \**********************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  data: function data() {
    return {
      preloader: true,
      title: '',
      provider: ''
    };
  },
  methods: {
    init: function init() {
      var _this = this;
      this.$root.axios.post('/slots/loadGame', {
        id: this.$route.params.id
      }).then(function (response) {
        var data = response.data;
        _this.preloader = false;
        if (data.error) {
          _this.$router.push('/slots');
          return _this.$toastr.Add({
            name: 'chatSendMsg',
            title: 'Ошибка',
            msg: data.message,
            type: 'error',
            defaultClassNames: ["animated", "zoomInUp"],
            timeout: 3000,
            progressbar: true
          });
        }
        _this.title = data.info.title;
        _this.provider = data.info.provider;
        document.getElementsByTagName("iframe")[0].src = data.url;
      });
    },
    fullscreen: function fullscreen() {
      document.getElementsByTagName("iframe")[0].requestFullscreen();
    }
  },
  mounted: function mounted() {
    this.init();
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=template&id=a49f2c58&":
/*!*********************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=template&id=a49f2c58& ***!
  \*********************************************************************************************************************************************************************************************************************************************************************************************/
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
    staticClass: "max-w-[1075px] px-[32px] sm:px-[16px] py-6 mx-auto relative flex flex-col space-y-[30px]"
  }, [_vm.preloader ? _c("div", {
    staticClass: "w-full py-12 flex items-center justify-center"
  }, [_c("Spin", {
    attrs: {
      color: "text-white"
    }
  })], 1) : _vm._e(), _vm._v(" "), _c("div", {
    staticClass: "flex flex-col space-y-[25px]",
    "class": [_vm.preloader ? "invisible" : ""]
  }, [_c("div", {
    staticClass: "flex relative flex-wrap items-center justify-center w-full"
  }, [_vm._m(0), _vm._v(" "), _vm._m(1), _vm._v(" "), _c("a", {
    staticClass: "sm:relative absolute transition-all duration-200 hover:bg-white hover:shadow-[0px_3px_22px_rgba(0,0,0,0.05)] rounded-full hover:text-[#8232E8] right-0 w-[48px] h-[48px] text-[#696F96] flex items-center justify-center",
    attrs: {
      href: "javascript:;"
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "/symbols.svg#resize"
    }
  })])])]), _vm._v(" "), _c("iframe", {
    staticClass: "w-full relative grid before:pt-[55%] sp:before:pt-[80%] bg-black rounded-[32px] overflow-hidden slotGame",
    attrs: {
      id: "slot",
      frameborder: "0",
      width: "100%",
      height: "100%",
      src: ""
    }
  })])]);
};
var staticRenderFns = [function () {
  var _vm = this,
    _c = _vm._self._c;
  return _c("a", {
    staticClass: "sm:relative absolute left-0 flex items-center h-[36px] text-[#526188] rounded-[14px] overflow-hidden transition-all duration-200 hover:text-white",
    attrs: {
      href: "/slots"
    }
  }, [_c("div", {
    staticClass: "font-bold pointer-events-none flex items-center h-full border-2 border-[#ECF1FF] rounded-[14px] px-[14px] pointer-events-none space-x-1.5 text-current"
  }, [_c("i", {
    staticClass: "w-2 z-[2] h-2 rotate-[135deg] border-r-2 border-b-2 border-current"
  }), _vm._v(" "), _c("span", {
    staticClass: "z-[2]"
  }, [_vm._v("Назад к слотам")])]), _vm._v(" "), _c("div", {
    staticClass: "gradient absolute transition-all duration-200 opacity-0 -left-[2px] z-[1] -top-[2px] w-[calc(100%_+_2px)] h-[calc(100%_+_2px)] bg-gradient-to-r from-[#3265E8] to-[#8232E8]"
  })]);
}, function () {
  var _vm = this,
    _c = _vm._self._c;
  return _c("div", {
    staticClass: "flex sm:w-full sm:mb-[20px] sm:-order-[1] flex-col items-center text-center space-y-1.5"
  }, [_c("b", {
    staticClass: "text-4xl !font-extrabold xq:text-2xl"
  }, [_vm._v("Michael Jackson")]), _vm._v(" "), _c("span", {
    staticClass: "text-base text-[#696F96] font-semibold"
  }, [_vm._v("Scientific Games")])]);
}];
render._withStripped = true;


/***/ }),

/***/ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-9.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-9.use[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css&":
/*!*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-9.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-9.use[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css& ***!
  \*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/laravel-mix/node_modules/css-loader/dist/runtime/api.js */ "./node_modules/laravel-mix/node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);
// Imports

var ___CSS_LOADER_EXPORT___ = _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n.slotGame {\r\n    aspect-ratio: 1280/720;\n}\r\n", ""]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-9.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-9.use[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css&":
/*!***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-9.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-9.use[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css& ***!
  \***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_9_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_9_use_2_node_modules_vue_loader_lib_index_js_vue_loader_options_SlotGame_vue_vue_type_style_index_0_id_a49f2c58_lang_css___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-9.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-9.use[2]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css& */ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-9.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-9.use[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css&");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_9_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_9_use_2_node_modules_vue_loader_lib_index_js_vue_loader_options_SlotGame_vue_vue_type_style_index_0_id_a49f2c58_lang_css___WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_9_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_9_use_2_node_modules_vue_loader_lib_index_js_vue_loader_options_SlotGame_vue_vue_type_style_index_0_id_a49f2c58_lang_css___WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./resources/frontend/views/games/SlotGame.vue":
/*!*****************************************************!*\
  !*** ./resources/frontend/views/games/SlotGame.vue ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _SlotGame_vue_vue_type_template_id_a49f2c58___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./SlotGame.vue?vue&type=template&id=a49f2c58& */ "./resources/frontend/views/games/SlotGame.vue?vue&type=template&id=a49f2c58&");
/* harmony import */ var _SlotGame_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./SlotGame.vue?vue&type=script&lang=js& */ "./resources/frontend/views/games/SlotGame.vue?vue&type=script&lang=js&");
/* harmony import */ var _SlotGame_vue_vue_type_style_index_0_id_a49f2c58_lang_css___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css& */ "./resources/frontend/views/games/SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");



;


/* normalize component */

var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__["default"])(
  _SlotGame_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _SlotGame_vue_vue_type_template_id_a49f2c58___WEBPACK_IMPORTED_MODULE_0__.render,
  _SlotGame_vue_vue_type_template_id_a49f2c58___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/views/games/SlotGame.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/views/games/SlotGame.vue?vue&type=script&lang=js&":
/*!******************************************************************************!*\
  !*** ./resources/frontend/views/games/SlotGame.vue?vue&type=script&lang=js& ***!
  \******************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_SlotGame_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./SlotGame.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_SlotGame_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/views/games/SlotGame.vue?vue&type=template&id=a49f2c58&":
/*!************************************************************************************!*\
  !*** ./resources/frontend/views/games/SlotGame.vue?vue&type=template&id=a49f2c58& ***!
  \************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_vue_loader_lib_index_js_vue_loader_options_SlotGame_vue_vue_type_template_id_a49f2c58___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_vue_loader_lib_index_js_vue_loader_options_SlotGame_vue_vue_type_template_id_a49f2c58___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_vue_loader_lib_index_js_vue_loader_options_SlotGame_vue_vue_type_template_id_a49f2c58___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./SlotGame.vue?vue&type=template&id=a49f2c58& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=template&id=a49f2c58&");


/***/ }),

/***/ "./resources/frontend/views/games/SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css&":
/*!**************************************************************************************************!*\
  !*** ./resources/frontend/views/games/SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css& ***!
  \**************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _node_modules_style_loader_dist_cjs_js_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_9_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_9_use_2_node_modules_vue_loader_lib_index_js_vue_loader_options_SlotGame_vue_vue_type_style_index_0_id_a49f2c58_lang_css___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/style-loader/dist/cjs.js!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-9.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-9.use[2]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css& */ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-9.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-9.use[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/SlotGame.vue?vue&type=style&index=0&id=a49f2c58&lang=css&");


/***/ })

}]);