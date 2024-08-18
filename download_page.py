# download_page.py

import os
import pymrio
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QMessageBox, QPushButton
from PySide6.QtCore import QThread, Signal, Slot, Qt

class WorkerThread(QThread):
    # Signal für Fortschrittsaktualisierungen
    progress = Signal(int)
    finished = Signal()

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        input_path = self.path
        print('in der run funktion mit:', input_path)
        year1 = 1996

        for i in range(27):
            exio3_folder = os.path.join(input_path, 'EXIO3_IXI')
            print('in der for mit', exio3_folder)
            try:
                exio_downloadlog = pymrio.download_exiobase3(
                    storage_folder=exio3_folder,
                    system="ixi",
                    years=[year1]
                )
            except Exception as e:
                print(f"Error during download: {e}")
                break

            # Fortschritt an GUI übermitteln
            self.progress.emit(i)

            # Jahre aktualisieren
            year1 += 1

        # Arbeitsabschluss signalisieren
        self.finished.emit()

class DownloadPage(QWidget):
    def __init__(self, app, path):
        super().__init__()
        self.app = app
        self.path = path  # Speichere den übergebenen Pfad
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Top Layout für die Buttons
        top_layout = QVBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Beenden Button hinzufügen
        self.app.add_exit_button(top_layout)

        # Zurück Button hinzufügen
        back_button = self.app.create_button('Zurück')
        back_button.clicked.connect(lambda: self.app.show_page(0))  # Zurück zur Startseite
        top_layout.addWidget(back_button)

        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)

        # Center Layout für den Hauptinhalt
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        # Label hinzufügen
        label = QLabel("Download Exiobase")
        label.setStyleSheet('font-size: 50px; color: black;')
        center_layout.addWidget(label, alignment=Qt.AlignCenter)

        # Fortschrittsbalken hinzufügen
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 26)  # Setze den Bereich passend zur Anzahl der Jahre
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

        self.start_download_process()

    def start_download_process(self):
        self.worker_thread = WorkerThread(self.path)
        self.worker_thread.progress.connect(self.update_progress)
        self.worker_thread.finished.connect(self.work_finished)
        self.worker_thread.start()

    @Slot(int)
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    @Slot()
    def work_finished(self):
        self.progress_bar.setValue(26)
        QMessageBox.information(self, 'Download complete', 'Download succesful!')
        self.app.show_page(3)  # Wechsle zur nächsten Seite (angenommen, die nächste Seite ist die vierte Seite im QStackedWidget)
