import errno
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *

import page3
import ui_functions
import values


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

class Page4(ui_functions.Topmenu):
    def __init__(self):
        super(Page4,self).__init__()
        self.setWindowTitle('My 화면')

        self.menuWidget.cellClicked.connect(self.menu_clicked)

    def setUI(self):
        super(Page4, self).setUI()

        hlayout = QHBoxLayout(self)
        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(10,10,10,10)

        title_label = QLabel(self)
        title_label.setText('나의 실습 영상')
        title_label.setFont(QFont(values.font, 15))

        # 폴더 경로보기

        self.model = QFileSystemModel()
        self.model.setRootPath(values.save_video_path)
        self.index_root = self.model.index(self.model.rootPath())

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.index_root)
        self.tree_view.clicked.connect(self.on_treeView_clicked)

        self.tree_view.header().hideSection(1)
        self.tree_view.header().hideSection(2)
        self.tree_view.header().resizeSection(0,values.width*0.25)
        self.tree_view.header().resizeSection(1, values.width*0.15)

        vlayout.addWidget(title_label, alignment=Qt.AlignCenter)
        vlayout.addSpacing(10)
        vlayout.addWidget(self.tree_view)

        #내 비디오 재생
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.videoWidget.setMinimumSize(values.width*0.6, values.video_height)

        hlayout.addLayout(vlayout)
        hlayout.addWidget(self.videoWidget)

        self.layout.addLayout(hlayout)

    def menu_clicked(self, row, col):
        data = self.menuWidget.item(row, col)
        if data.text() == 'HOME':
            self.secondWindow = page3.Page3()
            self.secondWindow.show()
            self.close()
        elif data.text() == 'My':
            self.secondWindow = Page4()
            self.secondWindow.show()
            self.close()

    @pyqtSlot(QModelIndex)
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        filePath = self.model.filePath(indexItem)
        self.mediaPlayer.stop()
        self.video_play(filePath)

    def video_play(self, path):
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl.fromLocalFile(path))
        )
        self.mediaPlayer.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Page4()
    mywindow.show()
    app.exec_()