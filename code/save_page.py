from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import values


class Save_choice(QWidget):
    def __init__(self):
        super(Save_choice, self).__init__()
        self.setUI()

    def setUI(self):
        #저장할까요 텍스트
        save_label = QLabel(self)
        save_label.setText('저장할까요?')
        save_label.setFont(QFont(values.font, 30))
        save_label.resize(values.width, 100)
        save_label.setAlignment(Qt.AlignCenter)

        #yes or no 버튼
        self.yes_button = QPushButton(self)
        self.yes_button.setIcon(QIcon(values.yes_button_img))
        self.yes_button.setStyleSheet('backgroud-color:rgba(0,0,0,0); border:None')
        self.yes_button.setIconSize(QSize(200, 200))
        self.no_button = QPushButton(self)
        self.no_button.setIcon(QIcon(values.no_button_img))
        self.no_button.setStyleSheet('backgroud-color:rgba(0,0,0,0);  border:None')
        self.no_button.setIconSize(QSize(200, 200))

        save_layout = QGridLayout(self)
        save_layout.setContentsMargins(50,50,50,150)
        save_layout.addWidget(save_label, 0, 0, 1, 2)
        save_layout.addWidget(self.yes_button, 1, 0, -1, 1)
        save_layout.addWidget(self.no_button, 1, 1, -1, 1)
