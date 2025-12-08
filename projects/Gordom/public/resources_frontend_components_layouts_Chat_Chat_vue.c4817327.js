(self["webpackChunk"] = self["webpackChunk"] || []).push([["resources_frontend_components_layouts_Chat_Chat_vue"],{

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=script&lang=js&":
/*!******************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=script&lang=js& ***!
  \******************************************************************************************************************************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ({
  name: 'Chat',
  components: {
    Message: function Message() {
      return __webpack_require__.e(/*! import() */ "resources_frontend_components_layouts_Chat_Message_vue").then(__webpack_require__.bind(__webpack_require__, /*! ./Message.vue */ "./resources/frontend/components/layouts/Chat/Message.vue"));
    },
    ModalChatRules: function ModalChatRules() {
      return Promise.all(/*! import() */[__webpack_require__.e("/js/vendor"), __webpack_require__.e("resources_frontend_components_modals_ChatRules_vue")]).then(__webpack_require__.bind(__webpack_require__, /*! @/components/modals/ChatRules.vue */ "./resources/frontend/components/modals/ChatRules.vue"));
    }
  },
  data: function data() {
    return {
      messages: [],
      msg: '',
      preloader: true,
      width: 0
    };
  },
  props: {
    chatOpen: {
      type: Boolean,
      "default": function _default() {}
    }
  },
  methods: {
    init: function init() {
      var _this = this;
      this.$root.axios.post('/chat/init').then(function (response) {
        var data = response.data;
        var messages = [];
        data.forEach(function (message) {
          messages.push({
            id: message.id,
            user: {
              id: message.user_id,
              avatar: message.avatar,
              nickname: message.login
            },
            role: message.role,
            date: message.time,
            message: message.text
          });
        });
        _this.preloader = false;
        _this.messages = messages.reverse();
      });
    },
    chatInitState: function chatInitState() {
      if (this.chatOpen) {
        this.$emit('chatInitState', false);
      } else {
        this.$emit('chatInitState', true);
      }
    },
    updateWidth: function updateWidth() {
      this.width = window.innerWidth;
      if (window.innerWidth <= 1075) {
        this.$emit('chatInitState', false);
      }
    },
    modalRules: function modalRules() {
      this.$modal.show('chat-rules');
    },
    addMessage: function addMessage() {
      var _this2 = this;
      this.$root.axios.post('/chat/send', {
        message: this.msg
      }).then(function (response) {
        var data = response.data;
        if (data.error) {
          return _this2.$toastr.Add({
            name: 'chatSendMsg',
            title: 'Ошибка',
            msg: data.message,
            type: 'error',
            defaultClassNames: ["animated", "zoomInUp"],
            timeout: 3000,
            progressbar: true
          });
        }
        _this2.msg = '';
      });
    }
  },
  mounted: function mounted() {
    this.init();
    if (window.innerWidth <= 1075) {
      this.$emit('chatInitState', false);
    }
  },
  created: function created() {
    window.addEventListener('resize', this.updateWidth);
  },
  sockets: {
    'chat.message': function chatMessage(data) {
      this.messages.push({
        id: data.id,
        user: {
          id: data.user_id,
          avatar: data.avatar,
          nickname: data.login
        },
        date: data.time,
        role: data.role,
        message: data.text
      });
    },
    'chat.delete': function chatDelete(data) {
      this.messages = this.messages.filter(function (item) {
        return item.id !== data.id;
      });
    }
  },
  watch: {
    '$route': function $route(to, from) {
      if (window.innerWidth <= 1075) {
        this.$emit('chatInitState', false);
      }
    }
  }
});

/***/ }),

