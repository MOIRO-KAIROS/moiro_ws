#! /usr/bin/env python3
# encoding:utf-8
import sys
import os
from ament_index_python.packages import get_package_share_directory
import time, traceback, subprocess

from moiro_gui.moiro_window_for_debug import Ui_MainWindow as moiro_window

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ansi2html import Ansi2HTMLConverter

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal

class ImageListenerThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        rclpy.init()
        self.node = rclpy.create_node('image_listener')
        self.subscription = self.node.create_subscription(Image, '/camera1/image_raw', self.listener_callback, 10)
        # self.subscription = self.node.create_subscription(Image, '/vision/dbg_image', self.listener_callback, 10)
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.change_pixmap_signal.emit(q_image)

    def run(self):
        while rclpy.ok():
            rclpy.spin_once(self.node, timeout_sec=0.1)

    def stop(self):
        self.node.destroy_node()
        rclpy.shutdown()

class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, device=0):
        super().__init__()
        self.device = device
        self._running = True # 창 종료 시, CameraThread 종료

    def run(self):
        # Set the camera device number
        self.capture = cv2.VideoCapture(self.device)
        while self._running:
            ret, frame = self.capture.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)
        self.capture.release()

    def stop(self):
        self._running = False
        self.wait()

class DebugThread(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, fr_process, hf_process):
        super().__init__()
        self.fr_process = fr_process
        self.hf_process = hf_process
        self.converter = Ansi2HTMLConverter()

    def run(self):
        while True:
            if self.hf_process:
                hf_err = self.hf_process.stderr.readline().decode().strip()
                if hf_err:
                    self.output_signal.emit(self.convert_ansi_to_html(hf_err))

            if self.fr_process:
                fr_output = self.fr_process.stdout.readline().decode().strip()
                if fr_output:
                    self.output_signal.emit(self.convert_ansi_to_html(fr_output))

    def update_processes(self, fr_process, hf_process):
        self.fr_process = fr_process
        self.hf_process = hf_process
    
    def convert_ansi_to_html(self, ansi_text):
        # print(ansi_text)
        # Convert ANSI text to HTML using ansi2html
        return self.converter.convert(ansi_text, full=False)
                                      
