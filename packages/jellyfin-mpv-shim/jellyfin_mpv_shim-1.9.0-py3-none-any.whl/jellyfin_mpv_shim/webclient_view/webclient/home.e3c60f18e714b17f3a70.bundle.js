(self.webpackChunk=self.webpackChunk||[]).push([[5177,7425,7282],{27282:function(e,t,n){"use strict";n.r(t),n.d(t,{setTabs:function(){return h},selectedTabIndex:function(){return b},getTabsElement:function(){return v}}),n(61013),n(63238),n(61418),n(5769);var r,i,o,s=n(83094),a=n(47518),l=n(47005),c=(n(29366),n(78066),document.querySelector(".skinHeader"));function u(){i||(i=c.querySelector(".headerTabs"))}function d(){this.selectedIndex(this.readySelectedIndex),this.readySelectedIndex=null}function f(e){function t(e){if(s.ZP.parentWithTag(e,"input"))return!1;var t=e.classList;return!t||!t.contains("scrollX")&&!t.contains("animatedScrollX")}for(var n=e;null!=n;){if(!t(n))return!1;n=n.parentNode}return!0}function h(e,t,s,h,b,v,m){if(!e)return r&&(i||(i=c.querySelector(".headerTabs")),u(),document.body.classList.remove("withSectionTabs"),i.innerHTML="",i.classList.add("hide"),r=null),{tabsContainer:i,replaced:!1};u();var p=i;if(r||p.classList.remove("hide"),r!==e){var g=0,y='<div is="emby-tabs"'+(null==t?"":' data-index="'+t+'"')+' class="tabs-viewmenubar"><div class="emby-tabs-slider" style="white-space:nowrap;">'+s().map((function(e){var t,n="emby-tab-button";return!1===e.enabled&&(n+=" hide"),e.cssClass&&(n+=" "+e.cssClass),t=e.href?'<a href="'+e.href+'" is="emby-linkbutton" class="'+n+'" data-index="'+g+'"><div class="emby-button-foreground">'+e.name+"</div></a>":'<button type="button" is="emby-button" class="'+n+'" data-index="'+g+'"><div class="emby-button-foreground">'+e.name+"</div></button>",g++,t})).join("")+"</div></div>";return p.innerHTML=y,window.CustomElements.upgradeSubtree(p),document.body.classList.add("withSectionTabs"),r=e,function(e,t,r){if(a.Z.touch){var i=function(n,r){f(r)&&e.contains(r)&&t.selectNext()},o=function(n,r){f(r)&&e.contains(r)&&t.selectPrevious()};n.e(5344).then(n.bind(n,85344)).then((function(t){var n=new(0,t.default)(e.parentNode.parentNode);l.Events.on(n,"swipeleft",i),l.Events.on(n,"swiperight",o),e.addEventListener("viewdestroy",(function(){n.destroy()}))}))}}(e,o=p.querySelector('[is="emby-tabs"]')),o.addEventListener("beforetabchange",(function(e){var t=h();if(null!=e.detail.previousIndex){var n=t[e.detail.previousIndex];n&&n.classList.remove("is-active")}var r=t[e.detail.selectedTabIndex];r&&r.classList.add("is-active")})),b&&o.addEventListener("beforetabchange",b),v&&o.addEventListener("tabchange",v),!1!==m&&(o.selectedIndex?o.selectedIndex(t):(o.readySelectedIndex=t,o.addEventListener("ready",d))),{tabsContainer:p,tabs:p.querySelector('[is="emby-tabs"]'),replaced:!0}}return o||(o=p.querySelector('[is="emby-tabs"]')),o.selectedIndex(t),r=e,{tabsContainer:p,tabs:o,replaced:!1}}function b(e){o||(o=i.querySelector('[is="emby-tabs"]')),null!=e?o.selectedIndex(e):o.triggerTabChange()}function v(){return document.querySelector(".tabs-viewmenubar")}},85081:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return g}}),n(12274),n(50987),n(63238),n(61418),n(3214),n(40895),n(5769),n(95374),n(32081),n(55849);var r=n(28321),i=n(27282),o=n(78695),s=(n(29366),n(6383));function a(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function l(e){var t=this.tabControllers;t&&(t.forEach((function(e){e.destroy&&e.destroy()})),this.tabControllers=null),this.view=null,this.params=null,this.currentTabController=null,this.initialTabIndex=null}function c(){}var u=function(){function e(t,n){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.tabControllers=[],this.view=t,this.params=n;var r=this,s=parseInt(n.tab||this.getDefaultTabIndex(n.parentId));function a(){return t.querySelectorAll(".tabContent")}function u(e){var t=parseInt(e.detail.selectedTabIndex),n=e.detail.previousIndex,i=null==n?null:r.tabControllers[n];i&&i.onPause&&i.onPause(),function(e,t){(function(e){return r.validateTabLoad?r.validateTabLoad(e):Promise.resolve()})(e).then((function(){r.getTabController(e).then((function(n){var i=!n.refreshed;n.onResume({autoFocus:null==t&&o.Z.tv,refresh:i}),n.refreshed=!0,s=e,r.currentTabController=n}))}))}(t,n)}this.initialTabIndex=s,t.addEventListener("viewbeforehide",this.onPause.bind(this)),t.addEventListener("viewbeforeshow",(function(e){i.setTabs(t,s,r.getTabs,a,c,u,!1)})),t.addEventListener("viewshow",(function(e){r.onResume(e.detail)})),t.addEventListener("viewdestroy",l.bind(this))}var t,n;return t=e,(n=[{key:"onResume",value:function(e){this.setTitle(),r.ZP.clearBackdrop();var t=this.currentTabController;t?t&&t.onResume&&t.onResume({}):i.selectedTabIndex(this.initialTabIndex)}},{key:"onPause",value:function(){var e=this.currentTabController;e&&e.onPause&&e.onPause()}},{key:"setTitle",value:function(){s.appRouter.setTitle("")}}])&&a(t.prototype,n),e}(),d=n(53754);function f(e){return(f="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function h(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function b(e,t,n){return(b="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=p(e)););return e}(e,t);if(r){var i=Object.getOwnPropertyDescriptor(r,t);return i.get?i.get.call(n):i.value}})(e,t,n||e)}function v(e,t){return(v=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function m(e,t){return!t||"object"!==f(t)&&"function"!=typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function p(e){return(p=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}n(78066),n(48366);var g=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&v(e,t)}(l,e);var t,r,i,o,a=(i=l,o=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}(),function(){var e,t=p(i);if(o){var n=p(this).constructor;e=Reflect.construct(t,arguments,n)}else e=t.apply(this,arguments);return m(this,e)});function l(e,t){return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,l),a.call(this,e,t)}return t=l,(r=[{key:"setTitle",value:function(){s.appRouter.setTitle(null)}},{key:"onPause",value:function(){b(p(l.prototype),"onPause",this).call(this,this),document.querySelector(".skinHeader").classList.remove("noHomeButtonHeader")}},{key:"onResume",value:function(e){b(p(l.prototype),"onResume",this).call(this,this,e),document.querySelector(".skinHeader").classList.add("noHomeButtonHeader")}},{key:"getDefaultTabIndex",value:function(){return 0}},{key:"getTabs",value:function(){return[{name:d.ZP.translate("Home")},{name:d.ZP.translate("Favorites")}]}},{key:"getTabController",value:function(e){if(null==e)throw new Error("index cannot be null");var t="";switch(e){case 0:t="hometab";break;case 1:t="favorites"}var r=this;return n(23935)("./".concat(t)).then((function(t){var n=t.default,i=r.tabControllers[e];return i||(i=new n(r.view.querySelector(".tabContent[data-index='"+e+"']"),r.params),r.tabControllers[e]=i),i}))}}])&&h(t.prototype,r),l}(u)},48366:function(e,t,n){"use strict";n(63238),n(61418),n(5769);var r=n(13800),i=n(83094),o=n(78695),s=n(12392),a=n(27515),l=n(47518),c=(n(67752),n(1892)),u=n.n(c),d=n(75869),f=(u()(d.Z,{insert:"head",singleton:!1}),d.Z.locals,Object.create(HTMLDivElement.prototype));function h(e){var t=e.detail.command;"end"===t?(a.Z.focusLast(this,"."+this.getAttribute("data-navcommands")),e.preventDefault(),e.stopPropagation()):"pageup"===t?(a.Z.moveFocus(e.target,this,"."+this.getAttribute("data-navcommands"),-12),e.preventDefault(),e.stopPropagation()):"pagedown"===t&&(a.Z.moveFocus(e.target,this,"."+this.getAttribute("data-navcommands"),12),e.preventDefault(),e.stopPropagation())}f.createdCallback=function(){this.classList.add("emby-scroller")},f.scrollToBeginning=function(){this.scroller&&this.scroller.slideTo(0,!0)},f.toStart=function(e,t){this.scroller&&this.scroller.toStart(e,t)},f.toCenter=function(e,t){this.scroller&&this.scroller.toCenter(e,t)},f.scrollToPosition=function(e,t){this.scroller&&this.scroller.slideTo(e,t)},f.getScrollPosition=function(){if(this.scroller)return this.scroller.getScrollPosition()},f.getScrollSize=function(){if(this.scroller)return this.scroller.getScrollSize()},f.getScrollEventName=function(){if(this.scroller)return this.scroller.getScrollEventName()},f.getScrollSlider=function(){if(this.scroller)return this.scroller.getScrollSlider()},f.addScrollEventListener=function(e,t){this.scroller&&i.ZP.addEventListener(this.scroller.getScrollFrame(),this.scroller.getScrollEventName(),e,t)},f.removeScrollEventListener=function(e,t){this.scroller&&i.ZP.removeEventListener(this.scroller.getScrollFrame(),this.scroller.getScrollEventName(),e,t)},f.attachedCallback=function(){this.getAttribute("data-navcommands")&&s.ZP.on(this,h);var e="false"!==this.getAttribute("data-horizontal"),t=this.querySelector(".scrollSlider");e&&(t.style["white-space"]="nowrap");var c,u=o.Z.desktop&&e&&"false"!==this.getAttribute("data-scrollbuttons"),d={horizontal:e,mouseDragging:1,mouseWheel:"false"!==this.getAttribute("data-mousewheel"),touchDragging:1,slidee:t,scrollBy:200,speed:e?270:240,elasticBounds:1,dragHandle:1,autoImmediate:!0,skipSlideToWhenVisible:"true"===this.getAttribute("data-skipfocuswhenvisible"),dispatchScrollEvent:u||"true"===this.getAttribute("data-scrollevent"),hideScrollbar:u||"true"===this.getAttribute("data-hidescrollbar"),allowNativeSmoothScroll:"true"===this.getAttribute("data-allownativesmoothscroll")&&!u,allowNativeScroll:!u,forceHideScrollbars:u,requireAnimation:u&&l.Z.edge};this.scroller=new r.Z(this,d),this.scroller.init(),this.scroller.reload(),o.Z.tv&&this.getAttribute("data-centerfocus")&&(this,c=this.scroller,i.ZP.addEventListener(this,"focus",(function(e){var t=a.Z.focusableParent(e.target);t&&c.toCenter(t)}),{capture:!0,passive:!0})),u&&function(e){n.e(6229).then(n.bind(n,6229)).then((function(){e.insertAdjacentHTML("beforebegin",'<div is="emby-scrollbuttons" class="emby-scrollbuttons padded-right"></div>')}))}(this)},f.pause=function(){var e=this.headroom;e&&e.pause()},f.resume=function(){var e=this.headroom;e&&e.resume()},f.detachedCallback=function(){this.getAttribute("data-navcommands")&&s.ZP.off(this,h);var e=this.headroom;e&&(e.destroy(),this.headroom=null);var t=this.scroller;t&&(t.destroy(),this.scroller=null)},document.registerElement("emby-scroller",{prototype:f,extends:"div"})},29366:function(e,t,n){"use strict";n(32081),n(67752);var r=n(83094),i=n(13800),o=n(47518),s=n(27515),a=n(1892),l=n.n(a),c=n(90685),u=(l()(c.Z,{insert:"head",singleton:!1}),c.Z.locals,n(2553),Object.create(HTMLDivElement.prototype)),d="emby-tab-button",f=d+"-active";function h(e){e.classList.add(f)}function b(e,t,n){var r;e.dispatchEvent(new CustomEvent("beforetabchange",{detail:{selectedTabIndex:t,previousIndex:n}})),null!=n&&n!==t&&(r=null)&&r.classList.remove("is-active")}function v(e){var t=this,n=t.querySelector("."+f),i=r.ZP.parentWithClass(e.target,d);if(i&&i!==n){n&&n.classList.remove(f);var o=n?parseInt(n.getAttribute("data-index")):null;h(i);var s=parseInt(i.getAttribute("data-index"));b(t,s,o),setTimeout((function(){t.selectedTabIndex=s,t.dispatchEvent(new CustomEvent("tabchange",{detail:{selectedTabIndex:s,previousIndex:o}}))}),120),t.scroller&&t.scroller.toCenter(i,!1)}}function m(e){var t=e.target.parentNode.querySelector(".lastFocused");t&&t.classList.remove("lastFocused"),e.target.classList.add("lastFocused")}function p(e){return e.querySelector("."+f)}function g(e,t){for(var n=e[t];n;){if(n.classList.contains(d)&&!n.classList.contains("hide"))return n;n=n[t]}return null}u.createdCallback=function(){this.classList.contains("emby-tabs")||(this.classList.add("emby-tabs"),this.classList.add("focusable"),r.ZP.addEventListener(this,"click",v,{passive:!0}),r.ZP.addEventListener(this,"focusout",m))},u.focus=function(){var e=this.querySelector("."+f),t=this.querySelector(".lastFocused");t?s.Z.focus(t):e?s.Z.focus(e):s.Z.autoFocus(this)},u.refresh=function(){this.scroller&&this.scroller.reload()},u.attachedCallback=function(){!function(e){if(!e.scroller){var t=e.querySelector(".emby-tabs-slider");t?(e.scroller=new i.Z(e,{horizontal:1,itemNav:0,mouseDragging:1,touchDragging:1,slidee:t,smart:!0,releaseSwing:!0,scrollBy:200,speed:120,elasticBounds:1,dragHandle:1,dynamicHandle:1,clickBar:1,hiddenScroll:!0,requireAnimation:!o.Z.safari,allowNativeSmoothScroll:!0}),e.scroller.init()):(e.classList.add("scrollX"),e.classList.add("hiddenScrollX"),e.classList.add("smoothScrollX"))}}(this);var e=this.querySelector("."+f),t=e?parseInt(e.getAttribute("data-index")):parseInt(this.getAttribute("data-index")||"0");if(-1!==t){this.selectedTabIndex=t;var n=this.querySelectorAll("."+d)[t];n&&h(n)}this.readyFired||(this.readyFired=!0,this.dispatchEvent(new CustomEvent("ready",{})))},u.detachedCallback=function(){this.scroller&&(this.scroller.destroy(),this.scroller=null),r.ZP.removeEventListener(this,"click",v,{passive:!0})},u.selectedIndex=function(e,t){var n=this;if(null==e)return n.selectedTabIndex||0;var r=n.selectedIndex();n.selectedTabIndex=e;var i=n.querySelectorAll("."+d);if(r===e||!1===t){b(n,e,r),n.dispatchEvent(new CustomEvent("tabchange",{detail:{selectedTabIndex:e}}));var o=i[r];h(i[e]),r!==e&&o&&o.classList.remove(f)}else v.call(n,{target:i[e]})},u.selectNext=function(){var e=g(p(this),"nextSibling");e&&v.call(this,{target:e})},u.selectPrevious=function(){var e=g(p(this),"previousSibling");e&&v.call(this,{target:e})},u.triggerBeforeTabChange=function(e){b(this,this.selectedIndex())},u.triggerTabChange=function(e){this.dispatchEvent(new CustomEvent("tabchange",{detail:{selectedTabIndex:this.selectedIndex()}}))},u.setTabEnabled=function(e,t){var n=this.querySelector('.emby-tab-button[data-index="'+e+'"]');t?n.classList.remove("hide"):n.classList.remove("add")},document.registerElement("emby-tabs",{prototype:u,extends:"div"})},75869:function(e,t,n){"use strict";var r=n(93476),i=n.n(r)()((function(e){return e[1]}));i.push([e.id,".emby-scroller-container{position:relative}.emby-scroller{margin-left:3.3%;margin-right:3.3%}.itemsContainer>.card>.cardBox{margin-left:0;margin-right:1.2em}.servers>.card>.cardBox{margin-left:.6em;margin-right:.6em}.layout-mobile .emby-scroller,.layout-tv .emby-scroller{padding-left:3.3%;padding-right:3.3%;margin-left:0;margin-right:0}",""]),t.Z=i},90685:function(e,t,n){"use strict";var r=n(93476),i=n.n(r)()((function(e){return e[1]}));i.push([e.id,".emby-tab-button{box-sizing:border-box;background:transparent;box-shadow:none;cursor:pointer;outline:none;width:auto;font-family:inherit;font-size:inherit;display:inline-block;vertical-align:middle;-webkit-flex-shrink:0;flex-shrink:0;margin:0;padding:1.5em;position:relative;height:auto;min-width:0;line-height:1.25;border-radius:0;overflow:hidden;font-weight:600}.emby-tab-button.show-focus:focus{-webkit-transform:scale(1.3)!important;transform:scale(1.3)!important;background:0!important}.emby-tabs-slider{position:relative}.tabContent:not(.is-active){display:none}",""]),t.Z=i}}]);