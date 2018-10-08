import copy
import os
import math
import ncloader

zlecenia_pliki = []
for file in os.listdir("."):
    if file.endswith(".NCX"):
        zlecenia_pliki.append(file)

print("Dostępne pliki: " + str(zlecenia_pliki) + "\n")

orderFilename = input('Podaj numer zlecenia z powyższej listy (bez .NCX!)')

with open(orderFilename+'.NCX') as f:
    content = f.read()


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

file = open('testfile.txt', 'w')

## Definicja zmiennych dla parametrów maszyny ##
Delta_X = 59.5
Delta_Y = -78.5
Odsuniecie_Y = 15.5

Delta_Z = -272.8
Disengage_Z = 95.92

kat_loza = 0.00
##

def writeInc(plik, tekst):
    plik.write(tekst)
    global i
    i += 1


def zmianaKata(kat):
    global Delta_Y
    global Delta_Z

    Okrag_Y = -175.375
    Okrag_Z = -331.15
    Okrag_R = 113.09
    katPierwotny = 31.06
    katKoncowy = math.radians(katPierwotny + kat)

    # Przy pierwszej zmianie kąta wpisywane są te linijki - nie jestesmy pewni dlaczego
    # Dlatego na wszelki wypadek dopisujemy.
    if Delta_Y != round(Okrag_Y + math.cos(katKoncowy) * Okrag_R, 2):
        writeInc(file, str(i * 10) + ';0;;Z;;24.00;;;;\n')
        writeInc(file, str(i * 10) + ';0;;Y;;16.50;;;;\n')
        writeInc(file, str(i * 10) + ';0;;Z;;24.00;;;;\n')
        writeInc(file, str(i * 10) + ';0;;Y;;16.50;;;;\n')
        writeInc(file, str(i * 10) + ';0;;Z;;24.00;;;;\n')
        writeInc(file, str(i * 10) + ';0;;Y;;16.50;;;;\n')

    # Natomiast funkcja przygotowawcza kąta jest zawsze - ?
    writeInc(file, str(i * 10) + ';97;10;;' + str(-kat) + ';;;;;\n')

    Delta_Y = round(Okrag_Y + math.cos(katKoncowy) * Okrag_R, 2)
    Delta_Z = round(Okrag_Z + math.sin(katKoncowy) * Okrag_R, 2)

## Definicja frezów i makr
frezList = [Frez(0,0,0), Frez(4,108,10000), Frez(5, 99.4,9000), Frez(6,92.3,11000), Frez(8, 98.7,12000), Frez(10,121.1,12000), Frez(6,130,8000)]

macroFrezDict = {"OTW MONT 8_6" : 3, "M4_D_HIDDEN KTZ - FRAME" : 3, "Drain for Frame - hidden d BJM machining 4034" : 3, "Drain for Frame - hidden d BJM machining 4035" : 3,
                'Holes for corner connector BJM macro KTZ1883' : 2}
##

arrBars = ncloader.load(content)
success = False

while (success == False):
    try:
        nrBelki = int(input('Podaj numer belki: '))
        nrCut = int(input('Podaj numer cięcia na belce: '))
    except:
        print("Wpisz liczbę naturalną np. 1, 3")

    try:
        macros = (arrBars[nrBelki].barCuts[nrCut].cutMacros)  ## wybór belki
        currentProfil = Profil(arrBars[nrBelki].barProfil, arrBars[nrBelki].barWidth, arrBars[nrBelki].barHeight,
                               arrBars[nrBelki].barCuts[nrCut].cutLength)
        success = True
    except:
        print("Nie ma takiej belki lub cięcia!")


i = 8 # Zaczynam od 8 linijki - 80, ale wczesniej jest jedna ikrementacja??
print('') #pusta linijka

for index, macro in enumerate(macros):
    if macro.macroIdent == 'Drain for Frame - hidden d BJM machining 4035':
        macros.remove(macro)
        break
else:
    index = -1

for macro in macros:
    if (
            macro.macroIdent == 'M4_D_HIDDEN KTZ - FRAME' or macro.macroIdent == "Drain for Frame - hidden d BJM machining 4034"):
        macro.macroObrot = 43.0
    macro.macroFrez = macroFrezDict[macro.macroIdent]  # przypasuj frez do makra

macrosSortedWX = copy.copy(macros)
macros.sort(key=lambda x: x.macroWX)
macrosSortedWX.sort(key=lambda x: x.macroWX)
macros.sort(key=lambda x: x.macroObrot)  # posortuj po obrocie 
macros.sort(key=lambda x: x.macroFrez, reverse=True)  # posortuj po narzędziu

for macro in macrosSortedWX:
    print(macro.macroIdent + ' w pozycji X: ' + str(macro.macroWX))

m_prev = 0
distanceList = []

