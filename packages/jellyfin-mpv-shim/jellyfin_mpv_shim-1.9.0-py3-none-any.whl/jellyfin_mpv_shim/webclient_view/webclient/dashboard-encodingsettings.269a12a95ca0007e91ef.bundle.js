(self.webpackChunk=self.webpackChunk||[]).push([[2832],{56669:function(e,t,n){"use strict";n.r(t),n(98010),n(95374),n(27471),n(61013),n(63238),n(32081),n(61418),n(72482),n(55849),n(5769),n(71848);var c,a=n(6594),r=n(53754),o=n(83094),l=n(17025),i=n(76543),u=n(61642);function d(e){a.ZP.hide(),(0,u.Z)(r.ZP.translate("FFmpegSavePathNotFound"))}function s(){var e=this,t=function(){a.ZP.show(),ApiClient.getNamedConfiguration("encoding").then((function(t){t.DownMixAudioBoost=$("#txtDownMixAudioBoost",e).val(),t.MaxMuxingQueueSize=e.querySelector("#txtMaxMuxingQueueSize").value,t.TranscodingTempPath=$("#txtTranscodingTempPath",e).val(),t.FallbackFontPath=e.querySelector("#txtFallbackFontPath").value,t.EnableFallbackFont=!!e.querySelector("#txtFallbackFontPath").value&&e.querySelector("#chkEnableFallbackFont").checked,t.EncodingThreadCount=$("#selectThreadCount",e).val(),t.HardwareAccelerationType=$("#selectVideoDecoder",e).val(),t.VaapiDevice=$("#txtVaapiDevice",e).val(),t.OpenclDevice=e.querySelector("#txtOpenclDevice").value,t.EnableTonemapping=e.querySelector("#chkTonemapping").checked,t.EnableVppTonemapping=e.querySelector("#chkVppTonemapping").checked,t.TonemappingAlgorithm=e.querySelector("#selectTonemappingAlgorithm").value,t.TonemappingRange=e.querySelector("#selectTonemappingRange").value,t.TonemappingDesat=e.querySelector("#txtTonemappingDesat").value,t.TonemappingThreshold=e.querySelector("#txtTonemappingThreshold").value,t.TonemappingPeak=e.querySelector("#txtTonemappingPeak").value,t.TonemappingParam=e.querySelector("#txtTonemappingParam").value||"0",t.EncoderPreset=e.querySelector("#selectEncoderPreset").value,t.H264Crf=parseInt(e.querySelector("#txtH264Crf").value||"0"),t.H265Crf=parseInt(e.querySelector("#txtH265Crf").value||"0"),t.DeinterlaceMethod=e.querySelector("#selectDeinterlaceMethod").value,t.DeinterlaceDoubleRate=e.querySelector("#chkDoubleRateDeinterlacing").checked,t.EnableSubtitleExtraction=e.querySelector("#chkEnableSubtitleExtraction").checked,t.EnableThrottling=e.querySelector("#chkEnableThrottling").checked,t.HardwareDecodingCodecs=Array.prototype.map.call(Array.prototype.filter.call(e.querySelectorAll(".chkDecodeCodec"),(function(e){return e.checked})),(function(e){return e.getAttribute("data-codec")})),t.EnableDecodingColorDepth10Hevc=e.querySelector("#chkDecodingColorDepth10Hevc").checked,t.EnableDecodingColorDepth10Vp9=e.querySelector("#chkDecodingColorDepth10Vp9").checked,t.EnableEnhancedNvdecDecoder=e.querySelector("#chkEnhancedNvdecDecoder").checked,t.EnableHardwareEncoding=e.querySelector("#chkHardwareEncoding").checked,t.AllowHevcEncoding=e.querySelector("#chkAllowHevcEncoding").checked,ApiClient.updateNamedConfiguration("encoding",t).then((function(){!function(e){ApiClient.getSystemInfo().then((function(t){return ApiClient.ajax({url:ApiClient.getUrl("System/MediaEncoder/Path"),type:"POST",data:JSON.stringify({Path:e.querySelector(".txtEncoderPath").value,PathType:"Custom"}),contentType:"application/json"}).then(i.ZP.processServerConfigurationUpdateResult,d)}))}(e)}),(function(){(0,u.Z)(r.ZP.translate("ErrorDefault")),i.ZP.processServerConfigurationUpdateResult()}))}))};return $("#selectVideoDecoder",e).val()?(0,u.Z)({title:r.ZP.translate("TitleHardwareAcceleration"),text:r.ZP.translate("HardwareAccelerationWarning")}).then(t):t(),!1}function h(){return[{href:"#!/encodingsettings.html",name:r.ZP.translate("Transcoding")},{href:"#!/playbackconfiguration.html",name:r.ZP.translate("ButtonResume")},{href:"#!/streamingsettings.html",name:r.ZP.translate("TabStreaming")}]}$(document).on("pageinit","#encodingSettingsPage",(function(){var e=this;c?Promise.resolve(c):ApiClient.getPublicSystemInfo().then((function(e){return c=e,e})),e.querySelector("#selectVideoDecoder").addEventListener("change",(function(){var t,n,a;"vaapi"==this.value?(e.querySelector(".fldVaapiDevice").classList.remove("hide"),e.querySelector("#txtVaapiDevice").setAttribute("required","required")):(e.querySelector(".fldVaapiDevice").classList.add("hide"),e.querySelector("#txtVaapiDevice").removeAttribute("required")),"nvenc"==this.value||"amf"==this.value?(e.querySelector(".fldOpenclDevice").classList.remove("hide"),e.querySelector("#txtOpenclDevice").setAttribute("required","required"),e.querySelector(".tonemappingOptions").classList.remove("hide")):"vaapi"==this.value?(e.querySelector(".fldOpenclDevice").classList.add("hide"),e.querySelector("#txtOpenclDevice").removeAttribute("required"),e.querySelector(".tonemappingOptions").classList.remove("hide")):(e.querySelector(".fldOpenclDevice").classList.add("hide"),e.querySelector("#txtOpenclDevice").removeAttribute("required"),e.querySelector(".tonemappingOptions").classList.add("hide")),"nvenc"==this.value?e.querySelector(".fldEnhancedNvdec").classList.remove("hide"):e.querySelector(".fldEnhancedNvdec").classList.add("hide"),"linux"!==c.OperatingSystem.toLowerCase()||"vaapi"!=this.value&&"qsv"!=this.value?e.querySelector(".fldVppTonemapping").classList.add("hide"):e.querySelector(".fldVppTonemapping").classList.remove("hide"),this.value?e.querySelector(".hardwareAccelerationOptions").classList.remove("hide"):e.querySelector(".hardwareAccelerationOptions").classList.add("hide"),t=e,n=(n=this.value)||"",Array.prototype.forEach.call(t.querySelectorAll(".chkDecodeCodec"),(function(e){-1===e.getAttribute("data-types").split(",").indexOf(n)?o.ZP.parentWithTag(e,"LABEL").classList.add("hide"):(o.ZP.parentWithTag(e,"LABEL").classList.remove("hide"),a=!0)})),a?t.querySelector(".decodingCodecsList").classList.remove("hide"):t.querySelector(".decodingCodecsList").classList.add("hide")})),$("#btnSelectEncoderPath",e).on("click.selectDirectory",(function(){n.e(3688).then(n.bind(n,63688)).then((function(t){var n=new(0,t.default);n.show({includeFiles:!0,callback:function(t){t&&$(".txtEncoderPath",e).val(t),n.close()}})}))})),$("#btnSelectTranscodingTempPath",e).on("click.selectDirectory",(function(){n.e(3688).then(n.bind(n,63688)).then((function(t){var n=new(0,t.default);n.show({callback:function(t){t&&$("#txtTranscodingTempPath",e).val(t),n.close()},validateWriteable:!0,header:r.ZP.translate("HeaderSelectTranscodingPath"),instruction:r.ZP.translate("HeaderSelectTranscodingPathHelp")})}))})),$("#btnSelectFallbackFontPath",e).on("click.selectDirectory",(function(){n.e(3688).then(n.bind(n,63688)).then((function(t){var n=new(0,t.default);n.show({includeDirectories:!0,callback:function(t){t&&(e.querySelector("#txtFallbackFontPath").value=t),n.close()},header:r.ZP.translate("HeaderSelectFallbackFontPath"),instruction:r.ZP.translate("HeaderSelectFallbackFontPathHelp")})}))})),$(".encodingSettingsForm").off("submit",s).on("submit",s)})).on("pageshow","#encodingSettingsPage",(function(){a.ZP.show(),l.Z.setTabs("playback",0,h);var e=this;ApiClient.getNamedConfiguration("encoding").then((function(t){ApiClient.getSystemInfo().then((function(n){!function(e,t,n){Array.prototype.forEach.call(e.querySelectorAll(".chkDecodeCodec"),(function(e){e.checked=-1!==(t.HardwareDecodingCodecs||[]).indexOf(e.getAttribute("data-codec"))})),e.querySelector("#chkDecodingColorDepth10Hevc").checked=t.EnableDecodingColorDepth10Hevc,e.querySelector("#chkDecodingColorDepth10Vp9").checked=t.EnableDecodingColorDepth10Vp9,e.querySelector("#chkEnhancedNvdecDecoder").checked=t.EnableEnhancedNvdecDecoder,e.querySelector("#chkHardwareEncoding").checked=t.EnableHardwareEncoding,e.querySelector("#chkAllowHevcEncoding").checked=t.AllowHevcEncoding,$("#selectVideoDecoder",e).val(t.HardwareAccelerationType),$("#selectThreadCount",e).val(t.EncodingThreadCount),$("#txtDownMixAudioBoost",e).val(t.DownMixAudioBoost),e.querySelector("#txtMaxMuxingQueueSize").value=t.MaxMuxingQueueSize||"",e.querySelector(".txtEncoderPath").value=t.EncoderAppPathDisplay||"",$("#txtTranscodingTempPath",e).val(n.TranscodingTempPath||""),e.querySelector("#txtFallbackFontPath").value=t.FallbackFontPath||"",e.querySelector("#chkEnableFallbackFont").checked=t.EnableFallbackFont,$("#txtVaapiDevice",e).val(t.VaapiDevice||""),e.querySelector("#chkTonemapping").checked=t.EnableTonemapping,e.querySelector("#chkVppTonemapping").checked=t.EnableVppTonemapping,e.querySelector("#txtOpenclDevice").value=t.OpenclDevice||"",e.querySelector("#selectTonemappingAlgorithm").value=t.TonemappingAlgorithm,e.querySelector("#selectTonemappingRange").value=t.TonemappingRange,e.querySelector("#txtTonemappingDesat").value=t.TonemappingDesat,e.querySelector("#txtTonemappingThreshold").value=t.TonemappingThreshold,e.querySelector("#txtTonemappingPeak").value=t.TonemappingPeak,e.querySelector("#txtTonemappingParam").value=t.TonemappingParam||"",e.querySelector("#selectEncoderPreset").value=t.EncoderPreset||"",e.querySelector("#txtH264Crf").value=t.H264Crf||"",e.querySelector("#txtH265Crf").value=t.H265Crf||"",e.querySelector("#selectDeinterlaceMethod").value=t.DeinterlaceMethod||"",e.querySelector("#chkDoubleRateDeinterlacing").checked=t.DeinterlaceDoubleRate,e.querySelector("#chkEnableSubtitleExtraction").checked=t.EnableSubtitleExtraction||!1,e.querySelector("#chkEnableThrottling").checked=t.EnableThrottling||!1,e.querySelector("#selectVideoDecoder").dispatchEvent(new CustomEvent("change",{bubbles:!0})),a.ZP.hide()}(e,t,n)}))}))}))}}]);