from PyQt5 import QtWidgets, QtCore


class LayoutButtonStyle:
    DEFAULT_STYLE = """
        QPushButton {
            background-color: #BBDEFB;
            border: none;
        }
        QPushButton:hover {
            background-color: #90CAF9;
        }
    """
    ACTIVE_LAYOUT = """
        background-color: #64B5F6;
        border: none;
    """
    ADD_LAYOUT = """
        QPushButton {
            opacity: 0;
            font-size: 30px;
            color: #0288D1;
            border: none;
        }
        QPushButton:hover {
            background-color: #BBDEFB;
        }
    """


class LayoutButton(QtWidgets.QPushButton):
    def __init__(self, ui, layoutStyle, clickConection, *args):
        super().__init__(*args)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setStyleSheet(layoutStyle)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.clicked.connect(clickConection)
