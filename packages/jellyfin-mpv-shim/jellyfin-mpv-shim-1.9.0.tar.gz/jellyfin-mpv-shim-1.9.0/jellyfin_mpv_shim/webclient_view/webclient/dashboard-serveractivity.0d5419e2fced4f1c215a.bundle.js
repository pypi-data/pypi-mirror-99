(self.webpackChunk=self.webpackChunk||[]).push([[838],{92780:function(t,e,i){"use strict";i(23938),i(98010),i(61013),i(63238),i(32081),i(40895);var n=i(47005),r=i(53754),a=i(83094),s=i(81390),o=i(9785),c=i(1197),l=(i(78066),i(17734),i(53913)),d=i(61642);function u(t,e){for(var i=0;i<e.length;i++){var n=e[i];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,n.key,n)}}function v(t,e,i,n,c){null==n&&(n=parseInt(e.getAttribute("data-activitystartindex")||"0")),c=c||parseInt(e.getAttribute("data-activitylimit")||"7");var l=new Date,d="false"!==e.getAttribute("data-useractivity");d?l.setTime(l.getTime()-864e5):l.setTime(l.getTime()-6048e5),ApiClient.getJSON(ApiClient.getUrl("System/ActivityLog/Entries",{startIndex:n,limit:c,minDate:l.toISOString(),hasUserId:d})).then((function(l){if(e.setAttribute("data-activitystartindex",n),e.setAttribute("data-activitylimit",c),!n){var d=a.ZP.parentWithClass(e,"activityContainer");d&&(l.Items.length?d.classList.remove("hide"):d.classList.add("hide"))}t.items=l.Items,function(t,e,i,n,a){t.innerHTML=i.Items.map((function(t){return function(t,e){var i="";i+='<div class="listItem listItem-border">';var n="#00a4dc",a="notifications";return"Error"!=t.Severity&&"Fatal"!=t.Severity&&"Warn"!=t.Severity||(n="#cc0000",a="notification_important"),t.UserId&&t.UserPrimaryImageTag?i+='<span class="listItemIcon material-icons dvr" style="width:2em!important;height:2em!important;padding:0;color:transparent;background-color:'+n+";background-image:url('"+e.getUserImageUrl(t.UserId,{type:"Primary",tag:t.UserPrimaryImageTag})+"');background-repeat:no-repeat;background-position:center center;background-size: cover;\"></span>":i+='<span class="listItemIcon material-icons '+a+'" style="background-color:'+n+'"></span>',i+='<div class="listItemBody three-line">',i+='<div class="listItemBodyText">',i+=t.Name,i+="</div>",i+='<div class="listItemBodyText secondary">',i+=s.Z(Date.parse(t.Date),Date.parse(new Date),{locale:o.ZP.getLocale()}),i+="</div>",i+='<div class="listItemBodyText secondary listItemBodyText-nowrap">',i+=t.ShortOverview||"",i+="</div>",i+="</div>",t.Overview&&(i+='<button type="button" is="paper-icon-button-light" class="btnEntryInfo" data-id="'.concat(t.Id,'" title="').concat(r.ZP.translate("Info"),'">\n                       <span class="material-icons info"></span>\n                    </button>')),i+"</div>"}(t,e)})).join("")}(e,i,l)}))}function Z(t,e,i){var n=this.options;n&&n.serverId===e.serverId()&&v(this,n.element,e)}function f(t){var e=a.ZP.parentWithClass(t.target,"btnEntryInfo");if(e){var i=e.getAttribute("data-id"),n=this.items;if(n){var r=n.filter((function(t){return t.Id.toString()===i}))[0];r&&function(t){(0,d.Z)({text:t.Overview})}(r)}}}var y=function(){function t(e){!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,t),this.options=e;var i=e.element;i.classList.add("activityLogListWidget"),i.addEventListener("click",f.bind(this));var r=l.Z.getApiClient(e.serverId);v(this,i,r);var a=Z.bind(this);this.updateFn=a,n.Events.on(c.default,"ActivityLogEntry",a),r.sendMessage("ActivityLogEntryStart","0,1500")}var e,i;return e=t,(i=[{key:"destroy",value:function(){var t=this.options;t&&(t.element.classList.remove("activityLogListWidget"),l.Z.getApiClient(t.serverId).sendMessage("ActivityLogEntryStop","0,1500"));var e=this.updateFn;e&&n.Events.off(c.default,"ActivityLogEntry",e),this.items=null,this.options=null}}])&&u(e.prototype,i),t}();e.Z=y},78498:function(t,e,i){"use strict";i.r(e),i.d(e,{default:function(){return a}});var n=i(92780),r=i(53754);function a(t,e){var i;"false"!==e.useractivity?(t.querySelector(".activityItems").setAttribute("data-useractivity","true"),t.querySelector(".sectionTitle").innerHTML=r.ZP.translate("HeaderActivity")):(t.querySelector(".activityItems").setAttribute("data-useractivity","false"),t.querySelector(".sectionTitle").innerHTML=r.ZP.translate("Alerts")),t.addEventListener("viewshow",(function(){i||(i=new n.Z({serverId:ApiClient.serverId(),element:t.querySelector(".activityItems")}))})),t.addEventListener("viewdestroy",(function(){i&&i.destroy(),i=null}))}},9785:function(t,e,i){"use strict";i.d(e,{Kd:function(){return Y},mF:function(){return $}});var n=i(77946),r=i(12496),a=i(11401),s=i(84146),o=i(59996),c=i(78210),l=i(9477),d=i(33026),u=i(91814),v=i(88303),Z=i(22410),f=i(35997),y=i(73956),m=i(86496),g=i(6902),p=i(35163),h=i(36749),b=i(89310),I=i(22481),L=i(75710),A=i(11109),k=i(74270),w=i(37159),S=i(27324),T=i(68490),E=i(19046),C=i(81905),P=i(19656),x=i(5905),U=i(64660),D=i(69509),O=i(24770),W=i(84216),q=i(77411),B=i(23282),M=i(60754),z=i(21430),F=i(45614),H=i(83305),j=i(95861),N=i(37405),J=i(6148),K=i(63258),_=i(50281),G=i(67889),Q=i(44362),R=i(69244),V=i(96730),X=i(53754);function Y(){return t=X.ZP.getCurrentLocale(),{af:n.Z,ar:r.Z,"be-by":a.Z,"bg-bg":s.Z,bn:o.Z,ca:c.Z,cs:l.Z,da:d.Z,de:u.Z,el:v.Z,"en-gb":Z.Z,"en-us":f.Z,eo:y.Z,es:m.Z,"es-ar":m.Z,"es-do":m.Z,"es-mx":m.Z,fa:g.Z,fi:p.Z,fr:h.Z,"fr-ca":b.Z,gl:I.Z,gsw:u.Z,he:L.Z,"hi-in":A.Z,hr:k.Z,hu:w.Z,id:S.Z,is:T.Z,it:E.Z,ja:C.Z,kk:P.Z,ko:x.Z,"lt-lt":U.Z,ms:D.Z,nb:O.Z,nl:W.Z,pl:q.Z,pt:B.Z,"pt-br":M.Z,"pt-pt":B.Z,ro:z.Z,ru:F.Z,sk:H.Z,"sl-si":j.Z,sv:N.Z,ta:J.Z,th:K.Z,tr:_.Z,uk:G.Z,vi:Q.Z,"zh-cn":R.Z,"zh-hk":R.Z,"zh-tw":V.Z}[t]||f.Z;var t}var $={addSuffix:!0,locale:Y()};e.ZP={getLocale:Y,localeWithSuffix:$}}}]);