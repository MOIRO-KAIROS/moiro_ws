from flask import Flask, render_template, request, Response
import threading
import subprocess
import cv2
import   requests

app = Flask(__name__)

camera_stream = None

class CameraStream:
    def __init__(self, device='0'):
        self.capture = cv2.VideoCapture(device)
        self.frame = None
        self.running = True
        self.lock = threading.Lock()
        threading.Thread(target=self.update, args=()).start()

    def update(self):
        while self.running:
            success, frame = self.capture.read()
            if success:
                with self.lock:
                    self.frame = frame

    def get_frame(self):
        with self.lock:
            if self.frame is None:
                return None
            ret, buffer = cv2.imencode('.jpg', self.frame)
            return buffer.tobytes()

    def stop(self):
        self.running = False
        self.capture.release()

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

def set_droidcam(cam_ip, cam_port):
    camera_device = None
    subprocess.Popen("ps aux | grep droidcam | grep -v grep | awk '{print $2}' | xargs kill -9", 
                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    # process.wait()
    command = f'droidcam-cli {cam_ip} {cam_port}'
    process = subprocess.Popen(['bash', '-c', command])
    # process.wait()

    process = subprocess.Popen("echo $(v4l2-ctl --list-devices | grep -A 1 'Droidcam') | awk '{print $3}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # 명령어 실행 결과 확인
    result = stdout.decode('utf-8').strip()
    
    if "/dev/video" in result:
        print(f"Droidcam is connected to {result}")
        camera_device = result
    else:
        print("Droidcam is not connected")

    # 프로세스가 완료될 때까지 대기 후 종료
    process.wait()

    return camera_device # echo $(v4l2-ctl --list-devices | grep -A 1 "Droidcam") | awk '{print $3}'

@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera_stream
    cam_ip = request.form['cam_ip']
    cam_port = request.form['cam_port']
    
    # droidcam-cli 명령어 실행
    camera_device = set_droidcam(cam_ip, cam_port) 
    
    if camera_stream is None:
        camera_stream = CameraStream(camera_device)
    else:
        camera_stream.stop()
        camera_stream = CameraStream(camera_device)

    return 'Camera stream started'

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera_stream
    if camera_stream is not None:
        camera_stream.stop()
        camera_stream = None
        # droidcam 시스템 종료
        subprocess.Popen("ps aux | grep droidcam | grep -v grep | awk '{print $2}' | xargs kill -9", 
                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return 'Camera stream stopped'
    return 'No camera stream to stop'

@app.route('/start_adaface', methods=['POST'])
def start_adaface():
    com1_ip = request.form['com1_ip']
    com1_port = request.form['com1_port']
    
    response = requests.post(f'http://{com1_ip}:{com1_port}/start_adaface')
    return response.text

@app.route('/start_follower', methods=['POST'])
def start_follower():
    com2_ip = request.form['com2_ip']
    com2_port = request.form['com2_port']
    
    response = requests.post(f'http://{com2_ip}:{com2_port}/start_follower')
    return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
