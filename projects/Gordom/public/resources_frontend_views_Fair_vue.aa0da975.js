(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_views_Fair_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Fair.vue?vue&type=script&lang=js&":
/*!************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Fair.vue?vue&type=script&lang=js& ***!
  \************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  data: function data() {
    return {
      preloader: true,
      sliderValue: 2.4
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

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Fair.vue?vue&type=template&id=946dde4c&lang=pug&":
/*!*************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Fair.vue?vue&type=template&id=946dde4c&lang=pug& ***!
  \*************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
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
      "xlink:href": "images/symbols.svg#fair"
    }
  })]), _c("span", [_vm._v("Честная игра")])])]), _c("div", {
    staticClass: "w-full flex-col rounded-xl space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex"
  }, [_c("div", {
    staticClass: "flex items-center justify-between gap-12"
  }, [_c("div", {
    staticClass: "w-full flex flex-col space-y-6"
  }, [_c("span", {
    staticClass: "text-grayLight uppercase font-['Rubik'] font-medium text-sm"
  }, [_vm._v("Результат игры "), _c("b", {
    staticClass: "text-violet"
  }, [_vm._v("#5320361")])]), _c("div", {
    staticClass: "flex flex-col space-y-4"
  }, [_c("div", {
    staticClass: "relative flex md:flex-col md:items-start md:space-y-4 items-center"
  }, [_c("span", {
    staticClass: "shrink-0 text-sm text-grayLight w-[20%] md:w-full"
  }, [_vm._v("Соль 1")]), _c("div", {
    staticClass: "w-[80%] md:w-full"
  }, [_c("div", {
    staticClass: "text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]"
  }, [_c("span", {
    staticClass: "max-w-full whitespace-nowrap text-ellipsis overflow-hidden"
  }, [_vm._v("6OA1jt9g2c9eQx27flwnQ586")]), _c("a", {
    staticClass: "transition-all shrink-0 duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center",
    attrs: {
      href: "javascript:;"
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#copy"
    }
  })])])])])]), _c("div", {
    staticClass: "relative flex md:flex-col md:items-start md:space-y-4 items-center"
  }, [_c("span", {
    staticClass: "shrink-0 text-sm text-grayLight w-[20%] md:w-full"
  }, [_vm._v("Соль 2")]), _c("div", {
    staticClass: "w-[80%] md:w-full"
  }, [_c("div", {
    staticClass: "text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]"
  }, [_c("span", {
    staticClass: "max-w-full whitespace-nowrap text-ellipsis overflow-hidden"
  }, [_vm._v("QaAKPH8d7T2T2Oud285m6C9d")]), _c("a", {
    staticClass: "transition-all shrink-0 duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center",
    attrs: {
      href: "javascript:;"
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#copy"
    }
  })])])])])]), _c("div", {
    staticClass: "relative flex md:flex-col md:items-start md:space-y-4 items-center"
  }, [_c("span", {
    staticClass: "shrink-0 text-sm text-grayLight w-[20%] md:w-full"
  }, [_vm._v("Число игры:")]), _c("div", {
    staticClass: "w-[80%] md:w-full"
  }, [_c("div", {
    staticClass: "text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]"
  }, [_c("span", {
    staticClass: "max-w-full whitespace-nowrap text-ellipsis overflow-hidden"
  }, [_vm._v("0.39326375111344614")]), _c("a", {
    staticClass: "transition-all shrink-0 duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center",
    attrs: {
      href: "javascript:;"
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#copy"
    }
  })])])])])]), _c("div", {
    staticClass: "relative flex md:flex-col md:items-start md:space-y-4 items-center"
  }, [_c("span", {
    staticClass: "shrink-0 text-sm text-grayLight w-[20%] md:w-full"
  }, [_vm._v("Хэш игры:")]), _c("div", {
    staticClass: "w-[80%] md:w-full"
  }, [_c("div", {
    staticClass: "text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]"
  }, [_c("span", {
    staticClass: "max-w-full whitespace-nowrap text-ellipsis overflow-hidden"
  }, [_vm._v("2c05877a04ba24e25de4f912357e6181da8544c6c9eb2c5c7edf0d87")]), _c("a", {
    staticClass: "transition-all shrink-0 duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center",
    attrs: {
      href: "javascript:;"
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#copy"
    }
  })])])])])]), _c("div", {
    staticClass: "relative flex md:flex-col md:items-start md:space-y-4 items-center"
  }, [_c("span", {
    staticClass: "shrink-0 text-sm text-grayLight w-[20%] md:w-full"
  }, [_vm._v("Общая строка:")]), _c("div", {
    staticClass: "w-[80%] md:w-full"
  }, [_c("div", {
    staticClass: "text-gray flex items-center justify-between border-0 sm:h-[52px] text-sm pl-5 pr-3 h-[52px] w-full h-full rounded-xl bg-[#1b1c20]"
  }, [_c("span", {
    staticClass: "max-w-full whitespace-nowrap text-ellipsis overflow-hidden"
  }, [_vm._v("6OA1jt9g2c9eQx27flwnQ5860.39326375111344614QaAKPH8d7T2T2Oud285m6C9d")]), _c("a", {
    staticClass: "transition-all shrink-0 duration-200 w-[32px] h-[32px] text-gray rounded-lg hover:bg-[#3c3c46] hover:text-grayLight flex items-center justify-center",
    attrs: {
      href: "javascript:;"
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#copy"
    }
  })])])])])])])]), _c("div", {
    staticClass: "shrink-0 2xl:hidden"
  }, [_c("img", {
    attrs: {
      src: __webpack_require__(/*! @/images/fair.png */ "./resources/frontend/images/fair.png")
    }
  })])]), _c("div", {
    staticClass: "flex flex-col space-y-[20px]"
  }, [_c("span", {
    staticClass: "text-grayLight uppercase font-['Rubik'] font-medium text-sm"
  }, [_vm._v("Описание")]), _c("div", {
    staticClass: "flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline"
  }, [_c("p", [_vm._v('"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."')])])])])])]) : _vm._e()])], 1);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./resources/frontend/images/fair.png":
