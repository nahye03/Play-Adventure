# Play-Adventure

## Table of Contents
1. 주요기술
2. Demo
3. 설치 방법
4. 라이브러리
5. Code

## 1. 주요 기술
### 영상 재생과 실시간 웹캠 동시 실행 및 버튼
- `QMediaPlayer` :소리가 포함된 영상 재생
- `QThread` : 영상 재생와 웹캡을 동시에 실행
- 상속을 통해 웹캠 화면 위에 버튼 생성 및 실행
### **Body Segmentation**
- Body Segmentation을 통해 배경 합성
- Mediapipe의 `Selfie segmentation Model` 사용
### **얼굴 및 눈 검출**
- OpenCV의 `haarcascade_frontalface_default` 와 `frontalEyes35x16`사용
- 얼굴 및 눈 검출 후 얼굴과 눈의 위치와 크기에 맞게 모자, 의상, 안경 합성

## 2. Demo
[![Video Label](http://img.youtube.com/vi/gZjyD-FFKBA/0.jpg)](https://youtu.be/gZjyD-FFKBA)

## 3. 설치 방법
```
pip install -r requirements.txt
```

## 4. 라이브러리
### PyQt 실행 관련 라이브러리
> - numpy==1.20.1
> - opencv-python==4.4.0.46
> - mediapipe==0.8.6.2
> - PyQt5==5.15.4
> - PyAutoGUI==0.9.53
> - pygame==2.0.3

### 화면 녹화+녹음 관련 라이브러리
참고 깃허브 : [Screen + Audio recording](https://github.com/Pranav433/screen_recorder)

> - cffi==1.14.5
> - ffmpeg-python==0.2.0
> - future==0.18.2
> - MouseInfo==0.1.3
> - Pillow==8.0.1
> - pycparser==2.20
> - PyGetWindow==0.0.9
> - PyMsgBox==1.0.9
> - pyperclip==1.8.2
> - PyRect==0.1.4
> - PyScreeze==0.1.28
> - pytweening==1.0.4
> - sounddevice==0.4.2
> - SoundFile==0.10.3.post1

## 5. Code
- [code](https://github.com/nahye03/Play-Adventure/tree/main/code) : 구현 code
  - [screen_record](https://github.com/nahye03/Play-Adventure/tree/main/code/screen_record) : 화면 녹화 부
  - [stickerNbackground](https://github.com/nahye03/Play-Adventure/tree/main/code/stickerNbackground) : 의상, 악세사리 꾸미기 함수
  - [final_idx.txt](https://github.com/nahye03/Play-Adventure/blob/main/code/final_idx.txt) : 꾸미기 결과값 저장
  - [mission_clock.py](https://github.com/nahye03/Play-Adventure/blob/main/code/mission_clock.py) : 시계 이동 미션
    - [mission_stamp.py](https://github.com/nahye03/Play-Adventure/blob/main/code/mission_stamp.py) : 도장찍기 미션
    - [ui_functions.py](https://github.com/nahye03/Play-Adventure/blob/main/code/ui_functions.py) : TopMenu Bar
    - [values.py](https://github.com/nahye03/Play-Adventure/blob/main/code/values.py) : 사용되는 변수의 값, 경로
    - [ui_main.py] (https://github.com/nahye03/Play-Adventure/blob/main/code/ui_main.py) : 시작 UI
  
- [imgs](https://github.com/nahye03/Play-Adventure/tree/main/imgs) : 사용되는 이미지
- [videos](https://github.com/nahye03/Play-Adventure/tree/main/videos) : 사용되는 동영상

