(self.webpackChunk=self.webpackChunk||[]).push([[2975],{17076:function(e){e.exports='<div id="playbackConfigurationPage" data-role="page" class="page type-interior playbackConfigurationPage withTabs"> <div> <div class="content-primary"> <form class="playbackConfigurationForm"> <div class="sectionTitleContainer flex align-items-center"> <h2 class="sectionTitle">${ButtonResume}</h2> </div> <div class="inputContainer"> <input is="emby-input" type="number" id="txtMinResumePct" name="txtMinResumePct" pattern="[0-9]*" required min="0" max="100" label="${LabelMinResumePercentage}"> <div class="fieldDescription"> ${LabelMinResumePercentageHelp} </div> </div> <div class="inputContainer"> <input is="emby-input" type="number" id="txtMaxResumePct" name="txtMaxResumePct" pattern="[0-9]*" required min="1" max="100" label="${LabelMaxResumePercentage}"> <div class="fieldDescription"> ${LabelMaxResumePercentageHelp} </div> </div> <div class="inputContainer"> <input is="emby-input" type="number" id="txtMinAudiobookResume" name="txtMinAudiobookResume" pattern="[0-9]*" required min="0" max="100" label="${LabelMinAudiobookResume}"> <div class="fieldDescription"> ${LabelMinAudiobookResumeHelp} </div> </div> <div class="inputContainer"> <input is="emby-input" type="number" id="txtMaxAudiobookResume" name="txtMaxAudiobookResume" pattern="[0-9]*" required min="1" max="100" label="${LabelMaxAudiobookResume}"> <div class="fieldDescription"> ${LabelMaxAudiobookResumeHelp} </div> </div> <div class="inputContainer"> <input is="emby-input" type="number" id="txtMinResumeDuration" name="txtMinResumeDuration" pattern="[0-9]*" required min="0" label="${LabelMinResumeDuration}"> <div class="fieldDescription"> ${LabelMinResumeDurationHelp} </div> </div> <div><button is="emby-button" type="submit" class="raised button-submit block"><span>${Save}</span></button></div> </form> </div> </div> </div> '}}]);