#  Copyright (c) 2023 Harikeshav R
#  All rights reserved.

from SpeechToSign.compiler import VideoDisplayer
from SpeechToSign.translator import ISLConverter
from ui_main import *


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Setup the UI from the UI file.
        self.setupUi(self)

        self.convert_button.clicked.connect(self.translate)

    def translate(self):
        converter = ISLConverter()
        video_displayer = VideoDisplayer()

        sentence = self.input_field.text()

        parsed = converter.convert_to_isl(sentence).split()
        video_displayer.show(parsed)
        video_displayer.destroy_delayed()


app = QApplication([])
app.setStyle("Fusion")

window = MainWindow()
window.show()

app.exec()
