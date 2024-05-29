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

lock = False


class Myagv_Window(moiro_window, QMainWindow):
    def __init__(self):
        super(Myagv_Window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('moiro Test Tool')
        self.ros = False
        self.run_launch = ""
        self.adaface_process = None
        self.adaface_button.setCheckable(True)
        self.adaface_button.clicked.connect(self.toggle_adaface)
        self.person_button.clicked.connect(self.reset_person_name)
    
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
                mes = f"Initialized with <b>{person_name}</b>"
            else:
                mes = show_warning_message(f'Target person Uninitialized')
            self.adaface_process = subprocess.Popen(['bash', '-c', f"source ~/.bashrc && source ~/moiro_ws/install/setup.bash && {command}"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.textBrowser_log.append(f" >>> {mes}")
            
            # GUI 차단되지 않고 프로세스 결과를 가져오기 위해 스레드 사용
            # threading.Thread(target=self.get_process_output, args=(self.adaface_process,), daemon=True).start()
            
        except Exception as e:
            e = traceback.format_exc()
            with open("/home/ubuntu/error.log", "a") as f:
                f.write(e)
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")
        
        
    def stop_adaface(self):
        kill_pid = ['/home/lee52/moiro_ws/install/adaface_ros/lib/adaface_ros/world_node',
                    '/home/lee52/moiro_ws/install/adaface_ros/lib/adaface_ros/face_recognition',
                    '/home/lee52/moiro_ws/install/yolov8_ros/lib/yolov8_ros/debug_node',
                    '/home/lee52/moiro_ws/install/yolov8_ros/lib/yolov8_ros/tracking_node',
                    '/home/lee52/moiro_ws/install/yolov8_ros/lib/yolov8_ros/yolov8_node',
                    '/home/lee52/moiro_ws/install/realsense2_camera/lib/realsense2_camera/realsense2_camera_node'
                    ]
        current_time = self.get_current_time()
        if self.adaface_process:
            for pid in kill_pid:
                subprocess.Popen(['bash', '-c', f"ps -ef | grep '{pid}' | grep -v grep | awk '{{print $2}}' | xargs kill"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.adaface_process = None  # Reset the subprocess
            mes = 'Stop Face recognition(Adaface)'
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")

    def execute_in_terminal(self, command=""):
        full_command = f"source ~/.bashrc && source ~/moiro_ws/install/setup.bash && {command}"
        process = subprocess.Popen(['bash', '-c', full_command], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # process.wait()

    def get_current_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return current_time
    
    def reset_person_name(self):
        current_time = self.get_current_time()
        try:
            person_name = self.person_comboBox.currentText()
            
            if self.adaface_process:
                mes = 'Reset target person: '
                if person_name:
                    mes += person_name
                    command = f"ros2 service call /vision/person_name moiro_interfaces/srv/Person \"{{person_name: {person_name}}}\""
                    subprocess.Popen(['bash', '-c', f"source ~/moiro_ws/install/setup.bash && {command}"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                mes = show_error_message("push 'Start FR' button, then push 'reset' button")
            
            self.textBrowser_log.append('[' + str(current_time) + ']' + ' ' + mes)
        except Exception as e:
            e = traceback.format_exc()
            with open("/home/ubuntu/error.log", "a") as f:
                f.write(e)
            self.textBrowser_log.append(f"[{str(current_time)}] {mes}")

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
