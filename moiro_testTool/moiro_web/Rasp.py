from flask import Flask, request
import subprocess
import os
from ament_index_python.packages import get_package_share_directory
from utils import kill_terminal

app = Flask(__name__)

@app.route('/start_rasp', methods=['POST'])
def reset_name():
    command = f"ros2 launch moiro_agv_bringup moiro_agv.launch.py"
    subprocess.Popen(['bash', '-c', command], shell=False)
    
    return f'Rasp start'

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        kill_terminal('5000')