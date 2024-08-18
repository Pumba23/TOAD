from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from IDA_main import ida_main
from progress_dialog import ProgressDialog  # Import der ProgressDialog-Klasse
import os
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl


class ReferenceApproach(QWidget):
    def __init__(self, app, ida_text, ida_index):
        super().__init__()
        self.app = app
        self.ida_text = ida_text
        self.ida_index = ida_index
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.app.add_exit_button(layout)  # Beenden-Button hinzufügen

        back_button = self.app.create_button('Zurück')
        back_button.clicked.connect(lambda: self.app.show_page(1))  # Zurück zur IDA-Seite
        layout.addWidget(back_button)

        #infobox
        infor_layout = QHBoxLayout()
        infor_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.infor_label = QLabel("Choose the Reference Approach of your Analysis:")
        self.infor_label.setStyleSheet("color: black; font-size: 50px;")  # Farbe und Größe ändern
        self.infor_label.setTextFormat(Qt.RichText)  # Setzt das Format auf RichText für HTML-Interpretation
        self.infor_label.setAlignment(Qt.AlignCenter)

        infor_layout.addWidget(self.infor_label)

        # Erstellen und Anpassen des Labels zur Anzeige der Sektor-Information
        #question_label = QLabel(f'You selected: {self.ida_text} (Index: {self.ida_index})\nChoose an option:')
        #font = QFont()
        #font.setPointSize(24)  # Schriftgröße auf 24 Punkte setzen
        #question_label.setFont(font)
        #question_label.setStyleSheet('color: white;')  # Schriftfarbe anpassen
        #layout.addWidget(question_label)
        layout.addLayout(infor_layout)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        year_by_year_button = self.app.create_button('Year-by-year')
        year_by_year_button.clicked.connect(lambda: self.start_process('Year-by-year'))
        button_layout.addWidget(year_by_year_button)

        cumulative_button = self.app.create_button('Cumulative')
        cumulative_button.clicked.connect(lambda: self.start_process('Cumulative'))
        button_layout.addWidget(cumulative_button)

        layout.addStretch(2)
        layout.addLayout(button_layout)

        layout.addStretch(3)
        self.setLayout(layout)

    def start_process(self, selection):
        # Create and show the progress dialog
        self.progress_dialog = ProgressDialog()
        self.progress_dialog.show()

        # Start the background processing
        self.thread = ProcessingThread(self.ida_text, self.ida_index, selection)
        self.thread.finished.connect(self.on_processing_finished)
        self.thread.start()

    def on_processing_finished(self, result):
        self.progress_dialog.stop()
        if result == 1:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Success")
            msg_box.setText(f'IDA: {self.ida_text} complete')
            #msg_box.move(self.geometry().center() - msg_box.rect().center())
            msg_box.exec()
            #QMessageBox.information(self, "Success", f'IDA: {self.ida_text} complete')
            self.show_popup()

        else:
            QMessageBox.warning(self, "Warning", "Processing did not complete as expected.")




    def show_popup(self):
        # Create a message box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Open Folder")
        msg_box.setText("Do you want to open the corresponding folder?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)



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




class ProcessingThread(QThread):
    finished = Signal(int)

    def __init__(self, ida_text, ida_index, selection):
        super().__init__()
        self.ida_text = ida_text
        self.ida_index = ida_index
        self.selection = selection

    def run(self):
        try:
            print('wo kommt der bumsindex her?')
            print(self.ida_index)
            result = ida_main(self.ida_text, self.ida_index, self.selection)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(-1)  # Verwende -1 oder einen anderen Fehlercode

