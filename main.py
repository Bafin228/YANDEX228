import sys
import requests
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    SCALE_INITIAL = 0.002
    SCALE_FACTOR = 2
    SCALE_MIN = 0.000125
    SCALE_MAX = 65

    def __init__(self):
        super().__init__()
        self.scale = self.SCALE_INITIAL
        self.initUI()
        self.getImage()

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        params = {
            'll': '37.530887,55.703118',
            'spn': f'{self.scale},{self.scale}',
            'l': 'map'
        }
        response = requests.get(map_request, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.pixmap = QPixmap()
        self.pixmap.loadFromData(response.content)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        keys = {
            Qt.Key_PageUp, Qt.Key_PageDown,
        }
        if event.key() == Qt.Key_PageUp:
            self.scale /= self.SCALE_FACTOR
        elif event.key() == Qt.Key_PageDown:
            self.scale *= self.SCALE_FACTOR
        if self.scale > self.SCALE_MAX:
            self.scale = self.SCALE_MAX
        elif self.scale < self.SCALE_MIN:
            self.scale = self.SCALE_MIN
        if event.key() in keys:
            self.getImage()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
