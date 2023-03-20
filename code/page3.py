import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import page2
import page4
import page6
import ui_functions
import values


class Page3(ui_functions.Topmenu):
    def __init__(self):
        super(Page3,self).__init__()

        self.img1_button.clicked.connect(self.img1_button_clicked)
        self.menuWidget.cellClicked.connect(self.menu_clicked)

    def setUI(self):
        super(Page3, self).setUI()
        self.setWindowTitle('main')
        self.recommend()

        self.layout.addLayout(self.recom_layout)

        self.layout.setSpacing(5)

    def img1_button_clicked(self):
        self.secondWindow = page6.Page6()
        self.secondWindow.show()
        self.close()

    def menu_clicked(self, row, col):
        data = self.menuWidget.item(row, col)
        if data.text() == '감정 선택':
            self.secondWindow = page2.Page2()
            self.secondWindow.show()
            self.close()
        elif data.text() == 'My':
            self.secondWindow = page4.Page4()
            self.secondWindow.show()
            self.close()

    def recommend(self):
        self.recom_layout = QVBoxLayout()

        self.recommend_text()
        self.recommend_img()

        self.recom_layout.addLayout(self.text_grid)
        self.recom_layout.addWidget(self.image_table, alignment=Qt.AlignCenter)
        self.recom_layout.setContentsMargins(0, 30, 0, 60)


    def recommend_text(self):
        self.text_grid = QHBoxLayout()

        text1 = QLabel(self)
        text1.setText("추천 작품")
        text1.setStyleSheet("color: white;"
                            "background: rgb(120,180,230);")
        text1.setFont(QFont(values.font, 15))

        text2 = QLabel(self)
        text2.setText("선택 해쉬태그:")
        text2.setStyleSheet("color: black;")
        text2.setFont(QFont(values.font, 15))

        text3 = QLabel(self)
        text3.setText("#가슴뭉클한 #용기있는")
        text3.setStyleSheet("color: rgb(100,150,200);")
        text3.setFont(QFont(values.font, 15))

        self.text_grid.addStretch(9)  # 숫자가 칸이아니라 비율임
        self.text_grid.addWidget(text1)
        self.text_grid.addStretch(1)
        self.text_grid.addWidget(text2)
        self.text_grid.addStretch(1)
        self.text_grid.addWidget(text3)
        self.text_grid.addStretch(50)

    def recommend_img(self):
        #추천 작품 table
        self.image_table = QTableWidget()
        self.image_table.setFixedSize(values.width * 0.8, values.height * 0.75)
        self.image_table.setRowCount(3)
        self.image_table.setColumnCount(3)
        self.image_table.setSpan(0,0,3,1)
        self.image_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.image_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.image_table.horizontalHeader().close()
        self.image_table.verticalHeader().close()

        #이미지 레이아웃
        self.img1_layout = QVBoxLayout()
        img1_text = QLabel()
        img1_text.setText("백범일지/S#5. 집 앞/윤봉길")
        img1_text.setFont(QFont(values.font, 13))
        img1 = QLabel(self)
        img1.setPixmap(QPixmap(values.img_path + values.page3_images[0]).scaledToWidth(values.width * 0.2))
        self.img1_layout.addStretch(5)
        self.img1_layout.addWidget(img1_text, alignment=Qt.AlignCenter)
        self.img1_layout.addStretch(1)
        self.img1_layout.addWidget(img1, alignment=Qt.AlignHCenter)
        self.img1_layout.addStretch(5)

        self.img2_layout = QVBoxLayout()
        img2_text = QLabel()
        img2_text.setText("백범일지/S#5. 집 앞/김구")
        img2_text.setFont(QFont(values.font, 13))
        img2 = QLabel(self)
        img2.setPixmap(QPixmap(values.img_path + values.page3_images[1]).scaledToWidth(values.width * 0.2))
        self.img2_layout.addWidget(img2_text, alignment=Qt.AlignCenter)
        self.img2_layout.addWidget(img2, alignment=Qt.AlignCenter)

        self.img3_layout = QVBoxLayout()
        img3_text = QLabel()
        img3_text.setText("사랑의집/S#4. 우리집/선생님")
        img3_text.setFont(QFont(values.font, 13))
        img3 = QLabel(self)
        img3.setPixmap(QPixmap(values.img_path + values.page3_images[2]).scaledToWidth(values.width * 0.2))
        self.img3_layout.addWidget(img3_text, alignment=Qt.AlignCenter)
        self.img3_layout.addWidget(img3, alignment=Qt.AlignCenter)

        self.img4_layout = QVBoxLayout()
        img4_text = QLabel()
        img4_text.setText("용기있는소년/S#5. 화이팅/올리버")
        img4_text.setFont(QFont(values.font, 13))
        img4 = QLabel(self)
        img4.setPixmap(QPixmap(values.img_path + values.page3_images[3]).scaledToWidth(values.width * 0.2))
        self.img4_layout.addWidget(img4_text, alignment=Qt.AlignCenter)
        self.img4_layout.addWidget(img4, alignment=Qt.AlignCenter)

        self.img5_layout = QVBoxLayout()
        img5_text = QLabel()
        img5_text.setText("이솝우화/S#2. 북풍과 태양/태양")
        img5_text.setFont(QFont(values.font, 13))
        img5 = QLabel(self)
        img5.setPixmap(QPixmap(values.img_path + values.page3_images[4]).scaledToWidth(values.width * 0.2))
        self.img5_layout.addWidget(img5_text, alignment=Qt.AlignCenter)
        self.img5_layout.addWidget(img5, alignment=Qt.AlignCenter)

        self.img6_layout = QVBoxLayout()
        img6_text = QLabel()
        img6_text.setText("은혜깊은 까치/S#2. 까치가 돌아왔다/까치")
        img6_text.setFont(QFont(values.font, 13))
        img6 = QLabel(self)
        img6.setPixmap(QPixmap(values.img_path + values.page3_images[5]).scaledToWidth(values.width * 0.2))
        self.img6_layout.addWidget(img6_text, alignment=Qt.AlignCenter)
        self.img6_layout.addWidget(img6, alignment=Qt.AlignCenter)

        self.img7_layout = QVBoxLayout()
        img7_text = QLabel()
        img7_text.setText("모아나/S#2. 테피티의 심장/모아나")
        img7_text.setFont(QFont(values.font, 13))
        img7 = QLabel(self)
        img7.setPixmap(QPixmap(values.img_path + values.page3_images[6]).scaledToWidth(values.width * 0.2))
        self.img7_layout.addWidget(img7_text, alignment=Qt.AlignCenter)
        self.img7_layout.addWidget(img7, alignment=Qt.AlignCenter)

        #이미지 버튼
        self.img1_button = QPushButton()
        self.img1_button.setStyleSheet('border-radius:1px;')
        self.img1_button.setLayout(self.img1_layout)

        img2_button = QPushButton()
        img2_button.setStyleSheet('border-radius:1px')
        img2_button.setLayout(self.img2_layout)

        img3_button = QPushButton()
        img3_button.setStyleSheet('border-radius:1px')
        img3_button.setLayout(self.img3_layout)

        img4_button = QPushButton()
        img4_button.setStyleSheet('border-radius:1px')
        img4_button.setLayout(self.img4_layout)

        img5_button = QPushButton()
        img5_button.setStyleSheet('border-radius:1px')
        img5_button.setLayout(self.img5_layout)

        img6_button = QPushButton()
        img6_button.setStyleSheet('border-radius:1px')
        img6_button.setLayout(self.img6_layout)

        img7_button = QPushButton()
        img7_button.setStyleSheet('border-radius:1px')
        img7_button.setLayout(self.img7_layout)

        # 추천 작품 table에 넣기
        self.image_table.setCellWidget(0, 0, self.img1_button)
        self.image_table.setCellWidget(0, 1, img2_button)
        self.image_table.setCellWidget(0, 2, img3_button)
        self.image_table.setCellWidget(1, 1, img4_button)
        self.image_table.setCellWidget(1, 2, img5_button)
        self.image_table.setCellWidget(2, 1, img6_button)
        self.image_table.setCellWidget(2, 2, img7_button)

    def menu(self):
        super(Page3, self).menu()
        self.menuWidget.setItem(0, 2, QTableWidgetItem("감정 선택"))
        self.menuWidget.setItem(0, 0, QTableWidgetItem("My"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = Page3()
    mywindow.show()
    app.exec_()