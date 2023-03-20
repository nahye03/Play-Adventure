import sys

import pygame
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *

import values


class Mission_stamp(QWidget):
    def __init__(self, parent=None):
        super(Mission_stamp, self).__init__(parent)
        self.initUI()

    def initUI(self):

        pygame.init()
        pygame.mixer.music.load(values.stamp_sound)

        sound = values.scene_sound
        self.player = QMediaPlayer()

        self.player.setMedia(
            QMediaContent(QUrl.fromLocalFile(sound))
        )

        # 전체 이미지
        self.back_img = QLabel(self)
        self.back_img.setAlignment(Qt.AlignCenter)
        img = QPixmap(values.mission_stamp).scaled(values.width, values.height)
        self.back_img.setPixmap(QPixmap(img))

        # 도장 이미지
        self.stamp_click = QPixmap(values.stamp).scaledToWidth(55)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.back_img)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Mission_stamp()
    mywindow.show()
    app.exec_()