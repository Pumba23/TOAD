import numpy as np

# GENAUERE BERECHNUNG
def SDA_LMDI_dt(Cct1, Cct2, Cet1, Cet2, CLt1, CLt2, Cyt1, Cyt2, m_results_x):
    tag = "DLlong"

    L0 = CLt1
    L1 = CLt2

    y0 = Cyt1
    y1 = Cyt2

    f0 = Cet1
    f1 = Cet2

    # Änderungen in den Komponenten
    delta_f = f1 - f0
    delta_L = L1 - L0
    delta_y = y1 - y0

    # Funktionen zur Berechnung der einzelnen Effekte
    def calc_effect_f(delta_f, L, y):
        return np.dot(delta_f, np.dot(L, y))

    def calc_effect_L(f, delta_L, y):
        return np.dot(f, np.dot(delta_L, y))

    def calc_effect_y(f, L, delta_y):
        return np.dot(f, np.dot(L, delta_y))

    # Listen zur Speicherung der Effekte für jede Sequenz
    effects_f = []
    effects_L = []
    effects_y = []

    # Sequenz: f, L, y
    effect_f = calc_effect_f(delta_f, L0, y0)
    effect_L = calc_effect_L(f1, delta_L, y0)
    effect_y = calc_effect_y(f1, L1, delta_y)
    effects_f.append(effect_f)
    effects_L.append(effect_L)
    effects_y.append(effect_y)

    # Sequenz: f, y, L
    effect_f = calc_effect_f(delta_f, L0, y0)
    effect_y = calc_effect_y(f1, L0, delta_y)
    effect_L = calc_effect_L(f1, delta_L, y1)
    effects_f.append(effect_f)
    effects_L.append(effect_L)
    effects_y.append(effect_y)

    # Sequenz: L, f, y
    effect_L = calc_effect_L(f0, delta_L, y0)
    effect_f = calc_effect_f(delta_f, L1, y0)
    effect_y = calc_effect_y(f1, L1, delta_y)
    effects_f.append(effect_f)
    effects_L.append(effect_L)
    effects_y.append(effect_y)

    # Sequenz: L, y, f
    effect_L = calc_effect_L(f0, delta_L, y0)
    effect_y = calc_effect_y(f0, L1, delta_y)
    effect_f = calc_effect_f(delta_f, L1, y1)
    effects_f.append(effect_f)
    effects_L.append(effect_L)
    effects_y.append(effect_y)

    # Sequenz: y, f, L
    effect_y = calc_effect_y(f0, L0, delta_y)
    effect_f = calc_effect_f(delta_f, L0, y1)
    effect_L = calc_effect_L(f1, delta_L, y1)
    effects_f.append(effect_f)
    effects_L.append(effect_L)
    effects_y.append(effect_y)

    # Sequenz: y, L, f
    effect_y = calc_effect_y(f0, L0, delta_y)
    effect_L = calc_effect_L(f0, delta_L, y1)
    effect_f = calc_effect_f(delta_f, L1, y1)
    effects_f.append(effect_f)
    effects_L.append(effect_L)
    effects_y.append(effect_y)

    # Durchschnitt der Effekte
    average_effect_f = sum(effects_f) / len(effects_f)
    average_effect_L = sum(effects_L) / len(effects_L)
    average_effect_y = sum(effects_y) / len(effects_y)

    # Ergebnisse
    #print("Durchschnittlicher Effekt der Änderungen in der Emissionsintensität:", average_effect_f)
    #print("Durchschnittlicher Effekt der Änderungen in der Leontief-Inversen:", average_effect_L)
    print("Durchschnittlicher Effekt der Änderungen in der Endnachfrage sectors:", average_effect_y)
    print("type der Endnachfrage:", type(average_effect_y))

    average_effect_f = int(average_effect_f.sum())
    average_effect_L = int(average_effect_L.sum())
    average_effect_y = int(average_effect_y.sum())

    print("Durchschnittlicher Effekt der Änderungen in der Endnachfrage summed:", average_effect_y)

    effect_round_e = round(average_effect_f, 5)
    effect_round_L = round(average_effect_L, 5)
    effect_round_y = round(average_effect_y, 5)

    sum5 = average_effect_f + average_effect_L + average_effect_y

    i = 1

    m_results_x[i, 0] = effect_round_e
    m_results_x[i, 1] = effect_round_L
    m_results_x[i, 2] = effect_round_y

    return m_results_x, tag, sum5
# Funktionen zur Berechnung der Effekte

