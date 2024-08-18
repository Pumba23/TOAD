# second approach
import numpy as np


def SDA_DL_ext(Clt1, Clt2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1, Cdt2, Cpt1, Cpt2, Cly1,
               Cly2, mc,
               m_results_x, sum1, sum2, i):
    tag = 'DL44'

    I = np.eye(Cbt1.shape[0])

    # Berechnung der Effekte

    def intensity_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1, Cdt2, Cpt1, Cpt2,
                         Clt1, Clt2, sum1, sum2):
        delta_Cet = Cet2 - Cet1
        # temp2_0 = 0.5 * (delta_Cet @ Clt1 @ (Cly1/sum1) @ Cdt1 @ Cpt1 + delta_Cet @ Clt2 @ (Cly2/sum2) @ Cdt2 @ Cpt2)
        temp2_0 = delta_Cet @ (0.5 * (Clt2 + Clt1)) @ (0.5 * ((Cly1 / sum1) + (Cly2 / sum2))) @ (
                    0.5 * (Cdt1 + Cdt2)) @ (0.5 * (Cpt1 + Cpt2))
        '''
        # Einzelne Schritte der Berechnung
        step1 = delta_Cet
        print("step1 (delta_Cet):")
        print(step1)

        step2 = 0.5 * (Clt2 + Clt1)
        print("step2 (0.5 * (Clt2 + Clt1)):")
        print(step2)

        step3 = 0.5 * ((Cly1 / sum1) + (Cly2 / sum2))
        print("step3 (0.5 * ((Cly1 / sum1) + (Cly2 / sum2))):")
        print(step3)

        step4 = 0.5 * (Cdt1 + Cdt2)
        print("step4 (0.5 * (Cdt1 + Cdt2)):")
        print(step4)

        step5 = 0.5 * (Cpt1 + Cpt2)
        print("step5 (0.5 * (Cpt1 + Cpt2)):")
        print(step5)

        # Kombinierte Schritte
        combined_step1 = step1 @ step2
        print("combined_step1 (step1 @ step2):")
        print(combined_step1)

        combined_step2 = combined_step1 @ step3
        print("combined_step2 (combined_step1 @ step3):")
        print(combined_step2)

        combined_step3 = combined_step2 @ step4
        print("combined_step3 (combined_step2 @ step4):")
        print(combined_step3)

        temp2_0 = combined_step3 @ step5
        print("temp2_0 (combined_step3 @ step5):")
        print(temp2_0)

        print('shape of effects before summation')
        print(temp2_0.shape)
        print(temp2_0)

        '''
        return temp2_0.sum()

    def intermediate_trade_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1, Cdt2,
                                  Cpt1, Cpt2, Clt1, Clt2, sum1, sum2):
        delta_Ctt = Ctt2 - Ctt1
        # temp2_0 = 0.5 * (Cet1 @ (Clt1@(delta_Ctt * Cst1)@Clt2) @ (Cly1/sum1) @ Cdt1 @ Cpt1 + Cet2 @ (Clt1@(delta_Ctt * Cst2)@Clt2) @ (Cly2/sum2) @ Cdt2 @ Cpt2)
        temp2_0 = (0.5 * (Cet1 + Cet2)) @ (Clt2 @ (delta_Ctt * (0.5 * (Cst2 + Cst1))) @ Clt1) @ (
                    0.5 * ((Cly1 / sum1) + (Cly2 / sum2))) @ (0.5 * (Cdt1 + Cdt2)) @ (0.5 * (Cpt1 + Cpt2))
        return temp2_0.sum()

    def structure_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1, Cdt2, Cpt1, Cpt2,
                         Clt1, Clt2, sum1, sum2):
        delta_Cst = Cst2 - Cst1
        # temp2_0 = 0.5 * (Cet1 @ (Clt1@(delta_Cst * Ctt1)@Clt2) @ (Cly1/sum1) @ Cdt1 @ Cpt1 + Cet2 @ (Clt1@(delta_Cst * Ctt2)@Clt2) @ (Cly2/sum2) @ Cdt2 @ Cpt2)
        temp2_0 = (0.5 * (Cet1 + Cet2)) @ (Clt2 @ (delta_Cst * (0.5 * (Ctt2 + Ctt1))) @ Clt1) @ (
                    0.5 * ((Cly1 / sum1) + (Cly2 / sum2))) @ (0.5 * (Cdt1 + Cdt2)) @ (0.5 * (Cpt1 + Cpt2))
        return temp2_0.sum()

    def bilateral_trade_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1, Cdt2, Cpt1,
                               Cpt2, Clt1, Clt2):
        delta_Cbt = Cbt2 - Cbt1
        # temp2_0 = 0.5 * (Cet1 @ Clt1 @ ((delta_Cbt * Cat1)/sum1) @ Cdt1 @ Cpt1 + Cet2 @ Clt2 @ ((delta_Cbt * Cat2)/sum2) @ Cdt2 @ Cpt2)
        temp2_0 = (0.5 * (Cet1 + Cet2)) @ (0.5 * (Clt2 + Clt1)) @ (delta_Cbt * (0.5 * (Cat1 + Cat2))) @ (
                    0.5 * (Cdt1 + Cdt2)) @ (0.5 * (Cpt1 + Cpt2))
        return temp2_0.sum()

    def consumption_structure_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1, Cdt2,
                                     Cpt1, Cpt2, Clt1, Clt2):
        delta_Cat = Cat2 - Cat1
        # temp2_0 = 0.5 * (Cet1 @ Clt1 @ ((delta_Cat * Cbt1)/sum1) @ Cdt1 @ Cpt1 + Cet2 @ Clt2 @ ((delta_Cat * Cbt2)/sum2) @ Cdt2 @ Cpt2)
        temp2_0 = (0.5 * (Cet1 + Cet2)) @ (0.5 * (Clt2 + Clt1)) @ (delta_Cat * (0.5 * (Cbt1 + Cbt2))) @ (
                    0.5 * (Cdt1 + Cdt2)) @ (0.5 * (Cpt1 + Cpt2))
        return temp2_0.sum()

    def domestic_consumption_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1, Cdt2,
                                    Cpt1, Cpt2, Clt1, Clt2, sum1, sum2):
        delta_Cdt = Cdt2 - Cdt1
        # temp2_0 = 0.5 * (Cet1 @ Clt1 @ (Cly1/sum1) @ delta_Cdt @ Cpt1 + Cet2 @ Clt2 @ (Cly2/sum2) @ delta_Cdt @ Cpt2)
        temp2_0 = (0.5 * (Cet1 + Cet2)) @ (0.5 * (Clt2 + Clt1)) @ (
                    0.5 * ((Cly1 / sum1) + (Cly2 / sum2))) @ delta_Cdt @ (0.5 * (Cpt1 + Cpt2))
        return temp2_0.sum()

    def price_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1, Cdt2, Cpt1, Cpt2,
                     Clt1, Clt2, sum1, sum2):
        delta_Cpt = Cpt2 - Cpt1
        # temp2_0 = 0.5 * (Cet1 @ Clt1 @ (Cly1/sum1) @ Cdt1@ delta_Cpt + Cet2 @ Clt2 @ (Cly2/sum2)  @ Cdt2 @ delta_Cpt)
        temp2_0 = (0.5 * (Cet1 + Cet2)) @ (0.5 * (Clt2 + Clt1)) @ (0.5 * ((Cly1 / sum1) + (Cly2 / sum2))) @ (
                    0.5 * (Cdt1 + Cdt2)) @ delta_Cpt
        return temp2_0.sum()

    # Berechnung der Effekte
    delta_intensity = intensity_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1,
                                       Cdt2, Cpt1, Cpt2, Clt1, Clt2, sum1, sum2)
    delta_intermediate_trade = intermediate_trade_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2,
                                                         Cat1, Cat2, Cdt1, Cdt2, Cpt1, Cpt2, Clt1, Clt2, sum1, sum2)
    delta_structure = structure_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1,
                                       Cdt2, Cpt1, Cpt2, Clt1, Clt2, sum1, sum2)
    delta_bilateral_trade = bilateral_trade_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1,
                                                   Cat2, Cdt1, Cdt2, Cpt1, Cpt2, Clt1, Clt2)
    delta_consumption_structure = consumption_structure_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1,
                                                               Cbt2, Cat1, Cat2, Cdt1, Cdt2, Cpt1, Cpt2, Clt1, Clt2)
    delta_domestic_consumption = domestic_consumption_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2,
                                                             Cat1, Cat2, Cdt1, Cdt2, Cpt1, Cpt2, Clt1, Clt2, sum1, sum2)
    delta_price = price_effect(Cly1, Cly2, Cet1, Cet2, Ctt1, Ctt2, Cst1, Cst2, Cbt1, Cbt2, Cat1, Cat2, Cdt1, Cdt2, Cpt1,
                               Cpt2, Clt1, Clt2, sum1, sum2)

    # Gesamteffekt
    delta_total = (delta_intermediate_trade + delta_structure + delta_bilateral_trade +
                   delta_consumption_structure + delta_domestic_consumption + delta_price + delta_intensity)

    '''
    # Ausgabe der Ergebnisse
    print(f"Intermediate Trade Effect: {delta_intermediate_trade}")
    print(f"Structure Effect: {delta_structure}")
    print(f"Bilateral Trade Effect: {delta_bilateral_trade}")
    print(f"Consumption Structure Effect: {delta_consumption_structure}")
    print(f"Domestic Consumption Effect: {delta_domestic_consumption}")
    print(f"Price Effect: {delta_price}")
    print(f"Intensity Effect: {delta_intensity}")
    print(f"Total Effect: {delta_total}")
    '''

    effect_round_intermediate_trade = round(delta_intermediate_trade, 3)
    effect_round_structure = round(delta_structure, 3)
    effect_round_bilateral_trade = round(delta_bilateral_trade, 3)
    effect_round_consumption_structure = round(delta_consumption_structure, 3)
    effect_round_domestic_consumption = round(delta_domestic_consumption, 3)
    effect_round_pop = round(delta_price, 3)
    effect_round_intensity = round(delta_intensity, 3)

    #    names_factors = ['Emission intensity', 'Intermediate trade', 'Overall Structure', 'Trade', 'Consumption pattern', 'Consumption volume', 'Population']

    i = 0

    m_results_x[i, 0] = effect_round_intensity
    m_results_x[i, 1] = effect_round_intermediate_trade
    m_results_x[i, 2] = effect_round_structure
    m_results_x[i, 3] = effect_round_bilateral_trade
    m_results_x[i, 4] = effect_round_consumption_structure
    m_results_x[i, 5] = effect_round_domestic_consumption
    m_results_x[i, 6] = effect_round_pop

    return m_results_x, tag
