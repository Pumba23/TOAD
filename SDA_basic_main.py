import pandas as pd
import numpy as np
from SDA_read_data import sda_read
from SDA_years import years
from SDA_basic_calc_24 import SDA_calc_new3
from SDA_parse_aggr import parse_aggr
from SDA_basic_mplot import plot_SDA_new
import winsound
import os
from SDA_result_summation import m_sum
from SDA_trade_approach import m_trade
from ghg_sector_diagramm_iot_sorted import iot_sector_plt
from SDA_import_pop import import_excel

def basic_SDA(sda_type, input0, inputend, order, category, selected_sector, order2, dl, callback=None):

    print('__-_________')
    print('sector bums')
    print(dl)

    start = 0
    k = 0
    input0 = int(input0)
    inputend = int(inputend)

    dekomp_type = order2
    reg_to_reg_type = order[0]
    if dekomp_type == 'yby':
        dekomp_type = 'yxy'
    if dekomp_type == 'cud':
        dekomp_type = 'sum'

    category = category[0] #DE
    selected_sector = selected_sector[0]
    print('test ob string')
    print(dekomp_type)


    #if reg_to_reg_type == 'from1to2':
        #case = 6
    #if reg_to_reg_type == 'from2to1':
        #case = 5
    if reg_to_reg_type == 'TBE':
        reg_to_reg_type = 'dom2'
    if reg_to_reg_type == 'PBE':
        reg_to_reg_type = 'pb'
    if reg_to_reg_type == 'CBE':
        reg_to_reg_type = 'cb'
    if reg_to_reg_type == 'BE':
        reg_to_reg_type = 'saldo'

    print(dekomp_type)

    plot_period = inputend - input0
    year0 = input0  # Initialize year0 with the starting year;
    # yeart = year0 + 1

    total_a = np.zeros((1, plot_period + 2))
    m_results_years = np.ndarray((1 * 9, 1), dtype=object)  # empty object for sector names
    m_ghg_curve = np.zeros((1 * 9, 1), dtype=object)  # empty object for ghg storing
    m_years = []

    while start < 2:
        yeart = year0 + 1
        period = year0, yeart
        # print(period)

        if dekomp_type == 'yxy':

            if start == 0:
                num_regions_0, num_sectors_0, world_0, v_sectors_0, v_regions_0 = parse_aggr(year0, category, selected_sector)
                num_regions_t, num_sectors_t, world_t, v_sectors_t, v_regions_t = parse_aggr(yeart, category, selected_sector)
                num_regions_0 = num_regions_0 + 1  # row as region
                m_c_0, m_e_0, m_L_0, m_Y_0, m_all_THG_units = sda_read(world_0)
                pop_0, pop_0_ww = import_excel(year0, category)
                m_c_t, m_e_t, m_L_t, m_Y_t, m_all_THG_units = sda_read(world_t)
                pop_t, pop_t_ww = import_excel(yeart, category)

                for i in range(0, num_sectors_0):  # sector i
                    m_results_years[i, 0] = v_sectors_0[i]

            else:
                m_c_0 = m_c_t
                m_e_0 = m_e_t
                m_L_0 = m_L_t
                m_Y_0 = m_Y_t
                pop_0 = pop_t
                num_regions_0 = num_regions_t
                num_sectors_0 = num_sectors_t
                v_sectors_0 = v_sectors_t
                num_regions_0 = num_regions_0 + 1  # row as region

                num_regions_t, num_sectors_t, world_t, v_sectors_t, v_regions_t = parse_aggr(yeart, category, selected_sector)
                m_c_t, m_e_t, m_L_t, m_Y_t, m_all_THG_units = sda_read(world_t)
                pop_t, pop_t_ww = import_excel(yeart, category)

            print("parsen durch für " + str(period))

            m_results_11, m_results_12, m_results_21, m_results_22, num_factors, list_factors_0, names_factors, m_Y_t_12, tag, total = SDA_calc_new3(
                m_c_0, m_e_0, m_L_0, m_Y_0, m_c_t, m_e_t, m_L_t, m_Y_t, num_regions_0, num_sectors_0, reg_to_reg_type,
                pop_0, pop_t, dl)

        if dekomp_type == 'sum':

            if start == 0:
                print("jahr null kontrolle:")
                print(str(year0))
                num_regions_0, num_sectors_0, world_0, v_sectors_0, v_regions_0 = parse_aggr(year0, category, selected_sector)
                pop_0 = import_excel(year0, category)
                num_regions_0 = num_regions_0 + 1  # row as region
                m_c_0, m_e_0, m_L_0, m_Y_0, m_all_THG_units_0 = sda_read(world_0)

            num_regions_t, num_sectors_t, world_t, v_sectors_t, v_regions_t = parse_aggr(yeart, category, selected_sector)
            num_regions_t = num_regions_t + 1
            m_c_t, m_e_t, m_L_t, m_Y_t, m_all_THG_units_t = sda_read(world_t)
            pop_t = import_excel(yeart, category)

            print("parsen durch für " + str(period))

            if start == 0:

                for i in range(0, num_sectors_0):  # sector i

                    m_results_years[i, 0] = v_sectors_0[i]


            m_results_11, m_results_12, m_results_21, m_results_22, num_factors, list_factors_0, names_factors, m_Y_t_12, tag, total = SDA_calc_new3(
                m_c_0, m_e_0, m_L_0, m_Y_0, m_c_t, m_e_t, m_L_t, m_Y_t, num_regions_0, num_sectors_0, reg_to_reg_type,
                pop_0, pop_t, dl)

        if start == 0:
            m_results, m_c_sum0, m_c_sum = m_trade(reg_to_reg_type, m_results_11, m_results_12, m_results_21,
                                                   m_results_22, m_c_0, m_c_t, start, num_factors)
            m_ghg_curve = np.hstack([m_ghg_curve, m_c_sum0])


        else:
            m_results, m_c_sum = m_trade(reg_to_reg_type, m_results_11, m_results_12, m_results_21, m_results_22, m_c_0,
                                         m_c_t, start, num_factors)

        total_a[0, k] = total

        k = k + 1
        print(str(k) + '. Durchlauf')
        if callback:
            callback(k)
        print('dzrchlazuf---------------------------------------------')


        m_ghg_curve = np.hstack([m_ghg_curve, m_c_sum])
        m_results_years = np.hstack([m_results_years, m_results])
        m_years.append(year0)


        print("rechnung durch für " + str(period))

        print("excel generiert für: " + str(period))

        start, year0 = years(start, year0, inputend)
        period = year0, yeart
        print(period)

        print("wechsel jahr nach: " + str(period))

    m_results_sum, m_print = m_sum(m_results_years, num_factors, plot_period, sda_type)

    date_str = iot_sector_plt(m_ghg_curve, input0, reg_to_reg_type, sda_type, v_sectors_0, plot_period, tag)

    day_month_str = date_str.split('_')[1].split('-')[::-1]
    day = '-'.join(day_month_str)



    df6 = pd.DataFrame(m_print)
    current_path = os.getcwd()
    folder6 = os.path.join(current_path, f'results\{sda_type}_{day}')
    if not os.path.exists(folder6):
        os.makedirs(folder6)
    file_path6 = os.path.join(folder6,
                              f'A_comprised_Results_of_{tag}_{sda_type}_+_{dekomp_type}_+_{reg_to_reg_type}_+_{date_str}.xlsx')

    df6.to_excel(file_path6, index=False)

    df7 = pd.DataFrame(total_a)
    current_path = os.getcwd()
    folder7 = os.path.join(current_path, f'results\{sda_type}_{day}')
    if not os.path.exists(folder7):
        os.makedirs(folder7)
    file_path7 = os.path.join(folder6,
                              f'total effects_of_{tag}_{sda_type}_+_{dekomp_type}_+_{reg_to_reg_type}_+_{date_str}.xlsx')

    df7.to_excel(file_path7, index=False)

    print('hier testdrucke')

    sum5 = np.sum(m_ghg_curve, axis=0)
    sum5 = sum5.reshape(1, -1)  # Zu einer Zeile machen
    length1 = len(sum5[0])
    print(sum5)
    print(length1)

    empty_row = np.zeros((1, length1))  # spalzte
    empty_row = empty_row.reshape(1, -1)  # Zu einer Zeile machen
    print(empty_row)
    print(m_ghg_curve)
    print('jahre')
    print(m_years)


    # Summen als 11. Zeile hinzufügen
    new_array = np.vstack([m_ghg_curve, empty_row, sum5])

    df4 = pd.DataFrame(new_array)
    current_path = os.getcwd()
    folder1 = os.path.join(current_path, f'results\{sda_type}_{day}')
    if not os.path.exists(folder1):
        os.makedirs(folder1)
    file_path1 = os.path.join(folder1,
                              f'GHG_curve_data_of_{tag}_{sda_type}_+_{dekomp_type}_+_{reg_to_reg_type}_+_{date_str}.xlsx')
    df4.to_excel(file_path1, index=False)


    plot_SDA_new(m_results_years, names_factors, num_factors, plot_period, input0, reg_to_reg_type, sda_type,
                 dekomp_type, tag, day)

    print("durchgelaufen. yeah")

    duration = 1000  # Millisekunden
    freq = 600  # Hz (höhere Frequenz für einen höheren Ton)
    repetitions = 5  # Anzahl der Wiederholungen
    for _ in range(repetitions):
        winsound.Beep(freq, duration)

    #print('Programm durchgelaufen. Mit so viel Liiiiiebe <3')


