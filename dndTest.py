from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPainter, QPen, QDropEvent
import sys

class Button(QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.setAcceptDrops(True)

    def mouseMoveEvent(self, e):

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        generateBtn = QPushButton('Generuj', self)
        generateBtn.move(270, 26)

        searchBtn = QPushButton('Wczytaj', self)
        searchBtn.move(575, 26)
        searchBtn.clicked.connect(self.openFileNameDialog)

        self.button1 = Button('K1', self)
        self.button1.resize(20,40)
        self.button1.move(620, 80)

        self.button2 = Button('K2', self)
        self.button2.resize(20, 40)
        self.button2.move(635, 80)

        self.button2 = Button('K3', self)
        self.button2.resize(20, 40)
        self.button2.move(650, 80)

        self.button2 = Button('K4', self)
        self.button2.resize(20, 40)
        self.button2.move(665, 80)

        self.textbox = QLineEdit('Wpisz nazwę profilu', self)
        self.textbox.resize(150, 20)
        self.textbox.move(100, 30)

        self.labelZlec = QLabel('', self)
        self.labelZlec.resize(150, 20)
        self.labelZlec.move(400, 30)

        self.label = QLabel('Pozycja klem: ', self)
        self.label.resize(500, 20)
        #self.label.setAlignment(Qt.AlignCenter)
        self.label.move(100, 140)

        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 200, 280, 150)
        self.resize(700, 220)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        self.setAcceptDrops(True)

        length = 1400

        point = e.pos()
        point.setX(e.pos().x()-10)  # Move to the center of square
        point.setY(80)  # 100 - wysokość buttona

        pointXStr = str(((point.x()-50)*length)/500)
        print(point.x())

        if point.x() < 50:
            point.setX(40)
            pointXStr = str(0)
        if point.x() > 550:
            point.setX(540)
            pointXStr = str(length)


        self.label.setText('Położenie: ' + str(e.source().text()) + ': ' + pointXStr + ', ')
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
        qp.drawLine(50, 100, 550, 100)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Wyszukaj plik *.NCX zlecenia", "",
                                                  "NCX files (*.ncx)", options=options)

        if fileName:
            print(fileName)
            self.labelZlec.setText(fileName)
            #x = self.xlsToCun(fileName)
            #time.sleep(1.0)
            #self.saveFileDialog(x)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()