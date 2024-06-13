from flask import Flask, request
import subprocess
import os
from ament_index_python.packages import get_package_share_directory
from utils import kill_terminal
import rclpy
from geometry_msgs.msg import Twist

app = Flask(__name__)

# adaface_ros 패키지의 경로 설정
human_follower_path = os.path.abspath(os.path.join(get_package_share_directory('human_follower'), "../../../"))

@app.route('/start_follower', methods=['POST'])
def start_follower():
    kill_terminal(os.path.join(human_follower_path, 'human_follower/lib/human_follower'))
    min_depth = request.json[0]
    max_depth = request.json[1]
    print(min_depth, max_depth)
    command = f"ros2 run human_follower human_follower min_depth:={min_depth} max_depth:={max_depth}"
    subprocess.Popen(['bash', '-c', command], shell=False)
    return 'Follower started on COM2'

@app.route('/reset_depth', methods=['POST'])
def reset_depth():
    min_depth = request.json[0]
    max_depth = request.json[1]
    
    command = f"ros2 service call /vision/target_depth moiro_interfaces/srv/TargetDepth \"{{min_depth: {min_depth}, max_depth: {max_depth}}}\""
    subprocess.Popen(['bash', '-c', command], shell=False)
    
    return f'Depth reset as {min_depth} ~ {max_depth} cm'

@app.route('/killHF', methods=['POST'])
def killHF():
    command = 'ros2 topic pub --once  /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"'
    process = subprocess.Popen(['bash', '-c', command], shell=False)
    process.wait()
    kill_terminal(os.path.join(human_follower_path, 'human_follower/lib/human_follower'))
    return 'Human Follower killed'


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        command = 'ros2 topic pub --once  /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"'
        process = subprocess.Popen(['bash', '-c', command], shell=False)
        process.wait()
        kill_terminal(os.path.join(human_follower_path, 'human_follower/lib/human_follower'))
        kill_terminal('5001')