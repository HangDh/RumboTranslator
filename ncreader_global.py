import sys
from PyQt5.QtWidgets import QApplication
import dndTest


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = dndTest.Example()
    ex.show()
    app.exec_()

