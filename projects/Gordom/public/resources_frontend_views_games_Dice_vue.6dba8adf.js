(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_views_games_Dice_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=script&lang=js&":
/*!******************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=script&lang=js& ***!
  \******************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var vue_range_slider_dist_vue_range_slider_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vue-range-slider/dist/vue-range-slider.css */ "./node_modules/vue-range-slider/dist/vue-range-slider.css");

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  name: 'Dice',
  data: function data() {
    return {
      isLoading: false,
      preloader: true,
      sliderValue: 50,
      betSum: 1,
      maxBetSum: 10000,
      minBetSum: 1,
      history: [],
      isWin: false,
      showPicker: false,
      interval: null
    };
  },
  components: {
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
  mounted: function mounted() {
    this.preloaderDestroy();
  },
  methods: {
    preloaderDestroy: function preloaderDestroy() {
      var _this = this;
      setTimeout(function () {
        _this.preloader = false;
      }, 300);
    },
    play: function play() {
      var _this2 = this;
      this.isLoading = true;
      this.$root.axios.post('/dice/bet', {
        amount: this.betSum,
        chance: this.sliderValue
      }).then(function (response) {
        var data = response.data;
        _this2.showPicker = true;
        _this2.isLoading = false;
        if ('error' in data) {
          return _this2.$toastr.Add({
            name: 'BetWheelToast',
            title: 'Ошибка',
            msg: data.message,
            type: 'error',
            defaultClassNames: ["animated", "zoomInUp"],
            timeout: 3000,
            progressbar: true
          });
        }
        _this2.isWin = data.status;
        _this2.history.unshift({
          id: new Date() / 1,
          percent: data.number,
          win: data.status
        });
        clearTimeout(_this2.timeout);
        _this2.timeout = setTimeout(function () {
          _this2.showPicker = false;
          _this2.$refs['dicePicker'].style.left = '0%';
        }, 5000);
        _this2.$refs['dicePicker'].style.left = data.number + 1 + '%';
        _this2.$root.user.balance = data.balance;
      });
    },
    maxBet: function maxBet() {
      this.betSum = this.maxBetSum;
    },
    minBet: function minBet() {
      this.betSum = this.minBetSum;
    },
    xBet: function xBet() {
      if (this.betSum <= this.maxBetSum) {
        this.betSum = this.betSum * 2;
      }
      if (this.betSum >= this.maxBetSum) {
        this.betSum = this.maxBetSum;
      }
    },
    dBet: function dBet() {
      if (this.betSum < 1) {
        return false;
      }
      this.betSum = (this.betSum / 2).toFixed();
    },
    onInputSumm: function onInputSumm(_ref) {
      var target = _ref.target;
      var val = target.value;
      var newVal = "".concat(Math.min(this.maxBetSum, Math.max(0, val.slice(-10000) | 0)));
      if (val !== newVal) {
        target.value = newVal;
        target.dispatchEvent(new Event('input'));
      }
      if (val === '') {
        target.value = '';
        target.dispatchEvent(new Event('input'));
      }
    },
    getNumber: function getNumber(number, one, two, five) {
      var n = Math.abs(number);
      n %= 100;
      if (n >= 5 && n <= 20) {
        return five;
      }
      n %= 10;
      if (n === 1) {
        return one;
      }
      if (n >= 2 && n <= 4) {
        return two;
      }
      return five;
    }
  },
  watch: {
    history: function history() {
      if (this.history.length >= 25) {
        this.history.pop();
      }
    }
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=template&id=1f1c662a&lang=pug&":
/*!*******************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=template&id=1f1c662a&lang=pug& ***!
  \*******************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
    staticClass: "flex flex-col -space-y-[20px]"
  }, [_c("div", {
    staticClass: "w-full flex items-center justify-center gap-6"
  }, [_c("div", {
    staticClass: "shrink-0 relative select-none"
  }, [_c("div", {
    staticClass: "absolute left-0 -top-[5px] w-full h-full flex items-center justify-center z-[1]"
  }, [_c("span", {
    staticClass: "font-['Deftone'] text-grayLight text-4xl tracking-[1px]"
  }, [_vm._v("Dice")])]), _c("img", {
    attrs: {
      src: __webpack_require__(/*! @/images/game.png */ "./resources/frontend/images/game.png")
    }
  })])]), _c("div", {
    staticClass: "relative w-full min-h-[50px] overflow-hidden rounded-xl"
  }, [_c("div", {
    staticClass: "w-full md:flex-col mt-[50px] md:space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex items-center justify-between"
  }, [_c("div", {
    staticClass: "w-[calc(100%_-_300px)] md:w-full flex flex-col space-y-5"
  }, [_c("div", {
    staticClass: "w-full flex flex-col items-center space-y-[30px]"
  }, [_c("img", {
    staticClass: "max-w-[75px]",
    attrs: {
      src: __webpack_require__(/*! @/images/logotype-small.svg */ "./resources/frontend/images/logotype-small.svg")
    }
  }), _c("p", {
    staticClass: "uppercase text-grayLight text-sm font-medium text-center sm:text-xs"
  }, [_vm._v("Угадай число и увеличь свой депозит!")])]), _c("div", {
    staticClass: "relative flex flex-col space-y-3"
  }, [_c("div", {
    staticClass: "flex items-center text-sm text-gray justify-between font-medium font-['Rubik'] [&_span]:w-[28px] [&_span]:text-center"
  }, [_c("span", [_vm._v("0")]), _c("span", [_vm._v("30")]), _c("span", [_vm._v("50")]), _c("span", [_vm._v("70")]), _c("span", [_vm._v("100")])]), _c("div", {
    staticClass: "flex relative flex-col bg-[#2c2c31] px-4 py-5 rounded-xl"
  }, [_c("div", {
    staticClass: "range__slider_wrap"
  }, [_c("range-slider", {
    staticClass: "!w-full [&_span.range-slider-rail]:bg-red [&_span.range-slider-fill]:bg-green [&_span.range-slider-knob]:!rounded-[10px] [&_span.range-slider-knob]:w-[28px] [&_span.range-slider-knob]:h-[28px] [&_span.range-slider-knob]:!border-0 [&_span.range-slider-knob]:bg-violet [&_span.range-slider-knob]:cursor-pointer [&_span.range-slider-knob]:hover:bg-violetHover",
    attrs: {
      min: "1",
      max: "95",
      step: "1"
    },
    model: {
      value: _vm.sliderValue,
      callback: function callback($$v) {
        _vm.sliderValue = $$v;
      },
      expression: "sliderValue"
    }
  })], 1), _c("div", {
    ref: "dicePicker",
    staticClass: "picker",
    "class": [{
      invisible: !_vm.showPicker
    }, {
      win: _vm.isWin
    }, {
      lose: !_vm.isWin
    }]
  })])]), _c("div", {
    staticClass: "relative w-full overflow-hidden before:absolute before:right-0 before:h-full before:top-0 before:w-[150px] before:bg-gradient-to-r before:to-[#202024] before:from-transparent before:z-[1]"
  }, [_c("div", {
    staticClass: "flex items-center space-x-3"
  }, _vm._l(_vm.history, function (item) {
    return _c("div", {
      key: item.id,
      staticClass: "min-w-[44px] min-h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs select-none",
      "class": item.win ? "text-green" : "text-red"
    }, [_vm._v(_vm._s(item.percent))]);
  }), 0)])]), _c("form", {
    staticClass: "w-[220px] md:w-full flex flex-col shrink-0 space-y-6",
    on: {
      submit: function submit($event) {
        $event.preventDefault();
        return _vm.play();
      }
    }
  }, [_c("div", {
    staticClass: "flex flex-col space-y-4"
  }, [_c("div", {
    staticClass: "w-full flex items-center justify-between text-sm bg-[#1b1c20] py-3 px-4 rounded-xl text-gray"
  }, [_c("span", {
    staticClass: "font-semibold"
  }, [_vm._v("Коэффициент:")]), _c("b", {
    staticClass: "uppercase font-['Rubik'] !font-medium text-grayLight text-base"
  }, [_vm._v("x" + _vm._s(parseFloat(100 / _vm.sliderValue).toFixed(2)))])]), _c("div", {
    staticClass: "w-full flex items-center justify-between text-sm bg-[#1b1c20] py-3 px-4 rounded-xl text-gray"
  }, [_c("span", {
    staticClass: "font-semibold"
  }, [_vm._v("Шанс:")]), _c("b", {
    staticClass: "uppercase font-['Rubik'] !font-medium text-grayLight text-base"
  }, [_vm._v(_vm._s(_vm.sliderValue + "%"))])])]), _c("div", {
    staticClass: "flex flex-col space-y-4"
  }, [_c("b", {
    staticClass: "text-grayLight !font-semibold text-sm"
  }, [_vm._v("Ваша ставка:")]), _c("div", {
    staticClass: "flex flex-col"
  }, [_c("div", {
    staticClass: "flex items-center justify-between md:justify-start md:space-x-3"
  }, [_c("a", {
    staticClass: "w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: _vm.maxBet
    }
  }, [_vm._v("Max ")]), _c("a", {
    staticClass: "w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: _vm.minBet
    }
  }, [_vm._v("Min ")]), _c("a", {
    staticClass: "w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: _vm.xBet
    }
  }, [_vm._v("X2 ")]), _c("a", {
    staticClass: "w-[44px] h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: _vm.dBet
    }
  }, [_vm._v("1/2")])])]), _c("input", {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: _vm.betSum,
      expression: "betSum"
    }],
    staticClass: "text-sm font-['Rubik'] bg-[#1b1c20] py-3 px-4 rounded-xl placeholder:text-gray text-white focus:border-0 focus:placeholder:opacity-0 focus:outline-0",
    attrs: {
      placeholder: "Введите сумму"
    },
    domProps: {
      value: _vm.betSum
    },
    on: {
      input: [function ($event) {
        if ($event.target.composing) return;
        _vm.betSum = $event.target.value;
      }, _vm.onInputSumm]
    }
  }), _c("div", {
    staticClass: "[&_button]:w-full"
  }, [_c("Btn", {
    "class": _vm.betSum ? "" : "opacity-[0.3] cursor-not-allowed pointer-events-none",
    attrs: {
      text: _vm.isLoading ? "Бросаем кости.." : "Играть",
      type: "button",
      theme: null,
      ico: "play"
    }
  })], 1)])])]), _c("img", {
    staticClass: "absolute top-0 left-1/2 -translate-x-1/2 max-w-fit",
    attrs: {
      src: __webpack_require__(/*! @/images/game-top-bar.svg */ "./resources/frontend/images/game-top-bar.svg")
    }
  })])]), _c("GamesBlock")], 1) : _vm._e()])], 1);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./resources/frontend/images/game-top-bar.svg":
