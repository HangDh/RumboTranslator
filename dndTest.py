from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QLabel, QLineEdit, QFileDialog, QTextEdit, QGraphicsView
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPainter, QPen, QFont, QPixmap
import datetime
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

    # Zdefiniowanie drag'n'dropa - bez drop Action? ;) - dropAction do usuniecia
    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)

# Pierwsze uruchomienie programu to zawsze klemy na 0 + arrBars - lista belek z cutsami - jako pusta lista
global klemy, arrBars
# -9999 dla rumby nowszej, brak wartosci dla drugiej
klemy = ['-9999', '-9999', '-9999', '-9999']
arrBars = []

def evaluateMathGeometry(arrayToChange, valueParam):
    for i, s in enumerate(arrayToChange):
        if type(arrayToChange[i]) == str:
            arrayToChange[i] = arrayToChange[i].replace('H', str(valueParam)).split(' ')
            sum = 0.0
            for part in arrayToChange[i]:
                sum += float(part)
            arrayToChange[i] = sum
    return arrayToChange

''' Funkcja wykorzystywana w celu pozyskania narzędzia posiadajacego najwieksza mozliwa
srednice do wykonania danego makra na podstawie rozmiaru makra'''
def getProperTool(macroDia, depth):
    with open('frez.json') as f:
        frezLib = json.load(f)
        choice = '0'
        for k, v in frezLib.items():
            if int(v['diameter']) == macroDia:
                if int(v['worklength']) >= depth:
                    return k
            if int(v['diameter']) < macroDia:
                if int(v['worklength']) >= depth:
                    if choice == '0':
                        choice = k
                    if int(v['diameter']) > int(frezLib[choice]['diameter']):
                        choice = k
        return choice

