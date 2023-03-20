from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import values
import sys


class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

class Topmenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(values.width, values.height)
        self.setStyleSheet('background-color:white')
        self.menu()
        self.setUI()

    def setUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.menuWidget)

        self.setLayout(self.layout)

    def menu(self):
        self.menuWidget = QTableWidget(self)
        # 배경 색상 설정
        self.menuWidget.setStyleSheet('background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(159, 212, 123), stop:1 rgb(83, 128, 53));')
        self.menuWidget.setFixedSize(values.width, 50)
        self.menuWidget.setRowCount(1)
        self.menuWidget.setColumnCount(3)
        delegate = AlignDelegate(self.menuWidget)  # 글자 중앙 정렬
        self.menuWidget.setItemDelegate(delegate)

        middle_button = QPushButton()
        middle_button.setStyleSheet('border:None; background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(159, 212, 123), stop:1 rgb(83, 128, 53));')

        self.menuWidget.setItem(0, 0, QTableWidgetItem("HOME"))
        self.menuWidget.setCellWidget(0, 1, middle_button)
        self.menuWidget.setItem(0, 2, QTableWidgetItem("My"))

        self.menuWidget.setFont(QFont(values.font, 15))
        self.menuWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) #cell 변경 금지

        self.menuWidget.setColumnWidth(0, 150)
        self.menuWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.menuWidget.setColumnWidth(2, 150)

        self.menuWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.menuWidget.horizontalHeader().close()
        self.menuWidget.verticalHeader().close()