import sys
from PySide6.QtWidgets import QApplication
from ui_components import MyApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.showFullScreen()  # Vollbildmodus aktivieren
    print("Main window shown.")
    sys.exit(app.exec())


 #testung
