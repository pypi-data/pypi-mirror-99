(self.webpackChunk=self.webpackChunk||[]).push([[2909],{72240:function(t,i,e){"use strict";e.r(i),e.d(i,{default:function(){return s}}),e(61013);var n=e(6594),a=e(53754);function s(t,i){t.addEventListener("viewshow",(function(){var i;i=t,n.ZP.show(),ApiClient.getJSON(ApiClient.getUrl("Notifications/Types")).then((function(t){var e="",s="",o=!0;e+=t.map((function(t){var i="";return t.Category!==s&&((s=t.Category)&&(i+="</div>",i+="</div>"),i+='<div class="verticalSection verticalSection-extrabottompadding">',i+='<div class="sectionTitleContainer" style="margin-bottom:1em;">',i+='<h2 class="sectionTitle">',i+=t.Category,i+="</h2>",o&&(o=!1,i+='<a is="emby-linkbutton" class="raised button-alt headerHelpButton" target="_blank" href="https://docs.jellyfin.org/general/server/notifications.html">',i+=a.ZP.translate("Help"),i+="</a>"),i+="</div>",i+='<div class="paperList">'),i+='<a class="listItem listItem-border" is="emby-linkbutton" data-ripple="false" href="notificationsetting.html?type='+t.Type+'">',t.Enabled?i+='<span class="listItemIcon material-icons notifications_active"></span>':i+='<span class="listItemIcon material-icons notifications_off" style="background-color:#999;"></span>',i+='<div class="listItemBody">',i+='<div class="listItemBodyText">'+t.Name+"</div>",i+="</div>",(i+='<button type="button" is="paper-icon-button-light"><span class="material-icons mode_edit"></span></button>')+"</a>"})).join(""),t.length&&(e+="</div>",e+="</div>"),i.querySelector(".notificationList").innerHTML=e,n.ZP.hide()}))}))}e(17734),e(78066)}}]);