/*!****************************************************!*\
  !*** ./resources/frontend/images/game-top-bar.svg ***!
  \****************************************************/
/***/ ((module) => {

module.exports = "/images/game-top-bar.svg?f7b660d1845dfd2a3aecd6a6772641fa";

/***/ }),

/***/ "./resources/frontend/images/game.png":
/*!********************************************!*\
  !*** ./resources/frontend/images/game.png ***!
  \********************************************/
/***/ ((module) => {

module.exports = "/images/game.png?16b66482fe87943a8de2a1c40c759c71";

/***/ }),

/***/ "./resources/frontend/images/logotype-small.svg":
/*!******************************************************!*\
  !*** ./resources/frontend/images/logotype-small.svg ***!
  \******************************************************/
/***/ ((module) => {

module.exports = "/images/logotype-small.svg?7d9e129b2db829882cc059e69386d76c";

/***/ }),

/***/ "./resources/frontend/images/star.svg":
/*!********************************************!*\
  !*** ./resources/frontend/images/star.svg ***!
  \********************************************/
/***/ ((module) => {

module.exports = "/images/star.svg?09607531fc889e7ae288c8c7dcef62d4";

/***/ }),

/***/ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss&":
/*!**********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss& ***!
  \**********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
___CSS_LOADER_EXPORT___.push([module.id, ".range__slider_wrap {\n  position: relative;\n}\n.range-slider {\n  padding: 0;\n}\n.range-slider-knob:before {\n  content: \"\";\n  position: absolute;\n  left: 50%;\n  top: 50%;\n  transform: translate(-50%, -50%);\n  width: 16px;\n  height: 16px;\n  background: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ") no-repeat center center/contain;\n}\n.picker.win::before {\n  background: #43c175;\n}\n.picker.lose::before {\n  background: #c90e0e;\n}\n.picker {\n  width: 16px;\n  height: 16px;\n  position: absolute;\n  top: 4px;\n  left: 100%;\n  transition: 0.15s ease-in;\n  transform: translateX(-8px);\n  border-radius: 100%;\n  border: 3px solid white;\n}\n.picker::before {\n  content: \"\";\n  width: 10px;\n  height: 10px;\n  position: absolute;\n  top: 50%;\n  left: 50%;\n  transform: translate(-50%, -50%);\n  border-radius: 100%;\n  z-index: 2;\n}\n.picker::after {\n  content: \"\";\n  width: 6px;\n  height: 6px;\n  position: absolute;\n  bottom: -4px;\n  left: 50%;\n  transform: translateX(-50%) rotate(45deg);\n  background: white;\n  z-index: 1;\n}", ""]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss&":
/*!**************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss& ***!
  \**************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Dice_vue_vue_type_style_index_0_id_1f1c662a_lang_scss___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss& */ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss&");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Dice_vue_vue_type_style_index_0_id_1f1c662a_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Dice_vue_vue_type_style_index_0_id_1f1c662a_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./resources/frontend/views/games/Dice.vue":
