from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class ConfirmationPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.app.add_exit_button(layout)  # Beenden-Button hinzufügen

        # Layout für die Ja/Nein-Abfrage
        question_layout = QVBoxLayout()
        question_label = QPushButton("Möchten Sie fortfahren?")
        question_label.setEnabled(False)  # Label statt Button für Frage
        question_layout.addWidget(question_label)

        button_layout = QHBoxLayout()  # Layout für Ja/Nein-Buttons
        button_layout.setAlignment(Qt.AlignCenter)

        yes_button = self.app.create_button('Ja')
        yes_button.clicked.connect(self.on_yes_clicked)
        button_layout.addWidget(yes_button)

        no_button = self.app.create_button('Nein')
        no_button.clicked.connect(self.on_no_clicked)
        button_layout.addWidget(no_button)

        question_layout.addLayout(button_layout)
        layout.addLayout(question_layout)
        self.setLayout(layout)

    def on_yes_clicked(self):
        # Aktion bei "Ja" (hier z.B. Seite wechseln)
        self.app.show_message("Sie haben 'Ja' gewählt.")
        # Hier könntest du z.B. die nächste Seite zeigen
        # self.app.show_page(3)  # Annahme: Die Seite mit Index 3 ist die nächste Seite

    def on_no_clicked(self):
        # Aktion bei "Nein" (hier z.B. Zurück zur vorherigen Seite)
        self.app.show_message("Sie haben 'Nein' gewählt.")
        self.app.show_page(0)  # Zurück zur ersten Seite, z.B.
