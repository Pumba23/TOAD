import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import os
import openpyxl

def plot_IDA(neue_werte_array, sector, jahre, spaltennamen, farben, legend_name, calculation_type, timeframe):

    # Aufteilen der negativen und positiven Werte für das Balkendiagramm
    #neue_werte_array[25,:] = 0 für transport yby

    positive_werte = np.maximum(0, neue_werte_array)
    negative_werte = np.minimum(0, neue_werte_array)

    # Größe der Gruppen und Balken
    anzahl_gruppen = len(jahre)
    print(anzahl_gruppen)
    breite_gruppe = 1
    breite_balken = 1  # Festlegen einer festen Balkenbreite

    # Positionen für die Balken
    positionen = np.arange(anzahl_gruppen) * (2*breite_gruppe)
    now = datetime.datetime.now()
    print(positionen)

    # Formatieren des Datums und der Uhrzeit für den Dateinamen
    date_str = now.strftime("%H-%M_%d-%m-%Y")

    plt.rcParams['figure.dpi'] = 1000  # Hier wird die DPI auf 1000 gesetzt

    # Erstellen des Balkendiagramms
    plt.figure(figsize=(16, 9))

    for i, spalte in enumerate(spaltennamen):
        # Balken für positive Werte
        plt.bar(positionen, positive_werte[:, i], breite_balken,
                bottom=np.sum(positive_werte[:, :i], axis=1),
                label=spalte, color=farben[i], align='center')

        # Balken für negative Werte unter der x-Achse
        plt.bar(positionen, negative_werte[:, i], breite_balken,
                bottom=np.sum(negative_werte[:, :i], axis=1), color=farben[i], align='center')
               # color=farben[i])

        # Berechnen und Eintragen der Summe aller Werte pro Jahr als Punkt
        summe_pro_jahr = np.sum(neue_werte_array, axis=1)
    plt.scatter(positionen, summe_pro_jahr, color='white', edgecolor='black', linewidth=0.3, marker='o', s=35, label='Sum', zorder=3)

    # Horizontalen Strich bei y=0 einziehen
    plt.axhline(0, color='black', linewidth=0.5)
    # Anpassen der Achsenbeschriftungen und Legende
    plt.xlabel('Year', labelpad=13, fontsize= 22)
    plt.ylabel('MT CO$_{2}$-eq', labelpad=7, fontsize= 22)
    plt.title(legend_name, fontsize= 22, y=1.02)

    legend = plt.legend(loc='lower left', bbox_to_anchor=(0.02, 0.02), fontsize=15)
    pufferval = 0.05

    if sector == 'Macro' and calculation_type == 'yby':
        legend = plt.legend(loc='lower left', bbox_to_anchor=(0.06, 0.015), fontsize=15)
        pufferval = 0.15
        plt.ylabel('MT CO$_{2}$-eq', labelpad=5, fontsize=22)
    if sector == 'A' and calculation_type == 'yby':
        legend = plt.legend(loc='lower left', bbox_to_anchor=(0.095, 0.015), fontsize=15)
        pufferval = 0.15
        plt.ylabel('MT CO$_{2}$-eq', labelpad=5, fontsize=22)
    if sector == 'T' and calculation_type == 'yby':
        legend = plt.legend(loc='upper center', bbox_to_anchor=(0.235, 0.99), ncol = 2, fontsize=15)
        pufferval = 0.15
        plt.ylabel('MT CO$_{2}$-eq', labelpad=5, fontsize=22)


    legend.get_frame().set_facecolor('white')  # Setze den Hintergrund der Legende auf Weiß
    legend.get_frame().set_alpha(1)
    max_negative_zeilen = np.sum(negative_werte, axis=1)
    max_positive_zeilen = np.sum(positive_werte, axis=1)
    max_n = np.min(max_negative_zeilen)
    max_p = np.max(max_positive_zeilen)
    print(max_n)
    print(max_p)
    puffer = (max_p - max_n) * pufferval
    y_min = max_n - puffer
    y_max = max_p + puffer
    plt.ylim(y_min, y_max)
    plt.xlim(-1, max(positionen) + breite_balken)  # Annahme: positionen enthält die Positionen der Balken und breite_balken ist die Breite der Balken


    plt.xticks(positionen*breite_balken, jahre, rotation=90, fontsize= 12)

    if timeframe == 1950:
        xtick_positions = positionen[::5] * breite_balken
        xtick_labels = jahre[::5]
        plt.xticks(xtick_positions, xtick_labels, rotation=90, fontsize=12)  # X-Achse Beschriftung für jedes 10. Jahr

    # Raster hinzufügen
    for pos in positionen + breite_balken:
        plt.axvline(x=pos, color='black', linestyle='--', linewidth=0.5)
    # Anzeigen des Diagramms

    # Dann das Gitter für die Y-Achse hinzufügen
    plt.grid(color='black', axis='y', linestyle='dotted', linewidth=0.5, zorder=0)
    # Sicherstellen, dass das Raster im Hintergrund gezeichnet wird
    plt.gca().set_axisbelow(True)

    plt.axvline(x=(0-breite_balken), color='black', linestyle='--', linewidth=0.5)
    plt.yticks(fontsize = 12)

    if sector == 'A':
        sector = 'Agriculture'
    if sector == 'T':
        sector = 'Transport'
    if sector == 'EI':
        sector = 'Energy industries'


    print("Plot für "+sector+" gedruckt")

    plt.tight_layout()
    current_path = os.getcwd()
    folder = os.path.join(current_path, f'plots', sector)
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'IDA_plot_of_{sector}_{calculation_type}_{timeframe}_at_{date_str}.png')
    plt.savefig(file_path)  # Hier wird der Plot mit der neuen DPI gespeichert
    #plt.show()



    df3 = pd.DataFrame(neue_werte_array)
    folder1 = os.path.join(current_path, f'results', sector)
    if not os.path.exists(folder1):
        os.makedirs(folder1)
    file_path1 = os.path.join(folder1, f'IDA_results_of_{sector}_{timeframe}_{calculation_type}_at_{date_str}.xlsx')
    df3.to_excel(file_path1, index=False)

    print("Result für "+sector+" gedruckt")
    print(file_path1)

    return y_min, y_max
