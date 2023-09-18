import base64
from urllib.parse import unquote, unquote_plus

import cv2
import numpy as np
from flask import Flask, Response, jsonify, render_template, request

from chatgpt import ChatGPT
from contentmoderator import ContentModerator
from contentsafety import ContentSafety
from conversation import ConversationUnderstanding
from formrecognizer import FormRecognizer
from msallib import MSAL
from speech import Speech
from textanalysis import TextAnalytics

app = Flask(__name__)



camera = cv2.VideoCapture(0)
current_frame=None

def generate_frames():
    global current_frame
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            current_frame=frame.copy()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

#upload the image and generate image file
@app.route('/upload',methods=['POST'])
def upload():
    data=request.json
    image_data=data.get('image')
    image_data = image_data.split(',')[1]  # 去除DataURL前缀
    image_bytes = bytes(image_data, encoding='utf-8')
    nparr = np.frombuffer(base64.b64decode(image_bytes), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('./static/captured_image.jpg', image)
    return {'status':'succeed','data':'captured_image.jpg'}

@app.route('/capture',methods=['POST'])
def capture():
    global current_frame
    if current_frame is not None:
        cv2.imwrite('./static/captured_image.jpg',current_frame)
        return "captured_image.jpg"
    else:
        pass

#convert the image to text
@app.route('/convert',methods=['POST'])
def pic_analyze():
    fr=FormRecognizer()
    path='./static/captured_image.jpg'
    image=cv2.imread(path)
    text=None
    if image is not None:
        byte_arr=cv2.imencode('.jpg',image)[1].tobytes()
        text=fr.get_text(byte_arr)
    return text

#get aad token
@app.route('/aadtoken',methods=['GET'])
def get_aad_token():
    auth=MSAL()
    token=auth.acquireToken()
    return token

#get the speech token
@app.route('/speechtoken',methods=['GET'])
def get_speech_token():
    speech=Speech()
    token=speech.get_token()
    return token

# get the intent of the text
@app.route('/intent',methods=['POST'])
def get_intent():
    text=request.get_data().decode('utf-8')
    conversation=ConversationUnderstanding()
    result=conversation.analyze_query(text)
    return result

# modify the content to remove PII, violence text etc.
@app.route('/refine',methods=['POST'])
def refine_content():
    text=request.get_data().decode('utf-8')
    moderator=ContentModerator()
    result=moderator.call_api(data=text)
    return result

# detect the text's violence level
@app.route('/safety',methods=['POST'])
def guard_content():
    text=request.get_data().decode('utf-8')
    guard=ContentSafety()
    result=guard.analyze_text(text=text)
    return result

@app.route('/summary',methods=['POST'])
def summary_content():
    text=request.get_data()
    text=text.decode('utf-8')
    text=text.replace('\'','')
    summarizer=TextAnalytics()
    result=summarizer.analyze_text(text=text)
    return result

@app.route('/assist',methods=['POST'])
def assist_response():
    data=request.get_json()
    chat=ChatGPT()
    res=chat.get_response(data=data)
    return res



if __name__ == '__main__':
    app.run(debug=True)