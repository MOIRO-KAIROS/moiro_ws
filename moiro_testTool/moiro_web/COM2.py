from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/start_follower', methods=['POST'])
def start_follower():
    # 여기에서 follower 명령어를 실행
    print("Success")
    # command = "ros2 launch follower_ros follower.launch.py"
    # subprocess.Popen(['bash', '-c', command])
    
    return 'Follower started on COM2'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)