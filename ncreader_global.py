import copy
import os
import json
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
    global inc
    inc += 1


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

# Definicja frezów i makr - Została zastąpiona przez definicję w JSON

arrBars = ncloader.load(content)
success = False

while (success == False):
    try:
        nrBelki = int(input('Podaj numer belki: '))
        nrCut = int(input('Podaj numer cięcia na belce: '))
    except:
        print("Wpisz liczbę naturalną np. 1, 3")

    try:
        macros = (arrBars[nrBelki].barCuts[nrCut].cutMacros)  # wybór belki
        currentProfil = Profil(arrBars[nrBelki].barProfil, arrBars[nrBelki].barWidth, arrBars[nrBelki].barHeight,
                               arrBars[nrBelki].barCuts[nrCut].cutLength)
        success = True
    except:
        print("Nie ma takiej belki lub cięcia!")


inc = 8  # Zaczynam od 8 linijki - 80
print('')  # pusta linijka

for index, macro in enumerate(macros):
    if macro.Ident == 'Drain for Frame - hidden d BJM machining 4035':
        macros.remove(macro)
        break
else:
    index = -1

with open("macro.json", "r", encoding='utf-8') as f:
    macroLib = json.load(f)

with open("frez.json", "r") as f:
    frezLib = json.load(f)

for macro in macros:
    macro.Obrot = macroLib[macro.Ident]['angle']
    macro.Frez = macroLib[macro.Ident]['tool'][0]

macrosSortedWX = copy.copy(macros)
macros.sort(key=lambda x: x.WX)
macrosSortedWX.sort(key=lambda x: x.WX)
macros.sort(key=lambda x: x.Obrot)  # posortuj po obrocie
macros.sort(key=lambda x: x.Frez, reverse=True)  # posortuj po narzędziu

for macro in macrosSortedWX:
    print(macro.Ident + ' w pozycji X: ' + str(macro.WX))

m_prev = 0
distanceList = []

for m in range(0, len(macrosSortedWX)):
    distanceList.append(macrosSortedWX[m].WX - m_prev)
    m_prev = macrosSortedWX[m].WX
    if (m == len(macrosSortedWX)-1):
        distanceList.append(arrBars[nrBelki].barCuts[nrCut].cutLength - macrosSortedWX[m].WX)

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

frezPoprzedni = 0
obrotPoprzedni = 0

