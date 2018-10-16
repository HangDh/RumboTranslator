from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel, QLineEdit, QFileDialog, QTextEdit, QGraphicsView
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPainter, QPen, QFont, QPixmap
import json
import math
import sys
import copy

import ncfunctions
import ncloader

class Frez(object):
    Srednica = 0
    Dlugosc = 0.0
    Predkosc = 0

    def __init__(self, srednica, dlugosc, predkosc):
        self.Srednica = srednica
        self.Dlugosc = dlugosc
        self.Predkosc = predkosc

class Profil(object):
    Name = ''
    Width = 0.0
    Height = 0.0
    Length = 0.0

    def __init__(self, name, width, height, length):
        self.Name = name
        self.Width = width
        self.Height = height
        self.Length = length

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

global klemy, arrBars
klemy = ['-9999', '-9999', '-9999', '-9999']
arrBars = []

class Example(QWidget):

    macros, currentProfil = [], Profil

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

        generateBtn = QPushButton('Generuj', self)
        generateBtn.move(270, 26)
        generateBtn.clicked.connect(self.generateFile)

        searchBtn = QPushButton('Wczytaj', self)
        searchBtn.move(650, 25)
        searchBtn.clicked.connect(self.openFileNameDialog)

        resetBtn = QPushButton('RESET', self)
        resetBtn.move(650, 150)
        resetBtn.clicked.connect(self.clampsReset)

        self.button1 = Button('K1', self)
        self.button1.resize(20, 40)
        self.button1.move(600, 80)

        self.button2 = Button('K2', self)
        self.button2.resize(20, 40)
        self.button2.move(615, 80)

        self.button3 = Button('K3', self)
        self.button3.resize(20, 40)
        self.button3.move(630, 80)

        self.button4 = Button('K4', self)
        self.button4.resize(20, 40)
        self.button4.move(645, 80)

        self.textboxK1 = QLineEdit('', self)
        self.textboxK1.resize(55, 20)
        self.textboxK1.move(130, 170)
        self.textboxK1.textChanged.connect(self.moveClampK1)

        self.textboxK2 = QLineEdit('', self)
        self.textboxK2.resize(55, 20)
        self.textboxK2.move(230, 170)
        self.textboxK2.textChanged.connect(self.moveClampK2)

        self.textboxK3 = QLineEdit('', self)
        self.textboxK3.resize(55, 20)
        self.textboxK3.move(330, 170)
        self.textboxK3.textChanged.connect(self.moveClampK3)

        self.textboxK4 = QLineEdit('', self)
        self.textboxK4.resize(55, 20)
        self.textboxK4.move(430, 170)
        self.textboxK4.textChanged.connect(self.moveClampK4)

        self.labelZlec = QLabel('', self)
        self.labelZlec.resize(150, 20)
        self.labelZlec.move(400, 30)

        self.label = QLabel('Pozycja klem: ', self)
        self.label.resize(500, 20)
        self.label.move(130, 135)

        self.macrosVis = []
        for i in range(20):
            self.macrosVis.append(QLabel('', self))

        self.textbox = QLineEdit('Wpisz nazwę profilu', self)
        self.textbox.resize(150, 20)
        self.textbox.move(100, 30)

        self.textBoxMacro = QTextEdit(self)
        self.textBoxMacro.resize(400, 230)
        self.textBoxMacro.move(20, 250)

        self.imageView = QLabel(self)
        self.imageView.setAlignment(Qt.AlignCenter)
        self.imageView.resize(320, 230)
        self.imageView.move(460, 250)


        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 200, 280, 150)
        self.resize(800, 500)

    def moveClampK1(self, e):
        try:
            length = self.currentProfil.Length
            flPosX = int(int(self.textboxK1.text())*500/length) + 45
            self.button1.setGeometry(flPosX, 80, 20, 40)
            klemy[0] = int(self.textboxK1.text())
        except:
            print('ERROR')

    def moveClampK2(self, e):
        try:
            length = self.currentProfil.Length
            flPosX = int(int(self.textboxK2.text())*500/length) + 40
            self.button2.setGeometry(flPosX, 80, 20, 40)
            klemy[1] = int(self.textboxK2.text())
        except:
            print('ERROR')

    def moveClampK3(self, e):
        try:
            length = self.currentProfil.Length
            flPosX = int(int(self.textboxK3.text())*500/length) + 40
            self.button3.setGeometry(flPosX, 80, 20, 40)
            klemy[2] = int(self.textboxK3.text())
        except:
            print('ERROR')

    def moveClampK4(self, e):
        try:
            length = self.currentProfil.Length
            flPosX = int(int(self.textboxK4.text())*500/length) + 40
            self.button4.setGeometry(flPosX, 80, 20, 40)
            klemy[3] = int(self.textboxK4.text())
        except:
            print('ERROR')

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        self.setAcceptDrops(True)

        length = self.currentProfil.Length
        point = e.pos()
        point.setX(e.pos().x()-10)  # Move to the center of square
        point.setY(80)  # 100 - wysokość buttona

        pointXStr = str(((point.x()-50)*length)/500)

        if point.x() < 50:
            point.setX(40)
            pointXStr = str(0)
        if point.x() > 550:
            point.setX(540)
            pointXStr = str(length)

        klemy[int(e.source().text()[1:])-1] = pointXStr
        if e.source().text()[1:] == '1':
            self.textboxK1.setText(pointXStr)
        if e.source().text()[1:] == '2':
            self.textboxK2.setText(pointXStr)
        if e.source().text()[1:] == '3':
            self.textboxK3.setText(pointXStr)
        if e.source().text()[1:] == '4':
            self.textboxK4.setText(pointXStr)
        e.source().move(point.x(), point.y())

        e.setDropAction(Qt.MoveAction)
        e.accept()

    myFont = QFont()
    myFont.setBold(True)
    myFont.setPixelSize(14)

    def readProfil(self):
        # Definicja frezów i makr - Została zastąpiona przez definicję w JSON
        global macros, currentProfil, macroLib, frezLib

        with open("macro.json", "r", encoding='utf-8') as f:
            macroLib = json.load(f)
        with open("frez.json", "r") as f:
            frezLib = json.load(f)

        if self.textbox.text() != 'Wpisz nazwę profilu':
            for i in range(20):
                self.macrosVis[i].setText('')
            for bar in arrBars:
                for cut in bar.barCuts:
                    if cut.cutDescription == self.textbox.text() or cut.cutNumber == self.textbox.text()[7:12]:
                        self.label.setText('')
                        self.textBoxMacro.setText('')
                        self.textBoxMacro.append('Belka: ' + cut.cutDescription + ', Długość: ' + str(cut.cutLength) + ', Profil: ' + bar.barProfil + '\n')
                        macros = cut.cutMacros  # wybór belki
                        for m in macros:
                            if m.Ident == 'Drain for Frame - hidden d BJM machining 4035':
                                macros.remove(m)
                        self.currentProfil = Profil(bar.barProfil, bar.barWidth, bar.barHeight, cut.cutLength)

                        self.imageView.setPixmap(QPixmap(".\\profile\\"+bar.barProfil+".png"))

                        for macro in macros:  # Przypisanie wartości z JSONA do właściwości obiektu
                            macro.Obrot = macroLib[macro.Ident]['angle']
                            macro.Frez = macroLib[macro.Ident]['tool']
                            macro.Description = macroLib[macro.Ident]['description']
                            macro.Type = macroLib[macro.Ident]['type']
                            macro.Width = macroLib[macro.Ident]['width']
                            macro.Height = macroLib[macro.Ident]['height']
                            macro.Approach = macroLib[macro.Ident]['approach']
                            macro.End = macroLib[macro.Ident]['end']
                            macro.PosY = macroLib[macro.Ident]['posY']

                        midx = 0
                        macrosSorted = copy.copy(macros)
                        macrosSorted.sort(key=lambda x: x.WX)
                        for m in macrosSorted:
                            self.textBoxMacro.append('Opis: ' + m.Description + ' PosX: ' + str(m.WX))
                            self.macrosVis[midx].resize(20,40)
                            self.macrosVis[midx].move((46+m.WX*500/self.currentProfil.Length), 80)
                            self.macrosVis[midx].setStyleSheet('color: red')
                            self.macrosVis[midx].setFont(self.myFont)
                            if '4034' in m.Ident or 'HIDDEN' in m.Ident:
                                self.macrosVis[midx].setText('O')
                            elif 'corner' in m.Ident:
                                self.macrosVis[midx].setText('C')
                            else:
                                self.macrosVis[midx].setText('M')
                            midx += 1
            try:
                for index, macro in enumerate(macros):
                    if macro.Ident == 'Drain for Frame - hidden d BJM machining 4035':
                        macros.remove(macro)
                        break
                else:
                    index = -1
            except:
                self.label.setText('Nie odnaleziono podanej belki w zleceniu')
            self.textbox.setFocus(True)
            self.textbox.selectAll()

    def clampsReset(self):
        global klemy
        klemy = ['-9999', '-9999', '-9999', '-9999']
        self.label.setText('Położenie klem zostało zresetowane')
        self.button1.move(620, 80)
        self.button2.move(635, 80)
        self.button3.move(650, 80)
        self.button4.move(665, 80)
        self.textboxK1.setText('')
        self.textboxK2.setText('')
        self.textboxK3.setText('')
        self.textboxK4.setText('')
        for i in range(20):
            self.macrosVis[i].setText('')

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
        self.textbox.clear()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Wyszukaj plik *.NCX zlecenia", "",
                                                  "NCX files (*.ncx)", options=options)
        if fileName:
            print(fileName)
            self.labelZlec.setText(fileName)

            with open(self.labelZlec.text()) as f:
                global content
                content = f.read()
            global arrBars, inc
            arrBars = ncloader.load(content)

            self.textbox.textChanged.connect(self.readProfil)
            self.textbox.setFocus(True)

    def generateFile(self):
        inc = 8  # Zaczynam od 8 linijki - 80

        def zmianaNarzedzia(frez, predkosc, file, inc, kat_loza):
            writeInc(file, str(inc * 10) + ';97;6;;1;' + str(frez) + ';4;' + str(predkosc) + ';;\n')
            inc += 1
            writeInc(file, str(inc * 10) + ';0;;Z;;24.00;;;;\n')
            inc += 1
            writeInc(file, str(inc * 10) + ';0;;Y;;16.50;;;;\n')
            inc += 1
            writeInc(file, str(inc * 10) + ';97;10;;' + str(kat_loza) + ';;;;;\n')  # Kąt łoża i obrót
            inc += 1
            writeInc(file, str(inc * 10) + ';97;4;;1;' + str(predkosc) + ';;;;\n')

        def writeInc(plik, tekst):
            plik.write(tekst)
            global inc
            inc += 1

        file = open(self.textbox.text()+'.txt', 'w')

        #  Definicja zmiennych dla parametrów maszyny ##
        global Delta_X, Delta_Y, Delta_Z, Odsuniecie_Y, kat_loza
        Delta_X = 59.5
        Delta_Y = -78.5
        Delta_Z = -272.8
        Odsuniecie_Y = 15.5
        Disengage_Z = 95.92
        kat_loza = 0.00

        def zmianaKata(kat):
            global Delta_Y, Delta_Z
            Okrag_Y = -175.375
            Okrag_Z = -331.15
            Okrag_R = 113.09
            katPierwotny = 31.06
            katKoncowy = math.radians(katPierwotny + kat)

            # Przy pierwszej zmianie kąta wpisywane są te linijki - nie jestesmy pewni dlaczego
            # Dlatego na wszelki wypadek dopisujemy.
            if Delta_Y != round(Okrag_Y + math.cos(katKoncowy) * Okrag_R, 2):
                writeInc(file, str(inc * 10) + ';0;;Z;;24.00;;;;\n')
                writeInc(file, str(inc * 10) + ';0;;Y;;16.50;;;;\n')
                writeInc(file, str(inc * 10) + ';0;;Z;;24.00;;;;\n')
                writeInc(file, str(inc * 10) + ';0;;Y;;16.50;;;;\n')
                writeInc(file, str(inc * 10) + ';0;;Z;;24.00;;;;\n')
                writeInc(file, str(inc * 10) + ';0;;Y;;16.50;;;;\n')
                # Funkcja przygotowawcza kąta
                writeInc(file, str(inc * 10) + ';97;10;;' + str(round(-kat, 2)) + ';;;;;\n')

            Delta_Y = round(Okrag_Y + math.cos(katKoncowy) * Okrag_R, 2)
            Delta_Z = round(Okrag_Z + math.sin(katKoncowy) * Okrag_R, 2)

        macrosSortedWX = copy.copy(macros)
        macros.sort(key=lambda x: x.WX)
        macrosSortedWX.sort(key=lambda x: x.WX)
        macros.sort(key=lambda x: x.Obrot)  # posortuj po obrocie
        macros.sort(key=lambda x: x.Frez, reverse=True)  # posortuj po narzędziu

        m_prev = 0
        distanceList = []

        for m in range(0, len(macrosSortedWX)):
            distanceList.append(macrosSortedWX[m].WX - m_prev)
            m_prev = macrosSortedWX[m].WX
            if (m == len(macrosSortedWX) - 1):
                distanceList.append(currentProfil.Length - macrosSortedWX[m].WX)

        for d in distanceList:
            if (currentProfil.Length > 1500):
                for i in range(int(d) // 20):
                    print('-', end='')
            else:
                for i in range(int(d) // 10):
                    print('-', end='')
        print('|\n')

        ### BLOK STAŁY STARTOWY ###
        file.write('10;97;80;;;;;;;\n' + '20;97;15;;;;;;;\n' + '30;97;99;;' + klemy[0] + ';' + klemy[1] + ';' + klemy[2] + ';' + klemy[
            3] + ';;\n')  # Pozycja klem - ustawiam na puste
        file.write('40;0;;Z;;24.00;;;;\n' + '50;0;;Y;;16.50;;;;\n' + '60;97;10;;0.00;;;;;\n' + '70;28;;XY;;;;;;\n')
        ### KONIEC BLOKU STAŁEGO RUMBA 1 ###

        frezPoprzedni = 0
        obrotPoprzedni = -1
        for macro in macros:
            frezWybrany = frezLib[str(macro.Frez[0])]
            obrot = macro.Obrot
            if (obrotPoprzedni != obrot):
                zmianaKata(macro.Obrot)

            Disengage_Z = ncfunctions.findNearest(macro.Obrot)
            wysDisengage = Delta_Z + frezWybrany['length'] + Disengage_Z

            if (obrotPoprzedni == obrot):
                writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round(wysDisengage, 2)) + ';;;;\n')

            if (frezPoprzedni != frezWybrany):
                zmianaNarzedzia(macro.Frez[0], frezWybrany['speed'], file, inc, kat_loza)

            XPos, YPos, ZPosStart, ZPosEnd = '', '', '', ''
            for i in range(len(macro.Approach)):
                # Blok ustawiania odpowiednich wartości X, Y, Z
                if (macro.Height[i] > frezWybrany['diameter'] and macro.Type != 'Hole'):
                    YPos = Delta_Y - Odsuniecie_Y - macro.PosY[i] + (macro.Height[i] - frezWybrany['diameter']) / 2
                else:
                    YPos = Delta_Y - Odsuniecie_Y - macro.PosY[i]

                if macro.Width[i] > frezWybrany['diameter'] and macro.Type != 'Hole':
                    XPos = Delta_X + macro.WX - macro.Width[i] / 2 + frezWybrany['diameter'] / 2
                else:
                    XPos = Delta_X + macro.WX
                # Oznaczenie wartości X, Y, Z zakończone

                # Inne zachowanie dla pierwszego wjazdu niż kolejnych
                if i == 0:
                    enterPos = wysDisengage
                elif macro.Approach[i] != macro.Approach[i - 1]:
                    enterPos = ZPosEnd  # końcówka poprzedniej obróbki!

                ZPosStart = Delta_Z + frezWybrany['length'] - macro.Approach[i]
                ZPosEnd = Delta_Z + frezWybrany['length'] - macro.End[i]

                writeInc(file, str(inc * 10) + ';0;;XYZ;;' + str(XPos) + ';' + str(YPos) + ';' + str(round(enterPos, 2)) + ';;\n')
                writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round(ZPosStart, 2)) + ';;;;\n')
                writeInc(file, str(inc * 10) + ';97;7;;2;;;;;\n')
                writeInc(file, str(inc * 10) + ';97;11;;;;;;;\n')
                writeInc(file, str(inc * 10) + ';1;;Z;200;' + str(round(ZPosEnd, 2)) + ';;;;\n')  # Praca w osi Z, zejście
                holeDiff = (macro.Height[i] - frezWybrany['diameter']) / 2

                if macro.Type == 'Slot':
                    XPos = Delta_X + macro.WX + macro.Width[i] / 2 - frezWybrany['diameter'] / 2
                    writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
                    writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(XPos) + ';' + str(YPos) + ';;;\n')
                if macro.Type == 'Hole' and holeDiff > 0:
                    writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
                    writeInc(file, str(inc * 10) + ';2;;XY;800;' + str(XPos) + ';' + str(YPos - holeDiff) + ';' + str(XPos) + ';' + str(YPos) + ';\n')
                    writeInc(file, str(inc * 10) + ';2;;XY;800;' + str(XPos) + ';' + str(YPos + holeDiff) + ';' + str(XPos) + ';' + str(YPos) + ';\n')

                writeInc(file, str(inc * 10) + ';97;9;;;;;;;\n')

                # Cofanie się n a pozycje Z jest niepotrzebne - wydlużenie czasu obróbki.
                # if i < len(macro.Approach) - 1:
                #    writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round(ZPosEnd, 2)) + ';;;;\n')

            frezPoprzedni = frezWybrany
            obrotPoprzedni = obrot

        writeInc(file, str(inc * 10) + ';0;;Z;;24.00;;;;\n')
        writeInc(file, str(inc * 10) + ';97;5;;;;;;;\n')
        writeInc(file, str(inc * 10) + ';97;50;;;;;;;\n')
        writeInc(file, str(inc * 10) + ';97;80;;;;;;;\n')
        writeInc(file, str(inc * 10) + ';97;15;;;;;;;\n')

        print('Plik wygenerowany pomyślnie!')
        file.close()
        self.textbox.clear()
        self.textbox.setFocus(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()