from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/start_adaface', methods=['POST'])
def start_adaface():
    # 여기에서 adaface 명령어를 실행
    print("Success")
    # command = "ros2 launch adaface_ros adaface.launch.py"
    # subprocess.Popen(['bash', '-c', command])
    
    return 'Adaface started on COM1'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)