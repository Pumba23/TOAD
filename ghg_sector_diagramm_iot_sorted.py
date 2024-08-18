
import numpy as np
import matplotlib.pyplot as plt
import datetime
import re
import os

def iot_sector_plt(m_ghg_curve, input0, reg_to_reg_type, sda_type, v_sectors_0, period, tag):


    now = datetime.datetime.now()
    date_str = now.strftime("%H-%M_%d-%m-%Y")
    day_month_str = date_str.split('_')[1].split('-')[::-1]
    day = '-'.join(day_month_str)

    plt.rcParams['figure.dpi'] = 1000  # Hier wird die DPI auf 1000 gesetzt

    labels = v_sectors_0
    #print("label test1")
    #print(v_sectors_0)
    labels = [re.sub(r'[\d-]+', '', string) for string in labels]
    #print("label test2")
    #print(labels)
    colors = ['green', 'red', 'lime', 'maroon', 'orange', 'blue', 'yellow', 'lightblue', 'purple']
    labels = ['Agriculture', 'Mining', 'Food', 'Non-energy-intensive manufacturing',
                      'Energy-intensive manufacturing', 'Electricity and gas', 'Services', 'Transport',
                      'Waste and wastewater supply']

    m_ghg_curve = m_ghg_curve.T

    num_cols = m_ghg_curve.shape[1]
    jahre = range(input0, input0+period+1+1)
    # Erstelle das Balkendiagramm
    plt.figure(figsize=(16, 9))
    anzahl_gruppen = len(jahre)
    breite_gruppe = 0.75  # Breite der Gruppen
    positionen = np.arange(anzahl_gruppen)  # Positionen der Balken
    x = anzahl_gruppen
    #print("ghg curve:")
    #print(m_ghg_curve)
    m_ghg_curve = m_ghg_curve[1:x + 1, :].astype(np.int64)
    m_ghg_curve = m_ghg_curve/1000


    new_order = [6, 1, 5, 3, 4, 0, 7, 2, 8]
    new_order = [5, 1, 4, 3, 6, 7, 0, 2, 8]

    m_ghg_curve = m_ghg_curve[:, new_order]


    def reorder_list(original_list, new_order):
        return [original_list[i] for i in new_order]


    colors = reorder_list(colors, new_order)
    labels = reorder_list(labels, new_order)

    #print('HIER sind die sektorenwerte: ')
    #print(m_ghg_curve)

    for i in range(0, num_cols):

        # Balken für positive Werte
        plt.bar(positionen, m_ghg_curve[:, i], breite_gruppe,
                bottom=np.sum(m_ghg_curve[:, :i], axis=1),
                label=labels[i], color=colors[i], align='center')

    if reg_to_reg_type == 'saldo':
        title = 'Balanced Approach'
    if reg_to_reg_type == 'cb':
        title = 'Consumption-based Approach'
    if reg_to_reg_type == 'pb':
        title = 'Production-based Approach'
    if reg_to_reg_type == 'dom2':
        title = 'Domestic Demand Approach'
    if reg_to_reg_type == 'dom1':
        title = 'Domestic Consumption RoW'
    if reg_to_reg_type == 'from1to2':
        title = 'Imports Germany'
    if reg_to_reg_type == 'from2to1':
        title = 'Exports Germany'

    plt.xlabel('Year', labelpad=12, fontsize=22)
    plt.ylabel('MT CO$_{2}$-eq', labelpad=5, fontsize=22)
    plt.title('Development of overall GHG Emissions in Germany - ' + title + ' (IOT)', fontsize=22)

    plt.xticks(positionen, jahre, rotation=90, fontsize=12)
    plt.yticks(fontsize=12)

    legend = plt.legend(loc='upper center', bbox_to_anchor=(0.67, 0.98), ncol=2, fontsize=15)
    legend.get_frame().set_facecolor('white')  # Setze den Hintergrund der Legende auf Weiß
    legend.get_frame().set_alpha(1)

    plt.ylim(0, 1400000)   # y-skala vergleichbar machen

    # Grid-Einstellungen im Hintergrund
    plt.grid(color='black', axis='y', linestyle='dotted', linewidth=0.8, zorder=0)

    # Sicherstellen, dass das Raster im Hintergrund gezeichnet wird
    plt.gca().set_axisbelow(True)

    plt.tight_layout()
    current_path = os.getcwd()
    folder = os.path.join(current_path, f'plots\{sda_type}_{day}')
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'ghg_curve_at_{tag}_{date_str}_verlauf_of_{sda_type}_+_{sda_type}.png')
    plt.savefig(file_path)  # Hier wird der Plot mit der neuen DPI gespeichert
    # plt.show()

    return date_str