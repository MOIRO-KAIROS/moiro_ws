# MOIRO Workspace

## 0. Intro
- ROS2 Humble Project for MOIRO
- `moiro_ws`는 실시간으로 타겟 인물을 촬영하는 로봇의 제어를 위한 workspace입니다.

## 1. Spec
<table>
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



## 2. Setup
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

## 3. RUN
### 1) Terminal로 실행하는 방법
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
#### (2) Terminal 입력
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
#### (3) Button 제어
- 버튼의 순서를 지켜서 시행해야함
- Reset의 경우, start만 했으면 적용됨
- [```Sequence```] Driodcam Connect -> Raspberry Pi connect -> start Adaface -> Sync play -> start Mycobot -> start Follower  

### 3) GUI로 실행하는 방법 - Debug 용
#### (1) droidcam 실행
```
droidcam
```
##### (2) Terminal 입력
```sh
// pip install pyqt5==5.13
ros2 run moiro_gui moiro_gui_simple
```
