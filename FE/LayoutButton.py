from PyQt5 import QtWidgets, QtCore


class LayoutButtonStyle:
    DEFAULT_STYLE = """
        QPushButton {
            background-color: #1dd1a1;
            border: none;
        }
        QPushButton:hover {
            background-color: #10ac84;
        }
    """
    ACTIVE_LAYOUT = """
        background-color: #01a3a4;
        border: none;
    """
    ADD_LAYOUT = """
        QPushButton {
            opacity: 0;
            font-size: 30px;
            color: #01a3a4;
            border: none;
        }
        QPushButton:hover {
            background-color: #1dd1a1;
        }
    """


class LayoutButton(QtWidgets.QPushButton):
    def __init__(self, ui, layoutStyle, clickConection, *args):
        super().__init__(*args)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setStyleSheet(layoutStyle)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.clicked.connect(clickConection)
