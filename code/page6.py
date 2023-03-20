import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *

import page3
import page4
import page7
import ui_functions
import values
from background_video import *


#꾸미기 버튼 layer
class overlay_button(QWidget):
    def __init__(self, parent = None):
        super(overlay_button, self).__init__(parent)

        #꾸미기 버튼
        self.makeup_button = QPushButton(self)
        size = values.height/6
        self.makeup_button.setStyleSheet('background-color : rgba(0,0,0,0)')
        self.makeup_button.setIcon(QIcon(values.page6_image))
        self.makeup_button.setIconSize(QSize(size,size))
        self.makeup_button.setGeometry(values.width / 2 - size -10, values.video_height*0.8, size, values.height*0.16)

        #꾸미기 완료 버튼
        # self.finish_button = QPushButton(self)
        # self.finish_button.setStyleSheet('background-color : rgba(0,0,0,0)')
        # self.finish_button.setIcon(QIcon(values.page6_image2))
        # self.finish_button.setIconSize(QSize(values.width/10, values.height/10))
        # self.finish_button.setGeometry(values.width / 2 - values.width/10 -10, 0, values.width/10, values.height/10)

#의상, 악세서리 선택 layer
class overlay_tab(overlay_button):
    def __init__(self, parent=None):
        super(overlay_tab, self).__init__(parent)

        self.groupButton = QButtonGroup(self)
        tab_table = QTableWidget(self)
        tab_table.setRowCount(1)
        tab_table.setColumnCount(2)
        tab_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tab_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tab_table.horizontalHeader().close()
        tab_table.verticalHeader().close()

        name = ['의상','악세사리']
        for i in range(len(name)):
            button = QPushButton(name[i])
            button.setFont(QFont(values.font, 13, QFont.Bold))
            button.setStyleSheet("background-color: rgba(0,0,0,0%);border: none;")
            tab_table.setCellWidget(0,i,button)
            self.groupButton.addButton(button, i)

        tab_table.setStyleSheet('background-color:rgb(255,244,231);border:rgb(255,213,90); girdline-color:rgb(255,213,90)')
        tab_table.setGeometry(10,values.height*0.8,values.width * 0.41,values.height/15)

        self.makeup_button.raise_()

#의상 layer
class overlay_cloth(overlay_button):
    def __init__(self, parent=None):
        super(overlay_cloth, self).__init__(parent)

        self.clothButton = QButtonGroup(self)
        cloth_table = QTableWidget(self)
        cloth_table.setRowCount(1)
        cloth_table.setColumnCount(len(values.clothes_path)+1)
        cloth_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        cloth_table.horizontalHeader().close()
        cloth_table.verticalHeader().close()

        #의상 버튼 만들기
        for i in range(len(values.clothes_path)):
            file_path = values.img_path + values.clothes_path[i]
            button = QPushButton(self)
            # button.setMinimumHeight(values.height*0.16)
            button.setIcon(QIcon(file_path))
            button.setIconSize(QSize(values.width*0.1, values.height*0.14))
            button.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: none;")
            cloth_table.setCellWidget(0, i, button)
            self.clothButton.addButton(button, i)

        # 이전 버튼
        button_pre = QPushButton('이전')
        # button_pre.setText('이전')
        button_pre.setMinimumWidth(values.width*0.08)
        button_pre.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: none; ")
        button_pre.setFont(QFont(values.font, 13))
        cloth_table.setCellWidget(0, len(values.clothes_path), button_pre)
        self.clothButton.addButton(button_pre, len(values.clothes_path))

        cloth_table.resizeColumnsToContents()
        cloth_table.setGeometry(10, values.video_height * 0.8, values.width * 0.44, values.height*0.16)
        cloth_table.setStyleSheet('background-color:rgb(255,244,231); gridline-color: rgb(255,213,90); border:rgb(255,213,90)')

        self.makeup_button.raise_()

#모자, 안경 선택 layer
class overlay_acc_tab(overlay_button):
    def __init__(self, parent=None):
        super(overlay_acc_tab, self).__init__(parent)

        name = ['모자', '안경', '그 외', '이전']

        self.accButton = QButtonGroup(self)
        acctab_table = QTableWidget(self)
        acctab_table.setRowCount(1)
        acctab_table.setColumnCount(len(name))
        acctab_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        acctab_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        acctab_table.horizontalHeader().close()
        acctab_table.verticalHeader().close()

        for i in range(len(name)):
            button = QPushButton(name[i])
            if name[i] =='이전':
                button.setFont(QFont(values.font, 13))
            else:
                button.setFont(QFont(values.font, 13, QFont.Bold))
            button.setStyleSheet("background-color: rgba(0,0,0,0%);border: none;")
            acctab_table.setCellWidget(0,i,button)
            self.accButton.addButton(button, i)

        acctab_table.setStyleSheet('background-color:rgb(255,244,231);border:rgb(255,213,90); girdline-color:rgb(255,213,90)')
        acctab_table.setGeometry(10,values.height*0.8,values.width * 0.41,values.height/15)

        self.makeup_button.raise_()

