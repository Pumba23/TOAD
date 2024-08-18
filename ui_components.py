# ui_components.py

import sys
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QPushButton, QMessageBox
from pages import FirstPage, IDAPage, SDAPage
from reference_approach import ReferenceApproach
from ident_approach import IdentApproach
from sda_scope import SDAScope  # Import der neuen Seite
from download_page import DownloadPage  # Import hinzufügen
from ref_approach_sda import RefApproachSDA  # Import der neuen Seite
from final_main_sda import FinalMainSDA
from sda_process_load import SDAProcessLoad  # Import der neuen Seite
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextEdit



class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout erstellen
        self.layout = QVBoxLayout()

        # StackedWidget zur Verwaltung der Ebenen
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Seiten hinzufügen
        self.first_page = FirstPage(self)
        self.ida_page = IDAPage(self)
        self.sda_page = SDAPage(self)
        self.reference_page = None  # Placeholder for reference page
        self.ident_approach_page = IdentApproach(self)  # Seite für IdentApproach
        self.sda_scope_page = None  # Placeholder for SDAScope page
        self.download_page = None  # Placeholder für Download-Seite
        self.ref_approach_sda_page = None  # Placeholder for RefApproachSDA page


        self.stacked_widget.addWidget(self.first_page)
        self.stacked_widget.addWidget(self.ida_page)
        self.stacked_widget.addWidget(self.sda_page)
        self.stacked_widget.addWidget(self.ident_approach_page)



        # Überprüfen Sie die Indizes der Seiten
        print("FirstPage index:", self.stacked_widget.indexOf(self.first_page))
        print("IDAPage index:", self.stacked_widget.indexOf(self.ida_page))
        print("SDAPage index:", self.stacked_widget.indexOf(self.sda_page))
        print("IdentApproach index:", self.stacked_widget.indexOf(self.ident_approach_page))


        # StackedWidget auf die Layout-Seite hinzufügen
        self.setLayout(self.layout)
        self.setWindowTitle('PySide6 Beispiel')
        self.setGeometry(0, 0, 800, 600)  # Setze eine anfängliche Größe


        self.contact_label = QLabel("Contact for help:<br>jonathan.kummer@rwth-aachen.de")
        self.contact_label.setStyleSheet("color: black; font-size: 20px;")  # Farbe und Größe ändern
        self.contact_label.setTextFormat(Qt.RichText)  # Setzt das Format auf RichText für HTML-Interpretation
        self.layout.addWidget(self.contact_label)  # Füge das Label dem Layout hinzu

        # PNG Bild unten rechts hinzufügen
        self.logo_label = QLabel(self)
        image = QImage('C:/Users/VolkerHome/PycharmProjects/TOAD/fcn_ese.png')
        # Skaliere das Bild mit einer bestimmten Filtermethode
        scaled_image = image.scaled(image.width() * 0.3, image.height() * 0.3, Qt.AspectRatioMode.KeepAspectRatio,
                                    Qt.TransformationMode.SmoothTransformation)

        # Konvertiere zurück zu QPixmap
        scaled_pixmap = QPixmap.fromImage(scaled_image)

        # Setze das verkleinerte Bild im QLabel
        self.logo_label.setPixmap(scaled_pixmap)
        self.logo_label.setFixedSize(scaled_pixmap.size())

        # Positionierung des Labels unten rechts
        self.position_logo()

        # Transparent für Mausereignisse machen (optional)
        self.logo_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Fenster im Vollbildmodus öffnen
        self.showFullScreen()

        # Hintergrundfarbe auf dunkelgrün setzen
        self.setStyleSheet('background-color: #DADADA;')
        #self.setStyleSheet('background-color: #DCDCDC;')


    def position_logo(self):
        """Positioniere das Logo unten rechts im Fenster."""
        self.logo_label.move(self.width() - self.logo_label.width()-10, self.height() - self.logo_label.height()-10)

        self.contact_label.move(10,
                                self.height() - self.contact_label.height() - 10)  # 10 Pixel Abstand vom unteren Rand und 10 Pixel vom linken Rand

    def resizeEvent(self, event):
        """Aktualisiere die Position des Logos bei einer Größenänderung des Fensters."""
        self.position_logo()
        super().resizeEvent(event)


    def create_button(self, text):
        button = QPushButton(text)
        button.setFixedSize(120, 120)  # Setze die feste Größe der Buttons
        button.setStyleSheet(

            'background-color: #C63D2E; '
            'border: 2px solid black; '
            'border-radius: 10px;'
            'color: white;'
            'font-size: 16px;'  # Schriftgröße erhöhen
        )  # Button-Stile
        return button

    def add_exit_button(self, layout):
        """ Fügt einen Beenden-Button zum Layout hinzu """
        exit_button = self.create_button('Beenden')
        exit_button.clicked.connect(self.close)  # Beendet die Anwendung
        layout.addWidget(exit_button)

    def show_page(self, index):
        print(f"Attempting to show page at index: {index}")
        self.stacked_widget.setCurrentIndex(index)
        print(f"Current page index is now: {self.stacked_widget.currentIndex()}")

    def show_reference_approach(self, ida_text, ida_index):
        """ Zeigt die Detailseite für einen IDA-Button """
        if self.reference_page:
            self.stacked_widget.removeWidget(self.reference_page)
        self.reference_page = ReferenceApproach(self, ida_text, ida_index)
        self.stacked_widget.addWidget(self.reference_page)
        self.stacked_widget.setCurrentWidget(self.reference_page)

    def start_process(self, selection):
        """ Startet den Prozess basierend auf der Auswahl """
        # Füge hier den Code zum Starten des Prozesses ein
        pass

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec()

    def show_sda_scope_page(self, sda_type):
        """ Zeigt die SDA Scope Seite """
        if self.sda_scope_page:
            self.stacked_widget.removeWidget(self.sda_scope_page)
        self.sda_scope_page = SDAScope(self, sda_type)
        self.stacked_widget.addWidget(self.sda_scope_page)
        self.stacked_widget.setCurrentWidget(self.sda_scope_page)

    def show_download_page(self, path):
        """ Zeigt die Download-Seite mit dem übergebenen Pfad """
        if self.download_page:
            self.stacked_widget.removeWidget(self.download_page)
        self.download_page = DownloadPage(self, path)
        self.stacked_widget.addWidget(self.download_page)
        self.stacked_widget.setCurrentWidget(self.download_page)

    def show_ref_approach_sda_page(self, sda_type, start_year, end_year, selected_demand, selected_region, selected_sector):
        """ Zeigt die RefApproachSDA-Seite mit den übergebenen Informationen """
        if self.ref_approach_sda_page:
            self.stacked_widget.removeWidget(self.ref_approach_sda_page)
        self.ref_approach_sda_page = RefApproachSDA(self, sda_type, start_year, end_year, selected_demand, selected_region, selected_sector)
        self.stacked_widget.addWidget(self.ref_approach_sda_page)
        self.stacked_widget.setCurrentWidget(self.ref_approach_sda_page)

    def show_sda_process_load_page(self, sda_type, start_year, end_year, selected_demand, selected_region, selected_sector, refapp):
        """ Zeigt die SDA Process Load Seite mit den übergebenen Informationen """
        if hasattr(self, 'sda_process_load_page'):
            self.stacked_widget.removeWidget(self.sda_process_load_page)
        self.sda_process_load_page = SDAProcessLoad(self, sda_type, start_year, end_year, selected_demand,
                                                    selected_region, selected_sector, refapp)
        self.stacked_widget.addWidget(self.sda_process_load_page)
        self.stacked_widget.setCurrentWidget(self.sda_process_load_page)


#if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #ex = MyApp()
    #ex.showFullScreen()  # Vollbildmodus aktivieren
    #sys.exit(app.exec())
