import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
import pandas as pd

def plot_2_lvl(lvl_2_factors, double_effects, colms_2_lvl, col_2_lvl, legend_name, jahre, sector, y_min, y_max):


    # Beispielarray erstellen (10 Zeilen, 6 Spalten) mit negativen Werten
    data = lvl_2_factors

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    # Anzahl der Zeilen und Spalten im Array
    num_rows, num_cols = data.shape

    # Positionen der Balken für jede Zeile
    row_indices = np.arange(num_rows)

    # Balkendiagramm erstellen
    fig, ax = plt.subplots(figsize=(16, 9))

    # Breite der Balken
    bar_width = 0.1
    # Balken für jede Spalte und Zeile erstellen
    for col in range(num_cols):
        if col < num_cols / double_effects:
            ax.bar(row_indices + col * bar_width, data[:, col], bar_width, label=colms_2_lvl[col], color=col_2_lvl[col],
                   align='center')

        else:
            ax.bar(row_indices + 0.1 + col * bar_width, data[:, col], bar_width, label=colms_2_lvl[col],
                   color=col_2_lvl[col], align='center')

    #plt.ylim(y_min, y_max)
    # Horizontalen Strich bei y=0 einziehen
    # Gitterlinien für jeden ganzen Y-Wert hinzufügen
    ax.set_yticks(np.arange(int(data.min()), int(data.max()) + 1))
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5)

    ax.axhline(0, color='black', linewidth=0.5)
    # Anpassen der Achsenbeschriftungen und Legende
    ax.set_xlabel('Year', labelpad=12, fontsize= 22)
    ax.set_ylabel('MT CO$_{2}$-eq', labelpad=5, fontsize= 22)
    ax.set_title('Second-level IDA - Agriculture (Food share & Productivity effect) ', fontsize=20, y=1.02)
    plt.xticks(row_indices + bar_width * (num_cols - 1) / 2, jahre, rotation=90, fontsize=12)
    ax.legend(fontsize=15)

    plt.tight_layout()
    folder = os.path.join(r'C:\Users\VolkerHome\PycharmProjects\TOAD\plots_Abgabe', sector)
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'_Abgabe_plot_of_{sector}_at_{date_str}_lvl_2.png')
    plt.savefig(file_path)  # Hier wird der Plot mit der neuen DPI gespeichert

    df3 = pd.DataFrame(data)
    folder1 = os.path.join(r'C:\Users\VolkerHome\PycharmProjects\TOAD\results_Abgabe', sector)
    if not os.path.exists(folder1):
        os.makedirs(folder1)
    file_path1 = os.path.join(folder1, f'_Abgabe_2_lvl_Decomposition_of_{sector}_at_{date_str}.xlsx')
    df3.to_excel(file_path1, index=False)

