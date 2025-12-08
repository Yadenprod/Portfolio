(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_views_games_Wheel_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=script&lang=js&":
/*!*******************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=script&lang=js& ***!
  \*******************************************************************************************************************************************************************************************************/
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
      wheelTimer: '00:20',
      preloader: true,
      sliderValue: 50,
      betSum: 1,
      minBetSum: 1,
      maxBetSum: 100000,
      rotate: 0,
      history: [],
      bets: [{
        id: 0,
        x: 2,
        color: 'black',
        users: []
      }, {
        id: 1,
        x: 3,
        color: 'green',
        users: []
      }, {
        id: 2,
        x: 5,
        color: 'orange',
        users: []
      }, {
        id: 3,
        x: 10,
        color: 'red',
        users: []
      }, {
        id: 4,
        x: 20,
        color: 'pink',
        users: []
      }, {
        id: 5,
        x: 100,
        color: 'violet',
        users: []
      }]
    };
  },
  components: {
    Table: function Table() {
      return __webpack_require__.e(/*! import() */ "resources_frontend_components_ui_Table_vue").then(__webpack_require__.bind(__webpack_require__, /*! @/components/ui/Table.vue */ "./resources/frontend/components/ui/Table.vue"));
    },
    Bets: function Bets() {
      return __webpack_require__.e(/*! import() */ "resources_frontend_components_pages_games_wheel_Bets_vue").then(__webpack_require__.bind(__webpack_require__, /*! @/components/pages/games/wheel/Bets.vue */ "./resources/frontend/components/pages/games/wheel/Bets.vue"));
    },
    GamesBlock: function GamesBlock() {
      return __webpack_require__.e(/*! import() */ "resources_frontend_components_layouts_Elements_GamesBlock_vue").then(__webpack_require__.bind(__webpack_require__, /*! @/components/layouts/Elements/GamesBlock.vue */ "./resources/frontend/components/layouts/Elements/GamesBlock.vue"));
    },
    Stats: function Stats() {
      return __webpack_require__.e(/*! import() */ "resources_frontend_components_layouts_Elements_Stats_vue").then(__webpack_require__.bind(__webpack_require__, /*! @/components/layouts/Elements/Stats.vue */ "./resources/frontend/components/layouts/Elements/Stats.vue"));
    }
  },
  mounted: function mounted() {
    this.init();
    this.$socket.emit('getWheelState');
  },
  methods: {
    init: function init() {
      var _this = this;
      this.$root.axios.post('/wheel/init').then(function (response) {
        var data = response.data;
        _this.bets.forEach(function (el, key) {
          _this.bets[key].users = [];
        });
        data.bets.map(function (bet) {
          var _this$bets$find = _this.bets.find(function (el) {
              return el.color == bet.color;
            }),
            id = _this$bets$find.id;
          _this.bets[id].users.push({
            username: bet.username,
            bet: bet.sum
          });
        });
        data.history.forEach(function (item) {
          _this.history.push(_this.getXByColor(item.winner_color));
        });
        _this.preloader = false;
      });
    },
    updateBalance: function updateBalance() {
      var _this2 = this;
      this.$root.axios.post('/user/updateBalance').then(function (response) {
        var data = response.data;
        if (!data.balance) return;
        _this2.$root.user.balance = data.balance;
      });
    },
    maxBet: function maxBet() {
      var _this$$root, _this$$root$user;
      this.betSum = ((_this$$root = this.$root) === null || _this$$root === void 0 ? void 0 : (_this$$root$user = _this$$root.user) === null || _this$$root$user === void 0 ? void 0 : _this$$root$user.balance) || 0;
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
      if (this.betSum <= 1) {
        return false;
      }
      this.betSum = (this.betSum / 2).toFixed();
    },
    onInputSumm: function onInputSumm(_ref) {
      var target = _ref.target;
      var val = target.value;
    },
    play: function play(color) {
      var _this3 = this;
      this.$root.axios.post('/wheel/bet', {
        amount: this.betSum,
        color: color
      }).then(function (response) {
        var data = response.data;
        if (data.error) {
          return _this3.$toastr.Add({
            name: 'BetWheelToast',
            title: 'Ошибка',
            msg: data.message,
            type: 'error',
            defaultClassNames: ["animated", "zoomInUp"],
            timeout: 3000,
            progressbar: true
          });
        }
        _this3.$root.user.balance = data.balance;
      });
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
    },
    getXByColor: function getXByColor(color) {
      var X = {
        black: 2,
        green: 3,
        orange: 5,
        red: 10,
        pink: 20,
        violet: 100
      };
      return {
        id: this.history.length + 1,
        x: X[color]
      };
    }
  },
  sockets: {
    wheelTimer: function wheelTimer(data) {
      var sec = data.seconds >= 10 ? data.seconds : "0".concat(data.seconds);
      var timer = "00:".concat(sec);
      this.wheelTimer = timer;
    },
    wheelBets: function wheelBets(data) {
      var _this4 = this;
      this.bets.forEach(function (el, key) {
        _this4.bets[key].users = [];
      });
      data.bets.map(function (bet) {
        var _this4$bets$find = _this4.bets.find(function (el) {
            return el.color == bet.color;
          }),
          id = _this4$bets$find.id;
        _this4.bets[id].users.push({
          username: bet.username,
          bet: bet.sum
        });
      });
    },
    wheelHistory: function wheelHistory(data) {
      var _this5 = this;
      this.updateBalance();
      this.bets.forEach(function (el, key) {
        _this5.bets[key].users = [];
      });
      if (this.history.length >= 20) {
        this.history.pop();
      }
      this.history.unshift(this.getXByColor(data.color));
    },
    wheelSpin: function wheelSpin(data) {
      this.wheelTimer = '00:20';
      var deg = data.position;
      this.rotate += deg + 360 * 6 - this.rotate % 360;
      this.$refs['wheel'].style.transition = "all ".concat(data.timer, "s cubic-bezier(0, 0.49, 0, 1) -7ms");
      this.$refs['wheel'].style.transform = "rotate(".concat(this.rotate, "deg)");
    }
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=template&id=241053c7&lang=pug&":
/*!********************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=template&id=241053c7&lang=pug& ***!
  \********************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
  }, [_c("div", {
    staticClass: "flex flex-col space-y-[50px] lg:space-y-[30px]",
    "class": [_vm.preloader ? "invisible" : ""]
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
  }, [_vm._v("Wheel")])]), _c("img", {
    attrs: {
      src: __webpack_require__(/*! @/images/game.png */ "./resources/frontend/images/game.png")
    }
  })])]), _c("div", {
    staticClass: "relative w-full flex flex-col min-h-[50px] overflow-hidden rounded-xl"
  }, [_c("div", {
    staticClass: "w-full flex-col mt-[50px] space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex items-center justify-between"
  }, [_c("div", {
    staticClass: "flex md:flex-col md:space-y-[30px] sm:!space-y-[20px] w-full items-center justify-between"
  }, [_c("div", {
    staticClass: "w-[calc(100%_-_300px)] md:w-full flex flex-col space-y-5 relative"
  }, [_c("div", {
    staticClass: "h-[344px] relative"
  }, [_c("div", {
    staticClass: "absolute flex left-1/2 -translate-x-1/2 -translate-y-[65%] top-0 w-[772px] h-[772px]"
  }, [_c("div", {
    staticClass: "absolute flex items-end justify-center left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[85%] h-[85%] rounded-full overflow-hidden pointer-events-none"
  }, [_c("div", {
    staticClass: "absolute left-0 top-0 w-full h-full flex items-end justify-center pb-[20%] md:pb-[15%]"
  }, [_c("div", {
    staticClass: "flex flex-col items-center space-y-2"
  }, [_c("span", {
    staticClass: "text-grayLight text-sm font-semibold"
  }, [_vm._v("До начала игры")]), _c("b", {
    staticClass: "text-violet text-3xl font-['Rubik'] !font-semibold"
  }, [_vm._v(_vm._s(_vm.wheelTimer))])])])]), _c("img", {
    ref: "wheel",
    staticClass: "wheel-preview absolute left-0 top-0 w-full h-full object-cover",
    attrs: {
      src: __webpack_require__(/*! @/images/games/wheel/wheel1.png */ "./resources/frontend/images/games/wheel/wheel1.png")
    }
  }), _c("img", {
    staticClass: "absolute left-1/2 -translate-x-1/2 -bottom-[50px]",
    attrs: {
      src: __webpack_require__(/*! @/images/games/wheel/cursor.svg */ "./resources/frontend/images/games/wheel/cursor.svg")
    }
  })])]), _c("div", {
    staticClass: "relative w-full overflow-hidden before:absolute before:right-0 before:h-full before:top-0 before:w-[150px] before:bg-gradient-to-r before:to-[#202024] before:from-transparent before:z-[1]"
  }, [_c("div", {
    staticClass: "flex items-center space-x-3"
  }, _vm._l(_vm.history, function (item, key) {
    return _c("div", {
      key: key,
      staticClass: "[&.x2]:!text-[#bec5da] [&.x3]:!text-[#44c276] [&.x5]:!text-[#f08929] [&.x10]:!text-[#f24841] [&.x20]:!text-[#d92c9f] [&.x100]:!text-[#7c75d9] min-w-[44px] min-h-[44px] bg-[#2c2c31] flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs select-none",
      "class": item.x === 2 ? "x2" :  false || item.x === 3 ? "x3" :  false || item.x === 5 ? "x5" :  false || item.x === 10 ? "x10" :  false || item.x === 20 ? "x20" :  false || item.x === 100 ? "x100" : ""
    }, [_vm._v(_vm._s("x" + item.x))]);
  }), 0)])]), _c("div", {
    staticClass: "w-[220px] md:w-full flex flex-col shrink-0 space-y-6"
  }, [_c("img", {
    staticClass: "max-h-[48px] md:hidden",
    attrs: {
      src: __webpack_require__(/*! @/images/logotype.svg */ "./resources/frontend/images/logotype.svg")
    }
  }), _c("div", {
    staticClass: "w-full flex flex-col items-center space-y-[30px] md:hidden"
  }, [_c("p", {
    staticClass: "uppercase text-grayLight text-sm font-medium text-center sm:text-xs"
  }, [_vm._v("Забери самый "), _c("br"), _vm._v(" крупный джекпот")]), _c("img", {
    staticClass: "max-w-[75px]",
    attrs: {
      src: __webpack_require__(/*! @/images/logotype-small.svg */ "./resources/frontend/images/logotype-small.svg")
    }
  })]), _c("div", {
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
  })])])]), _c("Bets", {
    attrs: {
      list: _vm.bets
    },
    on: {
      play: _vm.play
    }
  })], 1), _c("img", {
    staticClass: "absolute top-0 left-1/2 -translate-x-1/2 max-w-fit",
    attrs: {
      src: __webpack_require__(/*! @/images/game-top-bar.svg */ "./resources/frontend/images/game-top-bar.svg")
    }
  })])]), _c("GamesBlock")], 1)])], 1);
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

