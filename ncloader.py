import re
import math

def load(content):
    class Bar(object):
        barNumber = 0
        barLength = 0.0
        barProfil = ''
        barHeight = 0.0
        barWidth = 0.0
        barCuts = []

        def __init__(self, number):
            self.barNumber = number
            self.barCuts = []

    class Cut(object):
        cutLength = 0
        cutNumber = 0
        cutProfil = ''
        cutDescription = ''
        cutMacros = []
        cutWorks = []

        def __init__(self, length):
            self.cutLength = length
            self.cutDescription = ''
            self.cutWorks = []
            self.cutMacros = []

    class Macro(object):
        Ident = ''
        Comment = ''
        Description = ''
        Angle = 0.0
        Side = 0
        WX = 0.0
        PosY = 0
        Tool = '0'
        macroWorks = []

        def __init__(self, ident):
            self.Ident = ident
            self.macroWorks = []

    class Work(object):
        workComment = ''
        workType = ''
        workWX = 0.0
        workWY = 0.0
        workSide = 0
        workWW1 = 0
        workWW2 = 0
        workHeight = 0.0
        workD1 = 0.0
        workD2 = 0.0
        workAngle = 0.0

        def __init__(self, comment):
            self.workComment = comment

    bars = content.split(':BAR')
    ilosc_ciec = 0
    ilosc_obr = 0
    ilosc_obrCiec = 0
    idx = 0
    arrBars = [Bar(0)]

    for x in bars:
        # arrCuts.append('')
        sub_idx = 0
        macro_idx = 0
        work_idx = 0

        for y in x.split('\n'):
            if y.startswith('BNo'):
                bNum = re.search(r'= (\d*)', y, flags=0).group(1)
                arrBars.append(Bar(bNum))

            if y.startswith('BLength'):
                arrBars[idx].barLength = re.search(r'= (\d*.\d*)', y, flags=0).group(1)

            if y.startswith('BIdentNo'):
                arrBars[idx].barProfil = re.search(r'= "(.*)"', y, flags=0).group(1)

            if y.startswith('BHeight'):
                arrBars[idx].barHeight = re.search(r'= (\d*.\d*)', y, flags=0).group(1)

            if y.startswith('BWidth'):
                arrBars[idx].barWidth = re.search(r'= (\d*.\d*)', y, flags=0).group(1)

            if y.startswith('CLength'):
                tempLen = float(re.search(r'= (\d*.\d*)', y, flags=0).group(1))
                arrBars[idx].barCuts.append(Cut(tempLen))
                ilosc_ciec += 1
                macro_idx = 0
                sub_idx += 1

            if y.startswith('CDescription'):
                arrBars[idx].barCuts[sub_idx - 1].cutDescription = re.search(r'= "(.*)"', y, flags=0).group(1)
                arrBars[idx].barCuts[sub_idx - 1].cutProfil = arrBars[idx].barProfil
                arrBars[idx].barCuts[sub_idx - 1].cutMacros = []

            if y.startswith('CPartNo'):
                arrBars[idx].barCuts[sub_idx - 1].cutNumber = re.search(r'= (\d*)', y, flags=0).group(1)

            if y.startswith('WMacroIdent'):
                arrBars[idx].barCuts[sub_idx - 1].cutMacros.append(Macro(re.search(r'= "(.*)"', y, flags=0).group(1)))
                macro_idx += 1
                work_idx = 0

            if y.startswith('WComment') and macro_ident.startswith('WMacroIdent'):
                if macro_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].Comment = (
                        re.search(r'= "(.*)"', y, flags=0).group(1))

            if y.startswith('WX1') and macro_ident.startswith('WParent'):
                if macro_idx > 0:
                    if '-' in y:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].WX = float(
                            (re.search(r'= (-\d*.\d*)', y, flags=0).group(1)))
                    else:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].WX = float(
                            (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))


            if y.startswith('WComment') and macro_ident.startswith(':WORK'):
                arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks.append(Work(re.search(r'= "(.*)"', y, flags=0).group(1)))
                work_idx += 1

            if y.startswith('WType') and macro_ident.startswith('WPriority'):
                if work_idx > 0:
                    test = (re.search(r'= "(.)"', y, flags=0).group(1))
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx -1].workType = (
                        re.search(r'= "(.)"', y, flags=0).group(1))

            if y.startswith('WX1') and macro_ident.startswith('WType'):
                if work_idx > 0:
                    if '-' in y:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workWX = float(
                            (re.search(r'= (-\d*.\d*)', y, flags=0).group(1)))
                    else:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workWX = float(
                            (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))

            if y.startswith('WSide') and macro_ident.startswith('WX1'):
                if work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workSide = (
                        re.search(r'= (\d)', y, flags=0).group(1))

            if y.startswith('WPAngleX') and macro_ident.startswith('WSide'):
                if work_idx > 0:
                    if '-' in y:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workAngle = float(
                            (re.search(r'= (-\d*.\d*)', y, flags=0).group(1)))
                    else:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workAngle = float(
                            (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))

            if y.startswith('WY1') and (macro_ident.startswith('WSide') or macro_ident.startswith('WPTransZ')):
                if work_idx > 0:
                    if '-' in y:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workWY = float(
                            (re.search(r'= (-\d*.\d*)', y, flags=0).group(1)))
                    else:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workWY = float(
                            (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))

            if y.startswith('WHeight') and macro_ident.startswith('WY1'):
                if work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workHeight = float(
                        (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))

            if y.startswith('WW1') and macro_ident.startswith('WDepth'):
                if work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workWW1 = float(
                        (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))

            if y.startswith('WW2') and macro_ident.startswith('WW1'):
                if work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workWW2 = float(
                        (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))

            if y.startswith('WAngle') and macro_ident.startswith('WW2'):
                if work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workAngle = float(
                        (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))

            if y.startswith('WDT0D') and (macro_ident.startswith('WDrillCorr') or macro_ident.startswith('WAngle')):
                if work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workD1 = float(
                        (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))

            if y.startswith('WDT1D') and macro_ident.startswith('WDT0F'):
                if work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workD2 = float(
                        (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))

            macro_ident = y
        idx += 1

    return arrBars

