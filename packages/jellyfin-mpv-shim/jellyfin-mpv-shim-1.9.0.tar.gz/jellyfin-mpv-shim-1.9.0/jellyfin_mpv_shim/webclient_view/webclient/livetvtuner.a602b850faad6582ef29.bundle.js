(self.webpackChunk=self.webpackChunk||[]).push([[2379],{68823:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return s}}),r(98010),r(27471),r(61013),r(63238),r(61418),r(5769);var l=r(53754),n=r(6594),o=r(83094),u=(r(30983),r(78066),r(65219),r(50447),r(76543));function c(e){return-1!==["nextpvr"].indexOf(e||"")}function i(e,t){var r=e.querySelector(".selectType"),l=t.Type||"";t.Source&&c(t.Source)&&(l=t.Source),r.value=l,a.call(r),e.querySelector(".txtDevicePath").value=t.Url||"",e.querySelector(".txtFriendlyName").value=t.FriendlyName||"",e.querySelector(".txtUserAgent").value=t.UserAgent||"",e.querySelector(".fldDeviceId").value=t.DeviceId||"",e.querySelector(".chkFavorite").checked=t.ImportFavoritesOnly,e.querySelector(".chkTranscode").checked=t.AllowHWTranscoding,e.querySelector(".chkStreamLoop").checked=t.EnableStreamLooping,e.querySelector(".txtTunerCount").value=t.TunerCount||"0"}function a(){var e=this.value,t=o.ZP.parentWithClass(this,"page"),r="hdhomerun"===e,n="hdhomerun"===e,u="hdhomerun"===e,c="hdhomerun"===e,i="m3u"===e,a="m3u"===e,s="m3u"===e,d="m3u"===e,v="other"!==e,h=i,y=t.querySelector(".txtDevicePath");c?(y.label(l.ZP.translate("LabelTunerIpAddress")),t.querySelector(".fldPath").classList.remove("hide")):i?(y.label(l.ZP.translate("LabelFileOrUrl")),t.querySelector(".fldPath").classList.remove("hide")):t.querySelector(".fldPath").classList.add("hide"),h?(t.querySelector(".btnSelectPath").classList.remove("hide"),t.querySelector(".txtDevicePath").setAttribute("required","required")):(t.querySelector(".btnSelectPath").classList.add("hide"),t.querySelector(".txtDevicePath").removeAttribute("required")),d?t.querySelector(".fldUserAgent").classList.remove("hide"):t.querySelector(".fldUserAgent").classList.add("hide"),u?t.querySelector(".fldFavorites").classList.remove("hide"):t.querySelector(".fldFavorites").classList.add("hide"),n?t.querySelector(".fldTranscode").classList.remove("hide"):t.querySelector(".fldTranscode").classList.add("hide"),a?t.querySelector(".fldStreamLoop").classList.remove("hide"):t.querySelector(".fldStreamLoop").classList.add("hide"),s?(t.querySelector(".fldTunerCount").classList.remove("hide"),t.querySelector(".txtTunerCount").setAttribute("required","required")):(t.querySelector(".fldTunerCount").classList.add("hide"),t.querySelector(".txtTunerCount").removeAttribute("required")),r?t.querySelector(".drmMessage").classList.remove("hide"):t.querySelector(".drmMessage").classList.add("hide"),v?t.querySelector(".button-submit").classList.remove("hide"):t.querySelector(".button-submit").classList.add("hide")}function s(e,t){t.id||e.querySelector(".btnDetect").classList.remove("hide"),e.addEventListener("viewshow",(function(){var r=t.id;(function(e,t){return ApiClient.getJSON(ApiClient.getUrl("LiveTv/TunerHosts/Types")).then((function(r){var n=e.querySelector(".selectType"),o="";o+=r.map((function(e){return'<option value="'+e.Id+'">'+e.Name+"</option>"})).join(""),o+='<option value="other">',o+=l.ZP.translate("TabOther"),o+="</option>",n.innerHTML=o,n.disabled=null!=t,n.value="",a.call(n)}))})(e,r).then((function(){!function(e,t){e.querySelector(".txtDevicePath").value="",e.querySelector(".chkFavorite").checked=!1,e.querySelector(".txtDevicePath").value="",t&&ApiClient.getNamedConfiguration("livetv").then((function(r){var l=r.TunerHosts.filter((function(e){return e.Id===t}))[0];i(e,l)}))}(e,r)}))})),e.querySelector("form").addEventListener("submit",(function(t){return function(e){n.ZP.show();var t={Type:e.querySelector(".selectType").value,Url:e.querySelector(".txtDevicePath").value||null,UserAgent:e.querySelector(".txtUserAgent").value||null,FriendlyName:e.querySelector(".txtFriendlyName").value||null,DeviceId:e.querySelector(".fldDeviceId").value||null,TunerCount:e.querySelector(".txtTunerCount").value||0,ImportFavoritesOnly:e.querySelector(".chkFavorite").checked,AllowHWTranscoding:e.querySelector(".chkTranscode").checked,EnableStreamLooping:e.querySelector(".chkStreamLoop").checked};c(t.Type)&&(t.Source=t.Type,t.Type="m3u"),getParameterByName("id")&&(t.Id=getParameterByName("id")),ApiClient.ajax({type:"POST",url:ApiClient.getUrl("LiveTv/TunerHosts"),data:JSON.stringify(t),contentType:"application/json"}).then((function(e){u.ZP.processServerConfigurationUpdateResult(),u.ZP.navigate("livetvstatus.html")}),(function(){n.ZP.hide(),u.ZP.alert({message:l.ZP.translate("ErrorSavingTvProvider")})}))}(e),t.preventDefault(),t.stopPropagation(),!1})),e.querySelector(".selectType").addEventListener("change",a),e.querySelector(".btnDetect").addEventListener("click",(function(){r.e(9974).then(r.bind(r,29974)).then((function(e){return(new(0,e.default)).show({serverId:ApiClient.serverId()})})).then((function(t){i(e,t)}))})),e.querySelector(".btnSelectPath").addEventListener("click",(function(){r.e(3688).then(r.bind(r,63688)).then((function(t){var r=new(0,t.default);r.show({includeFiles:!0,callback:function(t){t&&(e.querySelector(".txtDevicePath").value=t),r.close()}})}))}))}}}]);