import os
import cv2
from datetime import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage
from video_draw import VideDraw
import mediapipe as mp
import time


class ImagePlayer(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, recognizer, camera_index=0):
        super(ImagePlayer, self).__init__()
        self.recognizer = recognizer
        self.Capture = None
        self.frame = None
        self.cameraId = camera_index
        self.ThreadActive = True
        self.previewSize = [640, 480]
        self.videDraw = VideDraw()

    def initParm(self):
        self.Capture = cv2.VideoCapture(self.cameraId, cv2.CAP_DSHOW)
        self.Capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.previewSize[0])
        self.Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.previewSize[1])
        self.Capture.set(cv2.CAP_PROP_SATURATION, 90)
        self.Capture.set(cv2.CAP_PROP_EXPOSURE, -1)
        self.mirror = True

    def run(self):
        self.ThreadActive = True
        self.initParm()
        if not self.Capture.isOpened():
            print("Failed to open camera.")
            self.ThreadActive = False
            return

        while self.ThreadActive:
            ret, self.frame = self.Capture.read()
            if ret:
                if self.mirror:  # If mirroring is enabled
                    self.frame = cv2.flip(self.frame, 1)
                # Convert frame to Mediapipe Image

                # Convert the frame from BGR to RGB as required by MediaPipe
                rgb_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

                # Get timestamp in milliseconds
                timestamp_ms = int(time.time() * 1000)

                # Perform gesture recognition
                self.recognizer.recognize_gesture(mp_image, timestamp_ms)
                # Display results on the frame
                Image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                Image = self.videDraw.draw_result(Image, self.recognizer.get_recognition_results())
                h, w, ch = Image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(Image.data, w, h, bytes_per_line, QImage.Format_RGB888)

                self.ImageUpdate.emit(convert_to_Qt_format)

        self.Capture.release()

    def stop(self):
        self.ThreadActive = False
        if self.Capture and self.Capture.isOpened():
            self.Capture.release()
        self.quit()

    def saveImage(self):
        date = datetime.now().strftime("%B-%d-%Y")
        date_folder = os.path.join("Saved", "Images", date)
        os.makedirs(date_folder, exist_ok=True)

        img_name = f"image_{datetime.now().strftime('%Hh%Mm%Ss')}.png"
        image_path = os.path.join(date_folder, img_name)

        if self.Capture and self.frame is not None:
            cv2.imwrite(image_path, self.frame)
            print(f"Image saved at {image_path}")
