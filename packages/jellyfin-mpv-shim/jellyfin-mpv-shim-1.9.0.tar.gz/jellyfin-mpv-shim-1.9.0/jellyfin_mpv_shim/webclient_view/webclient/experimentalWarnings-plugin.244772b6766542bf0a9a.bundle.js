(self.webpackChunk=self.webpackChunk||[]).push([[5004],{55687:function(e,a,t){"use strict";t.r(a),t(63238),t(61418);var n=t(53754),r=t(28978),i=t(38102),l=t(61642);function o(e,a){for(var t=0;t<a.length;t++){var n=a[t];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function s(e,a,t){if(i.M.supports(t))return Promise.resolve();var n=new Date;return a+=n.getFullYear()+"-w"+function(e){var a=new Date(Date.UTC(e.getFullYear(),e.getMonth(),e.getDate())),t=a.getUTCDay()||7;a.setUTCDate(a.getUTCDate()+4-t);var n=new Date(Date.UTC(a.getUTCFullYear(),0,1));return Math.ceil(((a-n)/864e5+1)/7)}(n),"1"===r.get(a,!1)?Promise.resolve():(r.set(a,"1",!1),(0,l.Z)(e).catch((function(){})))}var u=function(){function e(){!function(e,a){if(!(e instanceof a))throw new TypeError("Cannot call a class as a function")}(this,e),this.name="Experimental playback warnings",this.type="preplayintercept",this.id="expirementalplaybackwarnings"}var a,t;return a=e,(t=[{key:"intercept",value:function(e){var a=e.item;return a?"Iso"===a.VideoType?s(n.ZP.translate("UnsupportedPlayback"),"isoexpirementalinfo","nativeisoplayback"):"BluRay"===a.VideoType?s(n.ZP.translate("UnsupportedPlayback"),"blurayexpirementalinfo","nativeblurayplayback"):"Dvd"===a.VideoType?s(n.ZP.translate("UnsupportedPlayback"),"dvdexpirementalinfo","nativedvdplayback"):Promise.resolve():Promise.resolve()}}])&&o(a.prototype,t),e}();a.default=u}}]);