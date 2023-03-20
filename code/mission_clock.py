import sys

from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *

import values


class Button(QPushButton):
    def __init__(self, parent):
        QPushButton.__init__(self, parent)
        self.offset = 0

    def mouseMoveEvent(self, e: QMouseEvent):
        if e.buttons() != Qt.LeftButton:
            return

        mime_data = QMimeData()
        mime_data.setData("application/hotspot", b"%d %d" % (e.x(), e.y()))

        drag = QDrag(self)
        drag.setMimeData(mime_data)

        pixmap = QPixmap(self.size())
        pixmap.fill(QColor('transparent'))
        self.render(pixmap)
        drag.setPixmap(pixmap)

        drag.setHotSpot(e.pos() - self.rect().topLeft())
        drag.exec_(Qt.MoveAction)


class Mission_clock(QWidget):
    def __init__(self):
        super(Mission_clock, self).__init__()
        self.resize(values.width, values.height)

        self.initUI()

        sound = values.clock_backsound
        self.player_clock = QMediaPlayer()

        self.player_clock.setMedia(
            QMediaContent(QUrl.fromLocalFile(sound))
        )


    def initUI(self):
        self.left_hand = QLabel(self)
        left = QPixmap(values.left_hand).scaledToWidth(values.width * 0.5)
        self.left_hand.setPixmap(QPixmap(left))

        self.right_hand = QLabel(self)
        right = QPixmap(values.right_hand).scaledToWidth(values.width * 0.5)
        self.right_hand.setPixmap(QPixmap(right))

        self.mission_drag = QLabel(self)
        self.mission_drag.setAlignment(Qt.AlignCenter)
        self.mission_drag.setStyleSheet("background:transparent")
        mission = QPixmap(values.mission_clock).scaledToWidth(values.width * 0.3)
        self.mission_drag.setPixmap(QPixmap(mission))

        # 드래그
        self.setAcceptDrops(True)

        self.clock1 = Button(self)
        self.clock1.setIcon(QIcon(values.clock1))
        self.clock1.setIconSize(QSize(int(values.width * 0.25), int(values.height * 0.25)))
        self.clock1.setStyleSheet("background-color:transparent")
        self.clock1.setGeometry(int(values.width * 0.25), int(values.height * 0.54), int(values.width * 0.25), int(values.height * 0.25))

        self.clock2 = Button(self)
        self.clock2.setIcon(QIcon(values.clock2))
        self.clock2.setIconSize(QSize(int(values.width * 0.3), int(values.height * 0.3)))
        self.clock2.setStyleSheet("background-color:transparent")
        self.clock2.setGeometry(int(values.width * 0.55), int(values.height * 0.45), int(values.width * 0.3), int(values.height * 0.3))

        self.clock1.setCheckable(True)
        self.clock2.setCheckable(True)

        self.layout = QGridLayout()
        self.layout.addWidget(self.mission_drag, 0, 0, 1, 2)
        self.layout.addWidget(self.left_hand, 1, 0, -1, 1)
        self.layout.addWidget(self.right_hand, 1, 1, -1, 1)

        self.setLayout(self.layout)

    def dragEnterEvent(self, e):
        if e.mimeData():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.clock1.move(int(values.width * 0.65), int(values.height * 0.54))
        self.clock2.move(int(values.width * 0.16), int(values.height * 0.45))

        self.clock1.toggle()
        self.clock2.toggle()

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Mission_clock()
    mywindow.show()
    app.exec_()