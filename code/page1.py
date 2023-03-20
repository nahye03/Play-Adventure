import errno
import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import page2
import values


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

class Page1(QWidget):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.setFixedSize(values.width, values.height)
        self.setWindowTitle('시작')
        self.setUI()
        self.start_button.clicked.connect(self.start_button_clicked)

        # 결과 저장 폴더 만들기
        createFolder(values.save_video_path)

    def setUI(self):
        image = QImage(values.page1_image)
        image = image.scaled(self.width(), self.height())
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(image))
        self.setPalette(palette)

        self.start_button = QPushButton(self)
        self.start_button.setText('시작')
        self.start_button.setGeometry(values.width/2-values.width / 8, values.height/2-values.height / 20, values.width / 4, values.height / 10)
        self.start_button.setStyleSheet('color:white; background-color:rgb(130,130,130); border: 2px solid white;')
        self.start_button.setFont(QFont(values.font, 30))

    def start_button_clicked(self):
        self.secondWindow = page2.Page2()
        self.secondWindow.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Page1()
    mywindow.show()
    app.exec_()