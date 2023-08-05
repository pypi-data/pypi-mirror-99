(self.webpackChunk=self.webpackChunk||[]).push([[2966],{52966:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return o}}),r(98010),r(27471),r(61013),r(63238),r(61418),r(72482),r(5769),r(71848);var n=r(6594),i=r(53754),l=(r(65219),r(30983),r(17734),r(21865),r(76543)),s=r(47005);function o(e,t,o){function u(e,t){if(e&&t){var r=e.ListingProviders.filter((function(e){return e.Id===t}))[0];return r?Promise.resolve(r):u()}return ApiClient.getJSON(ApiClient.getUrl("LiveTv/ListingProviders/Default"))}function c(){n.ZP.show(),ApiClient.getNamedConfiguration("livetv").then((function(r){u(r,t).then((function(t){e.querySelector(".txtPath").value=t.Path||"",e.querySelector(".txtKids").value=(t.KidsCategories||[]).join("|"),e.querySelector(".txtNews").value=(t.NewsCategories||[]).join("|"),e.querySelector(".txtSports").value=(t.SportsCategories||[]).join("|"),e.querySelector(".txtMovies").value=(t.MovieCategories||[]).join("|"),e.querySelector(".txtMoviePrefix").value=t.MoviePrefix||"",e.querySelector(".txtUserAgent").value=t.UserAgent||"",e.querySelector(".chkAllTuners").checked=t.EnableAllTuners,e.querySelector(".chkAllTuners").checked?e.querySelector(".selectTunersSection").classList.add("hide"):e.querySelector(".selectTunersSection").classList.remove("hide"),function(e,t,r){for(var n="",i=0,l=r.length;i<l;i++){var s=r[i];n+='<div class="listItem">';var o=t.EnabledTuners||[],u=t.EnableAllTuners||-1!==o.indexOf(s.Id)?" checked":"";n+='<label class="listItemCheckboxContainer"><input type="checkbox" is="emby-checkbox" class="chkTuner" data-id="'+s.Id+'" '+u+"><span></span></label>",n+='<div class="listItemBody two-line">',n+='<div class="listItemBodyText">',n+=s.FriendlyName||d(s.Type),n+="</div>",n+='<div class="listItemBodyText secondary">',n+=s.Url,n+="</div>",n+="</div>",n+="</div>"}e.querySelector(".tunerList").innerHTML=n}(e,t,r.TunerHosts),n.ZP.hide()}))}))}function a(e){var t=e.value;return t?t.split("|"):[]}function d(e){switch(e=e.toLowerCase()){case"m3u":return"M3U Playlist";case"hdhomerun":return"HDHomerun";case"satip":return"DVB";default:return"Unknown"}}function v(e){var t=$(e.target).parents(".xmltvForm")[0];r.e(3688).then(r.bind(r,63688)).then((function(e){var r=new(0,e.default);r.show({includeFiles:!0,callback:function(e){if(e){var n=t.querySelector(".txtPath");n.value=e,n.focus()}r.close()}})}))}var h=this;h.submit=function(){e.querySelector(".btnSubmitListings").click()},h.init=function(){var r=!1===(o=o||{}).showCancelButton;e.querySelector(".btnCancel").classList.toggle("hide",r);var u=!1===o.showSubmitButton;e.querySelector(".btnSubmitListings").classList.toggle("hide",u),$("form",e).on("submit",(function(){return function(){n.ZP.show();var r=t;ApiClient.getNamedConfiguration("livetv").then((function(t){var u=t.ListingProviders.filter((function(e){return e.Id===r}))[0]||{};u.Type="xmltv",u.Path=e.querySelector(".txtPath").value,u.MoviePrefix=e.querySelector(".txtMoviePrefix").value||null,u.UserAgent=e.querySelector(".txtUserAgent").value||null,u.MovieCategories=a(e.querySelector(".txtMovies")),u.KidsCategories=a(e.querySelector(".txtKids")),u.NewsCategories=a(e.querySelector(".txtNews")),u.SportsCategories=a(e.querySelector(".txtSports")),u.EnableAllTuners=e.querySelector(".chkAllTuners").checked,u.EnabledTuners=u.EnableAllTuners?[]:$(".chkTuner",e).get().filter((function(e){return e.checked})).map((function(e){return e.getAttribute("data-id")})),ApiClient.ajax({type:"POST",url:ApiClient.getUrl("LiveTv/ListingProviders",{ValidateListings:!0}),data:JSON.stringify(u),contentType:"application/json"}).then((function(e){n.ZP.hide(),!1!==o.showConfirmation&&l.ZP.processServerConfigurationUpdateResult(),s.Events.trigger(h,"submitted")}),(function(){n.ZP.hide(),l.ZP.alert({message:i.ZP.translate("ErrorAddingXmlTvFile")})}))}))}(),!1})),e.querySelector("#btnSelectPath").addEventListener("click",v),e.querySelector(".chkAllTuners").addEventListener("change",(function(t){t.target.checked?e.querySelector(".selectTunersSection").classList.add("hide"):e.querySelector(".selectTunersSection").classList.remove("hide")})),c()}}}}]);