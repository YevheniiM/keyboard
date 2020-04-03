from PyQt5.Qt import *


class KeyboardCheckHint:
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

        self.choosenButton = """
                            border: 2px groove #4F5A61;
                            border-radius: 10px;
                            background: rgba(56, 93, 122, 0.6);
                            color: white;
                            margin: 7px 1px;
                            """
        self.choosenButtons = []

        window = QMainWindow()

        window.setWindowFlags(window.windowFlags() | Qt.Tool
                              | Qt.FramelessWindowHint | Qt.Popup
                              | Qt.WindowStaysOnTopHint)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        window.setContentsMargins(0, 0, 0, 0)
        font = QFont("Arial", 16, QFont.Bold)

        for letter in hints:
            self.buttons.append(QLabel(window))
            self.buttons[-1].setText(letter)
            self.buttons[-1].setFrameStyle(QLabel.Panel | QLabel.Sunken)
            self.buttons[-1].setAlignment(Qt.AlignCenter)
            self.buttons[-1].setStyleSheet(self.nonActiveButton)
            self.buttons[-1].setFont(font)
            self.layout.addWidget(self.buttons[-1])
        self.buttons[self.current_button].setStyleSheet(self.activeButton)

        widget = QWidget()
        widget.setLayout(self.layout)
        window.setFixedSize(24 * max([len(item) for item in hints]), 60 * len(hints))
        window.setAttribute(Qt.WA_TranslucentBackground, True)
        window.setCentralWidget(widget)
        self.window = window
        self.window.show()

    def window_show(self):
        self.window.show()

    def window_hide(self):
        self.window.hide()

    def activate_next_Button(self, event):
        if event.event_type == 'up':
            if not self.current_button in self.choosenButtons:
                self.buttons[self.current_button].setStyleSheet(self.nonActiveButton)
            else:
                self.buttons[self.current_button].setStyleSheet(self.choosenButton)
            self.current_button = (self.current_button + 1) % len(self.buttons)
            self.buttons[self.current_button].setStyleSheet(self.activeButton)

    def activate_prev_Button(self, event):
        if event.event_type == 'up':
            if not self.current_button in self.choosenButtons:
                self.buttons[self.current_button].setStyleSheet(self.nonActiveButton)
            else:
                self.buttons[self.current_button].setStyleSheet(self.choosenButton)
            self.current_button = (self.current_button - 1) % len(self.buttons)
            self.buttons[self.current_button].setStyleSheet(self.activeButton)

    def set_active(self, event):
        if event.event_type == 'up':
            if not self.current_button in self.choosenButtons:
                self.choosenButtons.append(self.current_button)
                self.buttons[self.current_button].setStyleSheet(self.choosenButton)
            else:
                self.choosenButtons.remove(self.current_button)
                self.buttons[self.current_button].setStyleSheet(self.activeButton)

    def get_active_index(self):
        return self.choosenButtons

    def set_new_hints(self, hints):
        for i in range(0, len(self.buttons)):
            self.buttons[i].setText(hints[i])



