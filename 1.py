import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('widget.ui', self)

        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.lon = "0"
        self.lat = "0"
        self.params = {
            "ll": ",".join([self.lon, self.lat]),
            "size": "650,450",
            "l": "map",
            "z": "1"
        }

        self.initUI()

        self.comboBox.addItems(["Схема", "Спутник", "Гибрид"])
        self.types = {"Схема": 'map', "Спутник": 'sat', "Гибрид": 'sat,skl'}

        self.comboBox.activated[str].connect(self.changed_type)
        self.ll0.textChanged.connect(self.changed_ll0)
        self.ll1.textChanged.connect(self.changed_ll1)
        self.zoom.textChanged.connect(self.changed_zoom)

    def changed_ll0(self):
        if self.ll0.text() == "":
            self.lon = '0'
        else:
            self.lon = self.ll0.text()
        self.params['ll'] = ",".join([self.lon, self.lat])
        self.set_image()

    def changed_ll1(self):
        if self.ll1.text() == "":
            self.lat = '0'
        else:
            self.lat = self.ll1.text()
        self.params['ll'] = ",".join([self.lon, self.lat])
        self.set_image()

    def changed_zoom(self):
        self.params['z'] = str(self.zoom.value())
        self.set_image()

    def changed_type(self, text):
        self.params['l'] = self.types[text]
        self.set_image()

    def set_image(self):
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

        self.set_image()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
