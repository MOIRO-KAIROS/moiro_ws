
import threading, subprocess
import cv2
import os

output_path = os.path.join(os.path.dirname(__file__), 'output')  # os.path.dirname(__file__) = moiro_testTool/moiro_web

def kill_terminal(pname): # subprocess.Popen("ps aux | grep droidcam | grep -v grep | awk '{print $2}' | xargs kill -9", shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    find_command = f"ps aux | grep {pname} | grep -v grep | awk '{{print $2}}'"

    process = subprocess.Popen(find_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    pids = stdout.decode('utf-8').strip().split()
    if pids:
        kill_command = f"kill -9 {' '.join(pids)    }"
        process = subprocess.Popen(kill_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        process.wait()

def create_filename(base_filename="video", extension=".mp4"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    existing_files = sorted(os.listdir(output_path))
    video_files = [f for f in existing_files if f.startswith(base_filename) and f.endswith(extension)]
    next_number = None
    if len(video_files) > 0:
        next_number = video_files[-1][len(base_filename):-len(extension)]
    if next_number is not None and str(next_number.isdigit()):
        next_number = int(next_number) + 1
    else:
        next_number = 1
    return os.path.join(output_path, f"{base_filename}{next_number}{extension}")

class CameraStream:
    def __init__(self, cam_ip, cam_port):
        self.cam_ip = cam_ip
        self.cam_port = cam_port
        self.device = self.set_droidcam()
        self.capture = cv2.VideoCapture(self.device)
        self.fps = self.capture .get(cv2.CAP_PROP_FPS)
        self.frame = None
        self.running = True
        self.lock = threading.Lock()
        self.recording = False
        self.out = None
        threading.Thread(target=self.update, args=()).start()

    def update(self):
        while self.running:
            success, frame = self.capture.read()
            if success:
                with self.lock:
                    self.frame = frame
                    if self.frame is not None and self.recording and self.out is not None:
                        self.out.write(self.frame)


    def get_frame(self):
        with self.lock:
            if self.frame is None:
                return None
            ret, buffer = cv2.imencode('.jpg', self.frame)
            return buffer.tobytes()

    def stop(self):
        self.running = False
        self.capture.release()
        self.stop_recording()
    
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

    def start_recording(self):
        filename = create_filename()
        if self.recording:
            print("Recording is already in progress.")
            return

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        frame_size = (int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fps = int(self.capture.get(cv2.CAP_PROP_FPS))
        self.out = cv2.VideoWriter(filename, fourcc, fps, frame_size)
        if not self.out.isOpened():
            print('File open failed!')
            self.stop_recording()
            return
        self.recording = True
        print("Recording started.")

    def stop_recording(self):
        if not self.recording:
            print("No recording in progress.")
            return

        self.recording = False
        if self.out is not None:
            self.out.release()
            self.out = None
            print("Recording stopped.")

if __name__ == "__main__":
    cam_ip = input("Enter camera IP: ")
    cam_port = input("Enter camera port: ")

    camera_stream = CameraStream(cam_ip, cam_port)
    
    camera_stream.start_recording()

    while True:
        with camera_stream.lock:
            if camera_stream.frame is not None:
                cv2.imshow('frame', camera_stream.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            camera_stream.stop_recording()
            camera_stream.stop()
            break

    cv2.destroyAllWindows()