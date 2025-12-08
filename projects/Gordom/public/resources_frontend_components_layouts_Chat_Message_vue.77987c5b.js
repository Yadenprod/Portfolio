"use strict";
(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_components_layouts_Chat_Message_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=script&lang=js&":
/*!*********************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=script&lang=js& ***!
  \*********************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  props: {
    messages: {
      type: Array,
      "default": function _default() {}
    }
  },
  data: function data() {
    return {
      selectedUser: null
    };
  },
  components: {
    modalBan: function modalBan() {
      return Promise.all(/*! import() */[__webpack_require__.e("/js/vendor"), __webpack_require__.e("resources_frontend_components_modals_Ban_vue")]).then(__webpack_require__.bind(__webpack_require__, /*! @/components/modals/Ban.vue */ "./resources/frontend/components/modals/Ban.vue"));
    }
  },
  methods: {
    selectMessage: function selectMessage(id) {
      var message = this.messages.find(function (item) {
        return item.id == id;
      });
      this.selectedUser = message.user.id;
    },
    modalBan: function modalBan(id) {
      this.$modal.show("modal-ban");
      this.selectMessage(id);
    },
    deleteMessage: function deleteMessage(id) {
      var _this = this;
      this.$root.axios.post('/chat/delete', {
        id: id
      }).then(function (response) {
        var data = response.data;
        if (data.error) {
          return _this.$toastr.Add({
            name: 'PromoToast',
            title: 'Ошибка',
            msg: data.message,
            type: 'error',
            defaultClassNames: ["animated", "zoomInUp"],
            timeout: 3000,
            progressbar: true
          });
        }
        _this.$toastr.Add({
          name: 'PromoToast',
          title: 'Успех',
          msg: 'Сообщение удалено',
          type: 'success',
          defaultClassNames: ["animated", "zoomInUp"],
          timeout: 3000,
          progressbar: true
        });
      });
    }
  },
  updated: function updated() {
    var _this2 = this;
    this.$nextTick(function () {
      var scrollbar = _this2.$refs.chatScroll;
      scrollbar.scrollTop = scrollbar.scrollHeight;
    });
  },
  mounted: function mounted() {
    var _this3 = this;
    this.$nextTick(function () {
      var scrollbar = _this3.$refs.chatScroll;
      scrollbar.scrollTop = scrollbar.scrollHeight;
    });
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=template&id=377ddc2a&lang=pug&":
/*!**********************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=template&id=377ddc2a&lang=pug& ***!
  \**********************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
    ref: "chatScroll",
    staticClass: "h-full overflow-auto space-y-3"
  }, [_vm._l(_vm.messages, function (item) {
    return _c("div", {
      key: item.id,
      staticClass: "w-full bg-[#2c2c31] p-3 flex items-start justify-between rounded-xl"
    }, [_c("div", {
      staticClass: "shrink-0 w-[40px] h-[40px] overflow-hidden top-0.5 relative rounded-xl",
      "class": item.role === "youtuber" ? "border-2 border-[#f24841]" :  false || item.role === "moderator" ? "border-2 border-[#44c276]" : ""
    }, [_c("img", {
      staticClass: "absolute left-0 top-0 w-full h-full object-cover",
      attrs: {
        src: item.user.avatar
      }
    })]), _c("div", {
      staticClass: "w-full flex flex-col py-1 pl-3.5 pr-1.5 relative space-y-1"
    }, [_c("div", {
      staticClass: "flex items-center justify-between"
    }, [_c("b", {
      staticClass: "text-xs text-[#cfcde9] max-w-[120px] overflow-hidden text-ellipsis whitespace-nowrap",
      "class": item.role === "admin" ? "!text-[#7c75d9]" :  false || item.role === "youtuber" ? "!text-[#f24841]" :  false || item.role === "moderator" ? "!text-[#44c276]" : ""
    }, [_vm._v(_vm._s(item.user.nickname))]), _c("div", {
      staticClass: "message__props flex items-center grow justify-end"
    }, [_c("span", {
      staticClass: "message__time text-xs text-[#46464e] font-bold"
    }, [_vm._v(_vm._s(item.date))]), _vm.$root.user !== null && (_vm.$root.user.is_admin || _vm.$root.user.is_moderator) ? _c("div", {
      staticClass: "message__actions flex items-center justify-between"
    }, [_c("span", {
      staticClass: "message__action flex w-[32px] h-[32px] items-center text-xs justify-center bg-[#3A3A40] rounded transition-all duration-200 hover:bg-[#7C75D9] hover:!text-white",
      on: {
        click: function click($event) {
          return _vm.deleteMessage(item.id);
        }
      }
    }, [_c("svg", {
      staticClass: "w-[12px] h-[12x]"
    }, [_c("use", {
      attrs: {
        "xlink:href": __webpack_require__(/*! @/images/symbols.svg */ "./resources/frontend/images/symbols.svg") + "#close"
      }
    })])]), _c("span", {
      staticClass: "message__action flex w-[32px] h-[32px] items-center text-xs justify-center bg-[#3A3A40] rounded transition-all duration-200 hover:bg-[#7C75D9] hover:!text-white",
      on: {
        click: function click($event) {
          return _vm.modalBan(item.id);
        }
      }
    }, [_vm._v("!")])]) : _vm._e()])]), _c("div", {
      staticClass: "text-xs text-[#6a6a7a] font-medium [&_p]:leading-[160%]",
      "class": item.role === "admin" ? "!text-[#cfcde9]" :  false || item.role === "youtuber" ? "!text-[#cfcde9]" :  false || item.role === "moderator" ? "!text-[#cfcde9]" : ""
    }, [_c("p", {
      domProps: {
        innerHTML: _vm._s(item.message)
      }
    })])])]);
  }), _c("modalBan", {
    attrs: {
      user_id: _vm.selectedUser
    }
  })], 2);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss&":