/***/ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=template&id=0a7068c5&lang=pug&":
/*!*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=template&id=0a7068c5&lang=pug& ***!
  \*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************/
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
    staticClass: "fixed right-0 top-0 h-full lg:h-[calc(100%_-_67px)] pr-[16px] py-[16px] transition-all duration-200 lg:p-0 lg:translate-x-[0%] lg:z-[20] lg:left-0 lg:top-[67px] lg:right-inherit",
    "class": _vm.chatOpen ? "" : "translate-x-[100%] lg:translate-x-[0%] lg:hidden"
  }, [!_vm.chatOpen ? _c("a", {
    staticClass: "lg:hidden absolute -left-[56px] top-[16px] w-[36px] h-[36px] rounded-[12px] bg-[#7c75d9] flex items-center justify-center transition-all duration-200 hover:bg-[#6962c1]",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: _vm.chatInitState
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px] rotate-[180deg]"
  }, [_c("use", {
    attrs: {
      "xlink:href": __webpack_require__(/*! @/images/symbols.svg */ "./resources/frontend/images/symbols.svg") + "#arrow"
    }
  })])]) : _vm._e(), _c("div", {
    staticClass: "relative overflow-hidden flex flex-col lg:w-full lg:rounded-none justify-between w-[300px] gap-6 h-full bg-[#202024] lg:px-4 px-6 rounded-xl pb-6 lg:pb-4"
  }, [_c("div", {
    staticClass: "pt-6 lg:pt-4 flex items-center justify-between"
  }, [_c("div", {
    staticClass: "flex flex-col space-y-1"
  }, [_c("b", {
    staticClass: "text-[#cfcde9] text-sm"
  }, [_vm._v("Online чат")]), _c("a", {
    staticClass: "text-[#46464e] text-sm font-semibold transition-all duration-200 hover:text-[#7c75d9]",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: function click($event) {
        return _vm.modalRules();
      }
    }
  }, [_vm._v("Правила чата")])]), _c("a", {
    staticClass: "w-[36px] h-[36px] rounded-[12px] bg-[#7c75d9] flex items-center justify-center transition-all duration-200 hover:bg-[#6962c1]",
    attrs: {
      href: "javascript:;"
    },
    on: {
      click: _vm.chatInitState
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px]"
  }, [_c("use", {
    attrs: {
      "xlink:href": __webpack_require__(/*! @/images/symbols.svg */ "./resources/frontend/images/symbols.svg") + "#arrow"
    }
  })])])]), _c("div", {
    staticClass: "w-full h-[calc(100%_-_185px)]",
    "class": _vm.preloader ? "flex items-center justify-center" : ""
  }, [_vm.preloader ? _c("Spin", {
    attrs: {
      color: "#cfcde9"
    }
  }) : _vm._e(), _c("Transition", {
    attrs: {
      "enter-active-class": "transition ease-out duration-800",
      "enter-class": "transform opacity-0 scale-95",
      "enter-to-class": "transform opacity-100 scale-100"
    }
  }, [!_vm.preloader ? _c("div", {
    staticClass: "w-full h-full [&_div.scroll-content]:space-y-3 [&_div.scrollbar-track]:bg-transparent [&_div.scrollbar-thumb]:bg-[#5d5d6a]/[0.5]"
  }, [_c("Message", {
    attrs: {
      messages: _vm.messages
    }
  })], 1) : _vm._e()])], 1), _c("form", {
    staticClass: "h-[70px] shrink-0 rounded-xl w-full bg-[#1b1c20]",
    on: {
      submit: function submit($event) {
        $event.preventDefault();
        return _vm.addMessage();
      }
    }
  }, [_c("div", {
    staticClass: "w-full h-full relative"
  }, [_c("input", {
    directives: [{
      name: "model",
      rawName: "v-model",
      value: _vm.msg,
      expression: "msg"
    }],
    staticClass: "w-full h-full pl-6 pr-28 font-semibold bg-transparent border-0 focus:ring-0 focus:ring-inherit focus:outline-0 text-sm",
    attrs: {
      type: "text"
    },
    domProps: {
      value: _vm.msg
    },
    on: {
      input: function input($event) {
        if ($event.target.composing) return;
        _vm.msg = $event.target.value;
      }
    }
  }), _c("button", {
    staticClass: "absolute cursor-pointer right-5 top-1/2 -translate-y-1/2 w-[36px] h-[36px] rounded-[12px] bg-[#7c75d9] flex items-center justify-center transition-all duration-200 hover:bg-[#6962c1] focus:ring-0 focus:outline-0",
    attrs: {
      type: "submit"
    }
  }, [_c("svg", {
    staticClass: "w-[18px] h-[18px] pointer-events-none"
  }, [_c("use", {
    attrs: {
      "xlink:href": __webpack_require__(/*! @/images/symbols.svg */ "./resources/frontend/images/symbols.svg") + "#send"
    }
  })])])])])]), _c("ModalChatRules")], 1);
};
var staticRenderFns = [];
render._withStripped = true;


