#! /usr/bin/env python3
# encoding:utf-8
import sys
import os
import time
import threading
import traceback
import subprocess
import time
from PyQt5.QtWidgets import QMainWindow, QApplication

from moiro_window import Ui_MainWindow as moiro_window

import cv2
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

lock = False

class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def run(self):
        self.capture = cv2.VideoCapture(0)
        while True:
            ret, frame = self.capture.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(p)

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

        self.follower_button.clicked.connect(self.reset_depth_range)
        self.reset_fr.clicked.connect(self.reset_person_name)
        self.reset_hf.clicked.connect(self.reset_depth_range)

        # 카메라 스레드 시작
        self.thread = CameraThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def closeEvent(self, event):
        self.thread.terminate()
        event.accept()

    def update_image(self, image):
        self.camera_label.setPixmap(QPixmap.fromImage(image))

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
            self.adaface_process = subprocess.Popen(['bash', '-c', f"source ~/.bashrc && source ~/moiro_ws/install/setup.bash && {command}"], shell=False)
            self.textBrowser_log.append(f" >>> {mes}")
            
            # GUI 차단되지 않고 프로세스 결과를 가져오기 위해 스레드 사용
            # threading.Thread(target=self.get_process_output, args=(self.adaface_process,), daemon=True).start()
            
        except Exception as e:
            e = traceback.format_exc()
            with open("/home/ubuntu/error.log", "a") as f:
                f.write(e)
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")
        
        
    def stop_adaface(self):
        kill_pid = ['/home/minha/moiro_ws/install/adaface_ros/lib/adaface_ros/world_node',
                    '/home/minha/moiro_ws/install/adaface_ros/lib/adaface_ros/face_recognition',
                    '/home/minha/moiro_ws/install/yolov8_ros/lib/yolov8_ros/debug_node',
                    '/home/minha/moiro_ws/install/yolov8_ros/lib/yolov8_ros/tracking_node',
                    '/home/minha/moiro_ws/install/yolov8_ros/lib/yolov8_ros/yolov8_node',
                    '/home/minha/moiro_ws/install/realsense2_camera/lib/realsense2_camera/realsense2_camera_node'
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
                    subprocess.Popen(['bash', '-c', f"source ~/moiro_ws/install/setup.bash && {command}"], shell=False)
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
        command = f"ros2 run human_follower human_follower "
        mes = 'Start Human follower..... '
        self.textBrowser_log.append(f"[{str(current_time)}] {mes}")
        try:
            min_depth = self.depth_min_input.text()
            max_depth = self.depth_max_input.text()
            if min_depth.isdigit() and max_depth.isdigit():
                command += f" min_depth:={min_depth} max_depth:={max_depth}"
                mes += f"{min_depth} cm ~ {max_depth} cm"
            else:
                command += f" min_depth:=100 max_depth:=150"
                mes = show_warning_message(f'Target Depth must be integer! (default: 100 ~ 150 cm)')
            self.follower_process = subprocess.Popen(['bash', '-c', f"source ~/.bashrc && source ~/moiro_ws/install/setup.bash && {command}"], shell=False)
            self.textBrowser_log.append(f" >>> {mes}") 

        except Exception as e:
            e = traceback.format_exc()
            with open("/home/ubuntu/error.log", "a") as f:
                f.write(e)
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")
        
        
    def stop_HF(self):
        kill_pid = ['/home/minha/moiro_ws/install/adaface_ros/lib/adaface_ros/human_follower'
                    ]
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
                    subprocess.Popen(['bash', '-c', f"source ~/moiro_ws/install/setup.bash && {command}"], shell=False)
            else:
                mes = show_error_message("push 'Start HF' button, then push 'reset' button")
            
            self.textBrowser_log.append('[' + str(current_time) + ']' + ' ' + mes)
        except Exception as e:
            e = traceback.format_exc()
            with open("/home/ubuntu/error.log", "a") as f:
                f.write(e)
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")


    def execute_in_terminal(self, command=""):
        full_command = f"source ~/.bashrc && source ~/moiro_ws/install/setup.bash && {command}"
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
    return f"<font style='color: yellow'><b>[Warning]</b> {message}</font>"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Myagv_Window()
    main_window.show()
    sys.exit(app.exec_())
