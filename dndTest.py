from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPainter, QPen, QDropEvent
import sys

class Button(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.setAcceptDrops(True)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if e.button() == Qt.LeftButton:
            print('Press')


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        self.button1 = Button('K1', self)
        self.button1.resize(20,40)
        self.button1.move(620, 40)

        self.button2 = Button('K2', self)
        self.button2.resize(20, 40)
        self.button2.move(635, 40)

        self.button2 = Button('K3', self)
        self.button2.resize(20, 40)
        self.button2.move(650, 40)

        self.button2 = Button('K4', self)
        self.button2.resize(20, 40)
        self.button2.move(665, 40)

        self.label = QLabel('Pozycja klem: ', self)
        self.label.resize(500, 20)
        #self.label.setAlignment(Qt.AlignCenter)
        self.label.move(100, 100)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 200, 280, 150)
        self.resize(700, 160)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        self.setAcceptDrops(True)

        position = e.pos()
        print(e.source())

        point = e.pos()
        point.setX(e.pos().x()-10) # Move to the center of square
        point.setY(80-40) # 100 - wysokość buttona

        if point.x() < 10:
            point.setX(10)
        if point.x() > 610:
            point.setX(610)

        self.label.setText(self.label.text() + str(e.source().text() +': '+ str(point.x() - 10)) + ', ')
        e.source().move(point.x(), point.y())

        e.setDropAction(Qt.MoveAction)
        e.accept()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(20, 60, 610, 60)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()