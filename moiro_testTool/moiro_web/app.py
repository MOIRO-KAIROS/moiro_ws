from flask import Flask, render_template, request, Response
import requests
from utils import CameraStream, kill_terminal

app = Flask(__name__)

camera_stream = None

def gen_frames():
    global camera_stream
    while True:
        try:
            if camera_stream is None:
                continue
            frame = camera_stream.get_frame()
            if frame is None:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera_stream
    cam_ip = request.form['cam_ip']
    cam_port = request.form['cam_port']
    
    if camera_stream is not None:
        camera_stream.stop()
    camera_stream = CameraStream(cam_ip, cam_port)

    return 'Camera stream started'

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera_stream
    if camera_stream is not None:
        camera_stream.stop()
        camera_stream = None
        kill_terminal("droidcam")
        return 'Camera stream stopped'
    return 'No camera stream to stop'
###
@app.route('/start_adaface', methods=['POST'])
def start_adaface():
    com1_ip = request.form['com1_ip']
    com1_port = request.form['com1_port']
    person_name = request.form['person_name']
    
    response = requests.post(f'http://{com1_ip}:{com1_port}/start_adaface',person_name)
    return response.text

@app.route('/reset_name', methods=['POST'])
def reset_name():
    com1_ip = request.form['com1_ip']
    com1_port = request.form['com1_port']
    person_name = request.form['person_name']
    
    response = requests.post(f'http://{com1_ip}:{com1_port}/reset_name',person_name)
    return response.text
###
@app.route('/start_follower', methods=['POST'])
def start_follower():
    com2_ip = request.form['com2_ip']
    com2_port = request.form['com2_port']
    min_depth = request.form['min_depth']
    max_depth = request.form['max_depth']
    
    response = requests.post(f'http://{com2_ip}:{com2_port}/start_follower',json=[min_depth, max_depth])
    return response.text
@app.route('/reset_depth', methods=['POST'])
def reset_depth():
    com2_ip = request.form['com2_ip']
    com2_port = request.form['com2_port']
    min_depth = request.form['min_depth']
    max_depth = request.form['max_depth']
    
    response = requests.post(f'http://{com2_ip}:{com2_port}/reset_depth',json=[min_depth, max_depth])
    return response.text

@app.route('/mycobot', methods=['POST'])
def mycobot():
    com2_ip = request.form['com2_ip']
    com2_port = request.form['com2_port']
    
    response = requests.post(f'http://{com2_ip}:{com2_port}/mycobot')
    return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
