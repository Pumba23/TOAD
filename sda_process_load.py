# sda_process_load.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QMessageBox
from PySide6.QtCore import QThread, Signal, Slot, Qt
from SDA_basic_main import basic_SDA  # Import der Funktion
from SDA_basic_main3 import basic_SDA3
from SDA_extended_main import ext_SDA  # Import der Funktion
import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

class WorkerThread(QThread):
    progress = Signal(int)
    finished = Signal()

    def __init__(self, sda_type, start_year, end_year, selected_demand, selected_region, selected_sector, refapp, dl, plot):
        super().__init__()
        self.sda_type = sda_type
        self.start_year = start_year
        self.end_year = end_year
        self.selected_demand = selected_demand
        self.selected_region = selected_region
        self.selected_sector = selected_sector
        self.dl = dl
        self.plot = plot
        self.refapp = refapp

    def run(self):
        # Rufe die basic_SDA-Funktion auf und übergebe die notwendigen Parameter
        if self.sda_type == 'basic':
            if self.plot == 'aggregated':
                basic_SDA(self.sda_type, self.start_year, self.end_year, self.selected_demand, self.selected_region, self.selected_sector, self.refapp, self.dl, self.update_progress_callback)
            if self.plot == 'sectoral':
                self.start_year = 1996
                self.end_year = 2021
                basic_SDA3(self.sda_type, self.start_year, self.end_year, self.selected_demand, self.selected_region,
                          self.selected_sector, self.refapp, self.dl, self.update_progress_callback)

        if self.sda_type == 'extended':
            ext_SDA(self.sda_type, self.start_year, self.end_year, self.selected_demand, self.selected_region, self.selected_sector, self.refapp, self.dl, self.update_progress_callback)

        self.finished.emit()

    def update_progress_callback(self, k):
        # Diese Methode wird von basic_SDA aufgerufen, um den Fortschritt zu aktualisieren
        self.progress.emit(k)
class SDAProcessLoad(QWidget):
    def __init__(self, app, sda_type, start_year, end_year, selected_demand, selected_region, selected_sector, refapp, dl, plot):
        super().__init__()
        self.finished = False  # Statusvariable hinzufügen
        self.app = app
        self.sda_type = sda_type
        self.start_year = start_year
        self.end_year = end_year
        self.selected_demand = selected_demand
        self.selected_region = selected_region
        self.selected_sector = selected_sector
        self.refapp = refapp
        self.dl = dl
        self.plot = plot
        self.period_pro = int(end_year) - int(start_year)
        self.initUI()



    def initUI(self):
        main_layout = QVBoxLayout()

        # Top Layout für die Buttons
        top_layout = QVBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Beenden Button hinzufügen
        self.app.add_exit_button(top_layout)

        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)

        # Center Layout für den Hauptinhalt
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        # Label hinzufügen
        label = QLabel("Processing SDA")
        label.setStyleSheet('font-size: 50px; color: black;')
        center_layout.addWidget(label, alignment=Qt.AlignCenter)

        # Fortschrittsbalken hinzufügen
        len5 = self.period_pro+1
        print('länge für anzeige-------------------------')
        print(len5)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, len5)  # Setze den Bereich passend zur Anzahl der Schritte
        self.progress_bar.setFixedSize(400, 40)  # Breite: 400px, Höhe: 40px
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid black;  /* Randfarbe */
                border-radius: 5px;       /* Abgerundete Ecken */
                text-align: center;       /* Text zentrieren */
                       color: black;             /* Textfarbe */
                font-size: 18px;          /* Textgröße */
            }
            QProgressBar::chunk {
                background-color: #C63D2E; /* Farbe des Fortschritts (grün) */
                width: 20px;               /* Breite des Fortschrittsstücks */
            }
        """)

        center_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        main_layout.addLayout(center_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

        self.start_process()

    def start_process(self):
        self.worker_thread = WorkerThread(self.sda_type, self.start_year, self.end_year, self.selected_demand, self.selected_region, self.selected_sector, self.refapp, self.dl, self.plot)
        self.worker_thread.progress.connect(self.update_progress)
        k = 0
        self.worker_thread.start()
        self.worker_thread.finished.connect(self.work_finished)


    @Slot(int)
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    @Slot()
    def work_finished(self):
        print('hier test - shop gepoppt upt?')
        if self.finished:
            return  # Verhindert das erneute Ausführen der Funktion
        self.finished = True

        len5 = self.period_pro+1
        self.progress_bar.setValue(len5)
        msg_box1 = QMessageBox()
        msg_box1.setIcon(QMessageBox.Information)
        msg_box1.setWindowTitle("Success")
        msg_box1.setText(f'SDA processing is complete!')
        print('hier da1?')
        #msg_box1.move(self.geometry().center() - msg_box1.rect().center())
        msg_box1.exec()
        # QMessageBox.information(self, "Success", f'IDA: {self.ida_text} complete')

        self.show_popup()
        print('hier da2?')
        self.app.show_page(0)


    def show_popup(self):
        # Create a message box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Open Folder")
        msg_box.setText("Do you want to open the corresponding folder?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        #msg_box.move(self.geometry().center() - msg_box.rect().center())

        # Show the message box and capture the response
        response = msg_box.exec()

        if response == QMessageBox.Yes:
            self.open_folder()


    def open_folder(self):
        current_path = os.getcwd()
        folder_path = os.path.join(current_path, f'plots')  # Replace this with the path to the folder you want to open
        if os.path.exists(folder_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
        else:
            QMessageBox.warning(self, "Error", "The folder does not exist!")

