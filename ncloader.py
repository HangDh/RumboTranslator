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
        macroIdent = ''
        macroComment = ''
        macroWX = 0.0
        macroObrot = 0.0
        macroWorks = []
        macroFrez = 0

        def __init__(self, ident):
            self.macroIdent = ident
            self.macroWorks = []
            self.macroFrez = 0

    class Work(object):
        workComment = ''
        workType = ''
        workWX = 0.0
        workWY = 0.0
        workSide = 0
        workHeight = 0.0
        workDepth = 0.0

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

            if y.startswith('WComment') and macro_ident.startswith(':WMacroIdent'):
                if macro_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroComment = (
                        re.search(r'= "(.*)"', y, flags=0).group(1))

            if y.startswith('WX1') and macro_ident.startswith('WParent'):
                if macro_idx > 0:
                    if '-' in y:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWX = float(
                            (re.search(r'= (-\d*.\d*)', y, flags=0).group(1)))
                    else:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWX = float(
                            (re.search(r'= (\d*.\d*)', y, flags=0).group(1)))

            if y.startswith('WComment') and macro_ident.startswith(':WORK'):
                if macro_idx > 0:
                    ilosc_obr += 1
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks.append(
                        Work(re.search(r'= "(.*)"', y, flags=0).group(1)))
                    work_idx += 1

            if y.startswith('WType') and macro_ident.startswith('WPriority'):
                if macro_idx > 0 and work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workType = (
                        re.search(r'= "(.*)"', y, flags=0).group(1))

            if y.startswith('WX1') and macro_ident.startswith('WType'):
                if macro_idx > 0 and work_idx > 0:
                    if '-' in y:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workWX = (
                            re.search(r'= (-\d*.\d*)', y, flags=0).group(1))
                    else:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workWX = (
                            re.search(r'= (\d*.\d*)', y, flags=0).group(1))

            if y.startswith('WY1'):
                if macro_idx > 0 and work_idx > 0:
                    if '-' in y:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workWY = (
                            re.search(r'= (-\d*.\d*)', y, flags=0).group(1))
                    else:
                        arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workWY = (
                            re.search(r'= (\d*.\d*)', y, flags=0).group(1))

            if y.startswith('WSide'):
                if macro_idx > 0 and work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workSide = (
                        re.search(r'(\d)', y, flags=0).group(1))

            if y.startswith('WHeight'):
                if macro_idx > 0 and work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workHeight = (
                        re.search(r'= (\d*.\d*)', y, flags=0).group(1))

            if y.startswith('WDepth'):
                if macro_idx > 0 and work_idx > 0:
                    arrBars[idx].barCuts[sub_idx - 1].cutMacros[macro_idx - 1].macroWorks[work_idx - 1].workDepth = (
                        re.search(r'= (\d*.\d*)', y, flags=0).group(1))

            # if y.startswith(':WORK'):
            # print(macro_ident)

            macro_ident = y
        idx += 1

    return arrBars

