(self.webpackChunk=self.webpackChunk||[]).push([[2831],{48850:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return y}}),r(15610),r(72410),r(63238),r(61418),r(40895),r(17460),r(72482),r(5769);var n=r(6594),a=r(2587),i=r(17146),o=r(66056),l=r(61097),s=r(28978),u=r(53754);function c(e,t){var r;if("undefined"==typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(r=function(e,t){if(e){if("string"==typeof e)return d(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?d(e,t):void 0}}(e))||t&&e&&"number"==typeof e.length){r&&(e=r);var n=0,a=function(){};return{s:a,n:function(){return n>=e.length?{done:!0}:{done:!1,value:e[n++]}},e:function(e){throw e},f:a}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var i,o=!0,l=!1;return{s:function(){r=e[Symbol.iterator]()},n:function(){var e=r.next();return o=e.done,e},e:function(e){l=!0,i=e},f:function(){try{o||null==r.return||r.return()}finally{if(l)throw i}}}}function d(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function y(e,t,d){var y=this;function m(e){var r=f(e),n=g[r];return n||(n=g[r]={query:{SortBy:"SortName",SortOrder:"Ascending",IncludeItemTypes:"BoxSet",Recursive:!0,Fields:"PrimaryImageAspectRatio,SortName",ImageTypeLimit:1,EnableImageTypes:"Primary,Backdrop,Banner,Thumb",StartIndex:0},view:a.ZP.getSavedView(r)||"Poster"},s.libraryPageSize()>0&&(n.query.Limit=s.libraryPageSize()),n.query.ParentId=t.topParentId,a.ZP.loadSavedQueryValues(r,n.query)),n}function v(e){return m(e).query}function f(e){return e.savedQueryKey||(e.savedQueryKey=a.ZP.getSavedQueryKey("moviecollections")),e.savedQueryKey}var b=function(){var e=y.getCurrentViewStyle(),t=d.querySelector(".itemsContainer");"List"==e?(t.classList.add("vertical-list"),t.classList.remove("vertical-wrap")):(t.classList.remove("vertical-list"),t.classList.add("vertical-wrap")),t.innerHTML=""},h=function e(t){n.ZP.show(),S=!0;var m=v(t);ApiClient.getItems(ApiClient.getCurrentUserId(),m).then((function(v){function b(){S||(s.libraryPageSize()>0&&(m.StartIndex+=m.Limit),e(d))}function h(){S||(s.libraryPageSize()>0&&(m.StartIndex=Math.max(0,m.StartIndex-m.Limit)),e(d))}var g;window.scrollTo(0,0);var p=a.ZP.getQueryPagingHtml({startIndex:m.StartIndex,limit:m.Limit,totalRecordCount:v.TotalRecordCount,showLimit:!1,updatePageSizeSetting:!1,addLayoutButton:!1,sortButton:!1,filterButton:!1}),w=y.getCurrentViewStyle();g="Thumb"==w?l.default.getCardsHtml({items:v.Items,shape:"backdrop",preferThumb:!0,context:"movies",overlayPlayButton:!0,centerText:!0,showTitle:!0}):"ThumbCard"==w?l.default.getCardsHtml({items:v.Items,shape:"backdrop",preferThumb:!0,context:"movies",lazy:!0,cardLayout:!0,showTitle:!0}):"Banner"==w?l.default.getCardsHtml({items:v.Items,shape:"banner",preferBanner:!0,context:"movies",lazy:!0}):"List"==w?o.Z.getListViewHtml({items:v.Items,context:"movies",sortBy:m.SortBy}):"PosterCard"==w?l.default.getCardsHtml({items:v.Items,shape:"auto",context:"movies",showTitle:!0,centerText:!1,cardLayout:!0}):l.default.getCardsHtml({items:v.Items,shape:"auto",context:"movies",centerText:!0,overlayPlayButton:!0,showTitle:!0});var P,L=d.querySelectorAll(".paging"),I=c(L);try{for(I.s();!(P=I.n()).done;)P.value.innerHTML=p}catch(e){I.e(e)}finally{I.f()}var C,B=c(L=d.querySelectorAll(".btnNextPage"));try{for(B.s();!(C=B.n()).done;)C.value.addEventListener("click",b)}catch(e){B.e(e)}finally{B.f()}var k,A=c(L=d.querySelectorAll(".btnPreviousPage"));try{for(A.s();!(k=A.n()).done;)k.value.addEventListener("click",h)}catch(e){A.e(e)}finally{A.f()}v.Items.length||(g="",g+='<div class="noItemsMessage centerMessage">',g+="<h1>"+u.ZP.translate("MessageNothingHere")+"</h1>",g+="<p>"+u.ZP.translate("MessageNoCollectionsAvailable")+"</p>",g+="</div>");var T=d.querySelector(".itemsContainer");T.innerHTML=g,i.default.lazyChildren(T),a.ZP.saveQueryValues(f(t),m),n.ZP.hide(),S=!1,Promise.resolve().then(r.bind(r,6610)).then((function(e){e.default.autoFocus(t)}))}))},g={},S=!1;this.getCurrentViewStyle=function(){return m(d).view},function(e){e.querySelector(".btnSort").addEventListener("click",(function(t){a.ZP.showSortMenu({items:[{name:u.ZP.translate("Name"),id:"SortName"},{name:u.ZP.translate("OptionImdbRating"),id:"CommunityRating,SortName"},{name:u.ZP.translate("OptionDateAdded"),id:"DateCreated,SortName"},{name:u.ZP.translate("OptionParentalRating"),id:"OfficialRating,SortName"},{name:u.ZP.translate("OptionReleaseDate"),id:"PremiereDate,SortName"}],callback:function(){v(e).StartIndex=0,h(e)},query:v(e),button:t.target})}));var t=e.querySelector(".btnSelectView");t.addEventListener("click",(function(e){a.ZP.showLayoutMenu(e.target,this.getCurrentViewStyle(),"List,Poster,PosterCard,Thumb,ThumbCard".split(","))})),t.addEventListener("layoutchange",(function(t){var r=t.detail.viewStyle;m(e).view=r,a.ZP.saveViewSetting(f(e),r),v(e).StartIndex=0,b(),h(e)})),e.querySelector(".btnNewCollection").addEventListener("click",(function(){r.e(6372).then(r.bind(r,86372)).then((function(e){new(0,e.default)({items:[],serverId:ApiClient.serverInfo().Id})}))}))}(d),b(),this.renderTab=function(){h(d)},this.destroy=function(){}}r(51547)},2587:function(e,t,r){"use strict";r(5769),r(61013),r(48410),r(63238),r(61418),r(17460),r(911),r(72482),r(14078);var n=r(28978),a=r(53754);function i(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var o={getSavedQueryKey:function(e){return window.location.href.split("#")[0]+(e||"")},loadSavedQueryValues:function(e,t){var r=n.get(e);return r?(r=JSON.parse(r),Object.assign(t,r)):t},saveQueryValues:function(e,t){var r={};t.SortBy&&(r.SortBy=t.SortBy),t.SortOrder&&(r.SortOrder=t.SortOrder),n.set(e,JSON.stringify(r))},saveViewSetting:function(e,t){n.set(e+"-_view",t)},getSavedView:function(e){return n.get(e+"-_view")},showLayoutMenu:function(e,t,n){var i=!0;n||(i=!1,n=(n=e.getAttribute("data-layouts"))?n.split(","):["List","Poster","PosterCard","Thumb","ThumbCard"]);var o=n.map((function(e){return{name:a.ZP.translate(e),id:e,selected:t==e}}));Promise.resolve().then(r.bind(r,32465)).then((function(t){t.default.show({items:o,positionTo:e,callback:function(t){e.dispatchEvent(new CustomEvent("layoutchange",{detail:{viewStyle:t},bubbles:!0,cancelable:!1})),i||window.$&&$(e).trigger("layoutchange",[t])}})}))},getQueryPagingHtml:function(e){var t=e.startIndex,r=e.limit,n=e.totalRecordCount,i="",o=Math.min(t+r,n),l=r<n;return i+='<div class="listPaging">',l&&(i+='<span style="vertical-align:middle;">',i+=a.ZP.translate("ListPaging",n?t+1:0,o,n),i+="</span>"),(l||e.viewButton||e.filterButton||e.sortButton||e.addLayoutButton)&&(i+='<div style="display:inline-block;">',l&&(i+='<button is="paper-icon-button-light" class="btnPreviousPage autoSize" '+(t?"":"disabled")+'><span class="material-icons arrow_back"></span></button>',i+='<button is="paper-icon-button-light" class="btnNextPage autoSize" '+(t+r>=n?"disabled":"")+'><span class="material-icons arrow_forward"></span></button>'),e.addLayoutButton&&(i+='<button is="paper-icon-button-light" title="'+a.ZP.translate("ButtonSelectView")+'" class="btnChangeLayout autoSize" data-layouts="'+(e.layouts||"")+'" onclick="LibraryBrowser.showLayoutMenu(this, \''+(e.currentLayout||"")+'\');"><span class="material-icons view_comfy"></span></button>'),e.sortButton&&(i+='<button is="paper-icon-button-light" class="btnSort autoSize" title="'+a.ZP.translate("Sort")+'"><span class="material-icons sort_by_alpha"></span></button>'),e.filterButton&&(i+='<button is="paper-icon-button-light" class="btnFilter autoSize" title="'+a.ZP.translate("Filter")+'"><span class="material-icons filter_list"></span></button>'),i+="</div>"),i+"</div>"},showSortMenu:function(e){Promise.all([Promise.resolve().then(r.bind(r,1115)),r.e(1674).then(r.bind(r,21674))]).then((function(t){var r=function(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e)){var r=[],n=!0,a=!1,i=void 0;try{for(var o,l=e[Symbol.iterator]();!(n=(o=l.next()).done)&&(r.push(o.value),!t||r.length!==t);n=!0);}catch(e){a=!0,i=e}finally{try{n||null==l.return||l.return()}finally{if(a)throw i}}return r}}(e,t)||function(e,t){if(e){if("string"==typeof e)return i(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?i(e,t):void 0}}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}(t,1)[0].default;function n(){var t=this.value;if(this.checked){var r=e.query.SortBy!=t;e.query.SortBy=t.replace("_",","),e.query.StartIndex=0,e.callback&&r&&e.callback()}}function o(){var t=this.value;if(this.checked){var r=e.query.SortOrder!=t;e.query.SortOrder=t,e.query.StartIndex=0,e.callback&&r&&e.callback()}}var l=r.createDialog({removeOnClose:!0,modal:!1,entryAnimationDuration:160,exitAnimationDuration:200});l.classList.add("ui-body-a"),l.classList.add("background-theme-a"),l.classList.add("formDialog");var s,u,c,d="";for(d+='<div style="margin:0;padding:1.25em 1.5em 1.5em;">',d+='<h2 style="margin:0 0 .5em;">',d+=a.ZP.translate("HeaderSortBy"),d+="</h2>",d+="<div>",s=0,u=e.items.length;s<u;s++){var y=e.items[s],m=y.id.replace(",","_");c=(e.query.SortBy||"").replace(",","_")==m?" checked":"",d+='<label class="radio-label-block"><input type="radio" is="emby-radio" name="SortBy" data-id="'+y.id+'" value="'+m+'" class="menuSortBy" '+c+" /><span>"+y.name+"</span></label>"}d+="</div>",d+='<h2 style="margin: 1em 0 .5em;">',d+=a.ZP.translate("HeaderSortOrder"),d+="</h2>",d+="<div>",d+='<label class="radio-label-block"><input type="radio" is="emby-radio" name="SortOrder" value="Ascending" class="menuSortOrder" '+(c="Ascending"==e.query.SortOrder?" checked":"")+" /><span>"+a.ZP.translate("Ascending")+"</span></label>",d+='<label class="radio-label-block"><input type="radio" is="emby-radio" name="SortOrder" value="Descending" class="menuSortOrder" '+(c="Descending"==e.query.SortOrder?" checked":"")+" /><span>"+a.ZP.translate("Descending")+"</span></label>",d+="</div>",d+="</div>",l.innerHTML=d,r.open(l);var v=l.querySelectorAll(".menuSortBy");for(s=0,u=v.length;s<u;s++)v[s].addEventListener("change",n);var f=l.querySelectorAll(".menuSortOrder");for(s=0,u=f.length;s<u;s++)f[s].addEventListener("change",o)}))}};window.LibraryBrowser=o,t.ZP=o}}]);