class Example(QWidget):
    # Makra - pusta lista, obecny profil to profil - potem nadamy mu właściwości
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

        # Przycisk resetu klem i zadań
        resetBtn = QPushButton('RESET', self)
        resetBtn.move(650, 150)
        resetBtn.clicked.connect(self.clampsReset)

        #Tutaj zaczyna się spis klem jako buttonow
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
        # Tutaj konczy się spis klem jako buttonow

        # Tutaj zaczynaja się textboxy z pozycjami klem
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
        # Tutaj kończą się textboxy z pozycjami klem

        self.labelZlec = QLabel('', self)
        self.labelZlec.resize(150, 20)
        self.labelZlec.move(400, 30)

        self.label = QLabel('Pozycja klem: ', self)
        self.label.resize(500, 20)
        self.label.move(130, 135)

        # Labele z nazwami makr - czy to C, O, W, M - literki od Cornerów, Odwodnień itp.
        self.macrosVis = []
        for i in range(20):
            self.macrosVis.append(QLabel('', self))

        # Miejsce do wpisania lub zeskanowania kodu
        self.textbox = QLineEdit('Wpisz numer/nazwe profilu', self)
        self.textbox.resize(150, 20)
        self.textbox.move(100, 30)

        # Tutaj znajdują się informacje o makrach, które będą wykonywane na danej belce.
        self.textBoxMacro = QTextEdit(self)
        self.textBoxMacro.resize(400, 230)
        self.textBoxMacro.move(20, 250)

        # ImageView - podgląd profilu
        self.imageView = QLabel(self)
        self.imageView.setAlignment(Qt.AlignCenter)
        self.imageView.resize(320, 230)
        self.imageView.move(460, 250)

        # Ogólne okno programu - RUMBOMINATOR
        self.setWindowTitle('Rumbominator 2018')
        self.setGeometry(300, 200, 280, 150)
        self.resize(800, 500)

    # Poruszkanie klemami - informacje na temat przemieszczeń z pola.
    def moveClampK1(self):
        try:
            length = self.currentProfil.Length
            # Ustal pozycje w X - weź pod uwagę długość profila
            flPosX = int(int(self.textboxK1.text())*500/length) + 45
            # Skalowanie wielkości klemy i ustawienie pozycji oraz rozmiaru.
            self.button1.setGeometry(flPosX+10, 80, 120*500/length, 40)
            # Zmień wartość w liscie (do poźniejszego zapisu do pliku)
            klemy[0] = int(self.textboxK1.text())
        except:
            print('ERROR')

    # J/W - klema K2
    def moveClampK2(self):
        try:
            length = self.currentProfil.Length
            flPosX = int(int(self.textboxK2.text())*500/length) + 45
            self.button2.setGeometry(flPosX+10, 80, 120*500/length, 40)
            klemy[1] = int(self.textboxK2.text())
        except:
            print('ERROR')

    # J/W - klema K3
    def moveClampK3(self):
        try:
            length = self.currentProfil.Length
            flPosX = int(int(self.textboxK3.text())*500/length) + 45
            self.button3.setGeometry(flPosX+20, 80, 120*500/length, 40)
            klemy[2] = int(self.textboxK3.text())
        except:
            print('ERROR')

    # J/W - klema K4
    def moveClampK4(self):
        try:
            length = self.currentProfil.Length
            flPosX = int(int(self.textboxK4.text())*500/length) + 45
            self.button4.setGeometry(flPosX+20, 80, 120*500/length, 40)
            klemy[3] = int(self.textboxK4.text())
        except:
            print('ERROR')

    # Początek drag and dropa - zaakceptowanie - pozwolenie na event.
    def dragEnterEvent(self, e):
        e.accept()

    # Drop - czyli po zakończeniu Drag.
    def dropEvent(self, e):
        self.setAcceptDrops(True)

        # Ustawianie klemy w pozycji na którą przesuwamy
        length = self.currentProfil.Length
        point = e.pos()
        point.setX(e.pos().x()+2)  # Klema jest z boku kursura (z boku miarki też)
        point.setY(80)  # 100 - wysokość buttona

        pointXStr = str(((point.x()-50)*length)/500)

        # Jeżeli przesuwamy sie za bardzo na lewo/prawo (za granice) - to przesun kleme na koniec profilu
        if point.x() < 50:
            point.setX(40)
            pointXStr = str(0)
        if point.x() > 550:
            point.setX(540)
            pointXStr = str(length)

        # Przesuwanie klem - ustawia na tekst-pozycje (setText) w odpowiednim boxie (dla K1,K2...)
        klemy[int(e.source().text()[1:])-1] = pointXStr
        if e.source().text()[1:] == '1':
            self.textboxK1.setText(pointXStr)
        if e.source().text()[1:] == '2':
            self.textboxK2.setText(pointXStr)
        if e.source().text()[1:] == '3':
            self.textboxK3.setText(pointXStr)
        if e.source().text()[1:] == '4':
            self.textboxK4.setText(pointXStr)

        # Przesuń i ustaw nową geometrie (weź pod uwagę długość profila!)
        e.source().move(point.x(), point.y())
        e.source().setGeometry(point.x(), point.y(), 120*500/length, 40)

        e.setDropAction(Qt.MoveAction)
        e.accept()

    # Ustalenie nowej czcionki (pogrubienie, większa czcionka - dla oznaczeń makr?)
    myFont = QFont()
    myFont.setBold(True)
    myFont.setPixelSize(14)

    def readProfil(self):
        # Definicja frezów i makr - Została zastąpiona przez definicję w JSON
        global macros, currentProfil, macroLib, frezLib

        # Definicje makr (JSON)
        with open("macro.json", "r", encoding='utf-8') as f:
            macroLib = json.load(f)
        # Definicje frezów (JSON)
        with open("frez.json", "r") as f:
            frezLib = json.load(f)

        # Wpisz nazwe profilu to początkowy string pola 'textbox' - po zmianie odpalamy funkcje.
        if self.textbox.text() != 'Wpisz nazwę profilu':
            # Dodaj 20 makr (bo raczej więcej nie będzie - wyświetl na belce) - zainicjowanie.
            # Inaczej nie dało się później zmieniać koloru, pozycji itp
            for i in range(20):
                self.macrosVis[i].setText('')
            # Iteracja wzdłuż barów, Cutów
            for bar in arrBars:
                for cut in bar.barCuts:
                    # Jeżeli uda sie znaleźć cutDescription lub cutNumber we wpisanym polu - to.
                    if cut.cutDescription == self.textbox.text() or cut.cutNumber == self.textbox.text()[7:12] or cut.cutNumber == self.textbox.text():
                        self.label.setText('')
                        self.textBoxMacro.setText('')
                        self.textBoxMacro.append('Belka: ' + cut.cutDescription + ', Długość: ' + str(cut.cutLength) + ', Profil: ' + bar.barProfil + '\n')
                        macros = cut.cutMacros  # wybór belki
                        sides = []
                        for m in macros:
                            # Ponieważ BJM miał dwa makra pod odwodnienie, to jedno z nich po prostu usuwamy
                            if m.Ident == 'Drain for Frame - hidden d BJM machining 4035':
                                macros.remove(m)

                            for work in m.macroWorks:
                                if work.workSide == '7':
                                    work.workSide = '1'
                                m.Side = work.workSide
                                sides.append(work.workSide)

                        if len(set(sides)) > 1:
                            self.textBoxMacro.append('KONIECZNE ROTACJE/KULANIE PROFILEM!')

                        # Dopisujemy właściwości do obecnego profilu - informacje czerpiac z bara (plik ncx)
                        self.currentProfil = Profil(bar.barProfil, bar.barWidth, bar.barHeight, cut.cutLength)
                        # Wczytaj obrazek z bar profilem
                        self.imageView.setPixmap(QPixmap(".\\profile\\"+bar.barProfil+'_'+sides[0]+".png"))

                        for macro in macros:  # Przypisanie wartości z JSONA do właściwości obiektu
                            try:
                                macro.Description = macroLib[macro.Ident]['description']
                            except:
                                macro.Description = macro.Ident

                        midx = 0
                        macrosSorted = copy.copy(macros)
                        macrosSorted.sort(key=lambda x: x.WX)
                        # Dla uszeregowanych makr - dodaj opisy w boxie, dodaj ich polozenie na belce, pokoloruj na czerwono ;)
                        for m in macrosSorted:
                            self.textBoxMacro.append('Opis: ' + m.Description + ' PosX: ' + str(m.WX))
                            self.macrosVis[midx].resize(20,40)
                            self.macrosVis[midx].move((46+m.WX*500/self.currentProfil.Length), 80)
                            self.macrosVis[midx].setStyleSheet('color: red')
                            self.macrosVis[midx].setFont(self.myFont)
                            # Odwodnienie - O, Corner - C, inne - M (montażowe)
                            if '4034' in m.Ident or 'HIDDEN' in m.Ident:
                                self.macrosVis[midx].setText('O')
                            elif 'corner' in m.Ident:
                                self.macrosVis[midx].setText('C')
                            else:
                                self.macrosVis[midx].setText('M')
                            midx += 1
            try:
                # Jeszcze raz dla pewności usuwamy makro 4035 ?
                for index, macro in enumerate(macros):
                    if macro.Ident == 'Drain for Frame - hidden d BJM machining 4035':
                        macros.remove(macro)
                        break
                else:
                    index = -1
            except:
                self.label.setText('Nie odnaleziono podanej belki w zleceniu')
            self.textbox.setFocus(True)
            if len(self.textbox.text()) == 5 or len(self.textbox.text()) == 11:
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
        global inc
        inc = 8  # Zaczynam od 8 linijki - 80

        ''' Stały cig znaków oznaczajcy zmiane narzędzia - konieczne każdorazowe wpisanie w celu poprawnego działania
        maszyn - Rumb '''
        def zmianaNarzedzia(frez, predkosc, fileIn, inc, kat_lozaIn):
            writeInc(fileIn, str(inc * 10) + ';97;6;;1;' + str(frez) + ';4;' + str(predkosc) + ';;\n')
            inc += 1
            writeInc(fileIn, str(inc * 10) + ';0;;Z;;24.00;;;;\n')
            inc += 1
            writeInc(fileIn, str(inc * 10) + ';0;;Y;;16.50;;;;\n')
            inc += 1
            writeInc(fileIn, str(inc * 10) + ';97;10;;' + str(kat_lozaIn) + ';;;;;\n')  # Kąt łoża i obrót
            inc += 1
            writeInc(fileIn, str(inc * 10) + ';97;4;;1;' + str(predkosc) + ';;;;\n')

        def writeInc(plik, tekst):
            plik.write(tekst)
            global inc
            inc += 1

        logFile = open('time.log', 'a')
        logFile.write(self.labelZlec.text() + ' - ' + self.textbox.text() + ' - ' + str(datetime.datetime.now()) + '\n')
        logFile.close()

        file = open(self.textbox.text()+'.txt', 'w')

        #  Definicja zmiennych dla parametrów maszyny ##
        global Delta_X, Delta_Y, Delta_Z, Odsuniecie_Y, kat_loza
        Delta_X = 59.5
        Delta_Y = -78.5
        Delta_Z = -272.8
        Odsuniecie_Y = 15.5
        Disengage_Z = 95.92
        kat_loza = 0.00

        ''' Zmiana kata - kolejny raz potrzebna jest całościowa funkcja, kilka linijek
        które wykonywane sa przez maszyne w przypadku zmiany kata obróbki '''
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

            Delta_Z = round(Okrag_Z + math.sin(katKoncowy) * Okrag_R, 2)
            Delta_Y = round(Okrag_Y + math.cos(katKoncowy) * Okrag_R, 2)

        for m in macros:
            # Iteracja poprzez worki w makrze
            diameterList = []
            depthList = []
            for work in m.macroWorks:
                diameterList.append(int(work.workWW1))
                depthList.append(int(work.workD2))
                m.Angle = work.workAngle

            for work in m.macroWorks:
                minDia = min(diameterList)
                maxDepth = max(depthList)
                nrFreza = getProperTool(minDia, maxDepth)
                if nrFreza == '0':
                    m.Tool = getProperTool(work.workWW1, work.workD2)
                m.Tool = nrFreza

        macrosSortedWX = copy.copy(macros)
        macros.sort(key=lambda x: x.WX)
        macros.sort(key=lambda x: x.Tool, reverse=True)  # posortuj po narzędziu
        macrosSortedWX.sort(key=lambda x: x.WX)

        m_prev = 0
        distanceList = []

        for m in range(0, len(macrosSortedWX)):
            distanceList.append(macrosSortedWX[m].WX - m_prev)
            m_prev = macrosSortedWX[m].WX
            if (m == len(macrosSortedWX) - 1):
                distanceList.append(self.currentProfil.Length - macrosSortedWX[m].WX)

        ### BLOK STAŁY STARTOWY ###
        file.write('10;97;80;;;;;;;\n' + '20;97;15;;;;;;;\n' + '30;97;99;;' + klemy[0] + ';' + klemy[1] + ';' + klemy[2] + ';' + klemy[
            3] + ';;\n')  # Pozycja klem - ustawiam na puste
        file.write('40;0;;Z;;24.00;;;;\n' + '50;0;;Y;;16.50;;;;\n' + '60;97;10;;0.00;;;;;\n' + '70;28;;XY;;;;;;\n')
        ### KONIEC BLOKU STAŁEGO RUMBA 1 ###

        frezPoprzedni = 0
        obrotPoprzedni = 0.0

        curProfil = Profil(arrBars[1].barProfil, arrBars[1].barWidth, arrBars[1].barHeight, arrBars[1].barLength)

        for macro in macros:
            workNr = 1
            obrot = macro.Angle  # Do sprawdzenia pozniej - poki co wykonujemy makra bez obracania łożem.

            Disengage_Z = ncfunctions.findNearest(obrot, self.currentProfil.Height)
            wysDisengage = Delta_Z + frezLib[macro.Tool]['length'] + Disengage_Z

            if (obrotPoprzedni != obrot):
                zmianaKata(obrot)
            else:
                if workNr > 1:
                    writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round(wysDisengage, 2)) + ';;;;\n')

            XPos, YPos, ZPosStart, ZPosEnd = '', '', '', ''

            for work in macro.macroWorks:
                frezWybrany = frezLib[macro.Tool]

                if (frezPoprzedni != frezWybrany):
                    zmianaNarzedzia(macro.Tool, frezWybrany['speed'], file, inc, kat_loza)

                # Blok ustawienia odpowiednich wartości X,Y,Z dla obróbki
                if work.workWW1 > frezWybrany['diameter'] and work.workType != 'C' and work.workType != 'R':
                    YPos = Delta_Y - Odsuniecie_Y - work.workWY + (work.workWW1 - frezWybrany['diameter']) / 2
                else:
                    YPos = Delta_Y - Odsuniecie_Y - work.workWY

                if work.workWW2 > frezWybrany['diameter'] and work.workType != 'C' and work.workType != 'R':
                    XPos = Delta_X + macro.WX + work.workWX - work.workWW2 / 2 + frezWybrany['diameter'] / 2
                else:
                    XPos = Delta_X + macro.WX + work.workWX
                # Blok ustawiania zakończony

                # Inne zachowanie dla pierwszego worka z Makro?
                if workNr == 1:
                    enterPos = wysDisengage
                else:
                    enterPos = ZPosEnd

                # W zależności od tego który side to rożne brane approach?
                if work.workSide == '1' or work.workSide == '6':
                    approach = float(curProfil.Height)
                else:
                    approach = float(curProfil.Width)

                ZPosStart = Delta_Z + frezWybrany['length'] + (approach - work.workD1)  # do sprawdzenia czy workHeight czy hardcodowac 2.0
                ZPosEnd = Delta_Z + frezWybrany['length'] + (approach - work.workD2)
                holeDiff = (work.workWW1 - frezWybrany['diameter']) / 2

                if work.workType == 'R':
                    writeInc(file, str(inc * 10) + ';0;;XYZ;;' + str(round(XPos - (work.workWW1 - frezWybrany['diameter'])/ 2, 2)) + ';' +
                             str(round(YPos + (work.workWW2 - frezWybrany['diameter']) / 2, 2)) + ';' + str(round(enterPos, 2)) + ';;\n')
                else:
                    YPos = round((Delta_Y - Odsuniecie_Y - work.workWY + (work.workWW2 - frezWybrany['diameter']) / 2), 2)
                    XPos = round((Delta_X + work.workWX + (work.workWW1 - frezWybrany['diameter']) / 2), 2)
                    writeInc(file, str(inc * 10) + ';0;;XYZ;;' + str(XPos) + ';' + str(YPos) + ';' + str(round(enterPos, 2)) + ';;\n')

                writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round(ZPosStart, 2)) + ';;;;\n')
                writeInc(file, str(inc * 10) + ';97;7;;2;;;;;\n')  # Zagadka - co powoduje ta linijka, czy możemy ją jakoś wyselekcjonować.
                writeInc(file, str(inc * 10) + ';97;11;;;;;;;\n')
                writeInc(file, str(inc * 10) + ';1;;Z;200;' + str(round(ZPosEnd, 2)) + ';;;;\n')  # Praca w osi Z, zejście

                if work.workType == 'R':
                    if work.workAngle == 0:
                        writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
                        writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(XPos + (work.workWW1 - frezWybrany['diameter']) / 2) + ';' +
                                 str(YPos + (work.workWW2 - frezWybrany['diameter']) / 2) + ';;;\n')
                        writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(XPos + (work.workWW1 - frezWybrany['diameter']) / 2) + ';' +
                                 str(YPos - (work.workWW2 - frezWybrany['diameter']) / 2) + ';;;\n')
                        writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(XPos - (work.workWW1 - frezWybrany['diameter']) / 2) + ';' +
                                 str(YPos - (work.workWW2 - frezWybrany['diameter']) / 2) + ';;;\n')
                        writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(XPos - (work.workWW1 - frezWybrany['diameter']) / 2) + ';' +
                                 str(YPos + (work.workWW2 - frezWybrany['diameter']) / 2) + ';;;\n')

                if work.workType == 'L':
                    if work.workAngle == 0:
                        YPos = round((Delta_Y - Odsuniecie_Y - work.workWY + (work.workWW2 - frezWybrany['diameter']) / 2), 2)
                        writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
                        writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(XPos) + ';' + str(YPos) + ';;;\n')
                    else:
                        XPos = round((Delta_X + work.workWX + (work.workWW1 - frezWybrany['diameter']) / 2), 2)
                        writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
                        writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(XPos) + ';' + str(YPos) + ';;;\n')

                if work.workType == 'C' and holeDiff > 0:
                    writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
                    writeInc(file, str(inc * 10) + ';2;;XY;800;' + str(XPos) + ';' + str(round(YPos - holeDiff, 2)) + ';' + str(XPos) + ';' + str(YPos) + ';\n')
                    writeInc(file, str(inc * 10) + ';2;;XY;800;' + str(XPos) + ';' + str(round(YPos + holeDiff, 2)) + ';' + str(XPos) + ';' + str(YPos) + ';\n')

                writeInc(file, str(inc * 10) + ';97;9;;;;;;;\n')

                # Cofanie się n a pozycje Z jest niepotrzebne - wydlużenie czasu obróbki - wyjatek kiedy maja inne Y
                if workNr < len(macro.macroWorks) - 1 and work.workWY != macro.macroWorks[workNr].workWY:
                    writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round(wysDisengage, 2)) + ';;;;\n')

                workNr += 1
                frezPoprzedni = frezWybrany
                obrotPoprzedni = obrot

        writeInc(file, str(inc * 10) + ';0;;Z;;24.00;;;;\n')
        # writeInc(file, str(inc * 10) + '0;;Y;;16.50;;;;\n')  #  w koncu ma byc czy nie?!
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