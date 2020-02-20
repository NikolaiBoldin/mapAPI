import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

SCREEN_SIZE = [600, 450]


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('widget.ui', self)

        self.api_server = "http://static-maps.yandex.ru/1.x/"

        lon = "179"
        lat = "55.703118"

        self.params = {
            "ll": ",".join([lon, lat]),
            "size": "650,450",
            "l": "map",
            "z": "10"

        }

        self.initUI()

        self.comboBox.addItems(["Схема", "Спутник", "Гибрид"])
        self.comboBox.activated[str].connect(self.onChanged)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.params['ll'] = ",".join([self.ll0.text(), self.ll1.text()])
        self.params['z'] = str(self.zoom.value())
        self.getImage()

    def getImage(self):
        response = requests.get(self.api_server, params=self.params)

        # Запишем полученное изображение в файл.
        with open(self.map_file, "wb") as file:
            file.write(response.content)
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)

    def initUI(self):
        # self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setFixedSize(770, 770)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.map_file = "map.png"

        self.image = QLabel(self)
        self.image.move(10, 310)
        self.image.resize(650, 450)

        self.getImage()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def onChanged(self, text):
        print(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
