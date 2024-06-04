from flask import Flask, request
import subprocess
import os
from ament_index_python.packages import get_package_share_directory
from utils import kill_terminal

app = Flask(__name__)

# adaface_ros 패키지의 경로 설정
adaface_ros_path = os.path.abspath(os.path.join(get_package_share_directory('adaface_ros'), "../../../"))
@app.route('/start_adaface', methods=['POST'])
def start_adaface():
    kill_terminal(os.path.join(adaface_ros_path, 'adaface_ros/lib/adaface_ros'))
    kill_terminal(os.path.join(adaface_ros_path, 'yolov8_ros/lib/yolov8_ros'))
    kill_terminal(os.path.join(adaface_ros_path, 'realsense2_camera/lib/realsense2_camera'))
    person_name = request.data.decode('utf-8')
    if not person_name:
        return 'Person name is required', 400
    
    command = f"ros2 launch adaface_ros adaface.launch.py person_name:={person_name}"
    subprocess.Popen(['bash', '-c', f"source ~/.bashrc && source {adaface_ros_path}/setup.bash && {command}"], shell=False)
    return 'Adaface started on COM1'

@app.route('/reset_name', methods=['POST'])
def reset_name():
    person_name = request.data.decode('utf-8')
    if not person_name:
        return 'Person name is required', 400
    
    command = f"ros2 service call /vision/person_name moiro_interfaces/srv/Person \"{{person_name: {person_name}}}\""
    subprocess.Popen(['bash', '-c', f"source ~/.bashrc && source {adaface_ros_path}/setup.bash && {command}"], shell=False)
    
    return f'Person name reset as <b>{person_name}</b>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)