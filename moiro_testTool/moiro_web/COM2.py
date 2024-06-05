from flask import Flask, request
import subprocess
import os
from ament_index_python.packages import get_package_share_directory
from utils import kill_terminal

app = Flask(__name__)

# adaface_ros 패키지의 경로 설정
human_follower_path = os.path.abspath(os.path.join(get_package_share_directory('human_follower'), "../../../"))
mycobot_path = os.path.abspath(os.path.join(get_package_share_directory('mycobot_movegroup'), "../../../"))

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
    
    command = f"ros2 service call /vision/target_depth moiro_interfaces/srv/TargetDepth \"{{min_depth: {min_depth}}}\"{{max_depth: {max_depth}}}\""
    subprocess.Popen(['bash', '-c', command], shell=False)
    
    return f'Depth reset as {min_depth} ~ {max_depth} cm'

@app.route('/mycobot', methods=['POST'])
def mycobot():
    # kill_terminal('mycobot_movegroup')
    # command = f"ros2 launch mycobot_movegroup mycobot_movegroup._service_class_interface.launch.py"
    # subprocess.Popen(['bash', '-c', f"source ~/.bashrc && source {mycobot_path}/setup.bash && {command}"], shell=False)
    print('I DONT KNOW HOW TO RUN MYCOBOT')
    return f'Mycobot started on COM2'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)