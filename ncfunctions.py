import numpy as np


def findNearest(value, profil_h):
    profil_h = float(profil_h)
    disengage = np.array(
        [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, -90, -85, -80, -75, -70, -65, -60, -55, -50, -45, -40, -35, -30, -25, -20,
         -15, -10, -5])
    # Przepisać dval żeby przeliczało zgodnie z wysokością profilu
    if profil_h > 70.92:
        diff_ = profil_h-70.92
        dval = diff_ + np.array(
            [95.92, 97.27, 100.08, 102.3, 103.94, 104.98, 105.42, 105.23, 104.44, 103.5, 101.43, 99.23, 96.46, 93.15, 89.32, 85, 80.22, 75.03, 69.45, 198.81,
             198.15, 196.17, 192.89, 188.33, 182.53, 175.52, 167.38, 158.15, 147.9, 137.54, 132.21, 118.3, 119.13, 111.49, 99.18, 94.3, 84.88])
    else:
        dval = np.array(
            [95.92, 97.27, 100.08, 102.3, 103.94, 104.98, 105.42, 105.23, 104.44, 103.5, 101.43, 99.23, 96.46, 93.15, 89.32, 85, 80.22, 75.03, 69.45, 198.81,
             198.15, 196.17, 192.89, 188.33, 182.53, 175.52, 167.38, 158.15, 147.9, 137.54, 132.21, 118.3, 119.13, 111.49, 99.18, 94.3, 84.88])

    disengage_val = {}
    val = 0
    for i in disengage:
        disengage_val.update({i: dval[val]})
        val += 1

    array = np.asarray(disengage)
    idx = (np.abs(array - value)).argmin()
    return disengage_val[array[idx]]