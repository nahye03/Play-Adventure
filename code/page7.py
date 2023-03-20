import os
import sys
import time

import PyQt5.QtCore
import pyautogui
import pygame
from PyQt5.QtWidgets import *
import PyQt5
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import cv2
from threading import Thread
from screen_record.recorder import Recorder
from datetime import datetime

import values
import ui_functions
from background_video import *
import mission_stamp
import mission_clock
import save_page
import page8, page3, page4

#학생 대사 자막
class overlay_text(QWidget):
    def __init__(self, parent=None):
        super(overlay_text, self).__init__(parent)

        self.text = QLabel(self)
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setFont(QFont(values.font, 15))
        self.text.setWordWrap(True)
        self.text.setMargin(5)
        self.text.setGeometry(0,values.video_height-values.height*0.15, values.width/2, values.height*0.15)
        self.text.setStyleSheet('color:white; background-color : rgba(0,0,0,0)')

#다음 버튼
class overlay_next(QWidget):
    def __init__(self, parent = None):
        super(overlay_next, self).__init__(parent)

        #꾸미기 완료 버튼
        self.next_button = QPushButton(self)
        self.next_button.setStyleSheet('background-color : rgba(0,0,0,0)')
        self.next_button.setIcon(QIcon(values.page7_image))
        self.next_button.setIconSize(QSize(values.width/10, values.height/15))
        self.next_button.setGeometry(values.width *0.41, values.height*0.02, values.width/10, values.height/15)

#영상 녹화
def record(rec,x,y,w,h):
    print("Recording...")
   # rec = Recorder(x, y, w, h)
    rec.record_screen()  # This will start the recording

