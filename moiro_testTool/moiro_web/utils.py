
import threading, subprocess
import cv2

def kill_terminal(pname): # subprocess.Popen("ps aux | grep droidcam | grep -v grep | awk '{print $2}' | xargs kill -9", shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    find_command = f"ps aux | grep {pname} | grep -v grep | awk '{{print $2}}'"

    process = subprocess.Popen(find_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    pids = stdout.decode('utf-8').strip().split()
    if pids:
        kill_command = f"kill -9 {' '.join(pids)    }"
        process = subprocess.Popen(kill_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        process.wait()

class CameraStream:
    def __init__(self, cam_ip, cam_port):
        self.cam_ip = cam_ip
        self.cam_port = cam_port
        self.device = self.set_droidcam()
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
    
    # droidcam-cli 세팅 & echo 디바이스 명
    def exe_terminal(self):
        kill_terminal("droidcam")
        subprocess.Popen(f'droidcam-cli {self.cam_ip} {self.cam_port}', shell=True)

        process = subprocess.Popen("echo $(v4l2-ctl --list-devices | grep -A 1 'Droidcam') | awk '{print $3}'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        process.wait()
        
        return stdout.decode('utf-8').strip()
    
    def set_droidcam(self):
        camera_device = None
        result = self.exe_terminal()
        if "/dev/video" in result:
            print(f"Droidcam is connected to {result}")
            camera_device = result
        else:
            print("Droidcam is not connected")

        return camera_device