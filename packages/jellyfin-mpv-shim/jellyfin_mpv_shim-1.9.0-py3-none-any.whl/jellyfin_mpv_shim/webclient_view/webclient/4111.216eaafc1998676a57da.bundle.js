(self.webpackChunk=self.webpackChunk||[]).push([[4111],{84111:function(e,n,t){"use strict";t.r(n),t.d(n,{download:function(){return a}}),t(61013),t(95374),t(55849);var o=t(47518);function r(e){var n=document.createElement("a");n.download="",n.href=e,n.dispatchEvent(new MouseEvent("click"))}var c=t(29856);function a(e){c.Z.downloadFiles(e)||function(e){if(!e)throw new Error("`urls` required");if(void 0===document.createElement("a").download)return function(e){var n=0;!function t(){var o=document.createElement("iframe");o.style.display="none",o.src=e[n++],document.documentElement.appendChild(o);var r=setInterval((function(){"complete"!==o.contentWindow.document.readyState&&"interactive"!==o.contentWindow.document.readyState||(clearInterval(r),setTimeout((function(){o.parentNode.removeChild(o)}),1e3),n<e.length&&t())}),100)}()}(e);var n=0;e.forEach((function(e){if(o.Z.firefox&&!function(e){var n=document.createElement("a");return n.href=e,window.location.hostname===n.hostname&&window.location.protocol===n.protocol}(e))return setTimeout(r.bind(null,e),100*++n);r(e)}))}(e.map((function(e){return e.url})))}}}]);