for macro in macros:
    frezWybrany = frezLib[str(macro.Frez)]
    wysDisengage = Delta_Z + frezWybrany['length'] + Disengage_Z
    obrot = macro.Obrot
    if (frezPoprzedni != frezWybrany):
        writeInc(file, str(inc * 10) + ';97;6;;1;' + str(macro.Frez) + ';4;' + str(frezWybrany['speed']) + ';;\n')
        writeInc(file, str(inc * 10) + ';0;;Z;;24.00;;;;\n')
        writeInc(file, str(inc * 10) + ';0;;Y;;16.50;;;;\n')
        writeInc(file, str(inc * 10) + ';97;10;;' + str(kat_loza) + ';;;;;\n')  # Kąt łoża i obrót
        writeInc(file, str(inc * 10) + ';97;4;;1;' + str(
            frezWybrany['speed']) + ';;;;\n')  # Uruchomienie narzędzia z zadanymi obrotami
    elif (obrotPoprzedni == obrot):
        writeInc(file, str(inc * 10) + ';0;;Z;;'+str(round(wysDisengage,2))+';;;;\n')
        zmianaKata(macro.Obrot)  # Wstawiamy 43, w programie pojawia sie -43, do poprawki!
    if (macro.Ident == 'OTW MONT 8_6'):  # Przerobić na wyszukiwanie z JSONA
        writeInc(file, str(inc * 10) + ';0;;XYZ;;' + str(Delta_X + macro.WX) + ';' + str(
            Delta_Y - Odsuniecie_Y - 12 + (8 - frezWybrany['diameter']) / 2) + ';'
                 + str(wysDisengage) + ';;\n')  # fi 8-6/2 , 13wys + 2.79zapasu
        writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round(Delta_Z + frezWybrany['length'] + 15.79,
                                                           2)) + ';;;;\n')  # 13wys + 2.79zapasu <- jako funkcja, to + 4 linijki w dol ?  
        writeInc(file, str(inc * 10) + ';97;7;;2;;;;;\n')
        writeInc(file, str(inc * 10) + ';97;11;;;;;;;\n')
        writeInc(file, str(inc * 10) + ';1;;Z;200;' + str(
            round(Delta_Z + frezWybrany['length'] + 7.79, 2)) + ';;;;\n')  # Praca w osi Z, zejście
        writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
        writeInc(file, str(inc * 10) + ';2;;XY;800;' + str(Delta_X + macro.WX) + ';' + str(
            Delta_Y - Odsuniecie_Y - 12 - (8 - frezWybrany['diameter']) / 2) + ';'
                 + str(Delta_X + macro.WX) + ';' + str(Delta_Y - Odsuniecie_Y - 12.00) + ';\n')
        writeInc(file, str(inc * 10) + ';2;;XY;800;' + str(Delta_X + macro.WX) + ';' + str(
            Delta_Y - Odsuniecie_Y - 12 + (8 - frezWybrany['diameter']) / 2) + ';'
                 + str(Delta_X + macro.WX) + ';' + str(Delta_Y - Odsuniecie_Y - 12.00) + ';\n')
        writeInc(file, str(inc * 10) + ';97;9;;;;;;;\n')
        writeInc(file, str(inc * 10) + ';0;;Z;;' + str(wysDisengage) + ';;;;\n')
        writeInc(file, str(inc * 10) + ';0;;XYZ;;' + str(Delta_X + macro.WX) + ';' + str(
            Delta_Y - Odsuniecie_Y - 12) + ';'+ str(wysDisengage) + ';;\n')
        writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round(Delta_Z + frezWybrany['length'] + 3.79,
                                                           2)) + ';;;;\n')  # 13wys + 2.79zapasu <- jako funkcja, to + 4 linijki w dol ?  
        writeInc(file, str(inc * 10) + ';97;7;;2;;;;;\n')
        writeInc(file, str(inc * 10) + ';97;11;;;;;;;\n')
        writeInc(file, str(inc * 10) + ';1;;Z;200;' + str(
            round(Delta_Z + frezWybrany['length'] - 2, 2)) + ';;;;\n')  # Praca w osi Z, zejście
        writeInc(file, str(inc * 10) + ';97;9;;;;;;;\n')

    if (macro.Ident == 'M4_D_HIDDEN KTZ - FRAME' or macro.Ident == "Drain for Frame - hidden d BJM machining 4034"):  # Przerobić na wyszukiwanie z JSONA
        Disengage_Z = 103.68  # Dla sprawdzenia, zmienil sie w programie
        wysDisengage = Delta_Z + frezWybrany['length'] + Disengage_Z  # Ponowne przeliczenie
        writeInc(file, str(inc * 10) + ';0;;XYZ;;' + str(
            Delta_X + macro.WX - 35 / 2 + frezWybrany['diameter'] / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';'  # 9.65 <- wyliczyć skąd, obrót, w innym miejscu makro?
                 + str(
            round(wysDisengage, 2)) + ';;\n')  # fi 8-6/2 , 13wys + 2.79zapasu, X - odwodnienie ma 35/2, frez d/2
        writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round((Delta_Z + frezWybrany['length'] - 37.03),
                                                           2)) + ';;;;\n')  # 13wys + 2.79zapasu <- jako funkcja, to + 4 linijki w dol ?  
        writeInc(file, str(inc * 10) + ';97;7;;2;;;;;\n')
        writeInc(file, str(inc * 10) + ';97;11;;;;;;;\n')
        writeInc(file, str(inc * 10) + ';1;;Z;200;' + str(round(Delta_Z + frezWybrany['length'] - 49.03,
                                                              2)) + ';;;;\n')  # Praca w osi Z, zejście - póki co na twardo przyjęte - do przeliczenia.
        writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
        writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(
            Delta_X + macro.WX + 35 / 2 - frezWybrany['diameter'] / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';;;\n')
        writeInc(file, str(inc * 10) + ';97;9;;;;;;;\n')
        # Druga polowka
        writeInc(file, str(inc * 10) + ';0;;XYZ;;' + str(
            Delta_X + macro.WX - 35 / 2 + frezWybrany['diameter'] / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';'
                 + str(round(Delta_Z + frezWybrany['length'] - 49.03,
                             2)) + ';;\n')  # fi 8-6/2 , 13wys + 2.79zapasu, X - odwodnienie ma 35/2, frez d/2
        writeInc(file, str(inc * 10) + ';0;;Z;;' + str(round(Delta_Z + frezWybrany['length'] - 49.03 - 0.01,
                                                           2)) + ';;;;\n')  # 13wys + 2.79zapasu <- jako funkcja, to + 4 linijki w dol ?  0.01 zapasu? nie wiem po co
        writeInc(file, str(inc * 10) + ';97;7;;2;;;;;\n')
        writeInc(file, str(inc * 10) + ';97;11;;;;;;;\n')
        writeInc(file, str(inc * 10) + ';1;;Z;200;' + str(round(Delta_Z + frezWybrany['length'] - 49.03 - 12.37,
                                                              2)) + ';;;;\n')  # Praca w osi Z, zejście - póki co na twardo przyjęte - do przeliczenia. 12.37 w glab
        writeInc(file, str(inc * 10) + ';28;;XY;;;;;;\n')
        writeInc(file, str(inc * 10) + ';1;;XY;800;' + str(
            Delta_X + macro.WX + 35 / 2 - frezWybrany['diameter'] / 2) + ';' + str(
            Delta_Y - Odsuniecie_Y - 55.25 + 9.65) + ';;;\n')
        writeInc(file, str(inc * 10) + ';97;9;;;;;;;\n')
        # print(macro.Ident + ' - ' + str(macro.WX) + ' - ' + str(wysDisengage))
    frezPoprzedni = frezWybrany
    obrotPoprzedni = obrot

writeInc(file, str(inc * 10) + ';0;;Z;;24.00;;;;\n')
writeInc(file, str(inc * 10) + ';97;5;;;;;;;\n')
writeInc(file, str(inc * 10) + ';97;50;;;;;;;\n')
writeInc(file, str(inc * 10) + ';97;80;;;;;;;\n')
writeInc(file, str(inc * 10) + ';97;15;;;;;;;\n')

print('Plik wygenerowany pomyślnie!')
file.close() 