(self.webpackChunk=self.webpackChunk||[]).push([[102,8995],{78995:function(e,t,i){"use strict";function n(e,t){var i=[];switch(e.textSize||""){case"smaller":i.push({name:"font-size",value:".8em"});break;case"small":i.push({name:"font-size",value:"inherit"});break;case"larger":i.push({name:"font-size",value:"2em"});break;case"extralarge":i.push({name:"font-size",value:"2.2em"});break;case"large":i.push({name:"font-size",value:"1.72em"});break;default:case"medium":i.push({name:"font-size",value:"1.36em"})}switch(e.dropShadow||""){case"raised":i.push({name:"text-shadow",value:"-1px -1px white, 0px -1px white, -1px 0px white, 1px 1px black, 0px 1px black, 1px 0px black"});break;case"depressed":i.push({name:"text-shadow",value:"1px 1px white, 0px 1px white, 1px 0px white, -1px -1px black, 0px -1px black, -1px 0px black"});break;case"uniform":i.push({name:"text-shadow",value:"-1px 0px #000000, 0px 1px #000000, 1px 0px #000000, 0px -1px #000000"});break;case"none":i.push({name:"text-shadow",value:"none"});break;default:case"dropshadow":i.push({name:"text-shadow",value:"#000000 0px 0px 7px"})}var n=e.textBackground||"transparent";n&&i.push({name:"background-color",value:n});var a=e.textColor||"#ffffff";switch(a&&i.push({name:"color",value:a}),e.font||""){case"typewriter":i.push({name:"font-family",value:'"Courier New",monospace'}),i.push({name:"font-variant",value:"none"});break;case"print":i.push({name:"font-family",value:"Georgia,Times New Roman,Arial,Helvetica,serif"}),i.push({name:"font-variant",value:"none"});break;case"console":i.push({name:"font-family",value:"Consolas,Lucida Console,Menlo,Monaco,monospace"}),i.push({name:"font-variant",value:"none"});break;case"cursive":i.push({name:"font-family",value:"Lucida Handwriting,Brush Script MT,Segoe Script,cursive,Quintessential,system-ui,-apple-system,BlinkMacSystemFont,sans-serif"}),i.push({name:"font-variant",value:"none"});break;case"casual":i.push({name:"font-family",value:"Gabriola,Segoe Print,Comic Sans MS,Chalkboard,Short Stack,system-ui,-apple-system,BlinkMacSystemFont,sans-serif"}),i.push({name:"font-variant",value:"none"});break;case"smallcaps":i.push({name:"font-family",value:"Copperplate Gothic,Copperplate Gothic Bold,Copperplate,system-ui,-apple-system,BlinkMacSystemFont,sans-serif"}),i.push({name:"font-variant",value:"small-caps"});break;default:i.push({name:"font-family",value:"inherit"}),i.push({name:"font-variant",value:"none"})}if(!t){var l=parseInt(e.verticalPosition,10),s=Math.abs(1.35*l);l<0?(i.push({name:"min-height",value:"".concat(s,"em")}),i.push({name:"margin-top",value:""})):(i.push({name:"min-height",value:""}),i.push({name:"margin-top",value:"".concat(s,"em")}))}return i}function a(e,t){var i=[];return t||(parseInt(e.verticalPosition,10)<0?(i.push({name:"top",value:""}),i.push({name:"bottom",value:"0"})):(i.push({name:"top",value:"0"}),i.push({name:"bottom",value:""}))),i}function l(e,t){return{text:n(e,t),window:a(e,t)}}function s(e,t){for(var i=0,n=e.length;i<n;i++){var a=e[i];t.style[a.name]=a.value}}function o(e,t){var i=l(t,!!e.preview);e.text&&s(i.text,e.text),e.window&&s(i.window,e.window)}i.r(t),i.d(t,{getStyles:function(){return l},applyStyles:function(){return o}}),i(32081),t.default={getStyles:l,applyStyles:o}},40046:function(e,t,i){"use strict";i.r(t),i.d(t,{default:function(){return A}}),i(48410);var n,a=i(53754),l=i(38102),s=i(67469),o=i(27515),r=i(78695),u=i(6594),c=i(78995),p=function(e,t){var i="";i+="<option value=''>"+a.ZP.translate("AnyLanguage")+"</option>";for(var n=0,l=t.length;n<l;n++){var s=t[n];i+="<option value='"+s.ThreeLetterISOLanguageName+"'>"+s.DisplayName+"</option>"}e.innerHTML=i},d=i(83094),v=i(47005),f=(i(17734),i(50447),i(83495),i(30983),i(65219),i(93462),i(1892)),b=i.n(f),m=i(79161),h=(b()(m.Z,{insert:"head",singleton:!1}),m.Z.locals,i(53913)),S=i(38440),y=i(82653),g=i.n(y);function w(e,t){for(var i=0;i<t.length;i++){var n=t[i];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function x(e){var t={};return t.textSize=e.querySelector("#selectTextSize").value,t.dropShadow=e.querySelector("#selectDropShadow").value,t.font=e.querySelector("#selectFont").value,t.textBackground=e.querySelector("#inputTextBackground").value,t.textColor=e.querySelector("#inputTextColor").value,t.verticalPosition=e.querySelector("#sliderVerticalPosition").value,t}function k(e){for(var t=d.ZP.parentWithClass(e.target,"subtitlesettings"),i=t.querySelectorAll(".subtitlesHelp"),n=0,a=i.length;n<a;n++)i[n].classList.add("hide");t.querySelector(".subtitles"+this.value+"Help").classList.remove("hide")}function C(e){var t=d.ZP.parentWithClass(e.target,"subtitlesettings"),i=x(t),n={window:t.querySelector(".subtitleappearance-preview-window"),text:t.querySelector(".subtitleappearance-preview-text"),preview:!0};c.default.applyStyles(n,i),c.default.applyStyles({window:t.querySelector(".subtitleappearance-fullpreview-window"),text:t.querySelector(".subtitleappearance-fullpreview-text")},i)}function L(e){clearTimeout(n),this._fullPreview.classList.remove("subtitleappearance-fullpreview-hide"),e&&this._refFullPreview++,0===this._refFullPreview&&(n=setTimeout($.bind(this),1e3))}function $(e){clearTimeout(n),e&&this._refFullPreview--,0===this._refFullPreview&&this._fullPreview.classList.add("subtitleappearance-fullpreview-hide")}var P=function(){function e(t){!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,e),this.options=t,function(e,t){if(e.element.classList.add("subtitlesettings"),e.element.innerHTML=a.ZP.translateHtml(g(),"core"),e.element.querySelector("form").addEventListener("submit",t.onSubmit.bind(t)),e.element.querySelector("#selectSubtitlePlaybackMode").addEventListener("change",k),e.element.querySelector("#selectTextSize").addEventListener("change",C),e.element.querySelector("#selectDropShadow").addEventListener("change",C),e.element.querySelector("#selectFont").addEventListener("change",C),e.element.querySelector("#inputTextColor").addEventListener("change",C),e.element.querySelector("#inputTextBackground").addEventListener("change",C),e.enableSaveButton&&e.element.querySelector(".btnSave").classList.remove("hide"),l.M.supports("subtitleappearancesettings")){e.element.querySelector(".subtitleAppearanceSection").classList.remove("hide"),t._fullPreview=e.element.querySelector(".subtitleappearance-fullpreview"),t._refFullPreview=0;var i=e.element.querySelector("#sliderVerticalPosition");i.addEventListener("input",C),i.addEventListener("input",(function(){return L.call(t)}));var n=window.PointerEvent?"pointer":"mouse";i.addEventListener("".concat(n,"enter"),(function(){return L.call(t,!0)})),i.addEventListener("".concat(n,"leave"),(function(){return $.call(t,!0)})),r.Z.tv&&(i.addEventListener("focus",(function(){return L.call(t,!0)})),i.addEventListener("blur",(function(){return $.call(t,!0)})),setTimeout((function(){i.classList.add("focusable"),i.enableKeyboardDragging()}),0)),e.element.querySelector(".chkPreview").addEventListener("change",(function(e){e.target.checked?L.call(t,!0):$.call(t,!0)}))}t.loadData(),e.autoFocus&&o.Z.autoFocus(e.element)}(t,this)}var t,i;return t=e,(i=[{key:"loadData",value:function(){var e=this,t=e.options.element;u.ZP.show();var i=e.options.userId,n=h.Z.getApiClient(e.options.serverId),a=e.options.userSettings;n.getUser(i).then((function(o){a.setUserInfo(i,n).then((function(){e.dataLoaded=!0;var i=a.getSubtitleAppearanceSettings(e.options.appearanceKey);!function(e,t,i,n,a){a.getCultures().then((function(i){l.M.supports("subtitleburnsettings")&&t.Policy.EnableVideoPlaybackTranscoding&&e.querySelector(".fldBurnIn").classList.remove("hide");var a=e.querySelector("#selectSubtitleLanguage");p(a,i),a.value=t.Configuration.SubtitleLanguagePreference||"",e.querySelector("#selectSubtitlePlaybackMode").value=t.Configuration.SubtitleMode||"",e.querySelector("#selectSubtitlePlaybackMode").dispatchEvent(new CustomEvent("change",{})),e.querySelector("#selectTextSize").value=n.textSize||"",e.querySelector("#selectDropShadow").value=n.dropShadow||"",e.querySelector("#inputTextBackground").value=n.textBackground||"transparent",e.querySelector("#inputTextColor").value=n.textColor||"#ffffff",e.querySelector("#selectFont").value=n.font||"",e.querySelector("#sliderVerticalPosition").value=n.verticalPosition,e.querySelector("#selectSubtitleBurnIn").value=s.Z.get("subtitleburnin")||"",C({target:e.querySelector("#selectTextSize")}),u.ZP.hide()}))}(t,o,0,i,n)}))}))}},{key:"submit",value:function(){this.onSubmit(null)}},{key:"destroy",value:function(){this.options=null}},{key:"onSubmit",value:function(e){var t=this,i=h.Z.getApiClient(t.options.serverId),n=t.options.userId,l=t.options.userSettings;return l.setUserInfo(n,i).then((function(){var e=t.options.enableSaveConfirmation;!function(e,t,i,n,l,o){u.ZP.show(),s.Z.set("subtitleburnin",t.querySelector("#selectSubtitleBurnIn").value),l.getUser(i).then((function(i){(function(e,t,i,n,a){var l=i.getSubtitleAppearanceSettings(n);return l=Object.assign(l,x(e)),i.setSubtitleAppearanceSettings(l,n),t.Configuration.SubtitleLanguagePreference=e.querySelector("#selectSubtitleLanguage").value,t.Configuration.SubtitleMode=e.querySelector("#selectSubtitlePlaybackMode").value,a.updateUserConfiguration(t.Id,t.Configuration)})(t,i,n,e.appearanceKey,l).then((function(){u.ZP.hide(),o&&(0,S.Z)(a.ZP.translate("SettingsSaved")),v.Events.trigger(e,"saved")}),(function(){u.ZP.hide()}))}))}(t,t.options.element,n,l,i,e)})),e&&e.preventDefault(),!1}}])&&w(t.prototype,i),e}(),q=i(28978),T=i(6610),D=q.UserSettings;function A(e,t){var i,n=t.userId||ApiClient.getCurrentUserId(),a=n===ApiClient.getCurrentUserId()?q:new D;e.addEventListener("viewshow",(function(){i?i.loadData():i=new P({serverId:ApiClient.serverId(),userId:n,element:e.querySelector(".settingsContainer"),userSettings:a,enableSaveButton:!0,enableSaveConfirmation:!0,autoFocus:T.default.isEnabled()})})),e.addEventListener("change",(function(){})),e.addEventListener("viewdestroy",(function(){i&&(i.destroy(),i=null)}))}},79161:function(e,t,i){"use strict";var n=i(93476),a=i.n(n)()((function(e){return e[1]}));a.push([e.id,".subtitleappearance-fullpreview{position:fixed;width:100%;height:100%;top:0;left:0;z-index:1000;pointer-events:none;transition:.2s}.subtitleappearance-fullpreview-hide{opacity:0}.subtitleappearance-fullpreview-window{position:absolute;width:100%;font-size:170%;text-align:center}.subtitleappearance-fullpreview-text{display:inline-block;max-width:70%}",""]),t.Z=a},82653:function(e){e.exports='<form style="margin:0 auto"> <div class="verticalSection"> <h2 class="sectionTitle"> ${Subtitles} </h2> <div class="selectContainer"> <select is="emby-select" id="selectSubtitleLanguage" label="${LabelPreferredSubtitleLanguage}"></select> </div> <div class="selectContainer"> <select is="emby-select" id="selectSubtitlePlaybackMode" label="${LabelSubtitlePlaybackMode}"> <option value="Default">${Default}</option> <option value="Smart">${Smart}</option> <option value="OnlyForced">${OnlyForcedSubtitles}</option> <option value="Always">${AlwaysPlaySubtitles}</option> <option value="None">${None}</option> </select> <div class="fieldDescription subtitlesDefaultHelp subtitlesHelp hide">${DefaultSubtitlesHelp}</div> <div class="fieldDescription subtitlesSmartHelp subtitlesHelp hide">${SmartSubtitlesHelp}</div> <div class="fieldDescription subtitlesAlwaysHelp subtitlesHelp hide">${AlwaysPlaySubtitlesHelp}</div> <div class="fieldDescription subtitlesOnlyForcedHelp subtitlesHelp hide">${OnlyForcedSubtitlesHelp}</div> <div class="fieldDescription subtitlesNoneHelp subtitlesHelp hide">${NoSubtitlesHelp}</div> </div> <div class="selectContainer fldBurnIn hide"> <select is="emby-select" id="selectSubtitleBurnIn" label="${LabelBurnSubtitles}"> <option value="">${Auto}</option> <option value="onlyimageformats">${OnlyImageFormats}</option> <option value="allcomplexformats">${AllComplexFormats}</option> </select> <div class="fieldDescription">${BurnSubtitlesHelp}</div> </div> </div> <div class="verticalSection subtitleAppearanceSection hide"> <h2 class="sectionTitle"> ${HeaderSubtitleAppearance} </h2> <div class="subtitleappearance-fullpreview subtitleappearance-fullpreview-hide"> <div class="subtitleappearance-fullpreview-window"> <div class="subtitleappearance-fullpreview-text"> ${HeaderSubtitleAppearance} <br> ${TheseSettingsAffectSubtitlesOnThisDevice} </div> </div> </div> <div style="margin:2em 0 2em"> <div class="subtitleappearance-preview flex align-items-center justify-content-center" style="margin:2em 0;padding:1.6em;color:#000;background:linear-gradient(140deg,#aa5cc3,#00a4dc)"> <div class="subtitleappearance-preview-window flex align-items-center justify-content-center" style="width:90%;padding:.25em"> <div class="subtitleappearance-preview-text flex align-items-center justify-content-center"> ${TheseSettingsAffectSubtitlesOnThisDevice} </div> </div> </div> <div class="fieldDescription">${SubtitleAppearanceSettingsDisclaimer}</div> <div class="fieldDescription">${SubtitleAppearanceSettingsAlsoPassedToCastDevices}</div> </div> <div class="selectContainer"> <select is="emby-select" id="selectTextSize" label="${LabelTextSize}"> <option value="smaller">${Smaller}</option> <option value="small">${Small}</option> <option value="">${Normal}</option> <option value="large">${Large}</option> <option value="larger">${Larger}</option> <option value="extralarge">${ExtraLarge}</option> </select> </div> <div class="selectContainer"> <select is="emby-select" id="selectFont" label="${LabelFont}"> <option value="">${Default}</option> <option value="typewriter">${Typewriter}</option> <option value="print">${Print}</option> <option value="console">${Console}</option> <option value="casual">${Casual}</option> <option value="smallcaps">${SmallCaps}</option> </select> </div> <div class="inputContainer hide"> <input is="emby-input" id="inputTextBackground" label="${LabelTextBackgroundColor}" type="text"/> </div> <div class="inputContainer hide"> <input is="emby-input" id="inputTextColor" label="${LabelTextColor}" type="text"/> </div> <div class="selectContainer"> <select is="emby-select" id="selectDropShadow" label="${LabelDropShadow}"> <option value="none">${None}</option> <option value="raised">${Raised}</option> <option value="depressed">${Depressed}</option> <option value="uniform">${Uniform}</option> <option value="">${DropShadow}</option> </select> </div> <div class="sliderContainer-settings"> <div class="sliderContainer"> <input is="emby-slider" id="sliderVerticalPosition" label="${LabelSubtitleVerticalPosition}" type="range" min="-16" max="16"/> </div> <div class="fieldDescription">${SubtitleVerticalPositionHelp}</div> </div> <div class="checkboxContainer"> <label> <input is="emby-checkbox" type="checkbox" class="chkPreview"/> <span>${Preview}</span> </label> </div> </div> <button is="emby-button" type="submit" class="raised button-submit block btnSave hide"> <span>${Save}</span> </button> </form> '}}]);