class Page7(ui_functions.Topmenu):
    def __init__(self):
        super(Page7, self).__init__()
        self.setWindowTitle('연극')
        self.scene_num = 1
        self.text_num = 0
        self.video_num = 0
        self.stamp_num = 0
        self.cnt = 0
        self.clock_num = 0
        self.finish = 0

        self.video_play(values.video_path + values.scene1_video[self.video_num])
        # self.video_play(values.video_path + values.scene6_video[self.video_num])

        self.video_thread = VideoThread()
        self.video_thread.image_change_signal.connect(self.set_image)
        self.video_thread.start()
        # self.video_thread.back_idx = 2

        self.video_thread2 = VideoThread2()
        self.video_thread2.image_change_signal.connect(self.set_images)

        # 텍스트 파일 존재여부 확인(의상, 악세서리 가져오기)
        isFile = os.path.isfile('final_idx.txt')
        if isFile:
            f = open('final_idx.txt', 'r')
            idx_list = []  # 인덱스 리스트 - 순서대로 cloth, hat, glasses
            # 텍스트 파일 한줄씩 읽어오기
            while True:
                line = f.readline()
                if not line:
                    break
                acc, idx = line.split()

                if idx == 'None':
                    idx_list.append(-1)
                    continue
                idx_list.append(int(idx))
            f.close()

            # 인덱스 변수 update
            self.video_thread.cloth_idx = idx_list[0] if (idx_list[0] >= 0) else None
            self.video_thread.hat_idx = idx_list[1] if (idx_list[1] >= 0) else None
            self.video_thread.glasses_idx = idx_list[2] if (idx_list[2] >= 0) else None

            if self.video_thread.cloth_idx != None:
                self.video_thread.cloth_on = True
            if self.video_thread.hat_idx != None:
                self.video_thread.hat_on = True
            if self.video_thread.glasses_idx != None:
                self.video_thread.glasses_on = True

        # 영상 녹화를 위한 record 객체 생성
        self.x, self.y, self.w, self.h = self.screen_area()
        self.rec = Recorder(self.x, self.y, self.w, self.h)
        self.record_thread = Thread(target=record(self.rec, self.x, self.y, self.w, self.h))
        self.record_thread.start()

        #overlay
        self.overlay_text = overlay_text(self.video_frame) #대사 자막
        self.overlay_next = overlay_next(self.video_frame) #다음 버튼
        self.overlay_next.next_button.setEnabled(False)

        #이벤트
        self.overlay_next.next_button.clicked.connect(self.next_button_clicked) #다음버튼 클릭 이벤트
        self.mediaPlayer.stateChanged.connect(self.mediaStateChange) #선생님 영상 상태 이벤트
        self.mediaPlayer_act1.stateChanged.connect(self.mediaStateChange) #act1 상태 이벤트
        self.mediaPlayer_act2.stateChanged.connect(self.mediaStateChange) #act2 상태 이벤트
        self.mediaPlayer_act3.stateChanged.connect(self.mediaStateChange) # act3 상태 이벤트
        self.mediaPlayer_act4.stateChanged.connect(self.mediaStateChange)  # act4 상태 이벤트
        self.letter_button.clicked.connect(self.letter_button_clicked) #편지 다 읽음 이벤트
        self.skip_button.clicked.connect(self.skip_button_clicked) #설명 스킵 버튼
        self.save_choice.yes_button.clicked.connect(self.save_yes_clicked) #저장 yes 이벤트
        self.save_choice.no_button.clicked.connect(self.save_no_clicked) #저장 no 이벤트
        self.menuWidget.cellClicked.connect(self.menu_clicked)  # 탑메뉴 클릭 이벤트

    def setUI(self):
        super(Page7, self).setUI()

        self.setAcceptDrops(True)

        #전체 레이아웃 선언
        videos_layout = QHBoxLayout()

        #선생님 영상
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()

        self.mediaPlayer2 = QLabel() #캡쳐미션할때 선생님

        #학생 영상
        self.video_frame = QLabel()

        #videos_layout 레이아웃에 추가
        videos_layout.addWidget(self.videoWidget)
        videos_layout.addWidget(self.mediaPlayer2)
        self.mediaPlayer2.hide()
        videos_layout.addWidget(self.video_frame)

        self.layout.addLayout(videos_layout)

        #씬 3 미션영상
        self.mediaPlayer_act1 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget_act1 = QVideoWidget()
        self.videoWidget_act1.setGeometry(0, values.menu_height, values.width, values.video_height)
        self.mediaPlayer_act1.setVideoOutput(self.videoWidget_act1)
        self.mediaPlayer_act1.setMedia(
            QMediaContent(QUrl.fromLocalFile(values.video_path + values.scene3_video[0]))
        )
        self.layout.addWidget(self.videoWidget_act1)
        self.videoWidget_act1.hide()

        #씬5 영상
        self.mediaPlayer_act2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget_act2 = QVideoWidget()
        self.videoWidget_act2.setGeometry(0, values.menu_height, values.width, values.video_height)
        self.mediaPlayer_act2.setVideoOutput(self.videoWidget_act2)
        self.mediaPlayer_act2.setMedia(
            QMediaContent(QUrl.fromLocalFile(values.video_path + values.scene5_video[0]))
        )
        self.layout.addWidget(self.videoWidget_act2)
        self.videoWidget_act2.hide()

        # 씬6 영상
        self.mediaPlayer_act3 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget_act3 = QVideoWidget()

        self.container = QWidget()
        self.container.setStyleSheet('background-color : rgba(100,0,0,0)')
        act3_layout = QVBoxLayout(self.container)
        act3_layout.setContentsMargins(0, 0, 0, 0)
        act3_layout.addWidget(self.videoWidget_act3)

        self.letter_button = QPushButton(self.container)
        self.letter_button.setIcon(QIcon(values.page7_image))
        self.letter_button.setIconSize(QSize(90, 90))
        self.letter_button.setGeometry(values.width - 90,values.video_height-60, 80, 50)

        self.videoWidget_act3.setGeometry(0, values.menu_height, values.width, values.video_height)
        self.mediaPlayer_act3.setVideoOutput(self.videoWidget_act3)
        self.mediaPlayer_act3.setMedia(
            QMediaContent(QUrl.fromLocalFile(values.video_path + values.scene6_video[8]))
        )

        self.layout.addWidget(self.container)
        self.container.hide()

        #마지막 설명 영상
        self.mediaPlayer_act4 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget_act4 = QVideoWidget()

        self.container4 = QWidget()
        self.container4.setStyleSheet('background-color : rgba(100,0,0,0)')
        act3_layout = QVBoxLayout(self.container4)
        act3_layout.setContentsMargins(0, 0, 0, 0)
        act3_layout.addWidget(self.videoWidget_act4)

        self.skip_button = QPushButton(self.container4)
        self.skip_button.setIcon(QIcon(values.skip_image))
        self.skip_button.setIconSize(QSize(100, 100))
        self.skip_button.setGeometry(values.width - 120, values.video_height - 100, 100, 80)

        self.videoWidget_act4.setGeometry(0, values.menu_height, values.width, values.video_height)
        self.mediaPlayer_act4.setVideoOutput(self.videoWidget_act4)
        self.mediaPlayer_act4.setMedia(
            QMediaContent(QUrl.fromLocalFile(values.page7_last_video))
        )
        self.layout.addWidget(self.container4)
        self.container4.hide()

        #저장 선택 화면
        self.save_choice = save_page.Save_choice()
        self.layout.addWidget(self.save_choice)
        self.save_choice.hide()

        #씬3_도장미션
        self.mission_stamp = mission_stamp.Mission_stamp()
        self.layout.addWidget(self.mission_stamp)
        self.mission_stamp.hide()

        #씬3_캡쳐미션
        # 촬영버튼
        self.capture = QPushButton(self)
        self.capture.setIcon(QIcon(values.camera))
        self.capture.setIconSize(QSize(int(values.width * 0.25), int(values.height * 0.25)))
        self.capture.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.capture.setGeometry(int(values.width * 0.82), int(values.height * 0.82),
                                 int(values.width * 0.25), int(values.height * 0.25))
        self.capture.clicked.connect(self.capturePressEvent)
        # 미션지
        self.mission_photo = QPushButton(self)
        self.mission_photo.setIcon(QIcon(values.mission_photo))
        self.mission_photo.setIconSize(QSize(int(values.width * 0.3), int(values.height * 0.3)))
        self.mission_photo.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: outset;")
        self.mission_photo.setGeometry(int(values.width * 0.77), int(values.height * 0.60),
                                       int(values.width * 0.3), int(values.height * 0.3))
        # 선언문
        self.mission_speech = QPushButton(self)
        self.mission_speech.setIcon(QIcon(values.mission_speech))
        self.mission_speech.setIconSize(QSize(int(values.width * 0.5), int(values.height * 0.5)))
        self.mission_speech.setStyleSheet("background:transparent")
        self.mission_speech.setGeometry(int(values.width * 0.25), int(values.height * 0.5),
                                        int(values.width * 0.5), int(values.height * 0.5))
        self.capture.hide()
        self.mission_photo.hide()
        self.mission_speech.hide()

        #씬6_시계미션
        self.mission_clock = mission_clock.Mission_clock()
        self.layout.addWidget(self.mission_clock)
        self.mission_clock.hide()

        self.next = QPushButton(self)
        self.next.setStyleSheet('background-color : rgba(0,0,0,0)')
        self.next.setIcon(QIcon(values.page7_image))
        self.next.setIconSize(QSize(values.width / 10, values.height / 15))
        self.next.setGeometry(values.width * 0.91, values.height * 0.082, values.width / 10,
                              values.height / 15)
        self.next.hide()

    # UI 위치 가져오기
    def screen_area(self):
        qr = self.frameGeometry()
        x = qr.x()
        y = qr.y()+95
        w = qr.width()
        h = qr.height()-95
        return x,y,w,h

    #메뉴 버튼 클릭 이벤트
    def menu_clicked(self, row, col):
        data = self.menuWidget.item(row, col)
        if data.text() == 'HOME':
            self.finish = 1
            self.video_thread.stop()
            self.video_thread2.stop()
            self.mediaPlayer.stop()
            self.mediaPlayer_act1.stop()
            self.mediaPlayer_act2.stop()
            self.mediaPlayer_act3.stop()
            self.mediaPlayer_act4.stop()
            self.rec.stop()
            self.secondWindow = page3.Page3()
            self.secondWindow.show()
            self.close()
        elif data.text() == 'My':
            self.finish = 1
            self.video_thread.stop()
            self.video_thread2.stop()
            self.mediaPlayer.stop()
            self.mediaPlayer_act1.stop()
            self.mediaPlayer_act2.stop()
            self.mediaPlayer_act3.stop()
            self.mediaPlayer_act4.stop()
            self.rec.stop()
            self.secondWindow = page4.Page4()
            self.secondWindow.show()
            self.close()

    #편지 다 읽음 이벤트
    def letter_button_clicked(self):
        self.mediaPlayer_act3.stop()

    #설명 영상 스킵 이벤트
    def skip_button_clicked(self):
        self.mediaPlayer_act4.stop()

    # 저장 yes 이벤트
    def save_yes_clicked(self):
        print('저장 yes')
        time_str = datetime.now().strftime('%m-%d %H-%M.%f')[:-3]
        self.rec.stop()
        self.rec.save(values.save_video_path + 'play_' + time_str + ".mp4")
        self.video_thread.stop()
        self.video_thread2.stop()
        self.mediaPlayer.stop()
        self.mediaPlayer_act1.stop()
        self.mediaPlayer_act2.stop()
        self.mediaPlayer_act3.stop()
        self.mediaPlayer_act4.stop()
        self.secondWindow = page8.Page8()
        self.secondWindow.show()
        self.close()

    # 저장 no 이벤트
    def save_no_clicked(self):
        print('저장 no')
        self.rec.stop()
        self.video_thread.stop()
        self.video_thread2.stop()
        self.mediaPlayer.stop()
        self.mediaPlayer_act1.stop()
        self.mediaPlayer_act2.stop()
        self.mediaPlayer_act3.stop()
        self.mediaPlayer_act4.stop()
        self.secondWindow = page8.Page8()
        self.secondWindow.show()
        self.close()

    #씬3 캡쳐 미션 이벤트
    def capturePressEvent(self):
        self.overlay_next.next_button.setEnabled(True)
        pygame.mixer.music.play()
        qr = self.frameGeometry()
        x = qr.x()
        y = qr.y() + 93
        w = qr.width()
        h = qr.height() - 93
        pyautogui.screenshot(f'{values.save_video_path}/my_screen{self.cnt}.png', region=(x, y, w, h))
        print('screenshot')
        self.cnt += 1

    #씬3 도장 미션 이벤트1
    def mousePressEvent(self, e):
        if self.stamp_num == 1:
            if int(values.width * 0.665) <= e.x() <= int(values.width * 0.691) \
                    and int(values.height * 0.7) <= e.y() <= int(values.height * 0.765):
                pygame.mixer.music.play()
                stamp = QPainter(self.mission_stamp.back_img.pixmap())
                stamp.drawPixmap(int(values.width * 0.65), int(values.height * 0.662), QPixmap(self.mission_stamp.stamp_click))
                stamp.end()
                self.mission_stamp.back_img.setPixmap(self.mission_stamp.back_img.pixmap())
                self.stamp_num =2

    #씬3 도장 미션 이벤트2
    def mouseReleaseEvent(self, event):
        if self.stamp_num == 2:
            self.stamp_num = 3
            self.mission_stamp.player.stop()
            self.mission_stamp.setVisible(False)
            #캡쳐 미션 화면 시작
            self.video_thread.start()
            self.video_thread2.start()
            self.video_frame.setVisible(True)
            self.mediaPlayer2.setVisible(True)
            self.overlay_text.text.setText('')
            self.overlay_next.next_button.setEnabled(False)
            #버튼 보이게
            self.capture.setVisible(True)
            self.mission_photo.setVisible(True)
            self.mission_speech.setVisible(True)
            #배경 음악 + 효과음
            sound = values.capture_sound
            self.player = QMediaPlayer()

            self.player.setMedia(
                QMediaContent(QUrl.fromLocalFile(sound))
            )
            self.player.play()

            pygame.init()
            pygame.mixer.music.load(values.photo_sound)

    #씬6 시계 미션 다음 이벤트
    def next_clock(self):
        self.mission_clock.setVisible(False)
        self.next.setVisible(False)
        self.mission_clock.player_clock.stop()
        self.video_thread.start()
        self.videoWidget.setVisible(True)
        self.video_frame.setVisible(True)
        self.video_num += 1
        self.video_play(values.video_path + values.scene6_video[self.video_num])
        self.overlay_next.next_button.setEnabled(False)
        self.overlay_text.text.setText('')

    # 씬6 시계 미션 이벤트
    def clock_state(self):
        self.next.setEnabled(True)
        self.next.clicked.connect(self.next_clock)
        self.mission_clock.clock1.setCheckable(False)
        self.mission_clock.clock2.setCheckable(False)

    #다음 버튼 클릭 이벤트
    def next_button_clicked(self):
        if self.scene_num ==1:
            if self.text_num == 1:
                self.overlay_text.text.setText(values.scene1_text[self.text_num])
                self.text_num += 1
            elif self.text_num == 2 or self.text_num == 3 or self.text_num == 4:
                self.mediaPlayer.stop()
                self.video_num += 1
                self.video_play(values.video_path + values.scene1_video[self.video_num])
                self.overlay_next.next_button.setEnabled(False)
                self.overlay_text.text.setText('')
        elif self.scene_num == 2:
            if self.text_num == 1:
                self.overlay_text.text.setText(values.scene2_text[self.text_num])
                self.text_num += 1
            elif self.text_num == 2 or self.text_num == 3:
                self.mediaPlayer.stop()
                self.video_num += 1
                self.video_play(values.video_path + values.scene2_video[self.video_num])
                self.overlay_next.next_button.setEnabled(False)
                self.overlay_text.text.setText('')
            elif self.text_num == 4:
                self.scene_num = 3
                self.video_thread.back_idx = 3
                self.video_num = 0
                self.text_num = 0
                self.video_thread.stop()
                self.mediaPlayer.stop()
                self.videoWidget.setVisible(False)
                self.video_frame.setVisible(False)
                self.videoWidget_act1.setVisible(True)
                self.mediaPlayer_act1.play()
                self.video_num += 1
        elif self.scene_num == 3:
            self.mediaPlayer2.setVisible(False)
            self.video_thread2.stop()
            self.player.stop()
            self.capture.setVisible(False)
            self.mission_photo.setVisible(False)
            self.mission_speech.setVisible(False)

            self.scene_num = 4
            self.video_thread.back_idx = 4
            self.video_num = 0
            self.text_num = 0
            self.videoWidget.setVisible(True)
            self.video_play(values.video_path + values.scene4_video[self.video_num])
            self.overlay_next.next_button.setEnabled(False)
            self.overlay_text.text.setText('')
        elif self.scene_num == 4:
            self.mediaPlayer.stop()
            self.video_num += 1
            self.video_play(values.video_path + values.scene4_video[self.video_num])
            self.overlay_next.next_button.setEnabled(False)
            self.overlay_text.text.setText('')
        elif self.scene_num == 5:
            self.mediaPlayer.stop()
            self.scene_num = 6
            self.video_thread.back_idx = 6
            self.video_num = 0
            self.text_num = 0
            self.video_play(values.video_path + values.scene6_video[self.video_num])
            self.overlay_next.next_button.setEnabled(False)
            self.overlay_text.text.setText('')
        elif self.scene_num == 6:
            if self.text_num == 1:
                self.overlay_text.text.setText(values.scene6_text[self.text_num])
                self.text_num += 1
            elif self.text_num == 2:
                self.mediaPlayer.stop()
                #미션하구 거기서 버튼 눌렀을때 아래 실행
                self.clock_num = 1
                self.video_thread.stop()
                self.video_frame.setVisible(False)
                self.videoWidget.setVisible(False)
                self.mission_clock.player_clock.play()
                self.mission_clock.setVisible(True)
                self.next.setVisible(True)
                self.next.setEnabled(False)
                self.setAcceptDrops(True)
                self.mission_clock.clock1.toggled.connect(self.clock_state)

            elif self.text_num == 3:
                self.mediaPlayer.stop()
                self.video_num += 1
                self.video_play(values.video_path + values.scene6_video[self.video_num])
                self.overlay_next.next_button.setEnabled(False)
                self.overlay_text.text.setText('')
            elif self.text_num == 4:
                self.mediaPlayer.stop()
                self.video_num += 1
                self.video_play(values.video_path + values.scene6_video[self.video_num])
                self.overlay_next.next_button.setEnabled(False)
                self.overlay_text.text.setText(values.scene6_text[self.text_num])
                self.text_num += 1


    #영상 종료시 이벤트
    def mediaStateChange(self):
        if self.finish == 0:
            #숫자로 나눠서 김구 대사 끝나면 다음 영상으로
            if self.scene_num ==1:
                if(self.video_num%2 == 0):
                    if (self.mediaPlayer.state() == QMediaPlayer.StoppedState):
                        if (self.video_num == 6):
                            self.video_num += 1
                            self.video_play(values.video_path + values.scene1_video[self.video_num])
                        else:
                            self.video_num += 1
                            self.video_play(values.video_path + values.scene1_video[self.video_num])
                            self.overlay_next.next_button.setEnabled(True)
                            self.overlay_text.text.setText(values.scene1_text[self.text_num])
                            self.text_num += 1
                elif (self.video_num == 7):
                    if (self.mediaPlayer.state() == QMediaPlayer.StoppedState):
                        self.scene_num = 2
                        self.video_thread.back_idx = 2
                        self.video_num = 0
                        self.text_num = 0
                        self.video_play(values.video_path + values.scene2_video[self.video_num])
            elif self.scene_num == 2:
                if (self.video_num % 2 == 0):
                    if (self.mediaPlayer.state() == QMediaPlayer.StoppedState):
                        self.video_num += 1
                        self.video_play(values.video_path + values.scene2_video[self.video_num])
                        self.overlay_next.next_button.setEnabled(True)
                        self.overlay_text.text.setText(values.scene2_text[self.text_num])
                        self.text_num += 1
            elif self.scene_num == 3:
                if self.video_num == 1:
                    if (self.mediaPlayer_act1.state() == QMediaPlayer.StoppedState):
                        self.mediaPlayer_act1.stop()
                        self.videoWidget_act1.setVisible(False)
                        #도장미션
                        self.stamp_num = 1
                        self.mission_stamp.setVisible(True)
                        self.mission_stamp.player.play()

            elif self.scene_num == 4:
                if (self.video_num % 2 == 0):
                    if (self.mediaPlayer.state() == QMediaPlayer.StoppedState):
                        if self.video_num == 6:
                            self.scene_num = 5
                            self.video_thread.back_idx = 5
                            self.video_num = 0
                            self.text_num = 0
                            #씬 5로 이동
                            self.video_thread.stop()
                            self.mediaPlayer.stop()
                            self.videoWidget.setVisible(False)
                            self.video_frame.setVisible(False)
                            self.videoWidget_act2.setVisible(True)
                            self.mediaPlayer_act2.play()
                        else:
                            self.video_num += 1
                            self.video_play(values.video_path + values.scene4_video[self.video_num])
                            self.overlay_next.next_button.setEnabled(True)
                            self.overlay_text.text.setText(values.scene4_text[self.text_num])
                            self.text_num += 1
            elif self.scene_num == 5:
                if self.video_num == 0:
                    if (self.mediaPlayer_act2.state() == QMediaPlayer.StoppedState):
                        self.mediaPlayer_act2.stop()
                        self.videoWidget_act2.setVisible(False)

                        self.video_thread.start()
                        self.videoWidget.setVisible(True)
                        self.video_frame.setVisible(True)
                        self.video_num += 1
                        self.video_play(values.video_path + values.scene5_video[self.video_num])
                        self.overlay_next.next_button.setEnabled(True)
                        self.overlay_text.text.setText(values.scene5_text[self.text_num])
            elif self.scene_num == 6:
                if (self.video_num % 2 == 0):
                    if (self.mediaPlayer.state() == QMediaPlayer.StoppedState):
                        if (self.video_num == 6):
                            self.video_num += 1
                            self.video_play(values.video_path + values.scene6_video[self.video_num])
                            self.overlay_text.text.setText('')
                        elif self.video_num == 8:
                            if (self.mediaPlayer_act3.state() == QMediaPlayer.StoppedState): #편지 미션 끝
                                self.container.setVisible(False)
                                self.container4.setVisible(True)
                                self.video_num += 1
                                self.mediaPlayer_act4.play()
                        else:
                            self.video_num += 1
                            self.video_play(values.video_path + values.scene6_video[self.video_num])
                            self.overlay_next.next_button.setEnabled(True)
                            self.overlay_text.text.setText(values.scene6_text[self.text_num])
                            self.text_num += 1
                elif (self.video_num == 7):
                    if (self.mediaPlayer.state() == QMediaPlayer.StoppedState):
                        self.video_thread.stop()
                        self.videoWidget.setVisible(False)
                        self.video_frame.setVisible(False)
                        self.container.setVisible(True)
                        self.video_num += 1
                        self.mediaPlayer_act3.play()
                elif self.video_num == 9:
                    if (self.mediaPlayer_act4.state() == QMediaPlayer.StoppedState):#설명 영상 끝
                        print('저장 선택으로')
                        self.container4.setVisible(False)
                        self.save_choice.setVisible(True)

    def video_play(self, path):
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(path))
        )
        self.mediaPlayer.play()

    @pyqtSlot(np.ndarray)
    def set_image(self, frame):
        max_width = self.video_frame.width()
        max_height = self.video_frame.height()

        h, w, ch = frame.shape
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(max_width, max_height)
        pixmap = QPixmap.fromImage(p)
        self.video_frame.setPixmap(pixmap)

    def set_images(self, frames):
        max_width = self.mediaPlayer2.width()
        max_height = self.mediaPlayer2.height()
        h, w, ch = frames.shape
        new_w = int(max_width * h / max_height)
        st_w = int(max_height / 2 - new_w / 2)
        rgb_image = cv2.cvtColor(frames[:, st_w:st_w + new_w, :], cv2.COLOR_RGB2BGR)
        rgb_image = cv2.flip(rgb_image, 1)
        bytes_per_line = ch * new_w
        rgb_image = cv2.resize(rgb_image, (max_width, max_height))
        convert_to_Qt_format = QImage(rgb_image.data, new_w, h, bytes_per_line, QImage.Format_RGB888)
        # p = convert_to_Qt_format.scaled(max_width, max_height)
        pixmap = QPixmap.fromImage(convert_to_Qt_format)

        self.mediaPlayer2.setPixmap(pixmap)

    def closeEvent(self, event):
        self.video_thread.stop()
        self.video_thread2.stop()
        self.mediaPlayer.stop()
        self.mediaPlayer_act1.stop()
        self.mediaPlayer_act2.stop()
        self.mediaPlayer_act3.stop()
        self.mediaPlayer_act4.stop()
        self.rec.stop()
        event.accept()

