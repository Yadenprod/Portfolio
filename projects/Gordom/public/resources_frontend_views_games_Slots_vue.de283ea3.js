(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_views_games_Slots_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=script&lang=js&":
/*!*******************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=script&lang=js& ***!
  \*******************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var vue_range_slider_dist_vue_range_slider_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vue-range-slider/dist/vue-range-slider.css */ "./node_modules/vue-range-slider/dist/vue-range-slider.css");
function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }
function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }
function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }
function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }
function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i]; return arr2; }

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  name: 'Slots',
  data: function data() {
    return {
      isProviderDropdownOpen: false,
      preloader: true,
      activeProvider: '',
      buttonLoader: false,
      providers: [{
        title: 'Все провайдеры',
        type: ''
      }, {
        title: 'pragmatic',
        type: 'pragmatic'
      }, {
        title: 'netent',
        type: 'netent'
      }, {
        title: 'amatic',
        type: 'amatic'
      }],
      slots: [],
      timeout: null,
      search: null,
      page: 1,
      total_page: 0
    };
  },
  components: {
    SlotCard: function SlotCard() {
      return __webpack_require__.e(/*! import() */ "resources_frontend_components_pages_games_slots_SlotCard_vue").then(__webpack_require__.bind(__webpack_require__, /*! @/components/pages/games/slots/SlotCard.vue */ "./resources/frontend/components/pages/games/slots/SlotCard.vue"));
    }
  },
  mounted: function mounted() {
    this.init();
  },
  methods: {
    init: function init(page) {
      var _this = this;
      this.buttonLoader = true;
      this.$root.axios.post('/slots/init', {
        page: page || this.page,
        search: this.search,
        provider: this.activeProvider
      }).then(function (response) {
        var _this$slots;
        var data = response.data;
        (_this$slots = _this.slots).push.apply(_this$slots, _toConsumableArray(data.data));
        _this.preloader = false;
        _this.total_page = data.last_page;
        _this.page = data.current_page;
        _this.buttonLoader = false;
      })["catch"](function (err) {
        _this.buttonLoader = false;
        _this.$toastr.Add({
          name: 'BetMinesToast',
          title: 'Ошибка',
          msg: 'При получении списка произошла ошибка',
          type: 'error',
          timeout: 3000,
          progressbar: true
        });
      });
    },
    loadMore: function loadMore() {
      if (this.buttonLoader) return;
      this.init(this.page + 1);
    },
    closeProviderDropdown: function closeProviderDropdown() {
      this.isProviderDropdownOpen = false;
    }
  },
  watch: {
    search: function search() {
      var _this2 = this;
      clearTimeout(this.timeout);
      this.timeout = setTimeout(function () {
        _this2.slots = [];
        _this2.preloader = true;
        _this2.init(1);
      }, 500);
    },
    activeProvider: function activeProvider() {
      this.slots = [];
      this.preloader = true;
      this.init(1);
    }
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=template&id=c5061cbe&scoped=true&lang=pug&":
/*!********************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=template&id=c5061cbe&scoped=true&lang=pug& ***!
  \********************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
    staticClass: "flex flex-col rounded-xl"
  }, [_c("Transition", {
    attrs: {
      "enter-active-class": "transition-all duration-[200ms] ease-out",
      "enter-class": "opacity-0",
      "enter-to-class": "opacity-100"
    }
  }, [_c("div", {
    staticClass: "flex flex-col space-y-[50px] lg:space-y-[30px] rounded-xl"
  }, [_c("div", {
    staticClass: "flex flex-col -space-y-[20px]"
  }, [_c("div", {
    staticClass: "relative w-full min-h-[50px] overflow-hidden rounded-xl"
  }, [_c("div", {
    staticClass: "w-full mt-[50px] md:space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1]"
  }, [_c("div", {
    staticClass: "w-full mb-12 sm:flex-col gap-4 flex items-center justify-between"
  }, [_c("label", {
    staticClass: "md:w-full md:max-w-none max-w-[234px] relative",
    attrs: {
      "for": "search"
    }
  }, [_c("svg", {
    staticClass: "w-[24px] h-[24px] absolute top-1/2 text-gray -translate-y-1/2 left-3.5"
  }, [_c("use", {
    attrs: {
      href: "images/symbols.svg#search"
    }
  })]), _c("input", {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: _vm.search,
      expression: "search"
    }],
    staticClass: "border-0 bg-[#3A3A43] h-[52px] w-full px-5 pl-12 rounded-xl text-sm font-medium placeholder:text-grayLight/[0.5] focus:ring-0 focus:outline-none focus:border-0",
    attrs: {
      placeholder: "Поиск",
      type: "text",
      name: "search",
      id: "search"
    },
    domProps: {
      value: _vm.search
    },
    on: {
      input: function input($event) {
        if ($event.target.composing) return;
        _vm.search = $event.target.value;
      }
    }
  })]), _c("div", {
    directives: [{
      name: "on-clickaway",
      rawName: "v-on-clickaway",
      value: _vm.closeProviderDropdown,
      expression: "closeProviderDropdown"
    }],
    staticClass: "md:w-full relative"
  }, [_c("div", {
    staticClass: "md:max-w-none max-w-[234px] relative bg-[#313136] h-[52px] px-5 rounded-xl flex items-center justify-between cursor-pointer",
    on: {
      click: function click($event) {
        _vm.isProviderDropdownOpen = !_vm.isProviderDropdownOpen;
      }
    }
  }, [_c("p", {
    staticClass: "text-sm pointer-events-none font-medium select-none text-grayLight/[0.5] mr-6"
  }, [_vm._v("Провайдеры")]), _c("i", {
    staticClass: "text-gray inline-block w-2 h-2 border-r-2 border-b-2 border-current rotate-[45deg] transition-all duration-200",
    "class": _vm.isProviderDropdownOpen ? ["rotate-[225deg]"] : ""
  })]), _c("Transition", {
    attrs: {
      "enter-active-class": "transition ease-out duration-100",
      "enter-class": "transform opacity-0 scale-95",
      "enter-to-class": "transform opacity-100 scale-100",
      "leave-active-class": "transition ease-in duration-75",
      "leave-class": "transform opacity-100 scale-100",
      "leave-to-class": "transform opacity-0 scale-95"
    }
  }, [_vm.isProviderDropdownOpen ? _c("div", {
    staticClass: "absolute w-full z-[1] p-2 origin-top-right right-0 mt-2 bg-[#313136] rounded-xl flex flex-col gap-1 shadow-[0px_4px_28px_rgba(0,0,0,0.08)]"
  }, _vm._l(_vm.providers, function (provider) {
    return _c("div", {
      staticClass: "px-3.5 py-2 rounded-md select-none text-sm transition-colors text-gray cursor-pointer hover:bg-[#3A3A43] hover:text-white",
      "class": [_vm.activeProvider == provider.type ? "bg-[#3A3A43] !text-white" : ""],
      on: {
        click: function click($event) {
          _vm.activeProvider = provider.type;
        }
      }
    }, [_vm._v(_vm._s(provider.title))]);
  }), 0) : _vm._e()])], 1)]), _vm.preloader ? _c("div", {
    staticClass: "w-full py-12 flex items-center justify-center"
  }, [_c("Spin", {
    attrs: {
      color: "text-white"
    }
  })], 1) : _vm._e(), !_vm.preloader ? _c("div", {
    staticClass: "grid grid-cols-5 2xl:grid-cols-3 sm:!grid-cols-2 gap-3.5"
  }, _vm._l(_vm.slots, function (item, id) {
    return _c("SlotCard", {
      key: id,
      attrs: {
        data: item
      }
    });
  }), 1) : _vm._e(), !_vm.preloader && !_vm.slots.length ? _c("div", {
    staticClass: "block text-center m-[25px]"
  }, [_c("span", [_vm._v("Не найдено")])]) : _vm._e(), !_vm.preloader && _vm.page !== _vm.total_page ? _c("div", {
    staticClass: "flex justify-center w-full mt-[30px]"
  }, [_c("div", {
    staticClass: "flex space-x-4 items-center"
  }, [_c("a", {
    staticClass: "h-[42px] px-6 rounded-full font-bold transition-all duration-200 hover:shadow-[0px_0px_0px_12px_rgba(86,79,232,0.12)] flex items-center justify-center text-white bg-gradient-to-r from-[#6a6a7a] to-[#6a6a7a]",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: _vm.loadMore
    }
  }, [_vm.buttonLoader ? _c("svg", {
    staticClass: "animate-spin mr-3 h-5 w-5 text-white !m-auto",
    attrs: {
      xmlns: "http://www.w3.org/2000/svg",
      fill: "none",
      viewBox: "0 0 24 24"
    }
  }, [_c("circle", {
    staticClass: "opacity-25",
    attrs: {
      cx: "12",
      cy: "12",
      r: "10",
      stroke: "currentColor",
      "stroke-width": "4"
    }
  }), _c("path", {
    staticClass: "opacity-75",
    attrs: {
      fill: "currentColor",
      d: "M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
    }
  })]) : _vm._e(), _vm._v(" " + _vm._s(!_vm.buttonLoader ? "Загрузить ещё" : ""))]), _c("span", {
    staticClass: "text-[#696F96] text-sm font-semibold"
  }, [_vm._v(_vm._s(_vm.page) + " из " + _vm._s(_vm.total_page))])])]) : _vm._e()])])])])])], 1);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./resources/frontend/images/star.svg":
/*!********************************************!*\
  !*** ./resources/frontend/images/star.svg ***!
  \********************************************/
/***/ ((module) => {

module.exports = "/images/star.svg?09607531fc889e7ae288c8c7dcef62d4";

/***/ }),

/***/ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true&":
/*!***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true& ***!
  \***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/laravel-mix/node_modules/css-loader/dist/runtime/api.js */ "./node_modules/laravel-mix/node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);
// Imports

var ___CSS_LOADER_EXPORT___ = _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});
// Module
___CSS_LOADER_EXPORT___.push([module.id, "input[type=checkbox][data-v-c5061cbe]:checked {\n  opacity: 10%;\n}", ""]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss&":
/*!***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss& ***!
  \***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../node_modules/laravel-mix/node_modules/css-loader/dist/runtime/api.js */ "./node_modules/laravel-mix/node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../node_modules/laravel-mix/node_modules/css-loader/dist/runtime/getUrl.js */ "./node_modules/laravel-mix/node_modules/css-loader/dist/runtime/getUrl.js");
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_laravel_mix_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _images_star_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../images/star.svg */ "./resources/frontend/images/star.svg");
/* harmony import */ var _images_star_svg__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_images_star_svg__WEBPACK_IMPORTED_MODULE_2__);
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});
var ___CSS_LOADER_URL_REPLACEMENT_0___ = _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_1___default()((_images_star_svg__WEBPACK_IMPORTED_MODULE_2___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".range__slider_wrap {\n  position: relative;\n}\n.range-slider {\n  padding: 0;\n}\n.range-slider-knob:before {\n  content: \"\";\n  position: absolute;\n  left: 50%;\n  top: 50%;\n  transform: translate(-50%, -50%);\n  width: 16px;\n  height: 16px;\n  background: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ") no-repeat center center/contain;\n}\n.picker {\n  width: 16px;\n  height: 16px;\n  position: absolute;\n  top: -10px;\n  left: 100%;\n  transform: translateX(-8px);\n  border-radius: 100%;\n  border: 3px solid white;\n}\n.picker::before {\n  content: \"\";\n  width: 10px;\n  height: 10px;\n  position: absolute;\n  top: 50%;\n  left: 50%;\n  transform: translate(-50%, -50%);\n  border-radius: 100%;\n  background: #43c175;\n  z-index: 2;\n}\n.picker::after {\n  content: \"\";\n  width: 6px;\n  height: 6px;\n  position: absolute;\n  bottom: -4px;\n  left: 50%;\n  transform: translateX(-50%) rotate(45deg);\n  background: white;\n  z-index: 1;\n}", ""]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true&":
/*!***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true& ***!
  \***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_style_index_0_id_c5061cbe_lang_scss_scoped_true___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true& */ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true&");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_style_index_0_id_c5061cbe_lang_scss_scoped_true___WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_style_index_0_id_c5061cbe_lang_scss_scoped_true___WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss&":
