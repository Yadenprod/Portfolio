(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_views_Bonus_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Bonus.vue?vue&type=script&lang=js&":
/*!*************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Bonus.vue?vue&type=script&lang=js& ***!
  \*************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  data: function data() {
    return {
      isLoading: false,
      preloader: true,
      list: [{
        sum: 1
      }, {
        sum: 250
      }, {
        sum: 50
      }, {
        sum: 20
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 100
      }, {
        sum: 15
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 250
      }, {
        sum: 50
      }, {
        sum: 20
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 100
      }, {
        sum: 15
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 5
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 'changeMe'
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }, {
        sum: 1
      }, {
        sum: 10
      }, {
        sum: 40
      }, {
        sum: 30
      }, {
        sum: 10
      }, {
        sum: 1
      }],
      promo: ''
    };
  },
  methods: {
    preloaderDestroy: function preloaderDestroy() {
      var _this = this;
      setTimeout(function () {
        _this.preloader = false;
      }, 300);
    },
    roll: function roll() {
      var _this2 = this;
      this.$root.axios.post('/bonus/take', {
        type: 'daily'
      }).then(function (response) {
        var data = response.data;
        if (data.error) {
          return _this2.$toastr.Add({
            name: 'PromoToast',
            title: 'Ошибка',
            msg: data.message,
            type: 'error',
            defaultClassNames: ["animated", "zoomInUp"],
            timeout: 3000,
            progressbar: true
          });
        }
        _this2.list = _this2.list.map(function (item) {
          return item.sum == 'changeMe' ? {
            sum: data.bonus
          } : item;
        });
        _this2.$refs['bonusCarousel'].style.marginLeft = '-7030px';
        setTimeout(function () {
          _this2.$toastr.Add({
            name: 'PromoToast',
            title: 'Успех',
            msg: 'Бонус получен',
            type: 'success',
            defaultClassNames: ["animated", "zoomInUp"],
            timeout: 3000,
            progressbar: true
          });
          _this2.$root.user.balance = data.balance;
        }, 10000);
      });
    },
    activate: function activate() {
      var _this3 = this;
      this.$root.axios.post('/promo/activate', {
        code: this.promo
      }).then(function (response) {
        var data = response.data;
        if (data.error) {
          return _this3.$toastr.Add({
            name: 'PromoToast',
            title: 'Ошибка',
            msg: data.message,
            type: 'error',
            defaultClassNames: ["animated", "zoomInUp"],
            timeout: 3000,
            progressbar: true
          });
        }
        _this3.$root.user.balance = data.balance;
        _this3.$toastr.Add({
          name: 'PromoToast',
          title: 'Успех',
          msg: 'Промокод активирован!',
          type: 'success',
          defaultClassNames: ["animated", "zoomInUp"],
          timeout: 3000,
          progressbar: true
        });
        _this3.promo = '';
      });
    }
  },
  mounted: function mounted() {
    this.preloaderDestroy();
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Bonus.vue?vue&type=template&id=71e115d9&lang=pug&":
/*!**************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Bonus.vue?vue&type=template&id=71e115d9&lang=pug& ***!
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
      "xlink:href": "images/symbols.svg#users"
    }
  })]), _c("span", [_vm._v("Бонусы")])])]), _c("div", {
    staticClass: "w-full flex-col rounded-xl space-y-[30px] p-[50px] md:p-[24px] bg-[#202024] relative z-[1] flex"
  }, [_c("div", {
    staticClass: "flex flex-col space-y-[30px]"
  }, [_c("span", {
    staticClass: "text-grayLight uppercase font-['Rubik'] font-medium text-sm"
  }, [_vm._v("Колесо ежедневных бонусов")]), _c("form", {
    staticClass: "flex flex-col space-y-3",
    on: {
      submit: function submit($event) {
        $event.preventDefault();
        return _vm.roll();
      }
    }
  }, [_c("div", {
    staticClass: "w-full flex flex-col items-center space-y-[30px]"
  }, [_c("img", {
    staticClass: "max-w-[75px]",
    attrs: {
      src: __webpack_require__(/*! @/images/logotype-small.svg */ "./resources/frontend/images/logotype-small.svg")
    }
  }), _c("p", {
    staticClass: "uppercase text-grayLight text-sm font-medium text-center sm:text-xs [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline"
  }, [_vm._v("Для получения бонуса, вы должны быть подписаны на нашу группу "), _c("a", {
    attrs: {
      href: "https://vk.com/TreasureCasino/",
      target: "_blank"
    }
  }, [_vm._v("vk.com/TreasureCasino")])])]), _c("div", {
    staticClass: "w-full relative h-[90px] overflow-hidden"
  }, [_c("div", {
    staticClass: "w-[2px] h-[90%] bg-violet absolute left-1/2 -translate-x-1/2 z-[1] top-1/2 -translate-y-1/2"
  }), _c("div", {
    staticClass: "w-[1920px] absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-[64px]"
  }, [_c("ul", {
    ref: "bonusCarousel",
    staticClass: "flex items-center w-fit space-x-2.5",
    staticStyle: {
      transform: "translateX(410px)",
      transition: "10s"
    }
  }, _vm._l(_vm.list, function (item) {
    return _c("li", {
      key: item.index,
      staticClass: "shrink-0 pointer-events-none flex w-[64px] h-[64px] rounded-xl bg-[#2c2c31] text-sm flex flex-col items-center justify-center space-y-0.5"
    }, [_c("b", [_vm._v(_vm._s(item.sum))]), _c("span", {
      staticClass: "text-gray"
    }, [_vm._v("мон.")])]);
  }), 0)])]), _c("div", {
    staticClass: "w-full flex justify-center"
  }, [_c("Btn", {
    attrs: {
      text: "Получить",
      type: "button",
      theme: null,
      ico: null
    }
  })], 1)])]), _c("div", {
    staticClass: "flex flex-col space-y-[20px]"
  }, [_c("span", {
    staticClass: "text-grayLight uppercase font-['Rubik'] font-medium text-sm"
  }, [_vm._v("Как это работает?")]), _c("div", {
    staticClass: "flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline"
  }, [_c("p", [_vm._v("Каждые 24 часа крутите бонусную рулетку и получайте от 1 до 100р на свой баланс")])])]), _c("div", {
    staticClass: "flex flex-col space-y-[20px]"
  }, [_c("span", {
    staticClass: "text-grayLight uppercase font-['Rubik'] font-medium text-sm"
  }, [_vm._v("Оставь отзыв и получи бонус")]), _c("div", {
    staticClass: "flex flex-col space-y-3 [&_p]:text-sm [&_p]:text-gray [&_p]:leading-[180%] [&_a]:text-violet [&_a]:underline hover:[&_a]:no-underline"
  }, [_c("p", [_vm._v('Отправьте в "Предложить новость" нашей группы '), _c("a", {
    attrs: {
      href: "https://vk.com/TreasureCasino/",
      target: "_blank"
    }
  }, [_vm._v("vk.com/TreasureCasino")]), _vm._v(" скриншот с крупным выигрышем (более 30000 монет) или большим коэффициентом (более х500) и получите бонус после публикации."), _c("br"), _vm._v(" Требования к посту:\n"), _c("br"), _vm._v(" —  Скриншот должен быть хорошего качества. Не стоит фотографировать экран компьютера, воспользуйтесь встроенными средствами для создания скриншотов. \n"), _c("br"), _vm._v(" —  На скриншоте не должно быть информации, не относящейся к сайту. \n"), _c("br"), _vm._v(" —  На скриншоте должен быть виден результат игры. Предпочтение отдается скриншотам, где результат показан непосредственно на странице режима, а не в профиле. \n"), _c("br"), _vm._v(' —  При возможности, обрежьте скриншот, удалив из него элементы, относящиеся к браузеру или операционной системе (такие как меню "Пуск", верхняя панель браузера и прочее). \n'), _c("br"), _vm._v(" —  Подпись к скриншоту не должна содержать нецензурной лексики и оскорблений. В подпись не следует включать просьбу о бонусе.")])])]), _c("div", {
    staticClass: "flex flex-col space-y-[20px]"
  }, [_c("span", {
    staticClass: "text-grayLight uppercase font-['Rubik'] font-medium text-sm"
  }, [_vm._v("Промокод")]), _c("form", {
    staticClass: "flex sm:flex-col sm:space-x-0 sm:space-y-3 sm:[&_button]:w-full items-stretch space-x-3",
    on: {
      submit: function submit($event) {
        $event.preventDefault();
        return _vm.activate();
      }
    }
  }, [_c("div", {
    staticClass: "relative"
  }, [_c("input", {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: _vm.promo,
      expression: "promo"
    }],
    staticClass: "border-0 sm:w-full sm:h-[52px] text-sm px-5 placeholder:text-gray focus:ring-0 focus:outline-0 h-full rounded-xl bg-[#1b1c20]",
    attrs: {
      type: "text",
      placeholder: "Введите промокод"
    },
    domProps: {
      value: _vm.promo
    },
    on: {
      input: function input($event) {
        if ($event.target.composing) return;
        _vm.promo = $event.target.value;
      }
    }
  })]), _c("Btn", {
    attrs: {
      text: "Активировать",
      type: "button",
      theme: null,
      ico: null
    }
  })], 1)])])])]) : _vm._e()])], 1);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./resources/frontend/images/logotype-small.svg":