/***/ "./resources/frontend/images/games/wheel/cursor.svg":
/*!**********************************************************!*\
  !*** ./resources/frontend/images/games/wheel/cursor.svg ***!
  \**********************************************************/
/***/ ((module) => {

module.exports = "/images/cursor.svg?29a9f58a0f6ce7ac11230292db948da2";

/***/ }),

/***/ "./resources/frontend/images/games/wheel/wheel1.png":
/*!**********************************************************!*\
  !*** ./resources/frontend/images/games/wheel/wheel1.png ***!
  \**********************************************************/
/***/ ((module) => {

module.exports = "/images/wheel1.png?410fceacc7f2422f7f08a75a15450966";

/***/ }),

/***/ "./resources/frontend/images/logotype-small.svg":
/*!******************************************************!*\
  !*** ./resources/frontend/images/logotype-small.svg ***!
  \******************************************************/
/***/ ((module) => {

module.exports = "/images/logotype-small.svg?7d9e129b2db829882cc059e69386d76c";

/***/ }),

/***/ "./resources/frontend/images/logotype.svg":
/*!************************************************!*\
  !*** ./resources/frontend/images/logotype.svg ***!
  \************************************************/
/***/ ((module) => {

module.exports = "/images/logotype.svg?ecdf3464793a87c722d99d408488659f";

/***/ }),

