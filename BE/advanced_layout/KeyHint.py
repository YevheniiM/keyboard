from PyQt5.Qt import *


class KeyHint:
    def __init__(self, hints):
        self.buttons = []
        self.current_button = 0
        self.nonActiveButton = """
                            border: 2px groove #4F5A61;
                            border-radius: 10px;
                            background: rgba(48, 55, 59, 0.8);
                            color: rgb(123,160,176);
                            margin: 7px 1px;
                            """
        self.activeButton = """
                        border: 2px groove #4F5A61;
                        border-radius: 10px;
                        background-color: #2e86de;
                        color: white;
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
        for letter in hints:
            self.buttons.append(QLabel(window))
            self.buttons[-1].setText(letter.lower())
            self.buttons[-1].setFrameStyle(QLabel.Panel | QLabel.Sunken)
            self.buttons[-1].setAlignment(Qt.AlignCenter)
            self.buttons[-1].setStyleSheet(self.nonActiveButton)
            layout.addWidget(self.buttons[-1])
        self.buttons[self.current_button].setStyleSheet(self.activeButton)
        widget = QWidget()
        widget.setLayout(layout)
        window.setFixedSize(60 * len(self.buttons), 60)
        window.setAttribute(Qt.WA_TranslucentBackground, True)
        window.setCentralWidget(widget)
        self.window = window
        self.window.show()

    def window_show(self):
        self.window.show()

    def window_hide(self):
        self.window.hide()

    def activate_next_Button(self):
        self.buttons[self.current_button].setStyleSheet(self.nonActiveButton)
        self.current_button = (self.current_button + 1) % len(self.buttons)
        self.buttons[self.current_button].setStyleSheet(self.activeButton)

    def activate_prev_Button(self):
        self.buttons[self.current_button].setStyleSheet(self.nonActiveButton)
        self.current_button = (self.current_button - 1) % len(self.buttons)
        self.buttons[self.current_button].setStyleSheet(self.activeButton)
