from flask import Flask, render_template, request, Response, jsonify
from flask_socketio import SocketIO, emit
import requests, os
from utils import CameraStream, kill_terminal
from ament_index_python.packages import get_package_share_directory

app = Flask(__name__)
# socketio = SocketIO(app)

camera_stream = None
embed_path = os.path.join(os.path.dirname(__file__), 'embed') # os.path.dirname(__file__) = moiro_testTool/moiro_web

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

@app.route('/get_file_list', methods=['GET'])
def get_file_list():
    dir_list = sorted(os.listdir(embed_path))
    dir_list = [os.path.splitext(f)[0] for f in dir_list]

    return jsonify(dir_list)

@app.route('/get_names_from_file', methods=['POST'])
def get_names_from_file():
    filename = os.path.join(embed_path, f"{request.form['filename']}.txt")
    # print(filename)
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            names = [line.strip() for line in file.readlines()]
        return jsonify(names)
    return jsonify([])

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
@app.route('/start_rasp', methods=['POST'])
def start_rasp():
    rasp_ip = request.form['rasp_ip']
    rasp_port = request.form['rasp_port']
    
    response = requests.post(f'http://{rasp_ip}:{rasp_port}/start_rasp')
    return response.text
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

@app.route('/sync_play', methods=['POST'])
def sync_play():
    com1_ip = request.form['com1_ip']
    com1_port = request.form['com1_port']
    
    response = requests.post(f'http://{com1_ip}:{com1_port}/sync_play')
    return response.text

@app.route('/killAdaface', methods=['POST'])
def killAdaface():
    com1_ip = request.form['com1_ip']
    com1_port = request.form['com1_port']
    
    response = requests.post(f'http://{com1_ip}:{com1_port}/killAdaface')
    return response.text

@app.route('/killSyncPlay', methods=['POST'])
def killSyncPlay():
    com1_ip = request.form['com1_ip']
    com1_port = request.form['com1_port']
    
    response = requests.post(f'http://{com1_ip}:{com1_port}/killSyncPlay')
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

@app.route('/killHF', methods=['POST'])
def killHF():
    com2_ip = request.form['com2_ip']
    com2_port = request.form['com2_port']
    
    response = requests.post(f'http://{com2_ip}:{com2_port}/killHF')
    return response.text

@app.route('/killMycobot', methods=['POST'])
def killMycobot():
    com2_ip = request.form['com2_ip']
    com2_port = request.form['com2_port']
    
    response = requests.post(f'http://{com2_ip}:{com2_port}/killMycobot')
    return response.text

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        kill_terminal('8080')