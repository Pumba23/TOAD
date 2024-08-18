from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt, QTimer


class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Decomposition in progress')
        self.setFixedSize(250, 250)  # Set a fixed size for the dialog



        layout = QVBoxLayout(self)

        # Set up QLabel and its background color
        self.spinner_label = QLabel(self)

        layout.addWidget(self.spinner_label, alignment=Qt.AlignCenter)

        # Set up QMovie
        self.movie = QMovie('C:/Users/VolkerHome/PycharmProjects/TOAD/spinner_image.gif')
        if not self.movie.isValid():
            print("Movie file is not valid")
        else:
            print("Movie file is valid")

        self.spinner_label.setMovie(self.movie)
        self.movie.frameChanged.connect(self.on_frame_changed)

        # Debugging: Check movie state regularly
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_movie_state)
        self.timer.start(100)  # Check every second

        # Start the movie and ensure it is running
        self.movie.start()
        print("Movie started")

    def on_frame_changed(self, frame):
        #print(f"Frame {frame} changed.")
        # Ensure that the movie is running
        if self.movie.state() != QMovie.Running:
            #print("Movie is not running, starting...")
            self.movie.start()

    def check_movie_state(self):
        #print(f"Movie state: {self.movie.state()}")
        l = 5

    def stop(self):
        print("Stopping movie and dialog.")
        self.movie.stop()
        self.accept()
