(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_views_Index_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Index.vue?vue&type=script&lang=js&":
/*!*************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Index.vue?vue&type=script&lang=js& ***!
  \*************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  name: 'Index',
  components: {
    'CardGame': function CardGame() {
      return __webpack_require__.e(/*! import() */ "resources_frontend_components_pages_index_CardGame_vue").then(__webpack_require__.bind(__webpack_require__, /*! @/components/pages/index/CardGame.vue */ "./resources/frontend/components/pages/index/CardGame.vue"));
    },
    Table: function Table() {
      return __webpack_require__.e(/*! import() */ "resources_frontend_components_ui_Table_vue").then(__webpack_require__.bind(__webpack_require__, /*! @/components/ui/Table.vue */ "./resources/frontend/components/ui/Table.vue"));
    },
    GamesBlock: function GamesBlock() {
      return __webpack_require__.e(/*! import() */ "resources_frontend_components_layouts_Elements_GamesBlock_vue").then(__webpack_require__.bind(__webpack_require__, /*! @/components/layouts/Elements/GamesBlock.vue */ "./resources/frontend/components/layouts/Elements/GamesBlock.vue"));
    },
    Stats: function Stats() {
      return __webpack_require__.e(/*! import() */ "resources_frontend_components_layouts_Elements_Stats_vue").then(__webpack_require__.bind(__webpack_require__, /*! @/components/layouts/Elements/Stats.vue */ "./resources/frontend/components/layouts/Elements/Stats.vue"));
    }
  },
  data: function data() {
    return {
      preloader: true,
      games: [{
        id: 1,
        name: 'Dice',
        path: '/dice',
        image: 'dice_prev.png'
      }, {
        id: 2,
        name: 'Mines',
        path: '/mines',
        image: 'mines_prev.png'
      }, {
        id: 3,
        name: 'Wheel',
        path: '/wheel',
        image: 'wheel_prev.png'
      }, {
        id: 4,
        name: 'Slots',
        path: '/slots',
        image: 'slots_prev.png'
      }
      // {
      //     id: 5,
      //     name: null,
      //     path: null,
      //     image: 'none_prev.png',
      // },
      ],

      online: 0
    };
  },
  mounted: function mounted() {
    this.preloaderDestroy();
    this.$socket.emit('getOnline');
  },
  methods: {
    preloaderDestroy: function preloaderDestroy() {
      var _this = this;
      setTimeout(function () {
        _this.preloader = false;
      }, 300);
    }
  },
  sockets: {
    online: function online(data) {
      this.online = data;
    }
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Index.vue?vue&type=template&id=284ce5e8&lang=pug&":
/*!**************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Index.vue?vue&type=template&id=284ce5e8&lang=pug& ***!
  \**************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
    staticClass: "flex flex-col space-y-[30px]"
  }, [_c("div", {
    staticClass: "flex w-full items-stretch justify-between gap-6"
  }, [_c("div", {
    staticClass: "shrink-0 xl:hidden w-[25%] flex flex-col py-6 justify-between space-y-6"
  }, [_c("div", {
    staticClass: "flex flex-col [&_h1]:font-['Rubik'] [&_h1]:text-[26px] [&_h1>span]:text-[#7c75d9] font-semibold text-[#cfcde9] [&_p]:text-sm [&_p]:text-[#cfcde9] [&_p]:leading-[180%] space-y-2"
  }, [_c("h1", [_c("span", [_vm._v("TREASURE")]), _vm._v(" Casino")]), _c("p", [_vm._v("Уникальные игры с выводом денег "), _c("br"), _vm._v(" и с большым шансом на победу")])]), _c("div", {
    staticClass: "flex flex-col space-y-2"
  }, [_c("span", {
    staticClass: "text-sm text-gray font-semibold"
  }, [_vm._v("Сейчас играют:")]), _c("div", {
    staticClass: "flex items-center space-x-3 font-['Rubik']"
  }, [_c("span", {
    staticClass: "flex relative h-2 w-2"
  }, [_c("span", {
    staticClass: "animate-ping absolute inline-flex h-full w-full rounded-full bg-green opacity-75"
  }), _c("span", {
    staticClass: "relative inline-flex rounded-full h-2 w-2 bg-green"
  })]), _c("b", {
    staticClass: "font-medium text-lg"
  }, [_vm._v(_vm._s(_vm.online))])])])]), _c("div", {
    staticClass: "w-full grid before:pt-[30%] xl:before:pt-[40%] sm:before:!pt-[70%] relative rounded-2xl overflow-hidden"
  }, [_c("div", {
    staticClass: "absolute left-0 top-0 w-full h-full flex items-center xl:justify-center justify-start z-[1]"
  }, [_c("div", {
    staticClass: "pl-20 xl:pl-0 flex flex-col items-center space-y-6"
  }, [_c("div", {
    staticClass: "flex flex-col items-center space-y-1"
  }, [_c("div", {
    staticClass: "uppercase text-6xl font-['Rubik'] xl:text-5xl sm:!text-4xl font-medium select-none text-white leading-[100%]"
  }, [_vm._v("Турниры")]), _c("p", {
    staticClass: "text-sm font-semibold text-grayLight"
  }, [_vm._v("стань первым среди лучших")])]), _c("Btn", {
    attrs: {
      text: "Забери джекпот",
      type: "link",
      path: "/tourniers",
      theme: null,
      ico: null
    }
  })], 1)]), _c("div", {
    staticClass: "absolute left-0 top-0 w-full h-full"
  }, [_c("img", {
    staticClass: "absolute left-0 top-0 w-full h-full object-cover",
    attrs: {
      src: __webpack_require__(/*! @/images/banner.png */ "./resources/frontend/images/banner.png")
    }
  })])])]), _c("div", {
    staticClass: "w-full flex flex-col space-y-[50px] lg:space-y-[30px]"
  }, [_c("div", {
    staticClass: "flex flex-col"
  }, [_c("div", {
    staticClass: "flex items-center justify-between mb-[30px] lg:mb-[20px]"
  }, [_c("div", {
    staticClass: "flex items-center text-grayLight uppercase font-['Rubik'] font-medium text-sm space-x-2"
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#games"
    }
  })]), _c("span", [_vm._v("Наши игры")])])]), _c("CardGame", {
    attrs: {
      games: _vm.games
    }
  })], 1), _c("GamesBlock")], 1)]) : _vm._e()])], 1);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./resources/frontend/images/banner.png":