/*!***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss& ***!
  \***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_style_index_1_id_c5061cbe_lang_scss___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss& */ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss&");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_style_index_1_id_c5061cbe_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_style_index_1_id_c5061cbe_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./resources/frontend/views/games/Slots.vue":
/*!**************************************************!*\
  !*** ./resources/frontend/views/games/Slots.vue ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Slots_vue_vue_type_template_id_c5061cbe_scoped_true_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Slots.vue?vue&type=template&id=c5061cbe&scoped=true&lang=pug& */ "./resources/frontend/views/games/Slots.vue?vue&type=template&id=c5061cbe&scoped=true&lang=pug&");
/* harmony import */ var _Slots_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Slots.vue?vue&type=script&lang=js& */ "./resources/frontend/views/games/Slots.vue?vue&type=script&lang=js&");
/* harmony import */ var _Slots_vue_vue_type_style_index_0_id_c5061cbe_lang_scss_scoped_true___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true& */ "./resources/frontend/views/games/Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true&");
/* harmony import */ var _Slots_vue_vue_type_style_index_1_id_c5061cbe_lang_scss___WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss& */ "./resources/frontend/views/games/Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");



;



/* normalize component */

var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_4__["default"])(
  _Slots_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Slots_vue_vue_type_template_id_c5061cbe_scoped_true_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Slots_vue_vue_type_template_id_c5061cbe_scoped_true_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  "c5061cbe",
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/views/games/Slots.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/views/games/Slots.vue?vue&type=script&lang=js&":
/*!***************************************************************************!*\
  !*** ./resources/frontend/views/games/Slots.vue?vue&type=script&lang=js& ***!
  \***************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Slots.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/views/games/Slots.vue?vue&type=template&id=c5061cbe&scoped=true&lang=pug&":
/*!******************************************************************************************************!*\
  !*** ./resources/frontend/views/games/Slots.vue?vue&type=template&id=c5061cbe&scoped=true&lang=pug& ***!
  \******************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_template_id_c5061cbe_scoped_true_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_template_id_c5061cbe_scoped_true_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_template_id_c5061cbe_scoped_true_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../../node_modules/pug-plain-loader/index.js!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Slots.vue?vue&type=template&id=c5061cbe&scoped=true&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=template&id=c5061cbe&scoped=true&lang=pug&");


/***/ }),

/***/ "./resources/frontend/views/games/Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true&":
/*!************************************************************************************************************!*\
  !*** ./resources/frontend/views/games/Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true& ***!
  \************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _node_modules_style_loader_dist_cjs_js_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_style_index_0_id_c5061cbe_lang_scss_scoped_true___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/style-loader/dist/cjs.js!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true& */ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=0&id=c5061cbe&lang=scss&scoped=true&");


/***/ }),

/***/ "./resources/frontend/views/games/Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss&":
/*!************************************************************************************************!*\
  !*** ./resources/frontend/views/games/Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss& ***!
  \************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _node_modules_style_loader_dist_cjs_js_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Slots_vue_vue_type_style_index_1_id_c5061cbe_lang_scss___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/style-loader/dist/cjs.js!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss& */ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Slots.vue?vue&type=style&index=1&id=c5061cbe&lang=scss&");


/***/ })

}]);