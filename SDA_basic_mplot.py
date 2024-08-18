import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
from SDA_ext_sector_last import SDA_sector_last


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

    m_results_years_n_u = m_results_years[:, 1:]
    m_results_years_n_u = np.sum(m_results_years_n_u, axis=0)
    period1 = len(m_results_years_n_u) / num_factors
    period1 = int(period1)
    num_factors = int(num_factors)
    plot_array = m_results_years_n_u.reshape((period1, num_factors)) / 1000000

    last = plot_array[period1 - 1, :]

    # Aufteilen der negativen und positiven Werte für das Balkendiagramm
    positive_werte = np.maximum(0, plot_array)
    negative_werte = np.minimum(0, plot_array)

    # Größe der Gruppen und Balken
    anzahl_gruppen = plot_period + 1 + 1  # erster jahr auch geplottet; zweites + für zerosplotten
    print(anzahl_gruppen)
    breite_gruppe = 1
    breite_balken = 1  # Festlegen einer festen Balkenbreite
    jahre = range(input0, input0 + period1)
    sector = reg_to_reg_type
    farben = ['blue', 'yellow', 'lightblue']
    if sda_type == 'ext':
        farben = ['blue', 'maroon', 'yellow', 'red', 'limegreen', 'lightblue', 'purple']

    # Positionen für die Balken
    positionen = np.arange(anzahl_gruppen) * (2 * breite_gruppe)
    now = datetime.datetime.now()
    print(positionen)
    print(names_factors)

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

    legend = plt.legend(loc='lower left', bbox_to_anchor=(0.02, 0.03), fontsize=15)

    if reg_to_reg_type == 'cb' and dekomp_type == 'yxy':
        legend = plt.legend(loc='upper center', bbox_to_anchor=(0.9, 0.98), fontsize=15)
    if reg_to_reg_type == 'saldo' and dekomp_type == 'yxy':
        legend = plt.legend(loc='upper center', bbox_to_anchor=(0.9, 0.98), fontsize=15)
    if reg_to_reg_type == 'dom2' and dekomp_type == 'yxy':
        legend = plt.legend(loc='upper center', bbox_to_anchor=(0.9, 0.98), fontsize=15)
    if reg_to_reg_type == 'from1to2' and dekomp_type == 'yxy':
        legend = plt.legend(loc='upper center', bbox_to_anchor=(0.9, 0.98), fontsize=15)
    if reg_to_reg_type == 'pb' and dekomp_type == 'yxy':
        legend = plt.legend(loc='upper center', bbox_to_anchor=(0.9, 0.98), fontsize=15)

    legend.get_frame().set_facecolor('white')  # Setze den Hintergrund der Legende auf Weiß
    legend.get_frame().set_alpha(1)
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

    if sda_type == 'ext':
        SDA_sector_last(last, farben, names_factors, tag, sda_type, dekomp_type, legend_name, date_str, day)

    print("Plot für " + sector + " gedruckt")

    print("Result für " + sector + " gedruckt")

    folder = os.path.join(fr'C:\Users\VolkerHome\PycharmProjects\Mario_calc\plots\{sda_type}')

    return y_min, y_max