/*!******************************************************!*\
  !*** ./resources/frontend/images/logotype-small.svg ***!
  \******************************************************/
/***/ ((module) => {

module.exports = "/images/logotype-small.svg?7d9e129b2db829882cc059e69386d76c";

/***/ }),

/***/ "./resources/frontend/views/Bonus.vue":
/*!********************************************!*\
  !*** ./resources/frontend/views/Bonus.vue ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Bonus_vue_vue_type_template_id_71e115d9_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Bonus.vue?vue&type=template&id=71e115d9&lang=pug& */ "./resources/frontend/views/Bonus.vue?vue&type=template&id=71e115d9&lang=pug&");
/* harmony import */ var _Bonus_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Bonus.vue?vue&type=script&lang=js& */ "./resources/frontend/views/Bonus.vue?vue&type=script&lang=js&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");





/* normalize component */
;
var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__["default"])(
  _Bonus_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Bonus_vue_vue_type_template_id_71e115d9_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Bonus_vue_vue_type_template_id_71e115d9_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/views/Bonus.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/views/Bonus.vue?vue&type=script&lang=js&":
/*!*********************************************************************!*\
  !*** ./resources/frontend/views/Bonus.vue?vue&type=script&lang=js& ***!
  \*********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Bonus_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Bonus.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Bonus.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Bonus_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/views/Bonus.vue?vue&type=template&id=71e115d9&lang=pug&":
/*!************************************************************************************!*\
  !*** ./resources/frontend/views/Bonus.vue?vue&type=template&id=71e115d9&lang=pug& ***!
  \************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Bonus_vue_vue_type_template_id_71e115d9_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Bonus_vue_vue_type_template_id_71e115d9_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Bonus_vue_vue_type_template_id_71e115d9_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../node_modules/pug-plain-loader/index.js!../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Bonus.vue?vue&type=template&id=71e115d9&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/views/Bonus.vue?vue&type=template&id=71e115d9&lang=pug&");


/***/ })

}]);