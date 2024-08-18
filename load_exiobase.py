import os
import pymrio
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fortschrittsanzeige Beispiel")

        # Erstelle den Fortschrittsbalken
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 25)  # Setze den Bereich passend zur Anzahl der Jahre
        self.progress_bar.setFixedSize(400, 40)  # Breite: 400px, Höhe: 40px

        # Erstelle einen Start-Button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_work)

        # Layout und Widget
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_work(self):
        self.start_button.setEnabled(False)
        input_path = os.getcwd()
        year1 = 1996

        for i in range(26):
            exio3_folder = os.path.join(input_path, 'EXIO3_IXI')
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
            self.progress_bar.setValue(i)

            # Jahre aktualisieren
            year1 += 1

            # Simulate some delay to see the progress
            time.sleep(1)

        self.progress_bar.setValue(25)
        self.start_button.setEnabled(True)
        print("Arbeit abgeschlossen!")

def create_progress_window():
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication instance does not exist. Please ensure QApplication is created before calling this function.")
    window = MainWindow()
    window.show()
    print("Main window shown.")
    return window
