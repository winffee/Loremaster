import cv2
from flask import Flask, Response, jsonify, render_template

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


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/shot_click',methods=['POST'])
def capture():
    global current_frame
    if current_frame is not None:
        cv2.imwrite('./static/captured_image.jpg',current_frame)
        return "captured_image.jpg"
    else:
        pass



if __name__ == '__main__':
    app.run(debug=True)