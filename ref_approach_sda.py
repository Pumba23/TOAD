# ref_approach_sda.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy, QRadioButton, QButtonGroup
from PySide6.QtCore import Qt
from final_main_sda import FinalMainSDA

class RefApproachSDA(QWidget):
    def __init__(self, app, sda_type, start_year, end_year, selected_demand, selected_region, selected_sector):
        super().__init__()
        self.app = app
        self.sda_type = sda_type
        self.start_year = start_year
        self.end_year = end_year
        self.selected_demand = selected_demand
        self.selected_region = selected_region
        self.selected_sector = selected_sector
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
        label = QLabel("Choose your Reference Approach")
        label.setStyleSheet('font-size: 50px; color: black;')  # Schriftgröße erhöht

        # Spacer Item, um das Label höher zu positionieren
        #spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #center_layout.addItem(spacer)

        center_layout.addWidget(label, alignment=Qt.AlignCenter)

        # Spacer Item, um das Label weiter oben zu halten
        spacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)  # Abstand erhöht
        center_layout.addItem(spacer)

        # Anzeige der übergebenen Informationen
        if self.sda_type == 'basic':
            sda_type = 'Fundamental'

        if self.sda_type == 'extended':
            sda_type = 'Extended'

        info_label = QLabel(f"SDA Type: {sda_type}\nStart Year: {self.start_year}\nEnd Year: {self.end_year}\n"
                            f"Selected Demand: {', '.join(self.selected_demand)}\nSelected Region: {', '.join(self.selected_region)}\n"
                            f"Selected Demand: {', '.join(self.selected_sector)}")
        info_label.setStyleSheet('font-size: 25px; color: black;')  # Schriftgröße erhöht

        center_layout.addWidget(info_label, alignment=Qt.AlignCenter)

        # Spacer Item zwischen den Zonen
        spacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)  # Abstand erhöht
        center_layout.addItem(spacer)

        # Radio Buttons für D&L polar und D&L detailed
        self.radio_button_group = QButtonGroup(self)
        radio_layout = QHBoxLayout()
        radio_layout.setAlignment(Qt.AlignCenter)

        self.dl_polar_radio = QRadioButton("D&L polar")
        self.dl_polar_radio.setChecked(True)
        self.dl_polar_radio.setStyleSheet('font-size: 25px; color: black;')  # Schriftgröße erhöht

        self.dl_detailed_radio = QRadioButton("D&L detailed")
        self.dl_detailed_radio.setStyleSheet('font-size: 25px; color: black;')  # Schriftgröße erhöht

        self.radio_button_group.addButton(self.dl_polar_radio)
        self.radio_button_group.addButton(self.dl_detailed_radio)

        radio_layout.addWidget(self.dl_polar_radio)
        radio_layout.addWidget(self.dl_detailed_radio)

        center_layout.addLayout(radio_layout)

        # Spacer Item zwischen den Zonen
        spacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)  # Abstand erhöht
        center_layout.addItem(spacer)

        # Button Layout für die Buttons nebeneinander
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        # Year-by-Year Button hinzufügen
        year_by_year_button = self.app.create_button('Year-by-year')
        year_by_year_button.clicked.connect(lambda: self.on_continue('yby'))
        button_layout.addWidget(year_by_year_button)

        # Cumulative Button hinzufügen
        cumulative_button = self.app.create_button('Cumulative')
        cumulative_button.clicked.connect(lambda: self.on_continue('cud'))
        button_layout.addWidget(cumulative_button)

        # Button Layout zum Center Layout hinzufügen
        #center_layout.addLayout(button_layout)

        # Layouts zur Hauptlayout hinzufügen
        main_layout.addLayout(top_layout)
        #main_layout.addStretch(1)
        main_layout.addLayout(center_layout)
        #main_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

        # Ausgabe der gesammelten Informationen
        print(f"SDA Type: {self.sda_type}")
        print(f"Start Year: {self.start_year}")
        print(f"End Year: {self.end_year}")
        print(f"Selected Demand: {', '.join(self.selected_demand)}")
        print(f"Selected Region: {', '.join(self.selected_region)}")
        print(f"Selected Region: {', '.join(self.selected_sector)}")


    #def on_continue(self, refapp):
     #   FinalMainSDA(self.sda_type, self.start_year, self.end_year, self.selected_demand, self.selected_region, refapp)

    def on_continue(self, refapp):
        self.app.show_sda_process_load_page(self.sda_type, self.start_year, self.end_year, self.selected_demand,
                                            self.selected_region, self.selected_sector, refapp)
