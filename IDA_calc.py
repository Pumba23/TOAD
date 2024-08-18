import numpy as np
import math
import pandas as pd

def calc_IDA(filtered_values, calculation_type, effects, period, sum_case):
    temp_array1 = np.array(filtered_values)
    print(temp_array1.shape)


    neue_spalten = effects + 1  # effects+ghg
    zeilen = period + 1  # period incl. first and last year
    effects_array = np.zeros((zeilen, neue_spalten))  # array for effects

    for i in range(0,neue_spalten):
       if i == 0 or i == 1:
           effects_array[:, i] = temp_array1[:, i + 1]  # ghg and activity effect
       elif 1 < i < effects:
           effects_array[:, i] = temp_array1[:, i + 1] / temp_array1[:, i] # effects
       elif i == effects:
           effects_array[:, i] = temp_array1[:, 1] / temp_array1[:, i]  # effects
       else:
           print("error")


    neue_werte_array = np.zeros((zeilen, effects))  # Initialize neue_werte_array with zeros, e.g. 34 rows, including base value, 6 columns for each effect
    eps = 0.00000000000000000000000001  # small value for avoiding 0, 10^-25


    for zeile in range(0, zeilen):
        Ct2 = effects_array[zeile][0]
        Ct1 = effects_array[zeile - 1][0]
        Ct0 = effects_array[0][0]
        if zeile == 0:
            Ct1 = Ct0

        Ct90 = effects_array[0][0]
        deltaC = Ct2 - Ct1


        zeilenwerte = []

        for spalte in range(1, neue_spalten):
            Cxt2 = effects_array[zeile][spalte]
            Cxt1 = effects_array[zeile - 1][spalte]
            Cxt0 = effects_array[0][spalte]
            Cxt90 = effects_array[0][spalte]


            if calculation_type == "yby":
                if math.log(Ct2) == math.log(Ct1):
                    gesamtsumme = ((Ct2 - Ct1)) / ((math.log(Ct2) - math.log(Ct1)) + eps) * math.log(Cxt2 / Cxt1)
                    rounded_number = round(gesamtsumme, 5)
                else:
                    gesamtsumme = (Ct2 - Ct1) / (math.log(Ct2) - math.log(Ct1)) * math.log(Cxt2 / Cxt1)
                    rounded_number = round(gesamtsumme, 5)
            elif calculation_type == "cud":
                if math.log(Ct2) == math.log(Ct90):
                    gesamtvonvorne = ((Ct2 - Ct90)) / ((math.log(Ct2) - math.log(Ct90)) + eps) * math.log(Cxt2 / Cxt90)
                    rounded_number = round(gesamtvonvorne, 5)
                else:
                    gesamtvonvorne = (Ct2 - Ct90) / (math.log(Ct2) - math.log(Ct90)) * math.log(Cxt2 / Cxt90)
                    rounded_number = round(gesamtvonvorne, 5)
            else:
                print("Ungültiger Berechnungstyp. Bitte 'jahr' oder 'gesamt' eingeben.")
                return None
            zeilenwerte.append(rounded_number)

        neue_werte_array[zeile] = zeilenwerte  # Fügen Sie die Werte zur entsprechenden Zeile in neue_werte_array hinzu

    #print(neue_werte_array)
    return neue_werte_array, zeilen