/*!*************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss& ***!
  \*************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../../node_modules/laravel-mix/node_modules/css-loader/dist/runtime/api.js */ "./node_modules/laravel-mix/node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);
// Imports

var ___CSS_LOADER_EXPORT___ = _node_modules_laravel_mix_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".message__props:hover > .message__time {\n  display: none;\n}\n.message__props:hover > .message__actions {\n  display: flex;\n}\n.message__actions {\n  display: none;\n  -moz-column-gap: 6px;\n       column-gap: 6px;\n}\n.message__action {\n  width: 16px;\n  height: 16px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  text-align: center;\n  padding: 4px;\n  cursor: pointer !important;\n}\n.message__action:hover {\n  color: #5e5e69;\n  background: #46464e;\n}", ""]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss&":
/*!*****************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss& ***!
  \*****************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Message_vue_vue_type_style_index_0_id_377ddc2a_lang_scss___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss& */ "./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss&");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Message_vue_vue_type_style_index_0_id_377ddc2a_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Message_vue_vue_type_style_index_0_id_377ddc2a_lang_scss___WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "./resources/frontend/components/layouts/Chat/Message.vue":
/*!****************************************************************!*\
  !*** ./resources/frontend/components/layouts/Chat/Message.vue ***!
  \****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Message_vue_vue_type_template_id_377ddc2a_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Message.vue?vue&type=template&id=377ddc2a&lang=pug& */ "./resources/frontend/components/layouts/Chat/Message.vue?vue&type=template&id=377ddc2a&lang=pug&");
/* harmony import */ var _Message_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Message.vue?vue&type=script&lang=js& */ "./resources/frontend/components/layouts/Chat/Message.vue?vue&type=script&lang=js&");
/* harmony import */ var _Message_vue_vue_type_style_index_0_id_377ddc2a_lang_scss___WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss& */ "./resources/frontend/components/layouts/Chat/Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");



;


/* normalize component */

var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_3__["default"])(
  _Message_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Message_vue_vue_type_template_id_377ddc2a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Message_vue_vue_type_template_id_377ddc2a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/components/layouts/Chat/Message.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/components/layouts/Chat/Message.vue?vue&type=script&lang=js&":
/*!*****************************************************************************************!*\
  !*** ./resources/frontend/components/layouts/Chat/Message.vue?vue&type=script&lang=js& ***!
  \*****************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Message_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Message.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Message_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/components/layouts/Chat/Message.vue?vue&type=template&id=377ddc2a&lang=pug&":
/*!********************************************************************************************************!*\
  !*** ./resources/frontend/components/layouts/Chat/Message.vue?vue&type=template&id=377ddc2a&lang=pug& ***!
  \********************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Message_vue_vue_type_template_id_377ddc2a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Message_vue_vue_type_template_id_377ddc2a_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Message_vue_vue_type_template_id_377ddc2a_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../../../node_modules/pug-plain-loader/index.js!../../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Message.vue?vue&type=template&id=377ddc2a&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=template&id=377ddc2a&lang=pug&");


/***/ }),

/***/ "./resources/frontend/components/layouts/Chat/Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss&":
/*!**************************************************************************************************************!*\
  !*** ./resources/frontend/components/layouts/Chat/Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss& ***!
  \**************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _node_modules_style_loader_dist_cjs_js_node_modules_laravel_mix_node_modules_css_loader_dist_cjs_js_clonedRuleSet_12_use_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_dist_cjs_js_clonedRuleSet_12_use_2_node_modules_sass_loader_dist_cjs_js_clonedRuleSet_12_use_3_node_modules_vue_loader_lib_index_js_vue_loader_options_Message_vue_vue_type_style_index_0_id_377ddc2a_lang_scss___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../node_modules/style-loader/dist/cjs.js!../../../../../node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!../../../../../node_modules/vue-loader/lib/loaders/stylePostLoader.js!../../../../../node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!../../../../../node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!../../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss& */ "./node_modules/style-loader/dist/cjs.js!./node_modules/laravel-mix/node_modules/css-loader/dist/cjs.js??clonedRuleSet-12.use[1]!./node_modules/vue-loader/lib/loaders/stylePostLoader.js!./node_modules/postcss-loader/dist/cjs.js??clonedRuleSet-12.use[2]!./node_modules/sass-loader/dist/cjs.js??clonedRuleSet-12.use[3]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Message.vue?vue&type=style&index=0&id=377ddc2a&lang=scss&");


/***/ })

}]);