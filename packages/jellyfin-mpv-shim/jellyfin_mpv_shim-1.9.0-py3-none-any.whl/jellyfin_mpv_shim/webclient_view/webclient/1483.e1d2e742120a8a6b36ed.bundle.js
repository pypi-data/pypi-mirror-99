(self.webpackChunk=self.webpackChunk||[]).push([[1483],{1483:function(e,t,i){"use strict";i.r(t),i.d(t,{default:function(){return x}}),i(25901),i(92189),i(63238),i(43512),i(61418),i(911),i(5769);var o=i(1115),n=i(12392),a=i(78695),s=i(27515),r=i(47518),l=i(38102),d=i(83094),c=i(1892),u=i.n(c),p=i(37637),h=(u()(p.Z,{insert:"head",singleton:!1}),p.Z.locals,i(56561),i(21865),i(53913)),f=i(98566),m=(i(60005),i(30754)),g=i.n(m),v=d.ZP.whichTransitionEvent(),w=r.Z.safari;function b(e,t){var i=h.Z.getApiClient(e.ServerId),o={};return e.BackdropImageTags&&e.BackdropImageTags.length?function(e,t,i){return(t=t||{}).type=t.type||"Backdrop",t.maxWidth||t.width||t.maxHeight||t.height||(t.quality=100),e.BackdropImageTags&&e.BackdropImageTags.length?(t.tag=e.BackdropImageTags[0],i.getScaledImageUrl(e.Id,t)):null}(e,o,i):"Photo"===e.MediaType&&t&&t.Policy.EnableContentDownloading?i.getItemDownloadUrl(e.Id):(o.type="Primary",function(e,t,i){return(t=t||{}).type=t.type||"Primary","string"==typeof e?i.getScaledImageUrl(e,t):e.ImageTags&&e.ImageTags[t.type]?(t.tag=e.ImageTags[t.type],i.getScaledImageUrl(e.Id,t)):"Primary"===t.type&&e.AlbumId&&e.AlbumPrimaryImageTag?(t.tag=e.AlbumPrimaryImageTag,i.getScaledImageUrl(e.AlbumId,t)):null}(e,o,i))}function y(e,t,i,o){return'<button is="paper-icon-button-light" class="autoSize '+t+'"'+(i?"":' tabindex="-1"')+(o=o?" autofocus":"")+'><span class="material-icons slideshowButtonIcon '+e+'"></span></button>'}function S(e){try{l.M.setUserScalable(e)}catch(e){console.error("error in appHost.setUserScalable: "+e)}}function x(e){var t,r,d,c,u;function p(){var e=r.querySelector(".btnSlideshowPause .material-icons");e&&e.classList.replace("play_arrow","pause")}function h(){var e=r.querySelector(".btnSlideshowPause .material-icons");e&&e.classList.replace("pause","play_arrow")}function m(e,t,i,o){var n=o.querySelector(".swiper-zoom-fakeimg");n&&(n.style.width=n.style.height=100*t+"%",t>1?n.classList.contains("swiper-zoom-fakeimg-hidden")&&setTimeout((function(){var e=function e(){i.removeEventListener(v,e),n.classList.remove("swiper-zoom-fakeimg-hidden")};parseFloat(i.style.transitionDuration.replace(/[a-z]/i,""))>0?i.addEventListener(v,e):e()}),0):n.classList.add("swiper-zoom-fakeimg-hidden"))}function x(e,t){return d.slides?k(e):function(e){return k({originalImage:b(e,d.user),Id:e.Id,ServerId:e.ServerId})}(e)}function k(e){var t="";return t+='<div class="swiper-slide" data-original="'+e.originalImage+'" data-itemid="'+e.Id+'" data-serverid="'+e.ServerId+'">',t+='<div class="swiper-zoom-container">',w&&(t+='<div class="swiper-zoom-fakeimg swiper-zoom-fakeimg-hidden" style="background-image: url(\''.concat(e.originalImage,"')\"></div>")),t+='<img src="'+e.originalImage+'" class="swiper-slide-img">',t+="</div>",(e.title||e.subtitle)&&(t+='<div class="slideText">',t+='<div class="slideTextInner">',e.title&&(t+='<h1 class="slideTitle">',t+=e.title,t+="</h1>"),e.description&&(t+='<div class="slideSubtitle">',t+=e.description,t+="</div>"),t+="</div>",t+="</div>"),t+"</div>"}function I(){if(t){var e=document.querySelector(".swiper-slide-active");return e?{url:e.getAttribute("data-original"),shareUrl:e.getAttribute("data-original"),itemId:e.getAttribute("data-itemid"),serverId:e.getAttribute("data-serverid")}:null}return null}function B(){var e=I();i.e(4111).then(i.bind(i,84111)).then((function(t){t.download([e])}))}function q(){var e=I();navigator.share({url:e.shareUrl})}function E(){g().isFullscreen||g().request(),P(!0)}function L(){g().isFullscreen&&g().exit(),P(!1)}function P(e){var t=r.querySelector(".btnFullscreen"),i=r.querySelector(".btnFullscreenExit");t&&t.classList.toggle("hide",e),i&&i.classList.toggle("hide",!e)}function T(){t.autoplay&&t.autoplay.start()}function z(){t.autoplay&&t.autoplay.stop()}function A(){r.querySelector(".btnSlideshowPause .material-icons").classList.contains("pause")?z():T()}function F(){L(),t&&(t.destroy(!0,!0),t=null),n.ZP.off(window,N),document.removeEventListener(window.PointerEvent?"pointermove":"mousemove",U)}function Z(){var e=r.querySelector(".slideshowBottomBar");e&&_(e,"down");var t=r.querySelector(".topActionButtons");t&&_(t,"up");var i=r.querySelector(".btnSlideshowPrevious");i&&_(i,"left");var o=r.querySelector(".btnSlideshowNext");o&&_(o,"right"),c&&(clearTimeout(c),c=null),c=setTimeout(C,3e3)}function C(){var e=r.querySelector(".slideshowBottomBar");e&&M(e,"down");var t=r.querySelector(".topActionButtons");t&&M(t,"up");var i=r.querySelector(".btnSlideshowPrevious");i&&M(i,"left");var o=r.querySelector(".btnSlideshowNext");o&&M(o,"right")}function D(e,t,i){var o={transform:"translate(0,0)",opacity:"1"},n={opacity:".3"};return"up"===e||"down"===e?n.transform="translate3d(0,"+i.offsetHeight*("down"===e?1:-1)+"px,0)":"left"!==e&&"right"!==e||(n.transform="translate3d("+i.offsetWidth*("right"===e?1:-1)+"px,0,0)"),t?[o,n]:[n,o]}function _(e,t){if(e.classList.contains("hide")){e.classList.remove("hide");var i=function(){var t=e.querySelector(".btnSlideshowPause");t&&s.Z.focus(t)};e.animate?requestAnimationFrame((function(){var o=D(t,!1,e);e.animate(o,{duration:300,iterations:1,easing:"ease-out"}).onfinish=i})):i()}}function M(e,t){if(!e.classList.contains("hide")){var i=function(){e.classList.add("hide")};e.animate?requestAnimationFrame((function(){var o=D(t,!0,e);e.animate(o,{duration:300,iterations:1,easing:"ease-out"}).onfinish=i})):i()}}function U(e){if("mouse"===(e.pointerType||(a.Z.mobile?"touch":"mouse"))){var t=e.screenX||0,i=e.screenY||0,o=u;if(!o)return void(u={x:t,y:i});if(Math.abs(t-o.x)<10&&Math.abs(i-o.y)<10)return;o.x=t,o.y=i,Z()}}function N(e){switch(e.detail.command){case"up":case"down":case"select":case"menu":case"info":Z();break;case"play":T();break;case"pause":z();break;case"playpause":A()}}this.show=function(){!function(e){d=e,(r=o.default.createDialog({exitAnimationDuration:e.interactive?400:800,size:"fullscreen",autoFocus:!1,scrollY:!1,exitAnimation:"fadeout",removeOnClose:!0})).classList.add("slideshowDialog");var i="";if(i+='<div class="slideshowSwiperContainer"><div class="swiper-wrapper"></div></div>',e.interactive&&!a.Z.tv){var s=a.Z.mobile;i+=y("keyboard_arrow_left","btnSlideshowPrevious slideshowButton hide-mouse-idle-tv",!1),i+=y("keyboard_arrow_right","btnSlideshowNext slideshowButton hide-mouse-idle-tv",!1),i+='<div class="topActionButtons">',s&&(l.M.supports("filedownload")&&e.user&&e.user.Policy.EnableContentDownloading&&(i+=y("file_download","btnDownload slideshowButton",!0)),l.M.supports("sharing")&&(i+=y("share","btnShare slideshowButton",!0)),g().isEnabled&&(i+=y("fullscreen","btnFullscreen",!0),i+=y("fullscreen_exit","btnFullscreenExit hide",!0))),i+=y("close","slideshowButton btnSlideshowExit hide-mouse-idle-tv",!1),i+="</div>",s||(i+='<div class="slideshowBottomBar hide">',i+=y("play_arrow","btnSlideshowPause slideshowButton",!0,!0),l.M.supports("filedownload")&&e.user&&e.user.Policy.EnableContentDownloading&&(i+=y("file_download","btnDownload slideshowButton",!0)),l.M.supports("sharing")&&(i+=y("share","btnShare slideshowButton",!0)),g().isEnabled&&(i+=y("fullscreen","btnFullscreen",!0),i+=y("fullscreen_exit","btnFullscreenExit hide",!0)),i+="</div>")}else i+='<div class="slideshowImage"></div><h1 class="slideshowImageText"></h1>';if(r.innerHTML=i,e.interactive&&!a.Z.tv){r.querySelector(".btnSlideshowExit").addEventListener("click",(function(e){o.default.close(r)}));var c=r.querySelector(".btnSlideshowPause");c&&c.addEventListener("click",A);var u=r.querySelector(".btnDownload");u&&u.addEventListener("click",B);var v=r.querySelector(".btnShare");v&&v.addEventListener("click",q);var b=r.querySelector(".btnFullscreen");b&&b.addEventListener("click",E);var k=r.querySelector(".btnFullscreenExit");k&&k.addEventListener("click",L),g().isEnabled&&g().on("change",(function(){P(g().isFullscreen)}))}if(S(!0),o.default.open(r).then((function(){S(!1)})),n.ZP.on(window,N),document.addEventListener(window.PointerEvent?"pointermove":"mousemove",U),r.addEventListener("close",F),function(e,i){var o;o=d.slides?d.slides:d.items,(t=new f.t(e.querySelector(".slideshowSwiperContainer"),{direction:"horizontal",loop:!1,zoom:{minRatio:1,toggle:!0},autoplay:!i.interactive,keyboard:{enabled:!0},preloadImages:!0,slidesPerView:1,slidesPerColumn:1,initialSlide:i.startIndex||0,speed:240,navigation:{nextEl:".btnSlideshowNext",prevEl:".btnSlideshowPrevious"},virtual:{slides:o,cache:!0,renderSlide:x,addSlidesBefore:1,addSlidesAfter:1}})).on("autoplayStart",p),t.on("autoplayStop",h),w&&t.on("zoomChange",m)}(r,e),a.Z.desktop){var I=r.querySelector(".topActionButtons");I&&I.classList.add("hide")}var T=r.querySelector(".btnSlideshowPrevious");T&&T.classList.add("hide");var z=r.querySelector(".btnSlideshowNext");z&&z.classList.add("hide")}(e)},this.hide=function(){r&&o.default.close(r)}}},37637:function(e,t,i){"use strict";var o=i(93476),n=i.n(o)()((function(e){return e[1]}));n.push([e.id,".slideshowDialog,.slideshowSwiperContainer,.swiper-slide,.swiper-wrapper{background:#000}.slideshowImage,.slideshowSwiperContainer{position:fixed;top:0;right:0;left:0;bottom:0;background-position:50%;background-size:contain;background-repeat:no-repeat;margin:0!important;color:#fff;line-height:normal}.slideshowImage-cover{background-size:cover}.slideshowImageText{position:fixed;bottom:.25em;right:.5em;color:#fff;z-index:1002;font-weight:400;text-shadow:3px 3px 0 #000,-1px -1px 0 #000,1px -1px 0 #000,-1px 1px 0 #000,1px 1px 0 #000}.slideshowButtonIcon{color:#fff;opacity:.7}.btnSlideshowPrevious{left:.5vh;top:45vh;z-index:1002;position:absolute}.btnSlideshowNext{top:45vh}.btnSlideshowNext,.topActionButtons{right:.5vh;z-index:1002;position:absolute}.topActionButtons{top:.5vh}.slideshowBottomBar{bottom:0;-webkit-justify-content:center;justify-content:center}.slideshowBottomBar,.slideshowTopBar{position:fixed;left:0;right:0;background-color:rgba(0,0,0,.7);color:#fff;padding:.5%;display:-webkit-flex;display:flex;-webkit-flex-direction:row;flex-direction:row;-webkit-align-items:center;align-items:center}.slideshowTopBar{top:0;text-align:right;-webkit-justify-content:flex-end;justify-content:flex-end}.slideshowExtraButtons{margin-left:auto;text-align:right}.slideText{position:absolute;left:0;right:0;bottom:10vh;text-align:center}.slideTextInner{margin:0 auto;max-width:60%;background:rgba(0,0,0,.8);display:inline-block;padding:.5em 1em;border-radius:.25em}.slideTitle{margin:0 0 .25em}.slideSubtitle{color:#ccc}.swiper-zoom-fakeimg{position:absolute;top:50%;left:50%;-webkit-transform:translate(-50%,-50%);transform:translate(-50%,-50%);background-position:50% 50%;background-repeat:no-repeat;background-size:contain;z-index:1;pointer-events:none}.swiper-zoom-fakeimg-hidden{display:none}",""]),t.Z=n}}]);