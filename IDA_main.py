from IDA_import_data import import_excel_data
from IDA_calc import calc_IDA
from IDA_plot import plot_IDA
from IDA_specs import specs_IDA
from IDA_M_Level import lvl_2_sum
from IDALplot_lvl_2 import plot_2_lvl


def ida_main(sector_in, sec_ind, calculation_type):
    #sector_in = input("Choose your IDA (Macro, EI, A, T): ")
    sectors = ['Macro', 'EI', 'A', 'T', 'Custom1', 'Custom2'] #available IDAs
    #sec_ind = sectors.index(sector_in) #Index of chosen IDA
    #print(sec_ind)

    if sector_in == 'Agriculture':
        sector_in = 'A'
    if sector_in == 'Transport':
        sector_in = 'T'
    if sector_in == 'Energy\nIndustries':
        sector_in = 'EI'
    if calculation_type == 'Year-by-year':
        calculation_type = 'yby'
    if calculation_type == 'Cumulative':
        calculation_type = 'cud'

    period, data_series, effects, jahre, spaltennamen, farben, start_year, legend_name, sum_case, colms_2_lvl, col_2_lvl, double_effects, timeframe = specs_IDA(sec_ind, sector_in)
    print('in main mit:')
    print(sector_in)
    '''
    print('----------')


    print(f"legend_name = \"{legend_name}\"")
    print(f"data_series = {data_series}")
    print(f"effects = {effects}")
    print("\nspaltennamen =", spaltennamen)
    print("farben =", farben)

    print('--------------')
    '''

    if sum_case == 1:

        sector_in = 'A1'

        filtered_values = import_excel_data(sector_in, period, data_series, start_year, sum_case)

        #calculation_type = input("Please type in your analysis scope ('yby' for year-by-year or 'cud' for cumulated): ")

        neue_werte_array, zeilen = calc_IDA(filtered_values, calculation_type, effects, period, sum_case)

        sector_in = 'A'

        plot_IDA(neue_werte_array, sector_in, jahre, spaltennamen, farben, legend_name, calculation_type, timeframe)

        array_store = neue_werte_array

        sector_in = 'A2' #crops

        filtered_values = import_excel_data(sector_in, period, data_series, start_year, sum_case)

        neue_werte_array, zeilen = calc_IDA(filtered_values, calculation_type, effects, period, sum_case)

        sector_in = 'A'

        plot_IDA(neue_werte_array, sector_in, jahre, spaltennamen, farben, legend_name, calculation_type, timeframe)

        summed_array = array_store + neue_werte_array

        y_min, y_max = plot_IDA(summed_array, sector_in, jahre, spaltennamen, farben, legend_name, calculation_type, timeframe)

        lvl_2_factors = lvl_2_sum(array_store, neue_werte_array, summed_array, sum_case, zeilen, double_effects, effects)

        plot_2_lvl(lvl_2_factors, double_effects, colms_2_lvl, col_2_lvl, legend_name, jahre, sector_in, y_min, y_max)

    elif sum_case == 0:
        print('test0000')
        filtered_values = import_excel_data(sector_in, period, data_series, start_year, sum_case)
        print('test0')

        #calculation_type = input("Please type in your analysis scope ('yby' for year-by-year or 'cud' for cumulated): ")

        neue_werte_array, zeilen = calc_IDA(filtered_values, calculation_type, effects, period, sum_case)
        print('test1')

        plot_IDA(neue_werte_array, sector_in, jahre, spaltennamen, farben, legend_name, calculation_type, timeframe)

    print('1 is da')

    return 1

