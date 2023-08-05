(self.webpackChunk=self.webpackChunk||[]).push([[4503],{94503:function(e){e.exports='<div class="verticalSection"> <div class="sectionTitleContainer flex align-items-center"> <h1 class="sectionTitle">Xml TV</h1> <a is="emby-linkbutton" rel="noopener noreferrer" class="raised button-alt headerHelpButton" target="_blank" href="https://docs.jellyfin.org/general/server/live-tv/setup-guide.html#adding-guide-data">${Help}</a> </div> </div> <form class="xmltvForm"> <div> <div class="inputContainer"> <div style="display:flex;align-items:center"> <div style="flex-grow:1"> <input is="emby-input" class="txtPath" label="${LabelFileOrUrl}" required="required" autocomplete="off"/> </div> <button type="button" is="paper-icon-button-light" id="btnSelectPath" class="emby-input-iconbutton"><span class="material-icons search"></span></button> </div> <div class="fieldDescription">${XmlTvPathHelp}</div> </div> <div class="inputContainer"> <input is="emby-input" class="txtMovies" label="${LabelMovieCategories}" autocomplete="off"/> <div class="fieldDescription">${XmlTvMovieCategoriesHelp}</div> </div> <div class="inputContainer"> <input is="emby-input" class="txtMoviePrefix" label="${LabelMoviePrefix}" autocomplete="off"/> <div class="fieldDescription">${LabelMoviePrefixHelp}</div> </div> <div class="inputContainer"> <input is="emby-input" class="txtKids" label="${LabelKidsCategories}" autocomplete="off"/> <div class="fieldDescription">${XmlTvKidsCategoriesHelp}</div> </div> <div class="inputContainer"> <input is="emby-input" class="txtNews" label="${LabelNewsCategories}" autocomplete="off"/> <div class="fieldDescription"></div> <div class="fieldDescription">${XmlTvNewsCategoriesHelp}</div> </div> <div class="inputContainer"> <input is="emby-input" class="txtSports" label="${LabelSportsCategories}" autocomplete="off"/> <div class="fieldDescription">${XmlTvSportsCategoriesHelp}</div> </div> <div class="inputContainer fldUserAgent"> <input is="emby-input" type="text" class="txtUserAgent" label="${LabelUserAgent}" autocomplete="off"/> <div class="fieldDescription">${UserAgentHelp}</div> </div> </div> <div> <label class="checkboxContainer"> <input type="checkbox" is="emby-checkbox" class="chkAllTuners"/> <span>${OptionEnableForAllTuners}</span> </label> <div class="selectTunersSection hide"> <h3 class="checkboxListLabel">${HeaderTuners}</h3> <div class="checkboxList paperList checkboxList-paperList tunerList"> </div> </div> </div> <div> <button is="emby-button" type="submit" class="raised button-submit block btnSubmitListings hide"><span>${Save}</span></button> <button is="emby-button" type="button" class="raised button-cancel block btnCancel hide" onclick="history.back()"><span>${ButtonCancel}</span></button> </div> </form> '}}]);