/*!********************************************!*\
  !*** ./resources/frontend/images/fair.png ***!
  \********************************************/
/***/ ((module) => {

module.exports = "/images/fair.png?94d46468c6c4eb12afb4a9a097065453";

/***/ }),

/***/ "./resources/frontend/views/Fair.vue":
/*!*******************************************!*\
  !*** ./resources/frontend/views/Fair.vue ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Fair_vue_vue_type_template_id_946dde4c_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Fair.vue?vue&type=template&id=946dde4c&lang=pug& */ "./resources/frontend/views/Fair.vue?vue&type=template&id=946dde4c&lang=pug&");
/* harmony import */ var _Fair_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Fair.vue?vue&type=script&lang=js& */ "./resources/frontend/views/Fair.vue?vue&type=script&lang=js&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");





/* normalize component */
;
var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__["default"])(
  _Fair_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Fair_vue_vue_type_template_id_946dde4c_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Fair_vue_vue_type_template_id_946dde4c_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/views/Fair.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/views/Fair.vue?vue&type=script&lang=js&":
/*!********************************************************************!*\
  !*** ./resources/frontend/views/Fair.vue?vue&type=script&lang=js& ***!
  \********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Fair_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Fair.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Fair.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Fair_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/views/Fair.vue?vue&type=template&id=946dde4c&lang=pug&":
/*!***********************************************************************************!*\
  !*** ./resources/frontend/views/Fair.vue?vue&type=template&id=946dde4c&lang=pug& ***!
  \***********************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Fair_vue_vue_type_template_id_946dde4c_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Fair_vue_vue_type_template_id_946dde4c_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Fair_vue_vue_type_template_id_946dde4c_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../node_modules/pug-plain-loader/index.js!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Fair.vue?vue&type=template&id=946dde4c&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Fair.vue?vue&type=template&id=946dde4c&lang=pug&");


/***/ })

}]);