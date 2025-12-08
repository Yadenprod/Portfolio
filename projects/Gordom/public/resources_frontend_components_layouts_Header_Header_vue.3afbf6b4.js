(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_components_layouts_Header_Header_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Header/Header.vue?vue&type=script&lang=js&":
/*!**********************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Header/Header.vue?vue&type=script&lang=js& ***!
  \**********************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var vue_odometer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! vue-odometer */ "./node_modules/vue-odometer/dist/vue-odometer.js");
/* harmony import */ var vue_odometer__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(vue_odometer__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var odometer_themes_odometer_theme_default_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! odometer/themes/odometer-theme-default.css */ "./node_modules/odometer/themes/odometer-theme-default.css");


/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  name: 'HeaderMain',
  data: function data() {
    return {
      menu: [{
        id: 1,
        name: 'Бонусы',
        path: '/bonus'
      }, {
        id: 2,
        name: 'Политика конфиденциальности',
        path: '/policy'
      }, {
        id: 3,
        name: 'FAQ',
        path: '/faq'
      }, {
        id: 4,
        name: 'Контакты',
        path: '/contacts'
      }],
      menuProfileDropdown: [{
        id: 0,
        name: 'Пригласить друзей',
        ico: 'users',
        path: '/refferal'
      },
      // {
      //     id: 1,
      //     name: 'Честная игра',
      //     ico: 'fair',
      //     path: '/provably-fair'
      // },
      // {
      //     id: 2,
      //     name: 'Профиль',
      //     ico: 'user',
      //     path: ''
      // },
      {
        id: 4,
        name: 'Выйти',
        ico: 'logout',
        path: '/logout'
      }],
      menuMobile: [{
        id: 1,
        name: 'Бонусы',
        ico: 'bonus',
        path: '/bonus'
      }, {
        id: 2,
        name: 'FAQ',
        ico: 'faq',
        path: '/faq'
      }, {
        id: 3,
        name: 'Контакты',
        ico: 'contacts',
        path: '/contacts'
      }],
      isMenuOpen: false,
      preloader: true
    };
  },
  components: {
    IOdometer: (vue_odometer__WEBPACK_IMPORTED_MODULE_0___default()),
    modalPay: function modalPay() {
      return Promise.all(/*! import() */[__webpack_require__.e("/js/vendor"), __webpack_require__.e("resources_frontend_components_modals_Pay_vue")]).then(__webpack_require__.bind(__webpack_require__, /*! @/components/modals/Pay.vue */ "./resources/frontend/components/modals/Pay.vue"));
    },
    modalSettings: function modalSettings() {
      return Promise.all(/*! import() */[__webpack_require__.e("/js/vendor"), __webpack_require__.e("resources_frontend_components_modals_Settings_vue")]).then(__webpack_require__.bind(__webpack_require__, /*! @/components/modals/Settings.vue */ "./resources/frontend/components/modals/Settings.vue"));
    },
    modalLogin: function modalLogin() {
      return Promise.all(/*! import() */[__webpack_require__.e("/js/vendor"), __webpack_require__.e("resources_frontend_components_modals_Login_vue")]).then(__webpack_require__.bind(__webpack_require__, /*! @/components/modals/Login.vue */ "./resources/frontend/components/modals/Login.vue"));
    },
    modalRegister: function modalRegister() {
      return Promise.all(/*! import() */[__webpack_require__.e("/js/vendor"), __webpack_require__.e("resources_frontend_components_modals_Register_vue")]).then(__webpack_require__.bind(__webpack_require__, /*! @/components/modals/Register.vue */ "./resources/frontend/components/modals/Register.vue"));
    }
  },
  methods: {
    closeMenu: function closeMenu() {
      this.isMenuOpen = false;
    },
    preloaderDestroy: function preloaderDestroy() {
      var _this = this;
      setTimeout(function () {
        _this.preloader = false;
      }, 800);
    },
    modalPay: function modalPay() {
      this.$modal.show('pay');
    },
    showModal: function showModal(modal) {
      this.$modal.show(modal);
    },
    login: function login() {
      location.href = '/auth/vkontakte';
    }
  },
  mounted: function mounted() {
    this.preloaderDestroy();
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Header/Header.vue?vue&type=template&id=6433bb36&":
/*!*********************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Header/Header.vue?vue&type=template&id=6433bb36& ***!
  \*********************************************************************************************************************************************************************************************************************************************************************************************************/
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
  return _c("header", {
    staticClass: "flex lg:fixed lg:left-0 lg:top-0 lg:w-full lg:bg-[#1b1c20] relative items-center justify-between py-[10px] lg:px-[16px] z-[21]"
  }, [_c("router-link", {
    staticClass: "sm:w-[44px] overflow-hidden",
    attrs: {
      to: "/",
      "active-class": "",
      "exact-active-class": ""
    }
  }, [_c("img", {
    staticClass: "max-h-[44px] sm:max-w-fit",
    attrs: {
      src: __webpack_require__(/*! @/images/logotype.svg */ "./resources/frontend/images/logotype.svg")
    }
  })]), _vm._v(" "), _c("nav", {
    staticClass: "flex 2xl:hidden items-center space-x-12"
  }, _vm._l(_vm.menu, function (item) {
    return _c("li", {
      key: item.id
    }, [_c("router-link", {
      staticClass: "text-[#6a6a7a] text-sm font-semibold transition-all duration-200 hover:text-[#c1c8dc] py-2 inline-block relative font-['Manrope'] before:absolute before:-bottom-2 before:w-0 before:h-[3px] before:rounded-full before:bg-[#7c75d9] before:transition-all before:duration-200 [&.active]:before:w-[25px] [&.active]:text-white",
      attrs: {
        to: item.path,
        "active-class": "active",
        "exact-active-class": "active"
      }
    }, [_vm._v("\n                " + _vm._s(item.name) + "\n            ")])], 1);
  }), 0), _vm._v(" "), _c("div", {
    staticClass: "flex items-center"
  }, [_vm.$root.user !== null ? _c("div", {
    staticClass: "h-[48px] rounded-[12px] pl-4 pr-2 bg-[#2c2c31] flex items-center justify-between shadow-[0px_4px_28px_rgba(0,0,0,0.03)]"
  }, [_c("div", {
    staticClass: "w-[140px] sm:w-[115px] h-full flex items-center space-x-3"
  }, [_c("img", {
    staticClass: "max-w-[16px]",
    attrs: {
      src: __webpack_require__(/*! @/images/logotype-small.svg */ "./resources/frontend/images/logotype-small.svg"),
      alt: ""
    }
  }), _vm._v(" "), _c("p", {
    staticClass: "flex items-center text-sm relative"
  }, [_c("Transition", {
    attrs: {
      "enter-active-class": "transition ease-out duration-100",
      "enter-class": "transform opacity-0 scale-95",
      "enter-to-class": "transform opacity-100 scale-100",
      "leave-active-class": "transition ease-in duration-75",
      "leave-class": "transform opacity-100 scale-100",
      "leave-to-class": "transform opacity-0 scale-95"
    }
  }, [!_vm.preloader ? _c("span", {
    staticClass: "flex items-center font-['Rubik']"
  }, [_c("b", [_c("IOdometer", {
    staticClass: "iOdometer",
    attrs: {
      value: _vm.$root.user.balance
    }
  })], 1)]) : _vm._e()]), _vm._v(" "), _vm.preloader ? _c("span", {
    staticClass: "relative w-[40px] h-[6px] h-full bg-[#3A3A40] rounded-sm loader overflow-hidden before:opacity-[0.1]"
  }) : _vm._e()], 1)]), _vm._v(" "), _c("a", {
    staticClass: "flex w-[32px] h-[32px] items-center justify-center bg-[#3A3A40] rounded-lg transition-all duration-200 hover:bg-[#7C75D9] hover:!text-white",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: function click($event) {
        return _vm.modalPay();
      }
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": __webpack_require__(/*! @/images/symbols.svg */ "./resources/frontend/images/symbols.svg") + "#plus"
    }
  })])])]) : _vm._e(), _vm._v(" "), _vm.$root.user !== null ? _c("div", {
    staticClass: "relative"
  }, [_c("div", {
    directives: [{
      name: "on-clickaway",
      rawName: "v-on-clickaway",
      value: _vm.closeMenu,
      expression: "closeMenu"
    }],
    staticClass: "relative"
  }, [_c("div", [_c("span", [_c("button", {
    staticClass: "flex w-[48px] h-[48px] items-center justify-center text-[#4C4F5A] transition-all duration-200 hover:text-[#c5cbe0] focus:ring-0 focus:ring-inherit focus:outline-0",
    attrs: {
      type: "button"
    },
    on: {
      click: function click($event) {
        _vm.isMenuOpen = !_vm.isMenuOpen;
      }
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": __webpack_require__(/*! @/images/symbols.svg */ "./resources/frontend/images/symbols.svg") + "#more"
    }
  })])])])]), _vm._v(" "), _c("Transition", {
    attrs: {
      "enter-active-class": "transition ease-out duration-100",
      "enter-class": "transform opacity-0 scale-95",
      "enter-to-class": "transform opacity-100 scale-100",
      "leave-active-class": "transition ease-in duration-75",
      "leave-class": "transform opacity-100 scale-100",
      "leave-to-class": "transform opacity-0 scale-95"
    }
  }, [_vm.isMenuOpen ? _c("div", {
    staticClass: "absolute z-[1] origin-top-right right-0 mt-2 w-56 rounded-xl overflow-hidden bg-[#313136] flex flex-col shadow-[0px_4px_28px_rgba(0,0,0,0.08)]"
  }, [_c("div", {
    staticClass: "p-4 bg-[#2d2d32] flex flex-col space-y-2"
  }, [_c("img", {
    staticClass: "w-[32px] h-[32px] rounded-full",
    attrs: {
      src: _vm.$root.user.avatar,
      alt: ""
    }
  }), _vm._v(" "), _c("div", {
    staticClass: "w-full flex items-end justify-between"
  }, [_c("div", {
    staticClass: "flex shrink-0 flex-col space-y-1"
  }, [_c("b", {
    staticClass: "text-sm !font-medium max-w-[100px] whitespace-nowrap overflow-hidden text-ellipsis"
  }, [_vm._v(_vm._s(_vm.$root.user.login))]), _vm._v(" "), _c("p", {
    staticClass: "text-sm font-normal text-[#6a6a7a] max-w-[100px] font-['Rubik'] whitespace-nowrap overflow-hidden text-ellipsis"
  }, [_vm._v("Id: " + _vm._s(_vm.$root.user.id))])]), _vm._v(" "), _c("button", {
    staticClass: "flex py-1 px-1.5 rounded-md items-center space-x-1 font-semibold text-[11px] transition-all duration-200 hover:bg-[#3a3a40]"
  }, [_c("svg", {
    staticClass: "w-[14px] h-[14px] text-[#c5cbe0]"
  }, [_c("use", {
    attrs: {
      "xlink:href": __webpack_require__(/*! @/images/symbols.svg */ "./resources/frontend/images/symbols.svg") + "#copy"
    }
  })]), _vm._v(" "), _c("span", {
    staticClass: "pointer-events-none"
  }, [_vm._v(_vm._s(_vm.$root.user.login))])])])]), _vm._v(" "), _c("div", {
    staticClass: "py-2"
  }, [_c("nav", {
    staticClass: "flex hidden 2xl:flex flex-col space-y-1"
  }, _vm._l(_vm.menuMobile, function (item) {
    return _c("li", {
      key: item.id,
      on: {
        click: function click($event) {
          _vm.isMenuOpen = false;
        }
      }
    }, [_c("router-link", {
      staticClass: "text-white font-['Manrope'] font-semibold flex items-center py-2 space-x-2 px-4 text-sm transition-all duration-200 hover:bg-[#3a3a40]",
      attrs: {
        to: item.path,
        "active-class": "",
        "exact-active-class": ""
      }
    }, [_c("svg", {
      staticClass: "w-[16px] h-[16px] text-[#c5cbe0]"
    }, [_c("use", {
      attrs: {
        "xlink:href": "../images/symbols.svg#" + item.ico
      }
    })]), _vm._v(" "), _c("span", {
      staticClass: "pointer-events-none"
    }, [_vm._v(_vm._s(item.name))])])], 1);
  }), 0), _vm._v(" "), _c("nav", {
    staticClass: "flex flex-col space-y-1"
  }, _vm._l(_vm.menuProfileDropdown, function (item) {
    return _c("li", {
      key: item.id,
      on: {
        click: function click($event) {
          _vm.isMenuOpen =  false || item.modal ? _vm.showModal(item.modal) : "";
        }
      }
    }, [_c("router-link", {
      staticClass: "text-white font-['Manrope'] font-semibold flex items-center py-2 space-x-2 px-4 text-sm transition-all duration-200 hover:bg-[#3a3a40]",
      attrs: {
        to: item.path,
        "active-class": "",
        "exact-active-class": ""
      }
    }, [_c("svg", {
      staticClass: "w-[16px] h-[16px] text-[#c5cbe0]"
    }, [_c("use", {
      attrs: {
        "xlink:href": "../images/symbols.svg#" + item.ico
      }
    })]), _vm._v(" "), _c("span", {
      staticClass: "pointer-events-none"
    }, [_vm._v(_vm._s(item.name))])])], 1);
  }), 0)])]) : _vm._e()])], 1)]) : _vm._e(), _vm._v(" "), _vm.$root.user == null ? _c("div", {
    staticClass: "relative flex items-center space-x-2"
  }, [_c("a", {
    staticClass: "font-['Rubik'] hover:bg-[#3A3A40] bg-[#2c2c31] whitespace-nowrap flex transition-all duration-200 items-center justify-center rounded-xl text-sm uppercase font-medium h-[52px] px-6 shadow-[0px_4px_35px_rgba(0,0,0,0.1)]",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: function click($event) {
        return _vm.login();
      }
    }
  }, [_vm._v("\n                Авторизация\n            ")])]) : _vm._e()]), _vm._v(" "), _c("modalPay"), _vm._v(" "), _c("modalSettings"), _vm._v(" "), _c("modalRegister"), _vm._v(" "), _c("modalLogin")], 1);
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

