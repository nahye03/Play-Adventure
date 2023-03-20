import sys

from PyQt5.QtWidgets import *
import page1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = page1.Page1()
    mywindow.show()
    app.exec_()