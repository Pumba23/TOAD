import numpy as np

#vereinfachte version
def SDA_LMDI_pl(Cct1, Cct2, Cet1, Cet2, CLt1, CLt2, Cyt1, Cyt2, m_results_x):
    tag = "DL"

    L0 = CLt1
    L1 = CLt2

    y0 = Cyt1
    y1 = Cyt2

    f0 = Cet1
    f1 = Cet2

    # Funktionen zur Berechnung der Effekte
    def intensitaetseffekt(f0, f1, L0, L1, y0, y1):


        delta_f = f1 - f0

        delta_E_int = delta_f@(0.5*(L1+L0))@(0.5*(y0+y1))
        return delta_E_int


    def struktureffekt(f0, f1, L0, L1, y0, y1):
        delta_L = L1 - L0

        delta_E_str = (0.5*(f1+f0))@delta_L@(0.5*(y0+y1))
        return delta_E_str

    def nachfrageneffekt(f0, f1, L0, L1, y0, y1):
        delta_y = y1 - y0
        delta_E_dem = (0.5*(f1+f0))@(0.5*(L0+L1))@delta_y
        return delta_E_dem

    # Berechnung der Effekte
    delta_E_int = intensitaetseffekt(f0, f1, L0, L1, y0, y1)
    delta_E_str = struktureffekt(f0, f1, L0, L1, y0, y1)
    delta_E_dem = nachfrageneffekt(f0, f1, L0, L1, y0, y1)

    #summieren über sektoren:

    delta_E_int = delta_E_int.sum()
    delta_E_str = delta_E_str.sum()
    delta_E_dem = delta_E_dem.sum()
    # Gesamteffekt
    delta_E_total = delta_E_int + delta_E_str + delta_E_dem
    # Ausgabe der Ergebnisse
    print(f"Intensitätseffekt: {delta_E_int}")
    print(f"Struktureffekt: {delta_E_str}")
    print(f"Nachfrageneffekt: {delta_E_dem}")
    print(f"Gesamteffekt: {delta_E_total}")



    effect_round_e = round(delta_E_int, 5)
    effect_round_L = round(delta_E_str, 5)
    effect_round_y = round(delta_E_dem, 5)

    i = 1

    m_results_x[i, 0] = effect_round_e
    m_results_x[i, 1] = effect_round_L
    m_results_x[i, 2] = effect_round_y

    return m_results_x, tag, delta_E_total
# Funktionen zur Berechnung der Effekte

