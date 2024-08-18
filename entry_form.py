import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Open Folder Example")
        self.setGeometry(300, 300, 300, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Button to trigger the popup
        open_folder_button = QPushButton("Open Folder", self)
        open_folder_button.clicked.connect(self.show_popup)

        layout.addWidget(open_folder_button)
        self.setLayout(layout)

    def show_popup(self):
        # Create a message box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Open Folder")
        msg_box.setText("Do you want to open the folder?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        # Show the message box and capture the response
        response = msg_box.exec()

        if response == QMessageBox.Yes:
            self.open_folder()

    def open_folder(self):
        folder_path = r'C:\Users\VolkerHome\PycharmProjects\TOAD\plots_Abgabe'  # Replace this with the path to the folder you want to open
        if os.path.exists(folder_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
        else:
            QMessageBox.warning(self, "Error", "The folder does not exist!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