#악세사리_모자 layer
class overlay_hat(overlay_button):
    def __init__(self, parent=None):
        super(overlay_hat, self).__init__(parent)

        self.hatButton = QButtonGroup(self)
        hat_table = QTableWidget(self)
        hat_table.setRowCount(1)
        hat_table.setColumnCount(len(values.hats_path)+1)
        hat_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        hat_table.horizontalHeader().close()
        hat_table.verticalHeader().close()

        #모자 버튼 만들기
        for i in range(len(values.hats_path)):
            file_path = values.img_path + values.hats_path[i]
            button = QPushButton(self)
            button.setIcon(QIcon(file_path))
            button.setIconSize(QSize(values.width*0.1, values.height*0.14))
            button.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: none;")
            hat_table.setCellWidget(0, i, button)
            self.hatButton.addButton(button, i)

        # 이전 버튼
        button_pre = QPushButton(self)
        button_pre.setText('이전')
        button_pre.setMinimumWidth(values.width*0.08)
        button_pre.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: none; ")
        button_pre.setFont(QFont(values.font, 13))
        hat_table.setCellWidget(0, len(values.hats_path), button_pre)
        self.hatButton.addButton(button_pre, len(values.hats_path))

        hat_table.resizeColumnsToContents()
        hat_table.setGeometry(10, values.video_height * 0.8, values.width * 0.44, values.height*0.16)
        hat_table.setStyleSheet('background-color:rgb(255,244,231); gridline-color: rgb(255,213,90); border:rgb(255,213,90)')

        self.makeup_button.raise_()

#악세사리_안경 layer
class overlay_glasses(overlay_button):
    def __init__(self, parent=None):
        super(overlay_glasses, self).__init__(parent)

        self.glassesButton = QButtonGroup(self)
        glasses_table = QTableWidget(self)
        glasses_table.setRowCount(1)
        glasses_table.setColumnCount(len(values.glasses_path)+1)
        glasses_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        glasses_table.horizontalHeader().close()
        glasses_table.verticalHeader().close()

        #모자 버튼 만들기
        for i in range(len(values.glasses_path)):
            file_path = values.img_path + values.glasses_path[i]
            button = QPushButton(self)
            button.setIcon(QIcon(file_path))
            button.setIconSize(QSize(values.width*0.1, values.height*0.14))
            button.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: none;")
            glasses_table.setCellWidget(0, i, button)
            self.glassesButton.addButton(button, i)

        # 이전 버튼
        button_pre = QPushButton(self)
        button_pre.setText('이전')
        button_pre.setMinimumWidth(values.width*0.08)
        button_pre.setStyleSheet("background-color: rgba(0,0,0,0%);border-style: none; ")
        button_pre.setFont(QFont(values.font, 13))
        glasses_table.setCellWidget(0, len(values.glasses_path), button_pre)
        self.glassesButton.addButton(button_pre, len(values.glasses_path))

        glasses_table.resizeColumnsToContents()
        glasses_table.setGeometry(10, values.video_height * 0.8, values.width * 0.44, values.height*0.16)
        glasses_table.setStyleSheet('background-color:rgb(255,244,231); gridline-color: rgb(255,213,90); border:rgb(255,213,90)')

        self.makeup_button.raise_()

