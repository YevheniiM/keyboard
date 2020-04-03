from PyQt5.Qt import *
from PyQt5.QtGui import QFont


class PredictionHint:
    def __init__(self, text):
        nonActiveButton = """
                                    border: 2px groove #4F5A61;
                                    border-radius: 10px;
                                    background: rgba(48, 55, 59, 0.8);
                                    color: rgb(123,160,176);
                                    margin: 7px 1px;
                                    """

        window = QMainWindow()

        window.setWindowFlags(window.windowFlags() | Qt.Tool
                              | Qt.FramelessWindowHint | Qt.Popup
                              | Qt.WindowStaysOnTopHint)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        window.setContentsMargins(0, 0, 0, 0)

        font = QFont("Arial", 16, QFont.Bold)

        self.texthint = QLabel(window)
        self.texthint.setText(text)
        self.texthint.setFrameStyle(QLabel.Panel | QLabel.Sunken)
        self.texthint.setAlignment(Qt.AlignCenter)
        self.texthint.setStyleSheet(nonActiveButton)
        self.texthint.setFont(font)
        layout.addWidget(self.texthint)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        window.setFixedSize(24 * len(text), 60)
        window.setAttribute(Qt.WA_TranslucentBackground, True)
        window.setCentralWidget(self.widget)
        self.window = window
        self.window.show()

    def change_text_hint(self, text):
        self.texthint.setText(text)
        self.window.setFixedSize(24 * len(text), 60)
        self.window.setCentralWidget(self.widget)

    def window_show(self):
        self.texthint.show()

    def window_hide(self):
        self.texthint.hide()

    def window_close(self):
        self.texthint.close()
