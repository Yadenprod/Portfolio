(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_views_games_Mines_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=script&lang=js&":
/*!*******************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=script&lang=js& ***!
  \*******************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var vue_range_slider_dist_vue_range_slider_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vue-range-slider/dist/vue-range-slider.css */ "./node_modules/vue-range-slider/dist/vue-range-slider.css");
/* harmony import */ var swiper_vue2__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! swiper-vue2 */ "./node_modules/swiper-vue2/dist/swiper-vue2.umd.min.js");
/* harmony import */ var swiper_vue2__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(swiper_vue2__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var swiper_swiper_bundle_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! swiper/swiper-bundle.css */ "./node_modules/swiper/swiper-bundle.css");
/* harmony import */ var _utils_getEmptyArr__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @/utils/getEmptyArr */ "./resources/frontend/utils/getEmptyArr.js");
function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }
function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }
function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }
function _defineProperty(obj, key, value) { key = _toPropertyKey(key); if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
function _toPropertyKey(arg) { var key = _toPrimitive(arg, "string"); return _typeof(key) === "symbol" ? key : String(key); }
function _toPrimitive(input, hint) { if (_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }




/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  name: 'Mines',
  data: function data() {
    return {
      preloader: true,
      sliderValue: 50,
      betSum: 1,
      maxBetSum: 10000,
      minBetSum: 1,
      bomb: 3,
      mines: [],
      chances: [],
      game: {
        isStart: false,
        win: 0
      },
      opened: [],
      controlledSwiper: null,
      coefs: [[], [1.09, 1.19, 1.3, 1.43, 1.58, 1.75, 1.96, 2.21, 2.5, 2.86, 3.3, 3.85, 4.55, 5.45, 6.67, 8.33, 10.71, 14.29, 20, 30, 50, 100, 300], [1.14, 1.3, 1.49, 1.73, 2.02, 2.37, 2.82, 3.38, 4.11, 5.05, 6.32, 8.04, 10.45, 13.94, 19.17, 27.38, 41.07, 65.71, 115, 230, 575, 2300], [1.19, 1.43, 1.73, 2.11, 2.61, 3.26, 4.13, 5.32, 6.95, 9.27, 12.64, 17.69, 25.56, 38.33, 60.24, 100.4, 180.71, 361.43, 843.33, 2530, 12650], [1.25, 1.58, 2.02, 2.61, 3.43, 4.57, 6.2, 8.59, 12.16, 17.69, 26.54, 41.28, 67.08, 115, 210.83, 421.67, 948.75, 2530, 8855, 53130], [1.32, 1.75, 2.37, 3.26, 4.57, 6.53, 9.54, 14.31, 22.12, 35.38, 58.97, 103.21, 191.67, 383.33, 843.33, 2108.33], [1.39, 1.96, 2.82, 4.13, 6.2, 9.54, 15.1, 24.72, 42.02, 74.7, 140.06, 280.13, 606.94, 1456.67, 4005.83, 13352.78], [1.47, 2.21, 3.38, 5.32, 8.59, 14.31, 24.72, 44.49, 84.04, 168.08, 360.16, 840.38, 2185, 6555, 24035, 120175, 1081575], [1.56, 2.5, 4.11, 6.95, 12.16, 22.12, 42.02, 84.04, 178.58, 408.19, 1020.47, 2857.31, 9286.25, 37145, 204297.5, 2042975], [1.67, 2.86, 5.05, 9.27, 17.69, 35.38, 74.7, 168.08, 408.19, 1088.5, 3265.49, 11429.23, 49526.67, 297160, 3268760], [1.79, 3.3, 6.32, 12.64, 26.54, 58.97, 140.06, 360.16, 1020.47, 3265.49, 12245.6, 57146.15, 371450, 4457400], [1.92, 3.85, 8.04, 17.69, 41.28, 103.21, 280.13, 840.38, 2857.31, 11429.23, 57146.15, 400023.08, 5200300], [2.08, 4.55, 10.45, 25.56, 67.08, 191.67, 606.94, 2185, 9286.25, 49526.67, 371450, 5200300], [2.27, 5.45, 13.94, 38.33, 115, 383.33, 1456.67, 6555, 37145, 297160, 4457400], [2.5, 6.67, 19.17, 60.24, 210.83, 843.33, 4005.83, 24035, 204297.5, 3268760], [2.78, 8.33, 27.38, 100.4, 421.67, 2108.33, 13352.78, 120175, 2042975], [3.13, 10.71, 41.07, 180.71, 948.75, 6325, 60087.5, 1081575], [3.57, 14.29, 65.71, 361.43, 2530, 25300, 480700], [4.17, 20, 115, 843.33, 8855, 177100], [5, 30, 230, 2530, 53130], [6.25, 50, 575, 12650], [8.33, 100, 2300], [12.5, 300], [25]]
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
    },
    Swiper: swiper_vue2__WEBPACK_IMPORTED_MODULE_1__.Swiper,
    SwiperSlide: swiper_vue2__WEBPACK_IMPORTED_MODULE_1__.SwiperSlide
  },
  mounted: function mounted() {
    this.mines = (0,_utils_getEmptyArr__WEBPACK_IMPORTED_MODULE_3__.getEmptyArr)(25, {
      status: false
    });
    this.init();
  },
  methods: {
    init: function init() {
      var _this = this;
      this.$root.axios.post('/mines/init').then(function (response) {
        var data = response.data;
        _this.preloader = false;
        if (typeof data.click !== 'undefined') {
          _this.game.isStart = true;
          _this.betSum = data.amount;
          _this.bomb = data.bombs;
          _this.opened = data.click;
          _this.game.win = data.total;
          _this.mines = _this.mines.map(function (item, index) {
            return data.click.indexOf(index + 1) !== -1 ? _objectSpread(_objectSpread({}, item), {}, {
              status: 'won'
            }) : item;
          });
        }
      });
    },
    startGame: function startGame() {
      var _this2 = this;
      this.$root.axios.post('/mines/start', {
        amount: this.betSum,
        bombs: this.bomb
      }).then(function (response) {
        var data = response.data;
        if (data.error) {
          return _this2.$toastr.Add({
            name: 'BetMinesToast',
            title: 'Ошибка',
            msg: data.message,
            type: 'error',
            timeout: 3000,
            progressbar: true
          });
        }
        _this2.mines = (0,_utils_getEmptyArr__WEBPACK_IMPORTED_MODULE_3__.getEmptyArr)(25, {
          status: false
        });
        _this2.opened = [];
        _this2.$root.user.balance = data.balance;
        _this2.game.isStart = true;
        _this2.game.win = 0;
        _this2.$toastr.Add({
          name: 'BetMinesToast',
          title: 'Успешно',
          msg: data.message,
          type: 'success',
          timeout: 3000,
          progressbar: true
        });
      });
    },
    openMine: function openMine(index) {
      var _this3 = this;
      this.$root.axios.post('/mines/open', {
        path: index
      }).then(function (response) {
        var data = response.data;
        if (data.error) {
          return _this3.$toastr.Add({
            name: 'BetMinesToast',
            title: 'Ошибка',
            msg: data.message,
            type: 'error',
            timeout: 3000,
            progressbar: true
          });
        }
        _this3.opened.push(index);
        if (data["continue"]) {
          // win - continue
          _this3.game.win = data.total;
          _this3.mines = _this3.mines.map(function (item) {
            return item.id === index - 1 ? _objectSpread(_objectSpread({}, item), {}, {
              status: 'won'
            }) : item;
          });
        } else {
          _this3.game.isStart = false;
          _this3.mines = _this3.mines.map(function (item, index) {
            return data.bombs.indexOf(index + 1) !== -1 ? _objectSpread(_objectSpread({}, item), {}, {
              status: 'lose'
            }) : _objectSpread(_objectSpread({}, item), {}, {
              status: 'won'
            });
          });
        }
        if (data.instwin) {
          _this3.game.isStart = false;
          _this3.mines = (0,_utils_getEmptyArr__WEBPACK_IMPORTED_MODULE_3__.getEmptyArr)(25, {
            status: false
          });
          _this3.opened = [];
          _this3.$root.user.balance = data.instwin.balance;
        }
      });
    },
    catchMines: function catchMines() {
      var _this4 = this;
      this.$root.axios.post('/mines/take').then(function (response) {
        var data = response.data;
        if (data.error) {
          return _this4.$toastr.Add({
            name: 'BetMinesToast',
            title: 'Ошибка',
            msg: data.message,
            type: 'error',
            timeout: 3000,
            progressbar: true
          });
        }
        _this4.$root.user.balance = data.balance;
        _this4.game.isStart = false;
        _this4.mines = (0,_utils_getEmptyArr__WEBPACK_IMPORTED_MODULE_3__.getEmptyArr)(25, {
          status: null
        });
        _this4.opened = [];
        _this4.$toastr.Add({
          name: 'BetMinesToast',
          title: 'Успешно',
          msg: 'Вы забрали ' + data.total + ' руб.',
          type: 'success',
          timeout: 3000,
          progressbar: true
        });
      });
    },
    autoSelect: function autoSelect() {
      var noActive = document.querySelectorAll('.opacity-40:not(.!opacity-100)');
      noActive[Math.floor(Math.random() * noActive.length)].click();
      this.autoBtn.isLoading = true;
    },
    preventDefault: function preventDefault(e) {
      e.preventDefault();
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
    },
    onSwiper: function onSwiper(swiper) {
      this.controlledSwiper = swiper;
    }
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=template&id=c4803728&lang=pug&":
/*!********************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=template&id=c4803728&lang=pug& ***!
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
  }, [_vm._v("Mines")])]), _c("img", {
    attrs: {
      src: __webpack_require__(/*! @/images/game.png */ "./resources/frontend/images/game.png")
    }
  })])]), _c("div", {
    staticClass: "relative w-full min-h-[50px] overflow-hidden rounded-xl"
  }, [_c("div", {
    staticClass: "w-full mt-[50px] space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex flex-col items-center justify-between"
  }, [_c("div", {
    staticClass: "w-full flex md:flex-col items-center justify-between"
  }, [_c("div", {
    staticClass: "w-[calc(100%_-_280px)] md:w-full flex md:flex-col items-stretch md:items-center justify-between md:justify-center"
  }, [_c("div", {
    staticClass: "flex items-center justify-center 2xl:hidden"
  }, [_c("img", {
    attrs: {
      src: __webpack_require__(/*! @/images/games/mines/bg.png */ "./resources/frontend/images/games/mines/bg.png")
    }
  })]), _c("div", {
    staticClass: "flex items-center flex-col md:order-[1] md:flex-row justify-between py-6 gap-6"
  }, [_c("div", {
    staticClass: "flex flex-col items-center text-grayLight font-['Rubik'] font-medium space-y-4"
  }, [_c("div", {
    staticClass: "w-[64px] h-[64px] sm:w-[48px] sm:h-[48px] sm:rounded-xl flex items-center justify-center rounded-2xl bg-violet"
  }, [_c("img", {
    staticClass: "max-w-[32px] sm:max-w-[22px]",
    attrs: {
      src: __webpack_require__(/*! @/images/logotype-small.svg */ "./resources/frontend/images/logotype-small.svg")
    }
  })]), _c("span", [_vm._v(_vm._s(25 - _vm.bomb))])]), _c("div", {
    staticClass: "flex flex-col items-center text-grayLight font-['Rubik'] font-medium space-y-4"
  }, [_c("div", {
    staticClass: "w-[64px] h-[64px] sm:w-[48px] sm:h-[48px] sm:rounded-xl text-[#d5daea] flex items-center justify-center rounded-2xl bg-red"
  }, [_c("svg", {
    staticClass: "w-[32px] h-[32px] sm:w-[22px] sm:h-[22px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#mines"
    }
  })])]), _c("span", [_vm._v(_vm._s(_vm.bomb))])])]), _c("div", {
    staticClass: "grid gap-[calc(64px_*_0.125)] grid-cols-[repeat(5,_64px)] grid-rows-[repeat(5,_64px)] sm:grid-cols-[repeat(5,_48px)] sm:grid-rows-[repeat(5,_48px)]"
  }, _vm._l(_vm.mines, function (item, key) {
    return _c("div", {
      key: item.id,
      staticClass: "overflow-hidden relative bg-[#2c2c31] flex items-center justify-center rounded-xl cursor-pointer transition-all duration-200",
      "class": ["opacity-40", {
        "!opacity-100 pointer-events-none": _vm.opened.indexOf(key + 1) !== -1
      }, {
        "hover:scale-105": item.status === null
      }, {
        "pointer-events-none": !_vm.game.isStart
      }],
      on: {
        click: function click($event) {
          return _vm.openMine(key + 1);
        }
      }
    }, [item.status === "won" ? _c("div", {
      staticClass: "w-full h-full flex items-center justify-center bg-violet"
    }, [_c("img", {
      staticClass: "max-w-[32px] sm:max-w-[22px]",
      attrs: {
        src: __webpack_require__(/*! @/images/logotype-small.svg */ "./resources/frontend/images/logotype-small.svg")
      }
    })]) : _vm._e(), item.status === "lose" ? _c("div", {
      staticClass: "text-[#d5daea] w-full h-full flex items-center justify-center bg-red"
    }, [_c("svg", {
      staticClass: "w-[32px] h-[32px] sm:w-[22px] sm:h-[22px]"
    }, [_c("use", {
      attrs: {
        "xlink:href": "images/symbols.svg#mines"
      }
    })])]) : _vm._e()]);
  }), 0)]), _c("form", {
    staticClass: "w-[220px] md:w-full flex flex-col shrink-0 space-y-6",
    on: {
      submit: function submit($event) {
        $event.preventDefault();
        return _vm.preventDefault.apply(null, arguments);
      }
    }
  }, [_c("div", {
    staticClass: "flex flex-col space-y-4"
  }, [_c("b", {
    staticClass: "text-grayLight !font-semibold text-sm"
  }, [_vm._v("Количество бомб:")]), _c("div", {
    staticClass: "flex flex-col"
  }, [_c("div", {
    staticClass: "flex items-center justify-between md:justify-start md:space-x-3"
  }, [_c("a", {
    staticClass: "w-[44px] h-[44px] bg-[#2c2c31] border-2 border-transparent flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]",
    "class": _vm.bomb === 3 ? "!border-violet text-violet hover:bg-[#2c2c31]" : "",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: function click($event) {
        _vm.bomb = 3;
      }
    }
  }, [_vm._v("3 ")]), _c("a", {
    staticClass: "w-[44px] h-[44px] bg-[#2c2c31] border-2 border-transparent flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]",
    "class": _vm.bomb === 5 ? "!border-violet text-violet hover:bg-[#2c2c31]" : "",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: function click($event) {
        _vm.bomb = 5;
      }
    }
  }, [_vm._v("5 ")]), _c("a", {
    staticClass: "w-[44px] h-[44px] bg-[#2c2c31] border-2 border-transparent flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]",
    "class": _vm.bomb === 10 ? "!border-violet text-violet hover:bg-[#2c2c31]" : "",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: function click($event) {
        _vm.bomb = 10;
      }
    }
  }, [_vm._v("10 ")]), _c("a", {
    staticClass: "w-[44px] h-[44px] bg-[#2c2c31] border-2 border-transparent flex items-center justify-center rounded-xl font-['Rubik'] font-medium text-xs transition-all duration-200 hover:bg-[#3A3A40]",
    "class": _vm.bomb === 24 ? "!border-violet text-violet hover:bg-[#2c2c31]" : "",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: function click($event) {
        _vm.bomb = 24;
      }
    }
  }, [_vm._v("24")])])])]), _c("div", {
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
  }, [!_vm.game.isStart ? _c("button", {
    staticClass: "font-['Rubik'] whitespace-nowrap focus:ring-0 focus:ring-inherit focus:outline-0 focus:border-0 flex transition-all duration-200 items-center justify-center rounded-xl text-sm uppercase font-medium h-[52px] px-6 shadow-[0px_4px_35px_rgba(0,0,0,0.1)] hover:bg-violetHover bg-violet",
    on: {
      click: _vm.startGame
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px] text-current mr-2"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#play"
    }
  })]), _vm._v("Играть         ")]) : _vm._e(), _vm.game.isStart ? _c("button", {
    staticClass: "hidden font-['Rubik'] whitespace-nowrap focus:ring-0 focus:ring-inherit focus:outline-0 focus:border-0 flex transition-all duration-200 items-center justify-center rounded-xl text-sm uppercase font-medium h-[52px] px-6 shadow-[0px_4px_35px_rgba(0,0,0,0.1)] hover:bg-grayHover bg-gray",
    on: {
      click: _vm.autoSelect
    }
  }, [_vm._v(" Автовыбор")]) : _vm._e(), _vm.game.isStart ? _c("button", {
    staticClass: "font-['Rubik'] whitespace-nowrap focus:ring-0 focus:ring-inherit focus:outline-0 focus:border-0 flex transition-all duration-200 items-center justify-center rounded-xl text-sm uppercase font-medium h-[52px] px-6 shadow-[0px_4px_35px_rgba(0,0,0,0.1)] hover:bg-violetHover bg-violet",
    on: {
      click: _vm.catchMines
    }
  }, [_vm._v("Забрать " + _vm._s(parseFloat(_vm.game.win).toFixed(2)))]) : _vm._e()])])])]), _c("div", {
    staticClass: "w-full relative flex items-center justify-between gap-5"
  }, [_c("a", {
    staticClass: "shrink-0 flex items-center justify-center text-violet w-[32px] h-[32px] rounded-lg bg-[#2c2c31] transition-all duration-200 hover:bg-violet hover:text-white",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: function click($event) {
        return _vm.controlledSwiper.slidePrev();
      }
    }
  }, [_c("svg", {
    staticClass: "w-[20px] h-[20px] -rotate-[180deg]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#arrow"
    }
  })])]), _c("swiper", {
    key: _vm.bomb,
    attrs: {
      freeMode: true,
      "slides-per-view": "auto",
      spaceBetween: 16
    },
    on: {
      swiper: _vm.onSwiper
    }
  }, _vm._l(_vm.coefs[_vm.bomb - 1], function (item, id) {
    return _c("swiper-slide", {
      key: item.id,
      staticClass: "!w-auto"
    }, [_c("div", {
      staticClass: "w-[64px] h-[64px] flex flex-col justify-center items-center bg-[#2c2c31] rounded-xl"
    }, [_c("b", {
      staticClass: "text-grayLight font-['Rubik'] !font-medium text-sm"
    }, [_vm._v(_vm._s("x" + parseFloat(item).toFixed(2)))]), _c("span", {
      staticClass: "text-gray font-semibold text-sm"
    }, [_vm._v(_vm._s(id + 1 + " hit"))])])]);
  }), 1), _c("a", {
    staticClass: "shrink-0 flex items-center justify-center text-violet w-[32px] h-[32px] rounded-lg bg-[#2c2c31] transition-all duration-200 hover:bg-violet hover:text-white",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: function click($event) {
        return _vm.controlledSwiper.slideNext();
      }
    }
  }, [_c("svg", {
    staticClass: "w-[20px] h-[20px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": "images/symbols.svg#arrow"
    }
  })])])], 1)]), _c("img", {
    staticClass: "absolute top-0 left-1/2 -translate-x-1/2 max-w-fit",
    attrs: {
      src: __webpack_require__(/*! @/images/game-top-bar.svg */ "./resources/frontend/images/game-top-bar.svg")
    }
  })])]), _c("GamesBlock")], 1) : _vm._e()])], 1);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./resources/frontend/utils/getEmptyArr.js":
