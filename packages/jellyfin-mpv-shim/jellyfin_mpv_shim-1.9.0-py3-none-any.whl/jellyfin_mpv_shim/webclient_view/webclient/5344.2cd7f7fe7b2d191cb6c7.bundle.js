(self.webpackChunk=self.webpackChunk||[]).push([[5344],{85344:function(e,t,n){"use strict";n.r(t);var r=n(83094),a=n(47005);function i(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function s(e){return e.changedTouches||e.targetTouches||e.touches}var l=function(){function e(t,n){var i,l,u,c,o,v;!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e);var h=this,p=(n=n||{}).swipeXThreshold||50,f=n.swipeYThreshold||50,d=n.ignoreTagNames||[],g=function(e){var t=s(e)[0];if(i=null,l=0,u=0,c=null,o=null,v=!1,t){var n=t.target;if(r.ZP.parentWithTag(n,d))return;i=n,l=t.clientX,u=t.clientY}},E=function(e){var t="touchmove"===e.type;if(i){var r,d,g,E,m=s(e)[0];m?(g=m.clientX||0,E=m.clientY||0,r=g-(l||0),d=E-(u||0)):(r=0,d=0);var w=null==c?r:r-c,b=null==o?d:d-o;c=r,o=d,r>p&&Math.abs(d)<30?a.Events.trigger(h,"swiperight",[i]):r<0-p&&Math.abs(d)<30?a.Events.trigger(h,"swipeleft",[i]):(d<0-f||v)&&Math.abs(r)<30?(v=!0,a.Events.trigger(h,"swipeup",[i,{deltaY:d,deltaX:r,clientX:g,clientY:E,currentDeltaX:w,currentDeltaY:b}])):(d>f||v)&&Math.abs(r)<30&&(v=!0,a.Events.trigger(h,"swipedown",[i,{deltaY:d,deltaX:r,clientX:g,clientY:E,currentDeltaX:w,currentDeltaY:b}])),t&&n.preventDefaultOnMove&&e.preventDefault()}t||(i=null,l=0,u=0,c=null,o=null,v=!1)};this.touchStart=g,this.touchEnd=E,r.ZP.addEventListener(t,"touchstart",g,{passive:!0}),n.triggerOnMove&&r.ZP.addEventListener(t,"touchmove",E,{passive:!n.preventDefaultOnMove}),r.ZP.addEventListener(t,"touchend",E,{passive:!0}),r.ZP.addEventListener(t,"touchcancel",E,{passive:!0})}var t,n;return t=e,(n=[{key:"destroy",value:function(){var e=this.elem;if(e){var t=this.touchStart,n=this.touchEnd;r.ZP.removeEventListener(e,"touchstart",t,{passive:!0}),r.ZP.removeEventListener(e,"touchmove",n,{passive:!0}),r.ZP.removeEventListener(e,"touchend",n,{passive:!0}),r.ZP.removeEventListener(e,"touchcancel",n,{passive:!0})}this.touchStart=null,this.touchEnd=null,this.elem=null}}])&&i(t.prototype,n),e}();t.default=l}}]);