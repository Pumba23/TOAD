import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import os
import openpyxl
import matplotlib.ticker as ticker
from SDA_sector_last import SDA_sector_last


def plot_SDA_new(m_results_years, names_factors, num_factors, plot_period, input0, reg_to_reg_type, sda_type,
                 dekomp_type, tag, day):
    if reg_to_reg_type == 'dom1':
        legend_name = "Fundamental SDA - Demand World Approach"
    if reg_to_reg_type == 'dom2':
        legend_name = "Fundamental SDA - Domestic Demand Approach"
    if reg_to_reg_type == 'cb':
        legend_name = "Fundamental SDA - Consumption-based Approach"
    if reg_to_reg_type == 'pb':
        legend_name = "Fundamental SDA - Production-based Approach"
    if reg_to_reg_type == 'saldo':
        legend_name = "Fundamental SDA - Balanced Approach"
    if reg_to_reg_type == 'from1to2':
        legend_name = "Fundamental SDA - Imports"
    if reg_to_reg_type == 'from2to1':
        legend_name = "Fundamental SDA - Exports"

    array = m_results_years[:, 1:]
    # m_results_years_n_u = np.sum(m_results_years_n_u, axis=0)
    col1 = array.shape[1]
    # Teile das Array in 15 Teile
    teile = np.split(array, col1, axis=1)

    # Staple jeweils drei Teile untereinander
    gestapelte_teile = [np.vstack(teile[i:i + num_factors]) for i in range(0, col1, num_factors)]

    # Füge die gestapelten Teile wieder zusammen
    finales_array = np.hstack(gestapelte_teile)
    finales_array1 = finales_array.T  # jahre auf als zeilen
    print('finaleee')
    print(finales_array1)
    print(finales_array1.shape)
    period1 = col1 / num_factors
    period1 = int(period1)
    print("perio1 iiiiist ------------------------------------")
    print(period1)
    num_factors = int(num_factors)
    plot_array = finales_array1 / 1000000

    last = plot_array[5, :]

    # Aufteilen der negativen und positiven Werte für das Balkendiagramm
    positive_werte = np.maximum(0, plot_array)
    negative_werte = np.minimum(0, plot_array)

    # Größe der Gruppen und Balken
    anzahl_gruppen = plot_period + 1  # erster jahr auch geplottet; zweites + für zerosplotten
    print(anzahl_gruppen)
    breite_gruppe = 1
    breite_balken = 1  # Festlegen einer festen Balkenbreite
    jahre = np.arange(1996, 2022, 5)
    print('jahre:')
    print(jahre)
    sector = reg_to_reg_type

    farben = [
        '#00008B', '#191970', '#000080', '#4169E1', '#4682B4',
        '#6495ED', '#87CEFA', '#87CEEB', '#00CED1', '#1B5E20',
        '#388E3C', '#43A047', '#66BB6A', '#A5D6A7', '#FF9800',
        '#FFD54F', '#FFEB3B', '#FFC107', '#8B0000', '#800000',
        '#B22222', '#A52A2A', '#CD5C5C', '#FF6347', '#FA8072',
        '#FF4500', '#FFC0CB'
    ]

    if sda_type == 'ext':
        farben = ['blue', 'maroon', 'yellow', 'red', 'limegreen', 'lightblue', 'purple']

    names_factors = [
        "Emission intensity Agriculture", "Emission intensity Mining", "Emission intensity Food",
        "Emission intensity Non-energy-intensive manufacturing",
        "Emission intensity Energy-intensive manufacturing", "Emission intensity Electricity and gas",
        "Emission intensity Services", "Emission intensity Transport", "Emission intensity Waste and water supply",

        "Structure Agriculture", "Structure Mining", "Structure Food", "Structure Non-energy-intensive manufacturing",
        "Structure Energy-intensive manufacturing", "Structure Electricity and gas",
        "Structure Services", "Structure Transport", "Structure Waste and water supply",

        "Activity Agriculture", "Activity Mining", "Activity Food", "Activity Non-energy-intensive manufacturing",
        "Activity Energy-intensive manufacturing", "Activity Electricity and gas",
        "Activity Services", "Activity Transport", "Activity Waste and water supply"
    ]

    # Positionen für die Balken
    positionen = np.arange(anzahl_gruppen) * (2 * breite_gruppe)
    now = datetime.datetime.now()
    print(positionen)
    print(names_factors)

    # jahre_filtered = [1996, 2001, 2006, 2011, 2016, 2021]
    # positionen = np.arange(len(jahre_filtered)) * (2 * breite_gruppe)

    # Formatieren des Datums und der Uhrzeit für den Dateinamen
    date_str = now.strftime("%H-%M_%d-%m-%Y")

    plt.rcParams['figure.dpi'] = 1000  # Hier wird die DPI auf 1000 gesetzt

    # Erstellen des Balkendiagramms
    plt.figure(figsize=(16, 9))

    for i, spalte in enumerate(names_factors):
        # Balken für positive Werte
        plt.bar(positionen, positive_werte[:, i], breite_balken,
                bottom=np.sum(positive_werte[:, :i], axis=1),
                label=spalte, color=farben[i], align='center')

        # Balken für negative Werte unter der x-Achse
        plt.bar(positionen, negative_werte[:, i], breite_balken,
                bottom=np.sum(negative_werte[:, :i], axis=1), color=farben[i], align='center')
        # color=farben[i])

        # Berechnen und Eintragen der Summe aller Werte pro Jahr als Punkt
        summe_pro_jahr = np.sum(plot_array, axis=1)
    plt.scatter(positionen, summe_pro_jahr, color='white', edgecolor='black', linewidth=0.5, marker='o', s=35,
                label='Sum', zorder=3)

    # Horizontalen Strich bei y=0 einziehen
    plt.axhline(0, color='black', linewidth=0.5)
    # Anpassen der Achsenbeschriftungen und Legende
    plt.xlabel('Year', labelpad=12, fontsize=20)
    plt.ylabel('MT CO$_{2}$-eq', labelpad=5, fontsize=20)
    plt.title(legend_name, fontsize=20, y=1.02)

    max_negative_zeilen = np.sum(negative_werte, axis=1)
    max_positive_zeilen = np.sum(positive_werte, axis=1)
    max_n = np.min(max_negative_zeilen)
    max_p = np.max(max_positive_zeilen)
    print(max_n)
    print(max_p)
    puffer = (max_p - max_n) * 0.05
    y_min = max_n - puffer
    y_max = max_p + puffer
    plt.ylim(y_min, y_max)
    plt.xlim(-1,
             max(positionen) + breite_balken)  # Annahme: positionen enthält die Positionen der Balken und breite_balken ist die Breite der Balken

    plt.xticks(positionen * breite_balken, jahre, rotation=90, fontsize=12)

    # Raster hinzufügen
    for pos in positionen + breite_balken:
        plt.axvline(x=pos, color='black', linestyle='--', linewidth=0.5)
    # Anzeigen des Diagramms

    # Grid-Einstellungen im Hintergrund
    plt.grid(color='black', axis='y', linestyle='dotted', linewidth=0.5, zorder=0)

    # Sicherstellen, dass das Raster im Hintergrund gezeichnet wird
    plt.gca().set_axisbelow(True)

    plt.axvline(x=(0 - breite_balken), color='black', linestyle='--', linewidth=0.5)
    plt.yticks(fontsize=12)

    plt.tight_layout()
    current_path = os.getcwd()
    folder = os.path.join(current_path, f'plots\{sda_type}_{day}')
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'{tag}_{sda_type}_{dekomp_type}_{legend_name}_at_{date_str}_.png')
    plt.savefig(file_path)  # Hier wird der Plot mit der neuen DPI gespeichert
    # plt.show()

    # legende
    legend_fig = plt.figure(figsize=(16, 9))
    ax_legend = legend_fig.add_subplot(111)
    ax_legend.axis('off')  # Keine Achsen anzeigen

    # Hier den Plot erstellen, um die Legende anzuzeigen
    for i, spalte in enumerate(names_factors):
        ax_legend.bar(0, 0, color=farben[i], label=spalte)

    legend = ax_legend.legend(loc='center', bbox_to_anchor=(0.5, 0.5), ncol=3, fontsize=15)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(1)


    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path1 = os.path.join(folder, f'legende_{tag}_{sda_type}_{dekomp_type}_{legend_name}_at_{date_str}_.png')
    legend_fig.savefig(file_path1, bbox_inches='tight', facecolor='white')

    print("Plot für " + sector + " gedruckt")

    # df3 = pd.DataFrame(m_results_years)
    # folder1 = os.path.join(fr'C:\Users\VolkerHome\PycharmProjects\Mario_calc\results\{sda_type}')
    # file_path1 = os.path.join(folder1, f'at_{date_str}_1_lvl_Decomposition_of_{sda_type}_+_{dekomp_type}_+_{sector}.xlsx')
    # df3.to_excel(file_path1, index=False)

    SDA_sector_last(last, farben, names_factors, tag, sda_type, dekomp_type, legend_name, date_str, day)

    print("Result für " + sector + " gedruckt")

    '''
    plt.figure(figsize=(12, 8))  # Ändere die Abbildungsgröße



    # Plotte die Linien mit angepassten Achsenbeschriftungen und Skalierung
    print("plotarray: ")
    print(plot_array)
    print("period ")
    print(plot_period)
    print("jahre ")
    print(jahre)
    print("transpo: ")
    print(plot_array)


    # Überprüfe die Dimensionen von plot_array und jahre
    print(f"Shape of plot_array: {plot_array.shape}")
    print(f"Length of jahre: {len(jahre)}")

    # Transponiere plot_array, um die Dimensionen zu korrigieren
    plot_array = plot_array.T
    print("transpo: ")
    print(plot_array)
    # Anzahl der Faktoren
    num_factors = plot_array.shape[0]

    # Überprüfe, ob die Länge von names_factors mit der Anzahl der Zeilen in plot_array übereinstimmt
    if len(names_factors) != num_factors:
        raise ValueError(
            "Die Anzahl der Namen in names_factors stimmt nicht mit der Anzahl der Faktoren in plot_array überein.")

    # Plotten der Daten
    for i in range(num_factors):
        plt.plot(jahre, plot_array[i, :], label=names_factors[i], linewidth=2)

    # Berechne die Summe pro Jahr
    summe_pro_jahr = np.sum(plot_array, axis=0)

    # Plotten der Summe
    plt.scatter(jahre, summe_pro_jahr, color='white', edgecolor='black', linewidth=0.3, marker='o', s=35, label='Sum',
                zorder=3)

    plt.title('Verlauf sda', fontsize=20)
    plt.xlabel('Jahr', fontsize=16)
    plt.ylabel('MT CO2 eq', fontsize=16)
    plt.grid(axis='y', linestyle='-', color='gray', linewidth=0.5)
    plt.legend(fontsize=12)
    plt.xticks(rotation=45, fontsize=12)  # Ändere die Größe und Rotation der X-Achsenbeschriftungen
    plt.yticks(fontsize=12)


    plt.tight_layout()

    #hier fodler name

    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'at_{date_str}_verlauf_of_{sda_type}_+_{dekomp_type}_+_{sector}.png')
    plt.savefig(file_path)  # Hier wird der Plot mit der neuen DPI gespeichert
    #plt.show()

    '''
    folder = os.path.join(fr'C:\Users\VolkerHome\PycharmProjects\Mario_calc\plots\{sda_type}')

    return y_min, y_max

