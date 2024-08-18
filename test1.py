import openpyxl
import os

current_path = os.getcwd()
path1 = os.path.join(current_path, f'SDA_specs')

excel_file_path = os.path.join(path1, f'sector_names.xlsx')
# Excel-Datei laden
wb = openpyxl.load_workbook(excel_file_path)
ws = wb.active

erste_zeile = [cell.value for cell in ws[1]]

# Ausgabe der Liste
print(erste_zeile)