import numpy as np

def zmianaNarzedzia(frez, predkosc, file, inc, kat_loza):
    writeInc(file, str(inc * 10) + ';97;6;;1;' + str(frez) + ';4;' + str(predkosc) + ';;\n')
    writeInc(file, str(inc * 10) + ';0;;Z;;24.00;;;;\n')
    writeInc(file, str(inc * 10) + ';0;;Y;;16.50;;;;\n')
    writeInc(file, str(inc * 10) + ';97;10;;' + str(kat_loza) + ';;;;;\n')  # Kąt łoża i obrót
    writeInc(file, str(inc * 10) + ';97;4;;1;' + str(predkosc) + ';;;;\n')

disengage = np.array([-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75, 90])
disengage_val = {-90: 198.81, -75: 192.89, -60: 175.52, -45:147.9, -30:118.3, -15:99.18, 0:95.92, 15:102.3, 30:105.42, 45:103.5, 60:96.46, 75:85, 90:69.45}

def find_nearest(value):
    array = np.asarray(disengage)
    idx = (np.abs(array - value)).argmin()
    return disengage_val[array[idx]]