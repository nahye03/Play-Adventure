import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import page3
import page4
import ui_functions
import values


class Page8(ui_functions.Topmenu):
    def __init__(self):
        super(Page8,self).__init__()
        self.setWindowTitle('종료창')

        self.home_button.clicked.connect(self.home_button_clicked)
        self.my_button.clicked.connect(self.my_button_clicked)
        self.menuWidget.cellClicked.connect(self.menu_clicked)  # 탑메뉴 클릭 이벤트


    def setUI(self):
        super(Page8, self).setUI()

        hlayout = QHBoxLayout(self)
        vlayout = QVBoxLayout(self)

        #김구 이미지
        img_label = QLabel()
        pixmap = QPixmap(values.page8_image)
        img_label.setPixmap(QPixmap(pixmap))

        #목록
        self.my_button = QPushButton(self)
        self.my_button.setIcon(QIcon(values.page8_play_img))
        self.my_button.setIconSize(QSize(90,90))
        self.my_button.setStyleSheet('border:None')
        self.my_button.setText('  내가 연기한 영상 보러가기')
        self.my_button.setFont(QFont(values.font, 20))

        button2 = QPushButton(self)
        button2.setIcon(QIcon(values.page8_play_img))
        button2.setIconSize(QSize(90,90))
        button2.setStyleSheet('border:None')
        button2.setText('  다시 처음부터 연기하기')
        button2.setFont(QFont(values.font, 20))

        self.home_button = QPushButton(self)
        self.home_button.setIcon(QIcon(values.page8_home_img))
        self.home_button.setIconSize(QSize(90,90))
        self.home_button.setStyleSheet('border:None')
        self.home_button.setText('  메인 화면')
        self.home_button.setFont(QFont(values.font, 20))

        vlayout.addStretch(1)
        vlayout.addWidget(self.my_button)
        vlayout.addStretch(4)
        vlayout.addWidget(button2)
        vlayout.addStretch(4)
        vlayout.addWidget(self.home_button)
        vlayout.addStretch(1)

        hlayout.addWidget(img_label,alignment=Qt.AlignCenter)
        hlayout.addLayout(vlayout)

        self.layout.addLayout(hlayout)

    #내가 한 영상 보러가기 이벤트
    def my_button_clicked(self):
        self.secondWindow = page4.Page4()
        self.secondWindow.show()
        self.close()

    #메인 화면 이벤트
    def home_button_clicked(self):
        self.secondWindow = page3.Page3()
        self.secondWindow.show()
        self.close()

    #탑메뉴 버튼 이벤트
    def menu_clicked(self, row, col):
        data = self.menuWidget.item(row, col)
        if data.text() == 'HOME':
            self.secondWindow = page3.Page3()
            self.secondWindow.show()
            self.close()
        elif data.text() == 'My':
            self.secondWindow = page4.Page4()
            self.secondWindow.show()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Page8()
    mywindow.show()
    app.exec_()