/***/ }),

/***/ "./resources/frontend/images/symbols.svg":
/*!***********************************************!*\
  !*** ./resources/frontend/images/symbols.svg ***!
  \***********************************************/
/***/ ((module) => {

module.exports = "/images/symbols.svg?f7fed230c3145a324091fa7c09a0dbea";

/***/ }),

/***/ "./resources/frontend/components/layouts/Chat/Chat.vue":
/*!*************************************************************!*\
  !*** ./resources/frontend/components/layouts/Chat/Chat.vue ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _Chat_vue_vue_type_template_id_0a7068c5_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./Chat.vue?vue&type=template&id=0a7068c5&lang=pug& */ "./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=template&id=0a7068c5&lang=pug&");
/* harmony import */ var _Chat_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./Chat.vue?vue&type=script&lang=js& */ "./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=script&lang=js&");
/* harmony import */ var _node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../../../node_modules/vue-loader/lib/runtime/componentNormalizer.js */ "./node_modules/vue-loader/lib/runtime/componentNormalizer.js");





/* normalize component */
;
var component = (0,_node_modules_vue_loader_lib_runtime_componentNormalizer_js__WEBPACK_IMPORTED_MODULE_2__["default"])(
  _Chat_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_1__["default"],
  _Chat_vue_vue_type_template_id_0a7068c5_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render,
  _Chat_vue_vue_type_template_id_0a7068c5_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "resources/frontend/components/layouts/Chat/Chat.vue"
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (component.exports);

/***/ }),

/***/ "./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=script&lang=js&":
/*!**************************************************************************************!*\
  !*** ./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=script&lang=js& ***!
  \**************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Chat_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Chat.vue?vue&type=script&lang=js& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=script&lang=js&");
 /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_index_js_vue_loader_options_Chat_vue_vue_type_script_lang_js___WEBPACK_IMPORTED_MODULE_0__["default"]); 

/***/ }),

/***/ "./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=template&id=0a7068c5&lang=pug&":
/*!*****************************************************************************************************!*\
  !*** ./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=template&id=0a7068c5&lang=pug& ***!
  \*****************************************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "render": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Chat_vue_vue_type_template_id_0a7068c5_lang_pug___WEBPACK_IMPORTED_MODULE_0__.render),
/* harmony export */   "staticRenderFns": () => (/* reexport safe */ _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Chat_vue_vue_type_template_id_0a7068c5_lang_pug___WEBPACK_IMPORTED_MODULE_0__.staticRenderFns)
/* harmony export */ });
/* harmony import */ var _node_modules_babel_loader_lib_index_js_clonedRuleSet_5_use_0_node_modules_vue_loader_lib_loaders_templateLoader_js_ruleSet_1_rules_2_node_modules_pug_plain_loader_index_js_node_modules_vue_loader_lib_index_js_vue_loader_options_Chat_vue_vue_type_template_id_0a7068c5_lang_pug___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! -!../../../../../node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!../../../../../node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!../../../../../node_modules/pug-plain-loader/index.js!../../../../../node_modules/vue-loader/lib/index.js??vue-loader-options!./Chat.vue?vue&type=template&id=0a7068c5&lang=pug& */ "./node_modules/babel-loader/lib/index.js??clonedRuleSet-5.use[0]!./node_modules/vue-loader/lib/loaders/templateLoader.js??ruleSet[1].rules[2]!./node_modules/pug-plain-loader/index.js!./node_modules/vue-loader/lib/index.js??vue-loader-options!./resources/frontend/components/layouts/Chat/Chat.vue?vue&type=template&id=0a7068c5&lang=pug&");


/***/ })

}]);