/***/ "./resources/frontend/images/star.svg":
/*!********************************************!*\
  !*** ./resources/frontend/images/star.svg ***!
  \********************************************/
/***/ ((module) => {

module.exports = "/images/star.svg?09607531fc889e7ae288c8c7dcef62d4";

/***/ }),

/***/ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss&":
/*!***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss& ***!
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
___CSS_LOADER_EXPORT___.push([module.id, ".range-slider-knob:before {\n  content: \"\";\n  position: absolute;\n  left: 50%;\n  top: 50%;\n  transform: translate(-50%, -50%);\n  width: 16px;\n  height: 16px;\n  background: url(" + ___CSS_LOADER_URL_REPLACEMENT_0___ + ") no-repeat center center/contain;\n}", ""]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss&":
/*!***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss& ***!
  \***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Wheel_vue_vue_type_style_index_0_id_241053c7_lang_scss___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss& */ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss&");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Wheel_vue_vue_type_style_index_0_id_241053c7_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Wheel_vue_vue_type_style_index_0_id_241053c7_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./resources/frontend/views/games/Wheel.vue":
/*!**************************************************!*\
  !*** ./resources/frontend/views/games/Wheel.vue ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Wheel_vue_vue_type_template_id_241053c7_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Wheel.vue?vue&type=template&id=241053c7&lang=pug& */ "./resources/frontend/views/games/Wheel.vue?vue&type=template&id=241053c7&lang=pug&");
