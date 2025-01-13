import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from video_capture import ImagePlayer
from gesture import GestureRecognizer
from PyQt5.QtWidgets import QDesktopWidget


class Frame_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("gesture")
        screen_geometry = QDesktopWidget().screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        self.resize(screen_width // 2, screen_height // 2)

        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        self.mainLayout = QtWidgets.QVBoxLayout(centralWidget)

        self.addCameraFeedBox()
        model_path = './checkpoints/gesture_recognizer.task'
        recognizer = GestureRecognizer(model_path)

        self.imagePlayer = ImagePlayer(recognizer, 0)
        self.imagePlayer.ImageUpdate.connect(self.ImageUpdateSlot)
        self.imagePlayer.start()

    def addCameraFeedBox(self):
        self.cameraFeedBox = QtWidgets.QGroupBox(self)
        self.cameraFeedBox.setTitle("Camera Feed")
        self.cameraFeedBox.setStyleSheet("""
            QGroupBox {
                border: 1px solid black;
                border-radius: 1px;
                margin-top: 1px;
                padding: 1px;
                background-color: rgb(245, 245, 245);
            }
        """)
        self.cameraFeedBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        feedLayout = QtWidgets.QVBoxLayout(self.cameraFeedBox)

        self.cameraFeed = QtWidgets.QLabel(self.cameraFeedBox)
        self.cameraFeed.setObjectName("cameraFeed")
        self.cameraFeed.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.cameraFeed.setAlignment(QtCore.Qt.AlignCenter)
        self.cameraFeed.setText("No Camera Feed")
        self.cameraFeed.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        feedLayout.addWidget(self.cameraFeed)

        self.mainLayout.addWidget(self.cameraFeedBox)

    def ImageUpdateSlot(self, image):
        if image:
            width = self.cameraFeed.width()
            height = self.cameraFeed.height()
            scaled_image = QPixmap.fromImage(image).scaled(
                width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.cameraFeed.setPixmap(scaled_image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Frame_MainWindow()
    win.show()
    sys.exit(app.exec_())
