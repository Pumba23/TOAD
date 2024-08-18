# ident_approach.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from sda_scope import SDAScope  # Import der neuen Seite

class IdentApproach(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.sda_type = None  # Instanzvariable für SDA-Typ
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Top Layout für die Buttons
        top_layout = QVBoxLayout()
        top_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Beenden Button hinzufügen
        self.app.add_exit_button(top_layout)

        # Zurück Button hinzufügen
        back_button = self.app.create_button('Zurück')
        back_button.clicked.connect(lambda: self.app.show_page(0))  # Zurück zur Startseite
        top_layout.addWidget(back_button)


        # Center Layout für den Hauptinhalt
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        # Label hinzufügen
        label = QLabel("Choose your SDA Identity")
        label.setStyleSheet('font-size: 50px; color: black;')

        # Spacer Item, um das Label höher zu positionieren
        #spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #center_layout.addItem(spacer)

        center_layout.addWidget(label, alignment=Qt.AlignCenter)

        # Spacer Item, um das Label weiter oben zu halten
        #spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #center_layout.addItem(spacer)

        # Button Layout für die Buttons nebeneinander
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        # Basic Button hinzufügen
        basic_button = self.app.create_button('Fundamental')
        basic_button.clicked.connect(lambda: self.set_sda_type('basic'))
        button_layout.addWidget(basic_button)

        # Extended Button hinzufügen
        extended_button = self.app.create_button('Extended')
        extended_button.clicked.connect(lambda: self.set_sda_type('extended'))
        button_layout.addWidget(extended_button)

        # Button Layout zum Center Layout hinzufügen
        #center_layout.addLayout(button_layout)

        # Layouts zur Hauptlayout hinzufügen
        main_layout.addLayout(top_layout)
        main_layout.addLayout(center_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def set_sda_type(self, sda_type):
        self.sda_type = sda_type
        print(f"SDA Type set to: {self.sda_type}")
        self.app.show_sda_scope_page(self.sda_type)  # Neue Seite anzeigen
