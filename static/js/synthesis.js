
var loremaster=loremaster||{}
loremaster.synthesis={}
let synthesis=loremaster.synthesis;
var synthesizer
var player

synthesis.completed=function(s,e){
    synthesizer.close()
}

synthesis.started=function(s,e){}

synthesis.getAudioConfig=function(){
    player = new SpeechSDK.SpeakerAudioDestination();
    return SpeechSDK.AudioConfig.fromSpeakerOutput(player)
}

synthesis.init=function(){
    const speechConfig=speech.getSpeechConfig(SpeechSDK.SpeechConfig);
    const audioConfig=synthesis.getAudioConfig();
    //speechConfig.speechSynthesisVoiceName = voiceOptions.value;
    speechConfig.speechSynthesisOutputFormat =  SpeechSDK.SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3;
    synthesizer = new SpeechSDK.SpeechSynthesizer(speechConfig, audioConfig);
    //register lifecycle methods
    synthesizer.synthesisStarted=synthesis.started;
    synthesizer.synthesisCompleted=synthesis.completed;
}

synthesis.speechTextAsync=function(text){
    synthesis.init();
    synthesizer.speakTextAsync(text);
}



jQuery(function () {
});