/***/ "./resources/frontend/images/logotype.svg":
/*!************************************************!*\
  !*** ./resources/frontend/images/logotype.svg ***!
  \************************************************/
/***/ ((module) => {

module.exports = "/images/logotype.svg?ecdf3464793a87c722d99d408488659f";

/***/ }),

/***/ "./resources/frontend/images/symbols.svg":
/*!***********************************************!*\
  !*** ./resources/frontend/images/symbols.svg ***!
  \***********************************************/
/***/ ((module) => {

module.exports = "/images/symbols.svg?f7fed230c3145a324091fa7c09a0dbea";

/***/ }),

/***/ "./resources/frontend/components/layouts/Header/Header.vue":
/*!*****************************************************************!*\
  !*** ./resources/frontend/components/layouts/Header/Header.vue ***!
  \*****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Header_vue_vue_type_template_id_6433bb36___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Header.vue?vue&type=template&id=6433bb36& */ "./resources/frontend/components/layouts/Header/Header.vue?vue&type=template&id=6433bb36&");
/* harmony import */ var _Header_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Header.vue?vue&type=script&lang=js& */ "./resources/frontend/components/layouts/Header/Header.vue?vue&type=script&lang=js&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");





/* normalize component */
;
var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__["default"])(
  _Header_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Header_vue_vue_type_template_id_6433bb36___WEBPACK_IMPORTED_MODULE_0__.render,
  _Header_vue_vue_type_template_id_6433bb36___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/components/layouts/Header/Header.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/components/layouts/Header/Header.vue?vue&type=script&lang=js&":
/*!******************************************************************************************!*\
  !*** ./resources/frontend/components/layouts/Header/Header.vue?vue&type=script&lang=js& ***!
  \******************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Header_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Header.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Header/Header.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Header_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/components/layouts/Header/Header.vue?vue&type=template&id=6433bb36&":
/*!************************************************************************************************!*\
  !*** ./resources/frontend/components/layouts/Header/Header.vue?vue&type=template&id=6433bb36& ***!
  \************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_vue_loader_lib_index_js_vue_loader_options_Header_vue_vue_type_template_id_6433bb36___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_vue_loader_lib_index_js_vue_loader_options_Header_vue_vue_type_template_id_6433bb36___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_vue_loader_lib_index_js_vue_loader_options_Header_vue_vue_type_template_id_6433bb36___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Header.vue?vue&type=template&id=6433bb36& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Header/Header.vue?vue&type=template&id=6433bb36&");


/***/ })

}]);