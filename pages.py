# pages.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QInputDialog
from PySide6.QtCore import Qt
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit
from PySide6.QtCore import Qt

class FirstPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        # Hauptlayout
        main_layout = QVBoxLayout(self)
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.app.add_exit_button(top_layout)


        #infobox
        info_layout = QHBoxLayout()
        info_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.info_label = QLabel("Willkommen in TOAD - Welcome to TOAD<br> <br>Choose your Type of Analysis:")
        self.info_label.setStyleSheet("color: black; font-size: 50px;")  # Farbe und Größe ändern
        self.info_label.setTextFormat(Qt.RichText)  # Setzt das Format auf RichText für HTML-Interpretation
        self.info_label.setAlignment(Qt.AlignCenter)

        info_layout.addWidget(self.info_label)


        # Zentriertes Layout für Buttons
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        # IDA Button
        id_button = self.app.create_button('IDA')
        id_button.clicked.connect(lambda: self.app.show_page(1))
        center_layout.addWidget(id_button)

        # SDA Button
        sda_button = self.app.create_button('SDA')
        sda_button.clicked.connect(lambda: self.app.show_page(2))
        center_layout.addWidget(sda_button)

        center_widget = QWidget()
        center_widget.setLayout(center_layout)

        # Layout zusammenfügen
        main_layout.addLayout(top_layout)
        main_layout.addLayout(info_layout)
        main_layout.addStretch(2)
        main_layout.addWidget(center_widget)
        main_layout.addStretch(3)

        self.setLayout(main_layout)

class IDAPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.app.add_exit_button(layout)

        # Rückkehr-Button
        back_button = self.app.create_button('Zurück')
        back_button.clicked.connect(lambda: self.app.show_page(0))
        layout.addWidget(back_button)

        #infobox
        info1_layout = QHBoxLayout()
        info1_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.info1_label = QLabel("Choose your Analysis (Sector) for IDA:")
        self.info1_label.setStyleSheet("color: black; font-size: 50px;")  # Farbe und Größe ändern
        self.info1_label.setTextFormat(Qt.RichText)  # Setzt das Format auf RichText für HTML-Interpretation
        self.info1_label.setAlignment(Qt.AlignCenter)

        info1_layout.addWidget(self.info1_label)

        # Buttons für IDA-Kategorien
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        buttons_text = ['Macro', 'Energy\nIndustries', 'Agriculture', 'Transport', 'Custom1', 'Custom2']
        for index, text in enumerate(buttons_text):
            button = self.app.create_button(text)
            button.clicked.connect(lambda checked, text=text, index=index: self.app.show_reference_approach(text, index))
            button_layout.addWidget(button)

        layout.addLayout(info1_layout)
        layout.addStretch(1)
        layout.addLayout(button_layout)
        layout.addStretch(1)
        self.setLayout(layout)


from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox, QInputDialog
from PySide6.QtCore import Qt
import os


class SDAPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.app.add_exit_button(layout)

        back_button = self.app.create_button('Zurück')
        back_button.clicked.connect(lambda: self.app.show_page(0))
        layout.addWidget(back_button)

        question_label = QLabel('First use?')
        question_label.setStyleSheet('font-size: 50px; color: black;')
        layout.addWidget(question_label, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        yes_button = self.app.create_button('Yes')
        yes_button.clicked.connect(self.handle_yes)
        button_layout.addWidget(yes_button)

        no_button = self.app.create_button('No')
        no_button.clicked.connect(self.handle_no)
        button_layout.addWidget(no_button)

        layout.addStretch(1)
        layout.addLayout(button_layout)
        layout.addStretch(1)
        self.setLayout(layout)

    def handle_yes(self):
        """Handler für den 'Yes'-Button."""
        current_path = os.getcwd()
        print("Current working directory:", current_path)
        # Create a QMessageBox instance and set its text color to black
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Confirmation')
        msg_box.setText(f'Is this your path?: {current_path}')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        msg_box.setStyleSheet(
            "QLabel{color: black;}"  # Text color of the message
            "QPushButton{color: black;}"  # Text color of the buttons
        )
        reply = msg_box.exec_()

        if reply == QMessageBox.No:
            input_dialog = QInputDialog(self)

            # Setze den Text des Labels, des Eingabefeldes und der Buttons auf schwarz
            input_dialog.setStyleSheet("""
                QLabel { color: black; }        /* Label text */
                QLineEdit { color: black; }     /* Input text */
                QPushButton { color: black; }   /* Button text */
            """)

            # Öffne den Dialog und bekomme den Eingabewert
            current_path, ok = input_dialog.getText(self, 'Input', 'Your own path:')

        # Navigiere zur Download-Seite
        self.app.show_download_page(current_path)  # Übergebe den Pfad  # Angenommen, die Download-Seite ist die vierte Seite im QStackedWidget
        print('hier ist der path: ', current_path)


    def handle_no(self):
        print('wir sind in no')
        self.app.show_page(3)

    def start_new_file(self, file_name, input_text=None):
        import subprocess
        print(f"Starting new file: {file_name} with input_text: {input_text}")
        if input_text:
            process = subprocess.Popen(['python', file_name, input_text])
        else:
            process = subprocess.Popen(['python', file_name])

        if process.poll() is None:
            print(f"{file_name} started successfully.")
        else:
            print(f"Failed to start {file_name}.")

        QMessageBox.information(self, 'Info', f'{file_name} gestartet.')


class ReferenceApproach(QWidget):
    def __init__(self, app, ida_text, ida_index):
        super().__init__()
        self.app = app
        self.ida_text = ida_text
        self.ida_index = ida_index
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        question_label = QLabel(f'Choose an option for {self.ida_text}:')
        question_label.setStyleSheet('font-size: 24px; color: black;')
        layout.addWidget(question_label)

        # Optionsbuttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        buttons_text = ['Option 1', 'Option 2', 'Option 3']
        for text in buttons_text:
            button = self.app.create_button(text)
            button.clicked.connect(lambda checked, text=text: self.start_process(text))
            button_layout.addWidget(button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def start_process(self, selection):
        """Startet den Prozess basierend auf der Auswahl."""
        self.app.start_process(selection)
        QMessageBox.information(self, 'Auswahl', f'Starting process for: {selection}')
