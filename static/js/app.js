var loremaster=loremaster||{}

function init_elements(){
    loremaster.video=document.getElementById('video');
    loremaster.originalText=document.getElementById('ori_text');
    loremaster.analyzeText=document.getElementById('analyze_text');
    loremaster.conversations=[{"role": "system", "content": "You are a helpful assistant."}];
    loremaster.mode='Accessibility';
}

//#region Actions
function capture_image(){
    const preview=document.getElementById("preview");
    const img_preview=document.getElementById("img_preview");
    preview.width=loremaster.video.videoWidth;
    preview.height=loremaster.video.videoHeight;
    preview.getContext('2d').drawImage(video,0,0);
    const imageData=preview.toDataURL('image/png');
    img_preview.src=imageData;
    fetch('/upload', {
        method: 'POST',
        body: JSON.stringify({ image: imageData }),
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log('Server response:', data);
        })
        .catch((error) => {
          console.error('Error sending image:', error);
        });
}

async function convert_text(){
    let spin=document.getElementById("spin-original");
    loremaster.originalText.innerText="";
    spin.hidden=false;
    $.ajax({
        url: '/convert',
        type: 'POST',
        success: (response) => {
            loremaster.originalText.innerText=response;
            //add an user input conversation
            spin.hidden=true;
            add_user_conversation(response);
            if(loremaster.mode=="Accessibility"){
                get_assist_chat(loremaster.conversations);
            }
            
        }
    })
}

function add_user_conversation(text){
    let item={"role": "user", "content": text};
    loremaster.conversations.push(item);
}

function add_system_conversation(text){
    let item={"role": "system", "content": text};
    loremaster.conversations.push(item);
}

async function get_assist_chat(data){
    let spin=document.getElementById("spin-assist");
    let assist_text=document.getElementById("assist_text");
    assist_text.innerHTML="";
    spin.hidden=false;
    $.ajax({
        url:'/assist',
        type:'POST',
        contentType:"application/json",
        data: JSON.stringify(data),
        success:(response)=>{
            assist_text.innerHTML=response;
            spin.hidden=true;
            synthesis.speechTextAsync(response);
            add_system_conversation(response);
        }
    })
}

async function moderate_text(text){
    let spin=document.getElementById("spin-analyze");
    spin.hidden=false;
    $.ajax({
        url:'/refine',
        type:'POST',
        data:text,
        contentType:"application/json",
        success:(response)=>{
            loremaster.analyzeText.innerHTML+="<b>Spell Corrected:</b>"+response.AutoCorrectedText
            spin.hidden=true;
        }
    })
}

function get_content_safety_color(result){
    switch(result){
        case 0: return 'green';
        case 1: return 'lightgreen';
        case 2: return 'yellow';
        case 3: return 'orange'
        case 4: return 'red'
    }
        
}
  

async function content_safety(text){
    let spin=document.getElementById('spin-analyze');
    spin.hidden=false;
    $.ajax({
        url: 'safety',
        type:'POST',
        data:text,
        contentType:"application/json",
        success:(response)=>{
            let violence_result=response.violence_result;
            let self_harm_result=response.self_harm_result;
            let hate_result=response.hate_result;
            let sexual_result=response.sexual_result;
            let violence_html="<span style='color: "+get_content_safety_color(violence_result)+";'>Violence Result:"+violence_result+"</span><br>";
            let self_harm_html="<span style='color: "+get_content_safety_color(self_harm_result)+";'>Self Harm Result: "+self_harm_result+"</span><br>";
            let hate_html="<span style='color: "+get_content_safety_color(hate_result)+";'>Hate Result: "+hate_result+"</span><br>";
            let sexual_html="<span style='color: "+get_content_safety_color(sexual_result)+";'>Sexual Result: "+sexual_result+"</span><br>";
            loremaster.analyzeText.innerHTML+="<br><b>Safety:</b>"+violence_html+"\n"+self_harm_html+"\n"+hate_html+"\n"+sexual_html;
            spin.hidden=true;
        }
    })
}

async function summary_content(text){
    let spin=document.getElementById('spin-analyze');
    spin.hidden=false;
    $.ajax({
        url: 'summary',
        type:'POST',
        data:text,
        contentType:"application/json",
        success:(response)=>{
            loremaster.analyzeText.innerHTML+="<b>Summary: </b>"+response;
            spin.hidden=true;
        }
    })
}

function analyze_text(){
    let text=loremaster.originalText.innerText;
    if(!text){
        alert("No Text for analysis!");
        return;
    }
    loremaster.analyzeText.innerHTML="";
    moderate_text(text);
    content_safety(text);
    summary_content(text);
}

function read_text(text){
    synthesis.speechTextAsync(text);
}
//#endregion

//#region Init functions
async function init_video(){
    
    navigator.mediaDevices.getUserMedia({video:true})
    .then((stream)=>{
        loremaster.video.srcObject=stream;
    }).catch(err=>{
        console.log(err);
    })
}
//#endregion



jQuery(function() {
    init_elements();
    init_video();
    //#region Button Click Events
    $("#btn_capture").on('click',function () {
        capture_image();
    });

    // $('#btn_record').on('click',(evt)=>{
    //     loremaster.speech.doRecognizeOnceAsync();
    // });
    $('#btn_listen').on('click',(evt)=>{
        loremaster.speech.doRecognizeAsync();
    })
    // $('#btn_chat').on('click',(evt)=>{
    //     loremaster.speech.doRecognizeChatAsync();
    // })
    
    $('#a_mode').on('click',(evt)=>{
        if(loremaster.mode=='Accessibility'){
            loremaster.mode='Children';
            
        }else{
            loremaster.mode='Accessibility';
        }
        $('#a_mode').text(loremaster.mode);
    })

    $('#btn_pause').on('click',(evt)=>{
        player.pause();
    })
    $('#btn_resume').on('click',(evt)=>{
        player.resume();
    })
    //#endregion

    //#region DOM Operations

    //#endregion
});