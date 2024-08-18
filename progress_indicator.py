from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bitte warten...")
        self.setModal(True)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #C63D2E;")  # Dunkelrot als Hintergrundfarbe
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.spinner_label = QLabel(self)
        pixmap = QPixmap('path/to/your/spinner_image.png')  # Pfad zum Spinner-Bild
        self.spinner_label.setPixmap(pixmap)
        self.spinner_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.spinner_label)
