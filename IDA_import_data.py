import openpyxl
import os

def import_excel_data(sector, period, data_series, start_year, sum_case):

    current_path = os.getcwd()
    #print(current_path)
    #print('pfad gewese')
    excel_file_path = os.path.join(current_path, r'IDA_data\IDA_' + sector + '.xlsx')
    print(excel_file_path)
    workbook = openpyxl.load_workbook(excel_file_path, data_only=True)
    sheet = workbook.active
    two_dimensional_array = []

    for row in sheet.iter_rows(min_row=(0+start_year), max_row=(period+2+start_year), values_only=True):
        two_dimensional_array.append(row)

    desired_rows = list(range(1, period+2))
    desired_columns = list(range(0, data_series+1))

    table_data = []
    filtered_values = []

    for row_index in desired_rows:
        if row_index < len(two_dimensional_array):
            row_data = two_dimensional_array[row_index]
            selected_columns_data = [row_data[col] for col in desired_columns if col < len(row_data)]
            integers_only = [val for val in selected_columns_data if isinstance(val, (int, float))]
            table_data.append([f"Zeile {row_index + 1}"] + integers_only)
            filtered_values.append(integers_only)
        else:
            print(f"Zeile {row_index} existiert nicht im Array.")

    print(filtered_values)
    return filtered_values