class Myagv_Window(moiro_window, QMainWindow):
    def __init__(self):
        super(Myagv_Window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('moiro Test Tool')
        self.ros = False
        self.run_launch = ""

        self.adaface_process = None
        self.follower_process = None
        self.adaface_button.setCheckable(True)
        self.adaface_button.clicked.connect(self.toggle_adaface)

        self.follower_button.setCheckable(True)
        self.follower_button.clicked.connect(self.toggle_follower)
        self.reset_fr.clicked.connect(self.reset_person_name)
        self.reset_hf.clicked.connect(self.reset_depth_range)

        # 카메라 스레드 시작
        self.camera_thread = CameraThread()
        self.camera_thread.change_pixmap_signal.connect(self.update_image)
        self.camera_thread.start()

        # ROS2 이미지 리스너 스레드 시작
        self.image_listener_thread = ImageListenerThread()
        self.image_listener_thread.change_pixmap_signal.connect(self.update_dbg)
        self.image_listener_thread.start()

        # Debugger 스레드 시작
        self.debug_thread = DebugThread(self.adaface_process, self.follower_process)
        self.debug_thread.output_signal.connect(self.append_debug_output)
        self.debug_thread.start()
        
        # self.paths example : /home/minha/moiro_gui_ws/install/
        self.paths = os.path.abspath(os.path.join(get_package_share_directory('adaface_ros'), "../../../"))
    ######################################################################################
    def append_debug_output(self, output):
        if "WARN" in output:
            colored_output = f"<font color='orange'>{output}</font>"
        elif "ERROR" in output:
            colored_output = f"<font color='red'>{output}</font>"
        else:
            colored_output = output
        self.textBrowser_debugger.append(colored_output)
        # self.textBrowser_debugger.verticalScrollBar().setValue(self.textBrowser_debugger.verticalScrollBar().maximum())

    def closeEvent(self, event):
        self.camera_thread.stop()
        self.image_listener_thread.stop()
        self.debug_thread.terminate()
        event.accept()

    def update_image(self, image):
        self.camera_label.setPixmap(QPixmap.fromImage(image))
        
    def update_dbg(self, image):
        self.dbg_image_label.setPixmap(QPixmap.fromImage(image))
    ######################################################################################

    def toggle_adaface(self):
        if self.adaface_button.isChecked():  # If button is checked
            self.start_adaface()  # Start adaface
        else:
            self.stop_adaface()  # Stop adaface

    def start_adaface(self):
        current_time = self.get_current_time()
        command = f"ros2 launch adaface_ros adaface.launch.py"
        mes = 'Start Face recognition(Adaface)..... '
        self.textBrowser_log.append(f"[{str(current_time)}] {mes}")
        try:
            person_name = self.person_comboBox.currentText()
            
            if person_name:
                command += f" person_name:={person_name}"
                mes = f"Initialized with <b>{person_name}"
            else:
                mes = show_warning_message(f'Target Value Uninitialized')
            self.adaface_process = subprocess.Popen(['bash', '-c', f"source ~/.bashrc && source {self.paths}/setup.bash && {command}"], shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.textBrowser_log.append(f" >>> {mes}")
            self.debug_thread.update_processes(self.adaface_process,self.follower_process)
            
            # GUI 차단되지 않고 프로세스 결과를 가져오기 위해 스레드 사용
            # threading.Thread(target=self.get_process_output, args=(self.adaface_process,), daemon=True).start()
            
        except Exception as e:
            e = traceback.format_exc()
            with open("/home/ubuntu/error.log", "a") as f:
                f.write(e)
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")
        
        
    def stop_adaface(self):
        kill_pid = [
                    os.path.join(self.paths, 'adaface_ros/lib/adaface_ros'),
                    os.path.join(self.paths, 'yolov8_ros/lib/yolov8_ros'),
                    os.path.join(self.paths, 'realsense2_camera/lib/realsense2_camera')
                    ]
        current_time = self.get_current_time()
        if self.adaface_process:
            for pid in kill_pid:
                subprocess.Popen(['bash', '-c', f"ps -ef | grep '{pid}' | grep -v grep | awk '{{print $2}}' | xargs kill"], shell=False)
            self.adaface_process = None  # Reset the subprocess
            mes = 'Stop Face recognition(Adaface)'
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")

    def reset_person_name(self):
        current_time = self.get_current_time()
        try:
            person_name = self.person_comboBox.currentText()
            
            if self.adaface_process:
                mes = 'Reset target person: '
                if person_name:
                    mes += person_name
                    command = f"ros2 service call /vision/person_name moiro_interfaces/srv/Person \"{{person_name: {person_name}}}\""
                    subprocess.Popen(['bash', '-c', f"source {self.paths}/setup.bash && {command}"], shell=False)
            else:
                mes = show_error_message("push 'Start FR' button, then push 'reset' button")
            
            self.textBrowser_log.append('[' + str(current_time) + ']' + ' ' + mes)
        except Exception as e:
            e = traceback.format_exc()
            with open("/home/ubuntu/error.log", "a") as f:
                f.write(e)
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")
    
    ######################################################################################
    def toggle_follower(self):
        if self.follower_button.isChecked():  # If button is checked
            self.start_HF()  # Start HF
        else:
            self.stop_HF()  # Stop HF

    def start_HF(self):
        current_time = self.get_current_time()
        command = f"ros2 run human_follower human_follower -ros-args --output screen "
        mes = 'Start Human follower! '
        self.textBrowser_log.append(f"[{str(current_time)}] {mes}")
        try:
            min_depth = self.depth_min_input.text()
            max_depth = self.depth_max_input.text()
            if min_depth.isdigit() and max_depth.isdigit():
                command += f" min_depth:={min_depth} max_depth:={max_depth}"
                mes += f"[ <b>{min_depth} cm ~ {max_depth} cm</b> ]"
            else:
                command += f" min_depth:=100 max_depth:=150"
                mes = show_warning_message(f'Target Depth must be integer! (default: <b>100 ~ 150 cm</b>)')
            self.follower_process = subprocess.Popen(['bash', '-c', f"source ~/.bashrc && source {self.paths}/setup.bash && {command}"], shell=False, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            self.textBrowser_log.append(f" >>> {mes}") 
            self.debug_thread.update_processes(self.adaface_process,self.follower_process)

        except Exception as e:
            e = traceback.format_exc()
            with open("/home/ubuntu/error.log", "a") as f:
                f.write(e)
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")
 
    def stop_HF(self):
        kill_pid = [os.path.join(self.paths, '/human_follower/lib/human_follower')]
        current_time = self.get_current_time()
        if self.follower_process:
            for pid in kill_pid:
                subprocess.Popen(['bash', '-c', f"ps -ef | grep '{pid}' | grep -v grep | awk '{{print $2}}' | xargs kill"], shell=False)
            self.follower_process = None  # Reset the subprocess
            mes = 'Stop Human Follower'
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")
    
    def reset_depth_range(self):
        current_time = self.get_current_time()
        try:
            min_depth = self.depth_min_input.text()
            max_depth = self.depth_max_input.text()
            if self.follower_process:
                mes = 'Reset target depth: '
                if min_depth.isdigit() and max_depth.isdigit():
                    mes += f"{min_depth} cm ~ {max_depth} cm"
                    command = f"ros2 service call /vision/target_depth moiro_interfaces/srv/TargetDepth \"{{min_depth: {min_depth}}}\"{{max_depth: {max_depth}}}\""
                    subprocess.Popen(['bash', '-c', f"source {self.paths}/setup.bash && {command}"], shell=False)
            else:
                mes = show_error_message("push 'Start HF' button, then push 'reset' button")
            
            self.textBrowser_log.append('[' + str(current_time) + ']' + ' ' + mes)
        except Exception as e:
            e = traceback.format_exc()
            with open("/home/ubuntu/error.log", "a") as f:
                f.write(e)
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")


    def execute_in_terminal(self, command=""):
        full_command = f"source ~/.bashrc && source {self.paths}/setup.bash && {command}"
        process = subprocess.Popen(['bash', '-c', full_command], shell=False)
        # process.wait()

    def get_current_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return current_time
    
    # 프로세스 결과를 가져와서 텍스트 브라우저에 출력
    def get_process_output(self, process):
        stdout, stderr = process.communicate()
        if stdout:
            self.textBrowser_debugger.append(stdout.decode('utf-8'))
        if stderr:
            self.textBrowser_debugger.append(stderr.decode('utf-8'))

def show_error_message(message):
    return f"<font style='color: red'><b>[Error]</b> {message}</font>"

def show_warning_message(message):
    return f"<font style='color: Orange'><b>[Warning]</b> {message}</font>"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Myagv_Window()
    main_window.show()
    sys.exit(app.exec_())