/*!*************************************************!*\
  !*** ./resources/frontend/utils/getEmptyArr.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getEmptyArr": () => (/* binding */ getEmptyArr)
/* harmony export */ });
function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }
function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }
function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? ownKeys(Object(source), !0).forEach(function (key) { _defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }
function _defineProperty(obj, key, value) { key = _toPropertyKey(key); if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }
function _toPropertyKey(arg) { var key = _toPrimitive(arg, "string"); return _typeof(key) === "symbol" ? key : String(key); }
function _toPrimitive(input, hint) { if (_typeof(input) !== "object" || input === null) return input; var prim = input[Symbol.toPrimitive]; if (prim !== undefined) { var res = prim.call(input, hint || "default"); if (_typeof(res) !== "object") return res; throw new TypeError("@@toPrimitive must return a primitive value."); } return (hint === "string" ? String : Number)(input); }
function getEmptyArr(length, def) {
  var arr = [];
  for (var i = 0; i < length; i++) {
    arr.push(_objectSpread(_objectSpread({}, def), {}, {
      id: i
    }));
  }
  return arr;
}

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

/***/ "./resources/frontend/images/games/mines/bg.png":
/*!******************************************************!*\
  !*** ./resources/frontend/images/games/mines/bg.png ***!
  \******************************************************/
/***/ ((module) => {

module.exports = "/images/bg.png?080f0c1ed05548d293dd3f8be4232b78";

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

/***/ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss&":
/*!***********************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss& ***!
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

/***/ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss&":
/*!***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss& ***!
  \***************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Mines_vue_vue_type_style_index_0_id_c4803728_lang_scss___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss& */ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss&");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Mines_vue_vue_type_style_index_0_id_c4803728_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Mines_vue_vue_type_style_index_0_id_c4803728_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./resources/frontend/views/games/Mines.vue":
/*!**************************************************!*\
  !*** ./resources/frontend/views/games/Mines.vue ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Mines_vue_vue_type_template_id_c4803728_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Mines.vue?vue&type=template&id=c4803728&lang=pug& */ "./resources/frontend/views/games/Mines.vue?vue&type=template&id=c4803728&lang=pug&");
/* harmony import */ var _Mines_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Mines.vue?vue&type=script&lang=js& */ "./resources/frontend/views/games/Mines.vue?vue&type=script&lang=js&");
/* harmony import */ var _Mines_vue_vue_type_style_index_0_id_c4803728_lang_scss___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss& */ "./resources/frontend/views/games/Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");