/*!**********************************************!*\
  !*** ./resources/frontend/images/banner.png ***!
  \**********************************************/
/***/ ((module) => {

module.exports = "/images/banner.png?c28de057442b380416b9d14ec4d635c9";

/***/ }),

/***/ "./resources/frontend/views/Index.vue":
/*!********************************************!*\
  !*** ./resources/frontend/views/Index.vue ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Index_vue_vue_type_template_id_284ce5e8_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Index.vue?vue&type=template&id=284ce5e8&lang=pug& */ "./resources/frontend/views/Index.vue?vue&type=template&id=284ce5e8&lang=pug&");
/* harmony import */ var _Index_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Index.vue?vue&type=script&lang=js& */ "./resources/frontend/views/Index.vue?vue&type=script&lang=js&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");





/* normalize component */
;
var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__["default"])(
  _Index_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Index_vue_vue_type_template_id_284ce5e8_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Index_vue_vue_type_template_id_284ce5e8_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/views/Index.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/views/Index.vue?vue&type=script&lang=js&":
/*!*********************************************************************!*\
  !*** ./resources/frontend/views/Index.vue?vue&type=script&lang=js& ***!
  \*********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Index_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Index.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Index.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Index_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/views/Index.vue?vue&type=template&id=284ce5e8&lang=pug&":
/*!************************************************************************************!*\
  !*** ./resources/frontend/views/Index.vue?vue&type=template&id=284ce5e8&lang=pug& ***!
  \************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Index_vue_vue_type_template_id_284ce5e8_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Index_vue_vue_type_template_id_284ce5e8_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Index_vue_vue_type_template_id_284ce5e8_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../node_modules/pug-plain-loader/index.js!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Index.vue?vue&type=template&id=284ce5e8&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Index.vue?vue&type=template&id=284ce5e8&lang=pug&");


/***/ })

}]);