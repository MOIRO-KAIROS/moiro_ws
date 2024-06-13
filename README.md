
<div align="center">
    <img src="https://github.com/MOIRO-KAIROS/moiro_ws/assets/114575723/f3451dd1-ff70-4d58-b156-9cacf88bf0ee" alt="moiro_logo" width="200" height="200">
</div>

<div align="center"><h1></h1><h1>📸&nbsp&nbsp INTRO</h1></div>

- ROS2 Humble Project for MOIRO
- ```moiro_ws```는 실시간으로 타겟 인물을 촬영하는 로봇의 제어를 위한 ROS2 Workspace입니다.
- 
  
<div align=center><h1></h1><h1>📸 STACKS</h1></div>

<div align=center> 
  <img src="https://img.shields.io/badge/c++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white">
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/ROS2-22314E?style=for-the-badge&logo=ros&logoColor=white">
  <img src="https://img.shields.io/badge/Unity-000000?style=for-the-badge&logo=unity&logoColor=white">
  <br>
  
  <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> 
  <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> 
  <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> 
  <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">
  <br>

  <img src="https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
  <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white">
  <img src="https://img.shields.io/badge/Arduino-00878F?style=for-the-badge&logo=arduino&logoColor=white">
  <img src="https://img.shields.io/badge/Fusion360-FF7800?style=for-the-badge&logo=autodesk&logoColor=white">
  <img src="https://img.shields.io/badge/STMicroelectronics-03234B?style=for-the-badge&logo=stmicroelectronics&logoColor=white">
  <br>
  
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
  <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
  <br>
</div>


<div align="center"><h1></h1><h1>📸&nbsp&nbsp SPEC</h1></div><table>
  <tr>
    <td>
      <img src="https://github.com/MOIRO-KAIROS/moiro_ws/assets/114575723/1e08a068-bfb8-4faa-b30f-63056fdee522" alt="moiro_hardware" width="450" height="600">
    </td>
    <td>
      <table>
        <tr>
          <th>Required Info</th>
          <th>Details</th>
        </tr>
        <tr>
          <th colspan="2">Hardware</th>
        </tr>
        <tr>
          <td>Camera Model</td>
          <td>Intel Realsense D435</td>
        </tr>
        <tr>
          <td>Agv Motor</td>
          <td>Robotics XL430-W250-T</td>
        </tr>
        <tr>
          <td>Motor control Board</td>
          <td>OpenCR</td>
        </tr>
        <tr>
          <td>Robot Arm</td>
          <td>Mycobot320 m5</td>
        </tr>
        <tr>
          <th colspan="2">Software</th>
        </tr>
        <tr>
          <td>Operating System & Version</td>
          <td>Ubuntu 22.04</td>
        </tr>
        <tr>
          <td>Driver</td>
          <td>535.171.04</td>
        </tr>
        <tr>
          <td>Cuda</td>
          <td>11.8</td>
        </tr>
        <tr>
          <td>ROS Version</td>
          <td>ROS2 humble</td>
        </tr>
        <tr>
          <td>Python Version</td>
          <td>Python 3.10.12</td>
        </tr>
      </table>
    </td>
  </tr>
</table>

<div align="center">
  <h1></h1><h1>📸&nbsp&nbsp  SETUP</h1>
</div>

### 1) Install & Submodule update

```sh
git clone https://github.com/your_username/moiro_ws.git
cd moiro_ws
git submodule update --init --recursive
```
### 2) Submodule setup

#### [ ```중요 : Submodule의 README를 참고하여 Setup 진행``` ]
- MOIRO vision setup : https://github.com/MOIRO-KAIROS/moiro_vision
- MOIRO agv setup : https://github.com/MOIRO-KAIROS/moiro_agv
- MOIRO arm setup :  https://github.com/MOIRO-KAIROS/moiro_arm
  

### 3) colcon build
```sh
cd moiro_ws
source /opt/ros/humble/setup.bash
colcon build
```

### 4) Terminal Setting
```sh
# Raspi
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "export ROS_DOMAIN_ID=<$WANTED_ROS_DOMAIN>" >> ~/.bashrc
echo "export LDS_MODEL=LDS-02" >> ~/.bashrc
echo "source $HOME/moiro_ws/install/setup.bash" >> ~/.bashrc
```

```sh
# COM
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "export ROS_DOMAIN_ID=<$WANTED_ROS_DOMAIN>" >> ~/.bashrc
echo "source $HOME/moiro_ws/install/setup.bash" >> ~/.bashrc
```

<div align="center">
  <h1></h1><h1>📸&nbsp&nbsp RUN</h1>
</div>

### 1) Using Terminal
- 명령어 순서 매우 주의해서 입력

```sh
# Rasp
ros2 launch moiro_agv_bringup moiro_agv.launch.py
```
```sh
# 부착 COM
ros2 launch adaface_ros adaface.launch.py person_name:=<$PERSON_NAME>
sudo chmod 777 /dev/ttyACM0
ros2 run moiro_arm_robot_driver sync_play
ros2 launch moiro_arm_move_group moiro_arm_move_group.launch.py
ros2 launch moiro_arm_move_group moiro_arm_move_group_service_class_interface.launch.py
```
```sh
# Monitoring COM
ros2 run human_follower human_follower min_depth:=<$min_depth> max_depth:=<$max_depth>"
```
### 2) Flask Web 
#### (1) droidcam install
- 참고하여서 설치 : https://www.youtube.com/watch?v=anUmPoF6eJY
```
droidcam
```
#### (2) Terminal
```
# port 가 이미 지정되어 있다면,
lsof -n -i -P | grep {PORT_NUM} | grep -v grep | awk '{print $2}' | xargs kill -9
# flask가 없다면,
pip install flask==3.0.3
```
<p align="center">
  <img src="https://github.com/MOIRO-KAIROS/moiro_ws/assets/114575723/f8eed014-ac45-4018-9183-0c9311b1579a" alt="moiro_web" width="800" height="400">