/* harmony import */ var _Wheel_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Wheel.vue?vue&type=script&lang=js& */ "./resources/frontend/views/games/Wheel.vue?vue&type=script&lang=js&");
/* harmony import */ var _Wheel_vue_vue_type_style_index_0_id_241053c7_lang_scss___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss& */ "./resources/frontend/views/games/Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");



;


/* normalize component */

var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__["default"])(
  _Wheel_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Wheel_vue_vue_type_template_id_241053c7_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Wheel_vue_vue_type_template_id_241053c7_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/views/games/Wheel.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/views/games/Wheel.vue?vue&type=script&lang=js&":
/*!***************************************************************************!*\
  !*** ./resources/frontend/views/games/Wheel.vue?vue&type=script&lang=js& ***!
  \***************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Wheel_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Wheel.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Wheel_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/views/games/Wheel.vue?vue&type=template&id=241053c7&lang=pug&":
/*!******************************************************************************************!*\
  !*** ./resources/frontend/views/games/Wheel.vue?vue&type=template&id=241053c7&lang=pug& ***!
  \******************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Wheel_vue_vue_type_template_id_241053c7_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Wheel_vue_vue_type_template_id_241053c7_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Wheel_vue_vue_type_template_id_241053c7_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../../node_modules/pug-plain-loader/index.js!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Wheel.vue?vue&type=template&id=241053c7&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=template&id=241053c7&lang=pug&");


/***/ }),

/***/ "./resources/frontend/views/games/Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss&":
/*!************************************************************************************************!*\
  !*** ./resources/frontend/views/games/Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss& ***!
  \************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _node_modules_style_loader_dist_cjs_js_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Wheel_vue_vue_type_style_index_0_id_241053c7_lang_scss___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/style-loader/dist/cjs.js!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss& */ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Wheel.vue?vue&type=style&index=0&id=241053c7&lang=scss&");


/***/ })

}]);