;


/* normalize component */

var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__["default"])(
  _Mines_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Mines_vue_vue_type_template_id_c4803728_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Mines_vue_vue_type_template_id_c4803728_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/views/games/Mines.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/views/games/Mines.vue?vue&type=script&lang=js&":
/*!***************************************************************************!*\
  !*** ./resources/frontend/views/games/Mines.vue?vue&type=script&lang=js& ***!
  \***************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Mines_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Mines.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Mines_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/views/games/Mines.vue?vue&type=template&id=c4803728&lang=pug&":
/*!******************************************************************************************!*\
  !*** ./resources/frontend/views/games/Mines.vue?vue&type=template&id=c4803728&lang=pug& ***!
  \******************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Mines_vue_vue_type_template_id_c4803728_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Mines_vue_vue_type_template_id_c4803728_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Mines_vue_vue_type_template_id_c4803728_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../../node_modules/pug-plain-loader/index.js!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Mines.vue?vue&type=template&id=c4803728&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=template&id=c4803728&lang=pug&");


/***/ }),

/***/ "./resources/frontend/views/games/Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss&":
/*!************************************************************************************************!*\
  !*** ./resources/frontend/views/games/Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss& ***!
  \************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _node_modules_style_loader_dist_cjs_js_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Mines_vue_vue_type_style_index_0_id_c4803728_lang_scss___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../node_modules/style-loader/dist/cjs.js!../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss& */ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/games/Mines.vue?vue&type=style&index=0&id=c4803728&lang=scss&");


/***/ })

}]);