</p>

```sh
## Flask용 (COM2) -- PORT : 8080
python3 moiro_testTool/moiro_web/app.py
```
```sh
# MOIRO AGV용 (Raspberry pi) -- PORT : 5000
# lsof -n -i -P | grep 8080 | grep -v grep | awk '{print $2}' | xargs kill -9
python3 moiro_testTool/moiro_web/Rasp.py
```
```sh
# Human Follower용 (COM2) -- PORT : 5001
# lsof -n -i -P | grep 5001 | grep -v grep | awk '{print $2}' | xargs kill -9
python3 moiro_testTool/moiro_web/COM2.py
```
```sh
# 부착 COM용 (COM1) -- PORT : 5000
# lsof -n -i -P | grep 5001 | grep -v grep | awk '{print $2}' | xargs kill -9
python3 moiro_testTool/moiro_web/COM1.py
```
#### (3) Button Control
- 버튼의 순서를 지켜서 시행해야함
- Reset의 경우, start만 했으면 적용됨
- Record button을 통해 현재 촬영화면을 저장 가능

- [```Sequence```] Driodcam Connect ➡️ Raspberry Pi connect ➡️ start Adaface ➡️ Sync play ➡️ start Mycobot ➡️ start Follower

### 3) Debug
#### (1) Node graph
<p align="center"><img src="https://github.com/MOIRO-KAIROS/moiro_ws/assets/114575723/2820b9b8-a629-47b0-a595-ca7b3a8badc4" alt="rqt_graph" width="500" height="500"></p>

#### (2) Rviz2
<p><img src="https://github.com/MOIRO-KAIROS/moiro_ws/assets/114575723/852765a3-bed0-4ad8-98a3-c00fb150145a" alt="rviz2" width="900" height="400"></p>

<div align="center">
  <h1></h1><h1> 📸&nbsp&nbsp  RESULT</h1>
</div>

### (1) Running MOIRO with moiro web
- [```LINK```]    https://www.youtube.com/watch?v=wvV16o518Vw
- [```SIDE VIDEO```]    Actual shot video by phone

<div align="center">
  <a href="https://www.youtube.com/watch?v=wvV16o518Vw">
    <img src="https://img.youtube.com/vi/wvV16o518Vw/0.jpg" alt="Video Label" width="800">
  </a>
</div>

<div align="center">
  <h1></h1><h1> 📸&nbsp&nbsp  CONTRIBUTE</h1>
</div>

<div align="center">
  <table>
    <tr>
      <td style="text-align: center;">
        <a href="https://github.com/Mincheol710313">
          <img src="https://avatars.githubusercontent.com/u/99674522?v=4" width="60px" alt="Mincheol Github">
        </a>
      </td>
      <td style="text-align: center;">
        <strong>신민철 (Mincheol Shin)</strong>
      </td>
      <td style="text-align: center;">
        <p>Team Leader & robot ARM control</p>
      </td>
    </tr>
    <tr>
      <td style="text-align: center;">
        <a href="https://github.com/sjxna20">
          <img src="https://avatars.githubusercontent.com/u/154571496?v=4" width="60px" alt="Hohyun Github">
        </a>
      </td>
      <td style="text-align: center;">
        <strong>김호현 (Hohyun Kim)</strong>
      </td>
      <td style="text-align: center;">
        <p>Hardware Design and Production</p>
      </td>
    </tr>
    <tr>
      <td style="text-align: center;">
        <a href="https://github.com/sjxna20">
          <img src="https://avatars.githubusercontent.com/u/155697546?v=4" width="60px" alt="Woosung Github">
        </a>
      </td>
      <td style="text-align: center;">
        <strong>노우성 (Woosung Roh)</strong>
      </td>
      <td style="text-align: center;">
        <p>Urdf and Moveit</p>
      </td>
    </tr>
    <tr>
      <td style="text-align: center;">
        <a href="https://github.com/No-Hyunwoo">
          <img src="https://avatars.githubusercontent.com/u/153826791?v=4" width="60px" alt="Hyunwoo Github">
        </a>
      </td>
      <td style="text-align: center;">
        <strong>노현우 (Hyunwoo No)</strong>
      </td>
      <td style="text-align: center;">
        <p>Odometry and Slam</p>
      </td>
    </tr>
    <tr>
      <td style="text-align: center;">
        <a href="https://github.com/Minha-Song">
          <img src="https://avatars.githubusercontent.com/u/114575723?v=4" width="60px" alt="Minha Github">
        </a>
      </td>
      <td style="text-align: center;">
        <strong>송민하 (Minha Song)</strong>
      </td>
      <td style="text-align: center;">
        <p> Vision AI, Flask web, AGV control algorithm </p>
      </td>
    </tr>
    <tr>
      <td style="text-align: center;">
        <a href="https://github.com/yeonju52">
          <img src="https://avatars.githubusercontent.com/u/77441026?v=4" width="60px" alt="Yeonju Github">
        </a>
      </td>
      <td style="text-align: center;">
        <strong>이연주 (Yeonju Lee)</strong>
      </td>
      <td style="text-align: center;">
        <p>Vision AI, Flask web, Unity</p>
      </td>
    </tr>
  </table>
</div>
