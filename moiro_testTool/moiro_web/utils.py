
import threading, subprocess
import cv2

class CameraStream:
    def __init__(self, cam_ip, cam_port):
        self.device = self.set_droidcam(cam_ip, cam_port)
        self.capture = cv2.VideoCapture(self.device)
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
    
    # droidcam-cli 세팅
    def set_droidcam(self, cam_ip, cam_port):
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
