import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import MultipleLocator

def SDA_sector_last(daten,farben,labels, tag, sda_type, dekomp_type, legend_name, date_str, day):
    num_bars = len(daten)

    labels = [
        'Emission\nintensity',
        'Intermediate\ntrade',
        'Overall\nstructure',
        'Trade',
        'Consumption\npattern',
        'Consumption\nvolume',
        'Population'
    ]

    # Positionen für die Balken
    bar_width = 0.8
    spacing = 0.1  # Abstand zwischen den Balken
    positions = np.arange(num_bars) * (bar_width + spacing)

    plt.rcParams['figure.dpi'] = 1000  # Hier wird die DPI auf 1000 gesetzt
    # Plotten
    plt.figure(figsize=(16, 9))

    # Plotten der Balken
    plt.bar(positions, daten, width=bar_width, color=farben, label=labels)

    # Horizontalen Strich bei y=0 einziehen
    plt.axhline(0, color='black', linewidth=0.5)
    # Anpassen der Achsenbeschriftungen und Legende
    plt.ylabel('MT CO$_{2}$-eq', labelpad=5, fontsize= 20)
    plt.title(f'{legend_name} (2022)', fontsize=20, y=1.02)

    plt.xticks(positions, labels, fontsize= 18)
    for tick in plt.gca().get_xticklabels():
        tick.set_y(-0.005)  # Setzt den Abstand nach unten (negative Werte vergrößern den Abstand)

    plt.gca().tick_params(axis='x', which='both', length=0)  # Entfernt die kleinen Markierungen auf der x-Achse

    plt.gca().yaxis.set_major_locator(MultipleLocator(100))  # Hauptintervalle von 10
    #plt.gca().yaxis.set_minor_locator(MultipleLocator(50))  # Unterintervalle von 2
    plt.grid(color='black', axis='y', linestyle='dotted', linewidth=0.5, zorder=0)

    # Sicherstellen, dass das Raster im Hintergrund gezeichnet wird
    plt.gca().set_axisbelow(True)

    plt.yticks(fontsize = 12)


    # Anzeigen des Plots
    plt.tight_layout()

    current_path = os.getcwd()
    folder = os.path.join(current_path, f'plots\{sda_type}_{day}')
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'whole_sectors_{tag}_{sda_type}_{dekomp_type}_{legend_name}_at_{date_str}_.png')
    plt.savefig(file_path)  # Hier wird der Plot mit der neuen DPI gespeichert