for m in range(0, len(macrosSortedWX)):
    distanceList.append(macrosSortedWX[m].macroWX - m_prev)
    m_prev = macrosSortedWX[m].macroWX
    if (m == len(macrosSortedWX)-1):
        distanceList.append(arrBars[nrBelki].barCuts[nrCut].cutLength - macrosSortedWX[m].macroWX)

print('Odległości pomiędzy obrobkami: ' + str(distanceList) + '\n')

for d in distanceList:
    print('|', end='')
    if (arrBars[nrBelki].barCuts[nrCut].cutLength > 1500):
        for i in range(int(d)//20):
            print('-', end='')
    else:
        for i in range(int(d)//10):
            print('-', end='')
print('|\n')

klemy = []
for klema in range(4):
    tempKlema = input('Podaj pozycję ' + str(klema+1) + '-ej klemy lub zostaw puste by pominąć: ')
    if tempKlema == '':
        tempKlema = str(-9999.00)
    klemy.append(tempKlema)

### BLOK STAŁY STARTOWY ###
file.write('10;97;80;;;;;;;\n' + '20;97;15;;;;;;;\n' + '30;97;99;;'+klemy[0]+';'+klemy[1]+';'+klemy[2]+';'+klemy[3]+';;\n') #Pozycja klem - ustawiam na puste
file.write('40;0;;Z;;24.00;;;;\n' + '50;0;;Y;;16.50;;;;\n' + '60;97;10;;0.00;;;;;\n' + '70;28;;XY;;;;;;\n')
### KONIEC BLOKU STAŁEGO RUMBA 1 ###

for macro in macros:
    frezWybrany = frezList[macro.macroFrez]
    wysDisengage = Delta_Z + frezWybrany.Dlugosc + Disengage_Z
    writeInc(file, str(i * 10) + ';97;6;;1;' + str(macro.macroFrez) + ';4;' + str(frezWybrany.Predkosc) + ';;\n')
    writeInc(file, str(i * 10) + ';0;;Z;;24.00;;;;\n')
    writeInc(file, str(i * 10) + ';0;;Y;;16.50;;;;\n')
    writeInc(file, str(i * 10) + ';97;10;;' + str(kat_loza) + ';;;;;\n')  # Kąt łoża i obrót
    writeInc(file, str(i * 10) + ';97;4;;1;' + str(
        frezWybrany.Predkosc) + ';;;;\n')  # Uruchomienie narzędzia z zadanymi obrotami
    if (macro.macroIdent == 'OTW MONT 8_6'):  # Przerobić na wyszukiwanie z JSONA
        writeInc(file, str(i * 10) + ';0;;XYZ;;' + str(Delta_X + macro.macroWX) + ';' + str(
            Delta_Y - Odsuniecie_Y - 12 + (8 - frezWybrany.Srednica) / 2) + ';'
                 + str(wysDisengage) + ';;\n')  # fi 8-6/2 , 13wys + 2.79zapasu
        writeInc(file, str(i * 10) + ';0;;Z;;' + str(round(Delta_Z + frezWybrany.Dlugosc + 15.79,
                                                           2)) + ';;;;\n')  # 13wys + 2.79zapasu <- jako funkcja, to + 4 linijki w dol ?  
        writeInc(file, str(i * 10) + ';97;7;;2;;;;;\n')
        writeInc(file, str(i * 10) + ';97;11;;;;;;;\n')
        writeInc(file, str(i * 10) + ';1;;Z;200;' + str(
            round(Delta_Z + frezWybrany.Dlugosc + 7.79, 2)) + ';;;;\n')  # Praca w osi Z, zejście
        writeInc(file, str(i * 10) + ';28;;XY;;;;;;\n')
        writeInc(file, str(i * 10) + ';2;;XY;800;' + str(Delta_X + macro.macroWX) + ';' + str(
            Delta_Y - Odsuniecie_Y - 12 - (8 - frezWybrany.Srednica) / 2) + ';'
                 + str(Delta_X + macro.macroWX) + ';' + str(Delta_Y - Odsuniecie_Y - 12) + ';\n')
        writeInc(file, str(i * 10) + ';2;;XY;800;' + str(Delta_X + macro.macroWX) + ';' + str(
            Delta_Y - Odsuniecie_Y - 12 + (8 - frezWybrany.Srednica) / 2) + ';'
                 + str(Delta_X + macro.macroWX) + ';' + str(Delta_Y - Odsuniecie_Y - 12) + ';\n')
        writeInc(file, str(i * 10) + ';97;9;;;;;;;\n')
        writeInc(file, str(i * 10) + ';0;;Z;;' + str(wysDisengage) + ';;;;\n')
        writeInc(file, str(i * 10) + ';0;;XYZ;;' + str(Delta_X + macro.macroWX) + ';' + str(
            Delta_Y - Odsuniecie_Y - 12 + (8 - frezWybrany.Srednica) / 2) + ';'
                 + str(wysDisengage) + ';;\n')
        writeInc(file, str(i * 10) + ';0;;Z;;' + str(round(Delta_Z + frezWybrany.Dlugosc + 3.79,
                                                           2)) + ';;;;\n')  # 13wys + 2.79zapasu <- jako funkcja, to + 4 linijki w dol ?  
        writeInc(file, str(i * 10) + ';97;7;;2;;;;;\n')
        writeInc(file, str(i * 10) + ';97;11;;;;;;;\n')
        writeInc(file, str(i * 10) + ';1;;Z;200;' + str(
            round(Delta_Z + frezWybrany.Dlugosc - 2, 2)) + ';;;;\n')  # Praca w osi Z, zejście
        writeInc(file, str(i * 10) + ';97;9;;;;;;;\n')

    if (
            macro.macroIdent == 'M4_D_HIDDEN KTZ - FRAME' or macro.macroIdent == "Drain for Frame - hidden d BJM machining 4034"):  # Przerobić na wyszukiwanie z JSONA
        zmianaKata(43)  # Wstawiamy 43, w programie pojawia sie -43, do poprawki!
        Disengage_Z = 103.68  # Dla sprawdzenia, zmienil sie w programie
        wysDisengage = Delta_Z + frezWybrany.Dlugosc + Disengage_Z  # Ponowne przeliczenie
        writeInc(file, str(i * 10) + ';0;;XYZ;;' + str(
            Delta_X + macro.macroWX - 35 / 2 + frezWybrany.Srednica / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';'  # 9.65 <- wyliczyć skąd, obrót, w innym miejscu makro?
                 + str(
            round(wysDisengage, 2)) + ';;\n')  # fi 8-6/2 , 13wys + 2.79zapasu, X - odwodnienie ma 35/2, frez d/2
        writeInc(file, str(i * 10) + ';0;;Z;;' + str(round((Delta_Z + frezWybrany.Dlugosc - 37.03),
                                                           2)) + ';;;;\n')  # 13wys + 2.79zapasu <- jako funkcja, to + 4 linijki w dol ?  
        writeInc(file, str(i * 10) + ';97;7;;2;;;;;\n')
        writeInc(file, str(i * 10) + ';97;11;;;;;;;\n')
        writeInc(file, str(i * 10) + ';1;;Z;200;' + str(round(Delta_Z + frezWybrany.Dlugosc - 49.03,
                                                              2)) + ';;;;\n')  # Praca w osi Z, zejście - póki co na twardo przyjęte - do przeliczenia.
        writeInc(file, str(i * 10) + ';28;;XY;;;;;;\n')
        writeInc(file, str(i * 10) + ';1;;XY;800;' + str(
            Delta_X + macro.macroWX + 35 / 2 - frezWybrany.Srednica / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';;;\n')
        writeInc(file, str(i * 10) + ';97;9;;;;;;;\n')
        # Druga polowka
        writeInc(file, str(i * 10) + ';0;;XYZ;;' + str(
            Delta_X + macro.macroWX - 35 / 2 + frezWybrany.Srednica / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';'
                 + str(round(Delta_Z + frezWybrany.Dlugosc - 49.03,
                             2)) + ';;\n')  # fi 8-6/2 , 13wys + 2.79zapasu, X - odwodnienie ma 35/2, frez d/2
        writeInc(file, str(i * 10) + ';0;;Z;;' + str(round(Delta_Z + frezWybrany.Dlugosc - 49.03 - 0.01,
                                                           2)) + ';;;;\n')  # 13wys + 2.79zapasu <- jako funkcja, to + 4 linijki w dol ?  0.01 zapasu? nie wiem po co
        writeInc(file, str(i * 10) + ';97;7;;2;;;;;\n')
        writeInc(file, str(i * 10) + ';97;11;;;;;;;\n')
        writeInc(file, str(i * 10) + ';1;;Z;200;' + str(round(Delta_Z + frezWybrany.Dlugosc - 49.03 - 12.37,
                                                              2)) + ';;;;\n')  # Praca w osi Z, zejście - póki co na twardo przyjęte - do przeliczenia. 12.37 w glab
        writeInc(file, str(i * 10) + ';28;;XY;;;;;;\n')
        writeInc(file, str(i * 10) + ';1;;XY;800;' + str(
            Delta_X + macro.macroWX + 35 / 2 - frezWybrany.Srednica / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';;;\n')
        writeInc(file, str(i * 10) + ';97;9;;;;;;;\n')
        # print(macro.macroIdent + ' - ' + str(macro.macroWX) + ' - ' + str(wysDisengage))

    writeInc(file, str(i * 10) + ';0;;Z;;24.00;;;;\n')
    writeInc(file, str(i * 10) + ';97;5;;;;;;;\n')
    writeInc(file, str(i * 10) + ';97;50;;;;;;;\n')
    writeInc(file, str(i * 10) + ';97;80;;;;;;;\n')
    writeInc(file, str(i * 10) + ';97;15;;;;;;;\n')

print('Plik wygenerowany pomyślnie!')
file.close() 