/*!*************************************************!*\
  !*** ./resources/frontend/views/games/Dice.vue ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Dice_vue_vue_type_template_id_1f1c662a_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Dice.vue?vue&type=template&id=1f1c662a&lang=pug& */ "./resources/frontend/views/games/Dice.vue?vue&type=template&id=1f1c662a&lang=pug&");
/* harmony import */ var _Dice_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Dice.vue?vue&type=script&lang=js& */ "./resources/frontend/views/games/Dice.vue?vue&type=script&lang=js&");
/* harmony import */ var _Dice_vue_vue_type_style_index_0_id_1f1c662a_lang_scss___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss& */ "./resources/frontend/views/games/Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");



;


/* normalize component */

var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__["default"])(
  _Dice_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Dice_vue_vue_type_template_id_1f1c662a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Dice_vue_vue_type_template_id_1f1c662a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/views/games/Dice.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/views/games/Dice.vue?vue&type=script&lang=js&":
/*!**************************************************************************!*\
  !*** ./resources/frontend/views/games/Dice.vue?vue&type=script&lang=js& ***!
  \**************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Dice_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Dice.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Dice_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/views/games/Dice.vue?vue&type=template&id=1f1c662a&lang=pug&":
/*!*****************************************************************************************!*\
  !*** ./resources/frontend/views/games/Dice.vue?vue&type=template&id=1f1c662a&lang=pug& ***!
  \*****************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Dice_vue_vue_type_template_id_1f1c662a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Dice_vue_vue_type_template_id_1f1c662a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Dice_vue_vue_type_template_id_1f1c662a_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../../node_modules/pug-plain-loader/index.js!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Dice.vue?vue&type=template&id=1f1c662a&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=template&id=1f1c662a&lang=pug&");


/***/ }),

/***/ "./resources/frontend/views/games/Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss&":
/*!***********************************************************************************************!*\
  !*** ./resources/frontend/views/games/Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss& ***!
  \***********************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _node_modules_style_loader_dist_cjs_js_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Dice_vue_vue_type_style_index_0_id_1f1c662a_lang_scss___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/style-loader/dist/cjs.js!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss& */ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Dice.vue?vue&type=style&index=0&id=1f1c662a&lang=scss&");


/***/ })

}]);