class Page6(ui_functions.Topmenu):
    def __init__(self):
        super(Page6,self).__init__()
        self.setWindowTitle('꾸미기 설명')

        self.video_num = 0
        self.first_cloth = 0
        self.finish = 0

        self.video_thread = VideoThread()
        self.video_thread.image_change_signal.connect(self.set_image)
        self.video_thread.start()

        # 꾸미기 버튼들
        self.overlay_button = overlay_button(self.video_frame) #꾸미기버튼
        self.overlay_tab = overlay_tab(self.video_frame)  #의상, 배경 선택 버튼
        self.overlay_tab.hide()
        self.overlay_cloth = overlay_cloth(self.video_frame)  # 의상 버튼
        self.overlay_cloth.hide()
        self.overlay_acc_tab = overlay_acc_tab(self.video_frame) #모자, 안경 선택 버튼
        self.overlay_acc_tab.hide()
        self.overlay_hat = overlay_hat(self.video_frame) #모자 버튼
        self.overlay_hat.hide()
        self.overlay_glasses = overlay_glasses(self.video_frame) #안경 버튼
        self.overlay_glasses.hide()

        #이벤트들
        self.skip_button.clicked.connect(self.skip_button_clicked)
        self.overlay_button.makeup_button.clicked.connect(self.makeup_button_clicked)
        self.overlay_tab.groupButton.buttonClicked.connect(self.tab_button_clicked)
        self.overlay_cloth.clothButton.buttonClicked[int].connect(self.cloth_button_clicked)
        self.overlay_acc_tab.accButton.buttonClicked.connect(self.acc_tab_button_clicked)
        self.overlay_hat.hatButton.buttonClicked[int].connect(self.hat_button_clicked)
        self.overlay_glasses.glassesButton.buttonClicked[int].connect(self.glasses_button_clicked)

        self.mediaPlayer.stateChanged.connect(self.mediaStateChange) #선생님 영상 상태 이벤트
        self.mediaPlayer_start.stateChanged.connect(self.mediaStateChange)

        self.menuWidget.cellClicked.connect(self.menu_clicked) #탑메뉴 클릭 이벤트

    def setUI(self):
        super(Page6, self).setUI()

        #전체 레이아웃 선언
        videos_layout = QHBoxLayout()

        #선생님 영상
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()

        #학생 영상
        self.video_frame = QLabel()

        #videos_layout 레이아웃에 추가
        videos_layout.addWidget(self.videoWidget)
        videos_layout.addWidget(self.video_frame)

        self.layout.addLayout(videos_layout)

        self.videoWidget.hide()
        self.video_frame.hide()

        #시작 영상
        self.mediaPlayer_start = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget_start = QVideoWidget()

        self.container = QWidget()
        self.container.setStyleSheet('background-color : rgba(100,0,0,0)')
        start_layout = QVBoxLayout(self.container)
        start_layout.setContentsMargins(0, 0, 0, 0)
        start_layout.addWidget(self.videoWidget_start)

        self.skip_button = QPushButton(self.container)
        self.skip_button.setIcon(QIcon(values.skip_image))
        self.skip_button.setIconSize(QSize(110, 110))
        self.skip_button.setGeometry(values.width - 120, values.video_height - 110, 110, 100)

        self.videoWidget_start.setGeometry(0, values.menu_height, values.width, values.video_height)
        self.mediaPlayer_start.setVideoOutput(self.videoWidget_start)
        self.mediaPlayer_start.setMedia(
            QMediaContent(QUrl.fromLocalFile(values.video_path + values.page6_video[0]))
        )
        self.layout.addWidget(self.container)
        self.mediaPlayer_start.play()

    def menu(self):
        super(Page6, self).menu()
        self.menuWidget.insertColumn(0)
        self.menuWidget.setItem(0,0,QTableWidgetItem("저장"))
        self.menuWidget.setColumnWidth(0, 150)

    def menu_clicked(self, row, col):
        data = self.menuWidget.item(row, col)
        if data.text() == 'HOME':
            self.finish = 1
            self.video_thread.stop()
            self.mediaPlayer_start.stop()
            self.mediaPlayer.stop()
            self.secondWindow = page3.Page3()
            self.secondWindow.show()
            self.close()
        elif data.text() == 'My':
            self.finish = 1
            self.video_thread.stop()
            self.mediaPlayer_start.stop()
            self.mediaPlayer.stop()
            self.secondWindow = page4.Page4()
            self.secondWindow.show()
            self.close()
        elif data.text() == '저장':
            self.finish = 1
            print('저장')
            self.video_thread.stop()
            self.mediaPlayer.stop()
            self.mediaPlayer_start.stop()
            self.secondWindow = page7.Page7()
            self.secondWindow.show()
            self.close()

    def mediaStateChange(self):
        if self.finish == 0:
            if(self.video_num == 0):
                if (self.mediaPlayer_start.state() == QMediaPlayer.StoppedState):
                    self.mediaPlayer_start.stop()
                    self.container.setVisible(False)
                    self.videoWidget.setVisible(True)
                    self.video_frame.setVisible(True)
                    self.video_num += 1
                    self.overlay_button.makeup_button.setEnabled(False)
                    self.video_play(values.video_path + values.page6_video[self.video_num]) #1번
            if (self.mediaPlayer.state() == QMediaPlayer.StoppedState):
                if self.video_num == 1:
                    self.video_num += 1
                    self.video_play(values.video_path + values.page6_video[self.video_num]) #2번
                    self.overlay_button.makeup_button.setEnabled(True)
                elif self.video_num == 3:
                    self.overlay_tab.groupButton.button(0).setEnabled(True)
                    self.overlay_tab.groupButton.button(1).setEnabled(True)
                    self.video_num = 4
                    self.video_play(values.video_path + values.page6_video[self.video_num]) #4번
                elif self.video_num == 5 or self.video_num == 6:
                    self.video_num += 1
                    self.video_play(values.video_path + values.page6_video[self.video_num]) #6번 / 7

    def skip_button_clicked(self):
        self.mediaPlayer_start.stop()

    def makeup_button_clicked(self):
        if self.video_num == 2:
            self.mediaPlayer.stop()
            self.video_num = 3
            self.video_play(values.video_path + values.page6_video[3]) #3번
            self.overlay_button.setVisible(False)
            self.overlay_tab.setVisible(True)
            self.overlay_tab.groupButton.button(0).setEnabled(False)
            self.overlay_tab.groupButton.button(1).setEnabled(False)

    #의상과 악세서리 선택 버튼
    def tab_button_clicked(self, button):
        if button.text() == '의상':
            if(self.video_num == 4 and self.first_cloth == 0):
                self.mediaPlayer.stop()
                self.video_num = 5
                self.video_play(values.video_path + values.page6_video[self.video_num]) #5번
                self.first_cloth += 1
            self.overlay_tab.setVisible(False)
            self.overlay_cloth.setVisible(True)

        if button.text() == '악세사리':
            self.overlay_tab.setVisible(False)
            self.overlay_acc_tab.setVisible(True)
            
    #악세사리 종류 선택 버튼
    def acc_tab_button_clicked(self, button):
        if button.text() == '모자':
            self.overlay_acc_tab.setVisible(False)
            self.overlay_hat.setVisible(True)
        elif button.text() == '안경':
            self.overlay_acc_tab.setVisible(False)
            self.overlay_glasses.setVisible(True)
        elif button.text() == '이전':
            self.overlay_acc_tab.setVisible(False)
            self.overlay_tab.setVisible(True)

    #옷 선택
    def cloth_button_clicked(self, button):
        if button == 0:
            self.video_thread.cloth_on = True
            self.video_thread.cloth_idx = 0
        elif button ==1:
            self.video_thread.cloth_on = True
            self.video_thread.cloth_idx = 1
        elif button ==2:
            self.video_thread.cloth_on = True
            self.video_thread.cloth_idx = 2
        # 이전 버튼
        else:
            self.overlay_cloth.setVisible(False)
            self.overlay_tab.setVisible(True)

    #모자 선택
    def hat_button_clicked(self, button):
        if button == 0:
            self.video_thread.glasses_on = False
            self.video_thread.glasses_idx = None
            self.video_thread.hat_on = True
            self.video_thread.hat_idx = 0
        elif button == 1:
            self.video_thread.glasses_on = False
            self.video_thread.glasses_idx = None
            self.video_thread.hat_on = True
            self.video_thread.hat_idx = 1
        #이전 버튼
        else:
            self.overlay_hat.setVisible(False)
            self.overlay_acc_tab.setVisible(True)

    #안경 선택
    def glasses_button_clicked(self, button):
        if button == 0:
            self.video_thread.hat_on = False
            self.video_thread.hat_idx = None
            self.video_thread.glasses_on = True
            self.video_thread.glasses_idx = 0
        elif button == 1:
            self.video_thread.hat_on = False
            self.video_thread.hat_idx = None
            self.video_thread.glasses_on = True
            self.video_thread.glasses_idx = 1
        # 이전 버튼
        else:
            self.overlay_glasses.setVisible(False)
            self.overlay_acc_tab.setVisible(True)

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

    def closeEvent(self, event):
        self.video_thread.stop()
        self.mediaPlayer.stop()
        self.mediaPlayer_start.stop()
        event.accept()

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
    back_idx = 0
    hat_idx = None
    cloth_idx= None
    glasses_idx = None

    def run(self):
        print("CAM RUN")
        self.capture = True

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        with self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
            while self.capture:
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
        idx_dict = {'cloth':self.cloth_idx,
                    'hat':self.hat_idx,
                    'glasses':self.glasses_idx}

        with open('final_idx.txt','w') as f:
            for name, idx in idx_dict.items():
                f.write(f'{name} {idx}\n')  # 중간에 space로 넣음

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Page6()
    mywindow.show()
    app.exec_()