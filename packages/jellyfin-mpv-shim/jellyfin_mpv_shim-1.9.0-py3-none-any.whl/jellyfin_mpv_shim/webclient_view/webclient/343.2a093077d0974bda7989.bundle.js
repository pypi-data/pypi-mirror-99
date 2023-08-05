(self.webpackChunk=self.webpackChunk||[]).push([[343],{28046:function(e,t,a){"use strict";a(23938),a(98010),a(95374),a(95623),a(27471),a(5769),a(61013),a(72410),a(69217),a(63238),a(32081),a(61418),a(61514),a(17460),a(55849),a(14078),a(86248);var i,r,n=a(53754),c=a(83094),l=(a(65219),a(50447),a(30983),a(80594)),s=a.n(l);function o(e,t,a,i,r,n,c){try{var l=e[n](c),s=l.value}catch(e){return void a(e)}l.done?t(s):Promise.resolve(s).then(i,r)}function d(e){return function(){var t=this,a=arguments;return new Promise((function(i,r){var n=e.apply(t,a);function c(e){o(n,i,r,c,l,"next",e)}function l(e){o(n,i,r,c,l,"throw",e)}c(void 0)}))}}function u(e){return ApiClient.getCultures().then((function(t){!function(e,t){var a="";a+="<option value=''></option>";for(var i=0;i<t.length;i++){var r=t[i];a+="<option value='".concat(r.TwoLetterISOLanguageName,"'>").concat(r.DisplayName,"</option>")}e.innerHTML=a}(e.querySelector("#selectLanguage"),t),function(e,t){for(var a="",i=0;i<t.length;i++){var r=t[i];a+='<label><input type="checkbox" is="emby-checkbox" class="chkSubtitleLanguage" data-lang="'.concat(r.ThreeLetterISOLanguageName.toLowerCase(),'" /><span>').concat(r.DisplayName,"</span></label>")}e.innerHTML=a}(e.querySelector(".subtitleDownloadLanguages"),t)}))}function p(e){return ApiClient.getCountries().then((function(t){var a="";a+="<option value=''></option>";for(var i=0;i<t.length;i++){var r=t[i];a+="<option value='".concat(r.TwoLetterISORegionName,"'>").concat(r.DisplayName,"</option>")}e.innerHTML=a}))}function h(e){var t="";t+="<option value='0'>".concat(n.ZP.translate("Never"),"</option>"),t+=[30,60,90].map((function(e){return"<option value='".concat(e,"'>").concat(n.ZP.translate("EveryNDays",e),"</option>")})).join(""),e.innerHTML=t}function b(e,t){var a="",i=e.querySelector(".metadataReaders");if(t.length<1)return i.innerHTML="",i.classList.add("hide"),!1;a+='<h3 class="checkboxListLabel">'.concat(n.ZP.translate("LabelMetadataReaders"),"</h3>"),a+='<div class="checkboxList paperList checkboxList-paperList">';for(var r=0;r<t.length;r++){var c=t[r];a+='<div class="listItem localReaderOption sortableOption" data-pluginname="'.concat(c.Name,'">'),a+='<span class="listItemIcon material-icons live_tv"></span>',a+='<div class="listItemBody">',a+='<h3 class="listItemBodyText">',a+=c.Name,a+="</h3>",a+="</div>",r>0?a+='<button type="button" is="paper-icon-button-light" title="'.concat(n.ZP.translate("Up"),'" class="btnSortableMoveUp btnSortable" data-pluginindex="').concat(r,'"><span class="material-icons keyboard_arrow_up"></span></button>'):t.length>1&&(a+='<button type="button" is="paper-icon-button-light" title="'.concat(n.ZP.translate("Down"),'" class="btnSortableMoveDown btnSortable" data-pluginindex="').concat(r,'"><span class="material-icons keyboard_arrow_down"></span></button>')),a+="</div>"}return a+="</div>",a+='<div class="fieldDescription">'.concat(n.ZP.translate("LabelMetadataReadersHelp"),"</div>"),t.length<2?i.classList.add("hide"):i.classList.remove("hide"),i.innerHTML=a,!0}function m(e,t){var a="",i=e.MetadataFetchers;return(i=_(i,t.MetadataFetcherOrder||[])).length?(a+='<div class="metadataFetcher" data-type="'+e.Type+'">',a+='<h3 class="checkboxListLabel">'+n.ZP.translate("LabelTypeMetadataDownloaders",n.ZP.translate(e.Type))+"</h3>",a+='<div class="checkboxList paperList checkboxList-paperList">',i.forEach((function(e,r){a+='<div class="listItem metadataFetcherItem sortableOption" data-pluginname="'+e.Name+'">';var c=(t.MetadataFetchers?t.MetadataFetchers.includes(e.Name):e.DefaultEnabled)?' checked="checked"':"";a+='<label class="listItemCheckboxContainer"><input type="checkbox" is="emby-checkbox" class="chkMetadataFetcher" data-pluginname="'+e.Name+'" '+c+"><span></span></label>",a+='<div class="listItemBody">',a+='<h3 class="listItemBodyText">',a+=e.Name,a+="</h3>",a+="</div>",r>0?a+='<button type="button" is="paper-icon-button-light" title="'+n.ZP.translate("Up")+'" class="btnSortableMoveUp btnSortable" data-pluginindex="'+r+'"><span class="material-icons keyboard_arrow_up"></span></button>':i.length>1&&(a+='<button type="button" is="paper-icon-button-light" title="'+n.ZP.translate("Down")+'" class="btnSortableMoveDown btnSortable" data-pluginindex="'+r+'"><span class="material-icons keyboard_arrow_down"></span></button>'),a+="</div>"})),a+="</div>",a+='<div class="fieldDescription">'+n.ZP.translate("LabelMetadataDownloadersHelp")+"</div>",a+="</div>"):a}function v(e,t){for(var a=e.TypeOptions||[],i=0;i<a.length;i++){var r=a[i];if(r.Type===t)return r}return null}function y(e,t,a){for(var i="",r=e.querySelector(".metadataFetchers"),n=0;n<t.TypeOptions.length;n++){var c=t.TypeOptions[n];i+=m(c,v(a,c.Type)||{})}return r.innerHTML=i,i?(r.classList.remove("hide"),e.querySelector(".fldAutoRefreshInterval").classList.remove("hide"),e.querySelector(".fldMetadataLanguage").classList.remove("hide"),e.querySelector(".fldMetadataCountry").classList.remove("hide")):(r.classList.add("hide"),e.querySelector(".fldAutoRefreshInterval").classList.add("hide"),e.querySelector(".fldMetadataLanguage").classList.add("hide"),e.querySelector(".fldMetadataCountry").classList.add("hide")),!0}function k(e,t,a){var i="",r=e.querySelector(".subtitleFetchers"),c=t.SubtitleFetchers;if(!(c=_(c,a.SubtitleFetcherOrder||[])).length)return i;i+='<h3 class="checkboxListLabel">'.concat(n.ZP.translate("LabelSubtitleDownloaders"),"</h3>"),i+='<div class="checkboxList paperList checkboxList-paperList">';for(var l=0;l<c.length;l++){var s=c[l];i+='<div class="listItem subtitleFetcherItem sortableOption" data-pluginname="'.concat(s.Name,'">');var o=(a.DisabledSubtitleFetchers?!a.DisabledSubtitleFetchers.includes(s.Name):s.DefaultEnabled)?' checked="checked"':"";i+='<label class="listItemCheckboxContainer"><input type="checkbox" is="emby-checkbox" class="chkSubtitleFetcher" data-pluginname="'.concat(s.Name,'" ').concat(o,"><span></span></label>"),i+='<div class="listItemBody">',i+='<h3 class="listItemBodyText">',i+=s.Name,i+="</h3>",i+="</div>",l>0?i+='<button type="button" is="paper-icon-button-light" title="'.concat(n.ZP.translate("Up"),'" class="btnSortableMoveUp btnSortable" data-pluginindex="').concat(l,'"><span class="material-icons keyboard_arrow_up"></span></button>'):c.length>1&&(i+='<button type="button" is="paper-icon-button-light" title="'.concat(n.ZP.translate("Down"),'" class="btnSortableMoveDown btnSortable" data-pluginindex="').concat(l,'"><span class="material-icons keyboard_arrow_down"></span></button>')),i+="</div>"}i+="</div>",i+='<div class="fieldDescription">'.concat(n.ZP.translate("SubtitleDownloadersHelp"),"</div>"),r.innerHTML=i}function g(e,t){var a="",i=e.ImageFetchers;if(!(i=_(i,t.ImageFetcherOrder||[])).length)return a;a+='<div class="imageFetcher" data-type="'+e.Type+'">',a+='<div class="flex align-items-center" style="margin:1.5em 0 .5em;">',a+='<h3 class="checkboxListLabel" style="margin:0;">'+n.ZP.translate("HeaderTypeImageFetchers",e.Type)+"</h3>";var r=e.SupportedImageTypes||[];(r.length>1||1===r.length&&"Primary"!==r[0])&&(a+='<button is="emby-button" class="raised btnImageOptionsForType" type="button" style="margin-left:1.5em;font-size:90%;"><span>'+n.ZP.translate("HeaderFetcherSettings")+"</span></button>"),a+="</div>",a+='<div class="checkboxList paperList checkboxList-paperList">';for(var c=0;c<i.length;c++){var l=i[c];a+='<div class="listItem imageFetcherItem sortableOption" data-pluginname="'+l.Name+'">';var s=(t.ImageFetchers?t.ImageFetchers.includes(l.Name):l.DefaultEnabled)?' checked="checked"':"";a+='<label class="listItemCheckboxContainer"><input type="checkbox" is="emby-checkbox" class="chkImageFetcher" data-pluginname="'+l.Name+'" '+s+"><span></span></label>",a+='<div class="listItemBody">',a+='<h3 class="listItemBodyText">',a+=l.Name,a+="</h3>",a+="</div>",c>0?a+='<button type="button" is="paper-icon-button-light" title="'+n.ZP.translate("Up")+'" class="btnSortableMoveUp btnSortable" data-pluginindex="'+c+'"><span class="material-icons keyboard_arrow_up"></span></button>':i.length>1&&(a+='<button type="button" is="paper-icon-button-light" title="'+n.ZP.translate("Down")+'" class="btnSortableMoveDown btnSortable" data-pluginindex="'+c+'"><span class="material-icons keyboard_arrow_down"></span></button>'),a+="</div>"}return a+="</div>",(a+='<div class="fieldDescription">'+n.ZP.translate("LabelImageFetchersHelp")+"</div>")+"</div>"}function S(e,t,a){for(var i="",r=e.querySelector(".imageFetchers"),n=0;n<t.TypeOptions.length;n++){var c=t.TypeOptions[n];i+=g(c,v(a,c.Type)||{})}return r.innerHTML=i,i?(r.classList.remove("hide"),e.querySelector(".chkSaveLocalContainer").classList.remove("hide")):(r.classList.add("hide"),e.querySelector(".chkSaveLocalContainer").classList.add("hide")),!0}function f(e){var t=e.querySelector(".btnSortable"),a=t.querySelector(".material-icons");e.previousSibling?(t.title=n.ZP.translate("Up"),t.classList.add("btnSortableMoveUp"),t.classList.remove("btnSortableMoveDown"),a.classList.remove("keyboard_arrow_down"),a.classList.add("keyboard_arrow_up")):(t.title=n.ZP.translate("Down"),t.classList.remove("btnSortableMoveUp"),t.classList.add("btnSortableMoveDown"),a.classList.remove("keyboard_arrow_up"),a.classList.add("keyboard_arrow_down"))}function L(e){var t,n=c.ZP.parentWithClass(e.target,"btnImageOptionsForType");if(n)return t=c.ZP.parentWithClass(n,"imageFetcher").getAttribute("data-type"),void a.e(3735).then(a.bind(a,53735)).then((function(e){var a=e.default,n=v(i,t);n||(n={Type:t},i.TypeOptions.push(n));var c=v(r||{},t);(new a).show(t,n,c)}));x.call(this,e)}function x(e){var t=c.ZP.parentWithClass(e.target,"btnSortable");if(t){var a=c.ZP.parentWithClass(t,"sortableOption"),i=c.ZP.parentWithClass(a,"paperList");if(t.classList.contains("btnSortableMoveDown")){var r=a.nextSibling;r&&(a.parentNode.removeChild(a),r.parentNode.insertBefore(a,r.nextSibling))}else{var n=a.previousSibling;n&&(a.parentNode.removeChild(a),n.parentNode.insertBefore(a,n))}Array.prototype.forEach.call(i.querySelectorAll(".sortableOption"),f)}}function w(e){e.querySelector(".metadataReaders").addEventListener("click",x),e.querySelector(".subtitleFetchers").addEventListener("click",x),e.querySelector(".metadataFetchers").addEventListener("click",x),e.querySelector(".imageFetchers").addEventListener("click",L)}function C(){return(C=d(regeneratorRuntime.mark((function e(t,a,c){var l;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:i={TypeOptions:[]},r=null,null===c&&t.classList.add("newlibrary"),t.innerHTML=n.ZP.translateHtml(s()),h(t.querySelector("#selectAutoRefreshInterval")),l=[u(t),p(t.querySelector("#selectCountry"))],Promise.all(l).then((function(){return E(t,a).then((function(){c&&q(t,c),w(t)}))}));case 8:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function E(e,t){return"homevideos"===t||"photos"===t?e.querySelector(".chkEnablePhotosContainer").classList.remove("hide"):e.querySelector(".chkEnablePhotosContainer").classList.add("hide"),"tvshows"!==t&&"movies"!==t&&"homevideos"!==t&&"musicvideos"!==t&&"mixed"!==t?e.querySelector(".chapterSettingsSection").classList.add("hide"):e.querySelector(".chapterSettingsSection").classList.remove("hide"),"tvshows"===t?(e.querySelector(".chkAutomaticallyGroupSeriesContainer").classList.remove("hide"),e.querySelector(".fldSeasonZeroDisplayName").classList.remove("hide"),e.querySelector("#txtSeasonZeroName").setAttribute("required","required")):(e.querySelector(".chkAutomaticallyGroupSeriesContainer").classList.add("hide"),e.querySelector(".fldSeasonZeroDisplayName").classList.add("hide"),e.querySelector("#txtSeasonZeroName").removeAttribute("required")),"books"===t||"boxsets"===t||"playlists"===t||"music"===t?e.querySelector(".chkEnableEmbeddedTitlesContainer").classList.add("hide"):e.querySelector(".chkEnableEmbeddedTitlesContainer").classList.remove("hide"),"tvshows"===t?e.querySelector(".chkEnableEmbeddedEpisodeInfosContainer").classList.remove("hide"):e.querySelector(".chkEnableEmbeddedEpisodeInfosContainer").classList.add("hide"),function(e,t){var a=e.classList.contains("newlibrary");return ApiClient.getJSON(ApiClient.getUrl("Libraries/AvailableOptions",{LibraryContentType:t,IsNewLibrary:a})).then((function(t){r=t,e.availableOptions=t,function(e,t){var a="",i=e.querySelector(".metadataSavers");if(!t.length)return i.innerHTML="",i.classList.add("hide"),!1;a+='<h3 class="checkboxListLabel">'.concat(n.ZP.translate("LabelMetadataSavers"),"</h3>"),a+='<div class="checkboxList paperList checkboxList-paperList">';for(var r=0;r<t.length;r++){var c=t[r];a+='<label><input type="checkbox" data-defaultenabled="'.concat(c.DefaultEnabled,'" is="emby-checkbox" class="chkMetadataSaver" data-pluginname="').concat(c.Name,'" ',!1,"><span>").concat(c.Name,"</span></label>")}a+="</div>",a+='<div class="fieldDescription" style="margin-top:.25em;">'.concat(n.ZP.translate("LabelMetadataSaversHelp"),"</div>"),i.innerHTML=a,i.classList.remove("hide")}(e,t.MetadataSavers),b(e,t.MetadataReaders),y(e,t,{}),k(e,t,{}),S(e,t,{}),t.SubtitleFetchers.length?e.querySelector(".subtitleDownloadSettings").classList.remove("hide"):e.querySelector(".subtitleDownloadSettings").classList.add("hide")})).catch((function(){return Promise.resolve()}))}(e,t)}function _(e,t){return(e=e.slice(0)).sort((function(e,a){return(e=t.indexOf(e.Name))<(a=t.indexOf(a.Name))?-1:e>a?1:0})),e}function q(e,t){i=t,r=e.availableOptions,e.querySelector("#selectLanguage").value=t.PreferredMetadataLanguage||"",e.querySelector("#selectCountry").value=t.MetadataCountryCode||"",e.querySelector("#selectAutoRefreshInterval").value=t.AutomaticRefreshIntervalDays||"0",e.querySelector("#txtSeasonZeroName").value=t.SeasonZeroDisplayName||"Specials",e.querySelector(".chkEnablePhotos").checked=t.EnablePhotos,e.querySelector(".chkEnableRealtimeMonitor").checked=t.EnableRealtimeMonitor,e.querySelector(".chkExtractChaptersDuringLibraryScan").checked=t.ExtractChapterImagesDuringLibraryScan,e.querySelector(".chkExtractChapterImages").checked=t.EnableChapterImageExtraction,e.querySelector("#chkSaveLocal").checked=t.SaveLocalMetadata,e.querySelector(".chkAutomaticallyGroupSeries").checked=t.EnableAutomaticSeriesGrouping,e.querySelector("#chkEnableEmbeddedTitles").checked=t.EnableEmbeddedTitles,e.querySelector("#chkEnableEmbeddedEpisodeInfos").checked=t.EnableEmbeddedEpisodeInfos,e.querySelector("#chkSkipIfGraphicalSubsPresent").checked=t.SkipSubtitlesIfEmbeddedSubtitlesPresent,e.querySelector("#chkSaveSubtitlesLocally").checked=t.SaveSubtitlesWithMedia,e.querySelector("#chkSkipIfAudioTrackPresent").checked=t.SkipSubtitlesIfAudioTrackMatches,e.querySelector("#chkRequirePerfectMatch").checked=t.RequirePerfectSubtitleMatch,Array.prototype.forEach.call(e.querySelectorAll(".chkMetadataSaver"),(function(e){e.checked=t.MetadataSavers?t.MetadataSavers.includes(e.getAttribute("data-pluginname")):"true"===e.getAttribute("data-defaultenabled")})),Array.prototype.forEach.call(e.querySelectorAll(".chkSubtitleLanguage"),(function(e){e.checked=!!t.SubtitleDownloadLanguages&&t.SubtitleDownloadLanguages.includes(e.getAttribute("data-lang"))})),b(e,_(e.availableOptions.MetadataReaders,t.LocalMetadataReaderOrder||[])),y(e,e.availableOptions,t),S(e,e.availableOptions,t),k(e,e.availableOptions,t)}t.ZP={embed:function(e,t,a){return C.apply(this,arguments)},setContentType:E,getLibraryOptions:function(e){var t={EnableArchiveMediaFiles:!1,EnablePhotos:e.querySelector(".chkEnablePhotos").checked,EnableRealtimeMonitor:e.querySelector(".chkEnableRealtimeMonitor").checked,ExtractChapterImagesDuringLibraryScan:e.querySelector(".chkExtractChaptersDuringLibraryScan").checked,EnableChapterImageExtraction:e.querySelector(".chkExtractChapterImages").checked,EnableInternetProviders:!0,SaveLocalMetadata:e.querySelector("#chkSaveLocal").checked,EnableAutomaticSeriesGrouping:e.querySelector(".chkAutomaticallyGroupSeries").checked,PreferredMetadataLanguage:e.querySelector("#selectLanguage").value,MetadataCountryCode:e.querySelector("#selectCountry").value,SeasonZeroDisplayName:e.querySelector("#txtSeasonZeroName").value,AutomaticRefreshIntervalDays:parseInt(e.querySelector("#selectAutoRefreshInterval").value),EnableEmbeddedTitles:e.querySelector("#chkEnableEmbeddedTitles").checked,EnableEmbeddedEpisodeInfos:e.querySelector("#chkEnableEmbeddedEpisodeInfos").checked,SkipSubtitlesIfEmbeddedSubtitlesPresent:e.querySelector("#chkSkipIfGraphicalSubsPresent").checked,SkipSubtitlesIfAudioTrackMatches:e.querySelector("#chkSkipIfAudioTrackPresent").checked,SaveSubtitlesWithMedia:e.querySelector("#chkSaveSubtitlesLocally").checked,RequirePerfectSubtitleMatch:e.querySelector("#chkRequirePerfectMatch").checked,MetadataSavers:Array.prototype.map.call(Array.prototype.filter.call(e.querySelectorAll(".chkMetadataSaver"),(function(e){return e.checked})),(function(e){return e.getAttribute("data-pluginname")})),TypeOptions:[]};return t.LocalMetadataReaderOrder=Array.prototype.map.call(e.querySelectorAll(".localReaderOption"),(function(e){return e.getAttribute("data-pluginname")})),t.SubtitleDownloadLanguages=Array.prototype.map.call(Array.prototype.filter.call(e.querySelectorAll(".chkSubtitleLanguage"),(function(e){return e.checked})),(function(e){return e.getAttribute("data-lang")})),function(e,t){t.DisabledSubtitleFetchers=Array.prototype.map.call(Array.prototype.filter.call(e.querySelectorAll(".chkSubtitleFetcher"),(function(e){return!e.checked})),(function(e){return e.getAttribute("data-pluginname")})),t.SubtitleFetcherOrder=Array.prototype.map.call(e.querySelectorAll(".subtitleFetcherItem"),(function(e){return e.getAttribute("data-pluginname")}))}(e,t),function(e,t){for(var a=e.querySelectorAll(".metadataFetcher"),i=0;i<a.length;i++){var r=a[i],n=r.getAttribute("data-type"),c=v(t,n);c||(c={Type:n},t.TypeOptions.push(c)),c.MetadataFetchers=Array.prototype.map.call(Array.prototype.filter.call(r.querySelectorAll(".chkMetadataFetcher"),(function(e){return e.checked})),(function(e){return e.getAttribute("data-pluginname")})),c.MetadataFetcherOrder=Array.prototype.map.call(r.querySelectorAll(".metadataFetcherItem"),(function(e){return e.getAttribute("data-pluginname")}))}}(e,t),function(e,t){for(var a=e.querySelectorAll(".imageFetcher"),i=0;i<a.length;i++){var r=a[i],n=r.getAttribute("data-type"),c=v(t,n);c||(c={Type:n},t.TypeOptions.push(c)),c.ImageFetchers=Array.prototype.map.call(Array.prototype.filter.call(r.querySelectorAll(".chkImageFetcher"),(function(e){return e.checked})),(function(e){return e.getAttribute("data-pluginname")})),c.ImageFetcherOrder=Array.prototype.map.call(r.querySelectorAll(".imageFetcherItem"),(function(e){return e.getAttribute("data-pluginname")}))}}(e,t),function(e){for(var t=(i||{}).TypeOptions||[],a=0;a<t.length;a++){var r=t[a],n=v(e,r.Type);n||(n={Type:r.Type},e.TypeOptions.push(n)),r.ImageOptions&&(n.ImageOptions=r.ImageOptions)}}(t),t},setLibraryOptions:q}},32819:function(e,t,a){"use strict";var i=a(1892),r=a.n(i),n=a(10778),c=(r()(n.Z,{insert:"head",singleton:!1}),n.Z.locals,a(67752),Object.create(HTMLInputElement.prototype));function l(e){if(13===e.keyCode)return e.preventDefault(),this.checked=!this.checked,this.dispatchEvent(new CustomEvent("change",{bubbles:!0})),!1}c.attachedCallback=function(){if("true"!==this.getAttribute("data-embytoggle")){this.setAttribute("data-embytoggle","true"),this.classList.add("mdl-switch__input");var e=this.parentNode;e.classList.add("mdl-switch"),e.classList.add("mdl-js-switch");var t=e.querySelector("span");e.insertAdjacentHTML("beforeend",'<div class="mdl-switch__trackContainer"><div class="mdl-switch__track"></div><div class="mdl-switch__thumb"><span class="mdl-switch__focus-helper"></span></div></div>'),t.classList.add("toggleButtonLabel"),t.classList.add("mdl-switch__label"),this.addEventListener("keydown",l)}},document.registerElement("emby-toggle",{prototype:c,extends:"input"})},10778:function(e,t,a){"use strict";var i=a(93476),r=a.n(i)()((function(e){return e[1]}));r.push([e.id,".mdl-switch{position:relative;z-index:1;vertical-align:middle;display:-webkit-inline-flex;display:inline-flex;-webkit-align-items:center;align-items:center;box-sizing:border-box;width:100%;margin:0;padding:0;overflow:visible;-webkit-touch-callout:none;-webkit-user-select:none;-ms-user-select:none;user-select:none;-webkit-flex-direction:row-reverse;flex-direction:row-reverse;-webkit-justify-content:flex-end;justify-content:flex-end}.toggleContainer{margin-bottom:1.8em}.mdl-switch__input{width:0;height:0;margin:0;padding:0;opacity:0;-ms-appearance:none;-moz-appearance:none;-webkit-appearance:none;appearance:none;border:none}.mdl-switch__trackContainer{position:relative;width:2.9em}.mdl-switch__track{background:hsla(0,0%,50.2%,.5);height:1em;border-radius:1em;cursor:pointer}.mdl-switch__input:checked+.mdl-switch__label+.mdl-switch__trackContainer>.mdl-switch__track{background:rgba(0,164,220,.5)}.mdl-switch__input[disabled]+.mdl-switch__label+.mdl-switch__trackContainer>.mdl-switch__track{background:rgba(0,0,0,.12);cursor:auto}.mdl-switch__thumb{background:#999;position:absolute;left:0;top:-.25em;height:1.44em;width:1.44em;border-radius:50%;cursor:pointer;box-shadow:0 2px 2px 0 rgba(0,0,0,.14),0 3px 1px -2px rgba(0,0,0,.2),0 1px 5px 0 rgba(0,0,0,.12);transition-duration:.28s;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-property:left;display:-webkit-flex;display:flex;-webkit-align-items:center;align-items:center;-webkit-justify-content:center;justify-content:center}.mdl-switch__input:checked+.mdl-switch__label+.mdl-switch__trackContainer>.mdl-switch__thumb{background:#00a4dc;left:1.466em;box-shadow:0 3px .28em 0 rgba(0,0,0,.14),0 3px 3px -2px rgba(0,0,0,.2),0 1px .56em 0 rgba(0,0,0,.12)}.mdl-switch__input[disabled]+.mdl-switch__label+.mdl-switch__trackContainer>.mdl-switch__thumb{background:#bdbdbd;cursor:auto}.mdl-switch__focus-helper{position:absolute;top:50%;left:50%;-webkit-transform:translate(-50%,-50%);transform:translate(-50%,-50%);display:inline-block;box-sizing:border-box;width:.6em;height:.6em;border-radius:50%;background-color:transparent}.mdl-switch__input:focus+.mdl-switch__label+.mdl-switch__trackContainer .mdl-switch__focus-helper{box-shadow:0 0 0 1.39em rgba(0,0,0,.05)}.mdl-switch__input:checked:focus+.mdl-switch__label+.mdl-switch__trackContainer .mdl-switch__focus-helper{box-shadow:0 0 0 1.39em rgba(0,164,220,.26);background-color:rgba(0,164,220,.26)}.mdl-switch__label{cursor:pointer;display:-webkit-inline-flex;display:inline-flex;-webkit-align-items:center;align-items:center;margin:0 0 0 .7em}.mdl-switch__input[disabled] .mdl-switch__label{color:#bdbdbd;cursor:auto}",""]),t.Z=r},80594:function(e){e.exports='<h2>${HeaderLibrarySettings}</h2> <div class="selectContainer fldMetadataLanguage hide"> <select is="emby-select" id="selectLanguage" label="${LabelMetadataDownloadLanguage}"></select> </div> <div class="selectContainer fldMetadataCountry hide"> <select is="emby-select" id="selectCountry" label="${LabelCountry}"></select> </div> <div class="checkboxContainer checkboxContainer-withDescription chkEnablePhotosContainer"> <label> <input type="checkbox" is="emby-checkbox" class="chkEnablePhotos" checked="checked"/> <span>${EnablePhotos}</span> </label> <div class="fieldDescription checkboxFieldDescription">${EnablePhotosHelp}</div> </div> <div class="inputContainer fldSeasonZeroDisplayName hide advanced"> <input is="emby-input" type="text" id="txtSeasonZeroName" label="${LabelSpecialSeasonsDisplayName}" value="Specials" required/> </div> <div class="checkboxContainer checkboxContainer-withDescription chkEnableEmbeddedTitlesContainer hide advanced"> <label> <input is="emby-checkbox" type="checkbox" id="chkEnableEmbeddedTitles"/> <span>${PreferEmbeddedTitlesOverFileNames}</span> </label> <div class="fieldDescription checkboxFieldDescription">${PreferEmbeddedTitlesOverFileNamesHelp}</div> </div> <div class="checkboxContainer checkboxContainer-withDescription chkEnableEmbeddedEpisodeInfosContainer hide advanced"> <label> <input is="emby-checkbox" type="checkbox" id="chkEnableEmbeddedEpisodeInfos"/> <span>${PreferEmbeddedEpisodeInfosOverFileNames}</span> </label> <div class="fieldDescription checkboxFieldDescription">${PreferEmbeddedEpisodeInfosOverFileNamesHelp}</div> </div> <div class="checkboxContainer checkboxContainer-withDescription advanced"> <label> <input type="checkbox" is="emby-checkbox" class="chkEnableRealtimeMonitor" checked="checked"/> <span>${LabelEnableRealtimeMonitor}</span> </label> <div class="fieldDescription checkboxFieldDescription">${LabelEnableRealtimeMonitorHelp}</div> </div> <div class="metadataReaders hide advanced" style="margin-bottom:2em"> </div> <div class="metadataFetchers hide" style="margin-bottom:2em"> </div> <div class="selectContainer fldAutoRefreshInterval hide advanced" style="margin:2em 0"> <select is="emby-select" id="selectAutoRefreshInterval" label="${LabelAutomaticallyRefreshInternetMetadataEvery}"></select> <div class="fieldDescription">${MessageEnablingOptionLongerScans}</div> </div> <div class="metadataSavers hide" style="margin-bottom:2em"> </div> <div class="imageFetchers hide advanced" style="margin-bottom:2em"> </div> <div class="checkboxContainer checkboxContainer-withDescription chkSaveLocalContainer hide"> <label> <input is="emby-checkbox" type="checkbox" id="chkSaveLocal"/> <span>${LabelSaveLocalMetadata}</span> </label> <div class="fieldDescription checkboxFieldDescription">${LabelSaveLocalMetadataHelp}</div> </div> <div class="checkboxContainer checkboxContainer-withDescription chkAutomaticallyGroupSeriesContainer hide advanced"> <label> <input type="checkbox" is="emby-checkbox" class="chkAutomaticallyGroupSeries"/> <span>${OptionAutomaticallyGroupSeries}</span> </label> <div class="fieldDescription checkboxFieldDescription">${OptionAutomaticallyGroupSeriesHelp}</div> </div> <div class="chapterSettingsSection hide"> <h2>${HeaderChapterImages}</h2> <div class="checkboxContainer checkboxContainer-withDescription fldExtractChapterImages"> <label> <input type="checkbox" is="emby-checkbox" class="chkExtractChapterImages"/> <span>${OptionExtractChapterImage}</span> </label> <div class="fieldDescription checkboxFieldDescription">${ExtractChapterImagesHelp}</div> </div> <div class="checkboxContainer checkboxContainer-withDescription fldExtractChaptersDuringLibraryScan advanced"> <label> <input type="checkbox" is="emby-checkbox" class="chkExtractChaptersDuringLibraryScan"/> <span>${LabelExtractChaptersDuringLibraryScan}</span> </label> <div class="fieldDescription checkboxFieldDescription">${LabelExtractChaptersDuringLibraryScanHelp}</div> </div> </div> <div class="subtitleDownloadSettings hide"> <h2>${HeaderSubtitleDownloads}</h2> <div> <h3 class="checkboxListLabel">${LabelDownloadLanguages}</h3> <div class="subtitleDownloadLanguages paperList checkboxList" style="max-height:10.5em;overflow-y:auto;padding:.5em 1em"> </div> </div> <br/> <div class="subtitleFetchers advanced" style="margin-bottom:2em"> </div> <div class="checkboxContainer checkboxContainer-withDescription"> <label> <input is="emby-checkbox" type="checkbox" id="chkRequirePerfectMatch" checked="checked"/> <span>${OptionRequirePerfectSubtitleMatch}</span> </label> <div class="fieldDescription checkboxFieldDescription">${OptionRequirePerfectSubtitleMatchHelp}</div> </div> <div class="checkboxContainer checkboxContainer-withDescription advanced"> <label> <input is="emby-checkbox" type="checkbox" id="chkSkipIfAudioTrackPresent"/> <span>${LabelSkipIfAudioTrackPresent}</span> </label> <div class="fieldDescription checkboxFieldDescription">${LabelSkipIfAudioTrackPresentHelp}</div> </div> <div class="checkboxContainer checkboxContainer-withDescription advanced"> <label> <input is="emby-checkbox" type="checkbox" id="chkSkipIfGraphicalSubsPresent"/> <span>${LabelSkipIfGraphicalSubsPresent}</span> </label> <div class="fieldDescription checkboxFieldDescription">${LabelSkipIfGraphicalSubsPresentHelp}</div> </div> <div class="checkboxContainer checkboxContainer-withDescription advanced"> <label> <input type="checkbox" is="emby-checkbox" id="chkSaveSubtitlesLocally" checked="checked"/> <span>${SaveSubtitlesIntoMediaFolders}</span> </label> <div class="fieldDescription checkboxFieldDescription">${SaveSubtitlesIntoMediaFoldersHelp}</div> </div> </div> '}}]);