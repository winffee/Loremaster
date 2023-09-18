var microphoneSources;
var region = "southeastasia";
var recognizer
var loremaster = loremaster || {};
loremaster.speech = loremaster.speech || {};
let speech = loremaster.speech;

//#region Init and Configurations
speech.Initialize = async function () {
    speech.authorizationToken = await speech.RequestAuthorizationToken();
}

speech.RequestAuthorizationToken = async function () {
    return $.ajax({
        url: '/speechtoken',
        type: 'GET',
    })
}

speech.getAudioConfig = function () {
    return SpeechSDK.AudioConfig.fromMicrophoneInput('default');
}

speech.getSpeechConfig = function (sdkConfigType) {
    var speechConfig;

    if (speech.authorizationToken) {
        speechConfig = sdkConfigType.fromAuthorizationToken(speech.authorizationToken, region);
    }

    // Defines the language(s) that speech should be translated to.
    // Multiple languages can be specified for text translation and will be returned in a map.
    if (sdkConfigType == SpeechSDK.SpeechTranslationConfig) {
        speechConfig.addTargetLanguage("en-US");

        // If voice output is requested, set the target voice.
        // If multiple text translations were requested, only the first one added will have audio synthesised for it.
        speechConfig.setProperty(SpeechSDK.PropertyId.SpeechServiceConnection_TranslationVoice, "en-US");
    }
    speechConfig.speechRecognitionLanguage = "en-US";
    return speechConfig;
}
//#endregion

//#region Speech Recognization Lifecycle

speech.onRecognizedResult = async function (result) {
    switch (result.reason) {
        case SpeechSDK.ResultReason.NoMatch:
            var noMatchDetail = SpeechSDK.NoMatchDetails.fromResult(result);
            break;
        case SpeechSDK.ResultReason.Canceled:
            var cancelDetails = SpeechSDK.CancellationDetails.fromResult(result);
            break;
        case SpeechSDK.ResultReason.RecognizedSpeech:
            console.log(result);
            if (result.text.startsWith("Intent")) {
                speech.showSpeechResult(result.text);
                let intent = await speech.getIntent(result.text);
                speech.showIntentResult(intent);
                speech.applyIntentAction(intent);
            } else if (result.text.startsWith("Chat")) {
                speech.showChatResult(result.text);
            } else {
                speech.showOtherResult("Sorry, I can't recognize what you said!");
            }

            break;
        case SpeechSDK.ResultReason.TranslatedSpeech:
            break;
        case SpeechSDK.ResultReason.RecognizedIntent:
            break;
    }
}


speech.onCanceled = function (sender, cancellationEventArgs) {
    window.console.log(cancellationEventArgs);

}

speech.applyConfiguration = function (recognizer) {

    //session started
    recognizer.sessionStarted = (sender, sessionEventArgs) => {
        speech.changeListenButton(true);
    };
    //session stopped
    recognizer.sessionStopped = (sender, sessionEventArgs) => {
        speech.changeListenButton(false);
    };
}

//#endregion

//#region Call API
speech.getIntent = async function (text) {
    const response = await $.ajax({
        url: '/intent',
        type: 'POST',
        data: text
    });
    let topIntent = response.result.prediction.topIntent;
    return topIntent;
}
//#endregion

//#region DOM Operations
speech.showChatResult = function (text) {
    add_user_conversation(text);
    get_assist_chat(loremaster.conversations);
}

speech.showOtherResult=function(text){
    $('#ori_text').text(text);
    read_text(text);
}

speech.showSpeechResult = function (text) {
    $("#speechResult").text(text);
}

speech.showIntentResult = function (text) {
    $("#intentResult").text(text);
}

speech.changeListenButton = function (recording) {
    if (recording) {
        $('#btn_listen').text('Listening...');
    } else {
        $('#btn_listen').text('Listen')
    }
}
//#endregion



//#region Main Functions

speech.applyIntentAction = function (intent) {
    switch (intent) {
        case 'Capture': capture_image(); break;
        case 'Convert Image': convert_text(); break;
        case 'Analyze Text': analyze_text(); break;
        //case 'Read Content': read_text(); break;
    }
}

speech.doRecognizeAsync = async function () {
    if (!recognizer) {
        var audioConfig = speech.getAudioConfig();
        var speechConfig = speech.getSpeechConfig(SpeechSDK.SpeechConfig);
        recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig);
        speech.applyConfiguration(recognizer);
    }
    recognizer.recognized = undefined

    recognizer.recognizeOnceAsync((successResult) => {
        console.log("successResult",successResult);
        speech.onRecognizedResult(successResult);
    }, (err) => {
        console.log(err);
    })
}



jQuery(function () {
    speech.Initialize();
});
//#endregion