"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_components_pages_games_wheel_Bets_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=script&lang=js&":
/*!***********************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=script&lang=js& ***!
  \***********************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  props: {
    list: {
      type: Array,
      "default": function _default() {}
    }
  },
  methods: {
    play: function play(color) {
      this.$emit('play', color);
    },
    getBank: function getBank(x) {
      var item = this.list.find(function (el) {
        return el.x === x;
      });
      var bets = item.users.map(function (el) {
        return el.bet;
      });
      if (!bets.length) return 0;
      return bets.reduce(function (total, amount) {
        return total + parseFloat(amount);
      });
    }
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=template&id=3b8c143a&lang=pug&":
/*!************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=template&id=3b8c143a&lang=pug& ***!
  \************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
    staticClass: "relative grid grid-cols-6 2xl:grid-cols-4 md:!grid-cols-3 md:gap-2 sm:flex sm:flex-col sm:gap-0 sm:space-y-3 gap-4 w-full"
  }, _vm._l(_vm.list, function (item) {
    return _c("div", {
      key: item.id,
      staticClass: "relative flex flex-col space-y-3"
    }, [_c("button", {
      staticClass: "justify-between flex items-center h-[58px] px-5 rounded-xl text-sm transition-all duration-200 focus:ring-0 focus:border-0 focus:outline-0",
      "class": item.x === 2 ? "bg-[#2c2c31] hover:bg-[#3A3A40] text-grayLight " :  false || item.x === 3 ? "bg-green hover:bg-greenHover text-white" :  false || item.x === 5 ? "bg-[#f08929] hover:bg-[#fd9739] text-white" :  false || item.x === 10 ? "bg-red hover:bg-redHover text-white" :  false || item.x === 20 ? "bg-[#d92c9f] hover:bg-[#e43fad] text-white" :  false || item.x === 100 ? "bg-violet hover:bg-violetHover text-white" : "",
      attrs: {
        type: "submit"
      },
      on: {
        click: function click($event) {
          return _vm.play(item.color);
        }
      }
    }, [_c("span", {
      staticClass: "font-semibold pointer-events-none"
    }, [_vm._v("Ставка")]), _c("b", {
      staticClass: "text-lg font-['Rubik'] pointer-events-none"
    }, [_vm._v(_vm._s("x" + item.x))])]), _c("div", {
      staticClass: "flex flex-col space-y-2 text-grayLight text-sm font-semibold"
    }, [_c("div", {
      staticClass: "flex items-center justify-between bg-[#1b1c20] py-2.5 px-4 rounded-lg"
    }, [_c("div", {
      staticClass: "flex items-center space-x-2"
    }, [_c("svg", {
      staticClass: "w-[16px] h-[16px]"
    }, [_c("use", {
      attrs: {
        "xlink:href": "images/symbols.svg#users"
      }
    })]), _c("span", [_vm._v(_vm._s(item.users.length))])]), _c("div", {
      staticClass: "flex items-center space-x-2"
    }, [_c("img", {
      staticClass: "max-w-[16px]",
      attrs: {
        src: __webpack_require__(/*! @/images/logotype-small.svg */ "./resources/frontend/images/logotype-small.svg")
      }
    }), _c("span", [_vm._v(_vm._s(parseFloat(_vm.getBank(item.x)).toFixed(2)))])])]), _c("div", {
      staticClass: "flex flex-col space-y-2.5 2xl:hidden"
    }, _vm._l(item.users, function (item) {
      return _c("div", {
        key: item.id,
        staticClass: "gap-[10px] flex items-center justify-between bg-[#1b1c20] py-2.5 px-4 rounded-lg"
      }, [_c("span", {
        staticClass: "max-w-full whitespace-nowrap text-ellipsis overflow-hidden"
      }, [_vm._v(_vm._s(item.username))]), _c("div", {
        staticClass: "shrink-0 flex items-center space-x-2"
      }, [_c("img", {
        staticClass: "max-w-[16px]",
        attrs: {
          src: __webpack_require__(/*! @/images/logotype-small.svg */ "./resources/frontend/images/logotype-small.svg")
        }
      }), _c("span", [_vm._v(_vm._s(item.bet))])])]);
    }), 0)])]);
  }), 0);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./resources/frontend/components/pages/games/wheel/Bets.vue":
/*!******************************************************************!*\
  !*** ./resources/frontend/components/pages/games/wheel/Bets.vue ***!
  \******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Bets_vue_vue_type_template_id_3b8c143a_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Bets.vue?vue&type=template&id=3b8c143a&lang=pug& */ "./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=template&id=3b8c143a&lang=pug&");
/* harmony import */ var _Bets_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Bets.vue?vue&type=script&lang=js& */ "./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=script&lang=js&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");





/* normalize component */
;
var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__["default"])(
  _Bets_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Bets_vue_vue_type_template_id_3b8c143a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Bets_vue_vue_type_template_id_3b8c143a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/components/pages/games/wheel/Bets.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=script&lang=js&":
/*!*******************************************************************************************!*\
  !*** ./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=script&lang=js& ***!
  \*******************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Bets_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Bets.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Bets_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=template&id=3b8c143a&lang=pug&":
/*!**********************************************************************************************************!*\
  !*** ./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=template&id=3b8c143a&lang=pug& ***!
  \**********************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Bets_vue_vue_type_template_id_3b8c143a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Bets_vue_vue_type_template_id_3b8c143a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Bets_vue_vue_type_template_id_3b8c143a_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../../../../node_modules/pug-plain-loader/index.js!../../../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Bets.vue?vue&type=template&id=3b8c143a&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/pages/games/wheel/Bets.vue?vue&type=template&id=3b8c143a&lang=pug&");


/***/ })

}]);