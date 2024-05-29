# moiro_ws

## Intro
`moiro_ws`는 [여기에 프로젝트 설명 추가].

| Required Info                         | PC / Raspberry Pi |
|---------------------------------|------------------------------------------- |
| Operating System & Version |  Ubuntu 22.04  | 
| Driver                            |  535.171.04 | 
| Cuda                            |  11.8 | 
| ROS Version    |  ROS2 humble |
| Python Version    |  Python 3.10.12 |
| Camera Model |  D435 | 

----------------------------------------------------------------------------------------------------

## Setup

### 1. 깃 레포지토리 클론 및 서브모듈 업데이트

```sh
git clone https://github.com/your_username/moiro_ws.git
cd moiro_ws
git submodule update --init --recursive
```

### 2. 구글 드라이브에서 파일 다운로드
#### (1)  ```pretrained``` 폴더 생성 후, weight(.ckpt) 다운로드
- 다운로드 (링크 클릭)
| Arch | Dataset    | Link                                                                                         |
|------|------------|----------------------------------------------------------------------------------------------|
| R50  | MS1MV2     | [gdrive](https://drive.google.com/file/d/1eUaSHG4pGlIZK7hBkqjyp2fc2epKoBvI/view?usp=sharing) |
#### (2) ```embed``` 폴더 생성 후, features.pt & ids.pt 생성
- 생성 방법: [moiro_vision](https://github.com/MOIRO-KAIROS/moiro_vision) 레포지토리로 이동
  
#### (3) 파일 구조 (pretrained와 embed 폴더 생성)
  ```
  moiro_vision
  ├── adaface_ros
  │   ├── adaface_ros
  │   │   ├── adaface_ros2.py
  │   │   ├── __init__.py
  │   │   └── script
  │   │       ├── embed
  │   │       ├── pretrained
  │   │       ├── ...
  │   ├── launch
  │   ├── package.xml
  │   ├── resource
  │   ├── setup.cfg
  │   ├── setup.py
  │   └── ...   
  ├── README.md
  └── yolov8_ros
  ```
