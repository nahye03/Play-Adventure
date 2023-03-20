import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *

import page3
import ui_functions
import values


class Page2(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(values.width, values.height)
        self.setWindowTitle('감정 선택')
        self.setStyleSheet('background-color:white')
        self.initUI()
        self.video_play(values.page2_video)

        self.finish_button.clicked.connect(self.finish_button_clicked)

    def initUI(self):
        self.emo_list = []

        # 레이아웃 선언
        layout = QHBoxLayout(self)  # 전체 틀
        right_layout = QVBoxLayout(self)  # 오른쪽 레이아웃

        # 왼쪽 화면
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()

        # 오른쪽 화면
        self.right_label = QLabel()
        self.emo_text = QLabel()  # 클릭한 감정 나타나게하기 (버튼 중복이 힘들것 같음)
        self.emo_text.setFont(QFont('Times', 15))
        self.emo_image = QLabel()  # 감정 그림
        self.emotion_table = QTableWidget()  # 감정 여러개 있는 표 레이아웃
        self.finish_button = QPushButton('선택 완료')
        self.finish_button.setFixedSize(values.width / 10, values.height / 20)
        self.finish_button.setStyleSheet('color:white; background-color:rgb(120,180,230); border-radius:5px')

        #이벤트 지정
        self.emotion_table.cellClicked.connect(self.cellclicked_event)

        # 감정 이미지 가져오기
        pixmap = QPixmap(values.page2_image)
        pixmap = pixmap.scaledToWidth(values.width/3)
        self.emo_image.setPixmap(pixmap)  # image path

        # 감정 선택 레이아웃
        emotion = [['기분좋은','평화로운','서러운','삐친','걱정되는','놀란','간절한'],
                  ['신나는','해맑은','슬픈','질투하는','지친','무서운','미안한'],
                  ['안도하는','행복한','외로운','심통나는','고민되는','답답한','반성하는'],
                  ['여유로운','흐뭇한','의기소침','짜증나는','변명하는','귀찮은','수줍은'],
                  ['보람찬','희망찬','후회되는','절망적인','억울한','괴로운','위축된'],
                  ['다정한','가슴뭉클','우울한','화난','용기있는','찝찝한','서러운']]

        self.emotion_table.setRowCount(6)
        self.emotion_table.setColumnCount(7)
        for i in range(self.emotion_table.rowCount()):
            for j in range(self.emotion_table.columnCount()):
                self.emotion_table.setItem(i,j,QTableWidgetItem(emotion[i][j]))

        self.emotion_table.setFixedSize(values.width *0.4, values.height *0.4)
        delegate = ui_functions.AlignDelegate(self.emotion_table) #글자 중앙 정렬
        self.emotion_table.setItemDelegate(delegate)
        self.emotion_table.setEditTriggers(QAbstractItemView.NoEditTriggers) #셀 수정 불가

        self.emotion_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.emotion_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.emotion_table.horizontalHeader().close()
        self.emotion_table.verticalHeader().close()

        # 오른쪽 레이아웃에 이미지, 표, 버튼 설정
        right_layout.addStretch(5)
        right_layout.addWidget(self.emo_text, alignment=Qt.AlignCenter)
        right_layout.addStretch(1)
        right_layout.addWidget(self.emo_image, alignment=Qt.AlignCenter)
        right_layout.addStretch(1)
        right_layout.addWidget(self.emotion_table, alignment=Qt.AlignHCenter)
        right_layout.addStretch(3)
        right_layout.addWidget(self.finish_button, alignment=Qt.AlignCenter)
        right_layout.addStretch(5)

        self.right_label.setLayout(right_layout)

        # 전체 레이아웃 설정
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.videoWidget)
        layout.addWidget(self.right_label)
        self.setLayout(layout)

    def cellclicked_event(self, row, col):
        data = self.emotion_table.item(row, col)
        self.emotion_table.item(row,col).setBackground(QColor(250,250,150))
        self.emo_list.append('#' + data.text())
        self.emo_text.setText(str(self.emo_list).replace('[', "").replace(']', ""))

    def finish_button_clicked(self):
        print('감정 선택 완료')
        self.mediaPlayer.stop()
        self.secondWindow = page3.Page3()
        self.secondWindow.show()
        self.close()

    def video_play(self, path):
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(path))
        )
        self.mediaPlayer.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Page2()
    mywindow.show()
    app.exec_()