class Button(QPushButton):
    def __init__(self, title, parent):
        QPushButton.__init__(self, title, parent)
        self.offset = 0

    def mouseMoveEvent(self, e: QMouseEvent):
        if e.buttons() != Qt.LeftButton:
            return

        mime_data = QMimeData()
        mime_data.setData("application/hotspot", b"%d %d" % (e.x(), e.y()))

        drag = QDrag(self)
        drag.setMimeData(mime_data)

        pixmap = QPixmap(self.size())
        # self.render(pixmap)
        drag.setPixmap(pixmap)

        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_(Qt.MoveAction)

class VideoThread(QThread):
    capture = False
    pause = False
     # 비디오 프레임 전달
    image_change_signal = pyqtSignal(np.ndarray)

    video_width = int(values.width / 2)  # 683
    video_height = values.video_height  # 384

    # 클래스 객체 생성
    u = user_custom(values.model_path, values.img_path, (video_width, video_height))
    # 배경전환을 위한 초기화
    mp_drawing = mp.solutions.drawing_utils
    mp_selfie_segmentation = mp.solutions.selfie_segmentation

    #꾸미기 상태
    hat_on = False
    glasses_on = False
    cloth_on = False
    background_on = True
    back_idx = 1
    hat_idx = None
    cloth_idx= None
    glasses_idx = None


    def run(self):
        print("CAM RUN")
        self.capture = True

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        with self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
            while self.capture:
                time.sleep(0.01)
                ret, img = cap.read()
                if not ret:
                    self.stop()
                    break
                img = cv2.resize(img, (self.video_width, self.video_height), interpolation=cv2.INTER_CUBIC)
                if self.background_on or self.hat_on or self.glasses_on or self.cloth_on:
                    custom_img = img.copy()
                    if self.background_on:
                        custom_img = self.u.backgroud_video(self.back_idx, custom_img,selfie_segmentation)

                    if self.cloth_on:
                        custom_img = self.u.wear_cloth(self.cloth_idx, custom_img)
                    if self.hat_on:
                        custom_img = self.u.wear_hat(self.hat_idx, custom_img)
                    elif self.glasses_on:
                        custom_img = self.u.wear_glasses(self.glasses_idx, custom_img)

                    self.image_change_signal.emit(custom_img)

                else:
                    self.image_change_signal.emit(img)


    def stop(self):
        self.capture = False
        self.wait()

class VideoThread2(QThread):
    capture = False
    pause = False
    image_change_signal = pyqtSignal(np.ndarray)  # 비디오 프레임 전달

    def run(self):
        print("CAM RUN2")
        self.capture = True

        cap = cv2.VideoCapture(values.scene_3_2)

        while self.capture:
            ret, frame = cap.read()

            if not ret:
                self.stop()
                break
            if self.pause:
                while True:
                    if self.pause == False:
                        break
            time.sleep(0.1)
            self.image_change_signal.emit(frame)

    def stop(self):
        self.capture = False
        self.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Page7()
    mywindow.show()
    app.exec_()