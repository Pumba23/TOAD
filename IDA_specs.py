from IDA_costum_imp import import_specs

def specs_IDA(sec_ind, sector):
    colms_2_lvl = 0
    col_2_lvl = 0
    #sum_case = 1  # summation of share and productivity effect
    start_year = 23
    double_effects = 0
    start_year = 0
    sum_case = 0

    if sec_ind == 0:

        #timeframe = input("Please type in your timeframe scope ('50' for 1950 - 2022  or '90' for 1991 - 2022): ")
        timeframe = '90'
        if timeframe == '50':
            start = 1950
            timeframe = start
            end = 2023
            period = end - start
            legend_name = "IDA of GHG Emissions - Macro-level 1950"
            jahre = range(start, end + 1)  # last value not included
            start_year = start - 1950 # startyear in excelsheet


        elif timeframe == '90':
            start = 1991
            timeframe = start
            end = 2023
            period = end - start
            legend_name = "IDA of GHG Emissions - Macro-level 1991"
            jahre = range(start, end + 1)  # last value not included
            start_year = start - 1950 + 1  # startyear in excelsheet

        data_series = 5
        effects = 5

        spaltennamen = ['Population effect', 'Affluence effect', 'Technology effect', 'Renewable energy effect',
                        'Fuel mix effect']
        farben = ['purple', 'lightblue', 'blue', 'green', 'yellow']


    elif sec_ind == 1:

        start = 1991
        timeframe = start
        end = 2023
        period = end - start
        legend_name = "IDA of GHG Emissions - Electricity Generation"
        data_series = 6
        effects = 6
        jahre = range(start, end+1)  # last value not included
        spaltennamen = ['Population effect', 'Electricity consumption effect', 'Distribution efficiency effect',
                        'Trade effect', 'Renewable energy sources effect', 'Intensity effect (generation efficiency)']
        farben = ['purple', 'lightblue', 'blue', 'yellow', 'mediumspringgreen', 'red']
        start_year = start-1990+1 # startyear in excelsheet
        


    elif sec_ind == 2:
        start = 1991
        timeframe = start
        end = 2022
        period = end - start
        legend_name = "IDA of GHG Emissions - Agriculture"
        data_series = 5
        effects = 5
        jahre = range(start, end+1)  # last value not included
        spaltennamen = ['Population effect', 'Diet effect', 'Trade effect', 'Food share effect', 'Productivity effect']
        farben = ['purple', 'lightblue', 'yellow', 'green', 'blue']
        colms_2_lvl = ['Food share effect', 'Food share effect animal-based', 'Food share effect plant-based',
                        'Productivity effect', 'Productivity effect animal-based', 'Productivity effect plant-based']
        col_2_lvl = ['limegreen', 'darkgreen', 'springgreen', '#4169E1', 'darkblue', 'lightblue']
        sum_case = 1 #summation of share and productivity effect
        start_year = start - 1990 + 1 # startyear in excelsheet
        double_effects = 2

    elif sec_ind == 3:
        start = 1995
        timeframe = start
        end = 2022
        period = end - start
        #legend_name = "IDA of GHG Emissions - Road Passenger Transport (without 2020)"
        legend_name = "IDA of GHG Emissions - Road Passenger Transport"
        data_series = 9
        effects = 9
        jahre = range(start, end+1)  # last value not included
        spaltennamen = ['Population effect', 'Distance effect', 'Transportation effect',
                        'Occupancy effect', 'Electric vehicle effect', 'Vehicle efficiency effect',
                        'Bio-fuel effect', 'Trade effect', 'Intensity effect (fuel mix)']
        farben = ['purple', 'lightblue', 'orange', 'darkgreen', 'limegreen', 'blue', 'maroon', 'yellow', 'red']
        start_year = start-1990+1 # startyear in excelsheet,

    elif sec_ind == 4:

        # Werte aus import_specs
        start, end, legend_name, data_series, effects, spaltennamen, farben = import_specs(sector)
        timeframe = start
        period = end - start
        jahre = range(start, end + 1)  # last value not included
        start_year = start - 1990 + 1  # startyear in excelsheet


    elif sec_ind == 5:

        start, end, legend_name, data_series, effects, spaltennamen, farben = import_specs(sector)
        timeframe = start
        period = end - start
        jahre = range(start, end+1)  # last value not included
        start_year = start-1990+1 # startyear in excelsheet,




    return period, data_series, effects, jahre, spaltennamen, farben,start_year, legend_name, sum_case, colms_2_lvl, col_2_lvl, double_effects, timeframe