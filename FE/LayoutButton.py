from PyQt5 import QtWidgets, QtCore, QtGui


class LayoutButtonStyle:
    DEFAULT_STYLE = """
        QPushButton {
            color: #424E59;
            border: none;
            padding-bottom: 7px;
        }
        QPushButton:hover {
            color: white;
        }
    """
    ACTIVE_LAYOUT = """
        color: #F7B500;
        border: none;
        border-bottom: 2px solid #F7B500;
        padding-bottom: 7px;
    """
    ADD_LAYOUT = """
        QPushButton {
            opacity: 0;
            font-size: 30px;
            color: #6D7278;
            border: none;
            border-radius: 4px;
            background-color: #424E59;
            padding-bottom: 3px;
        }
        QPushButton:hover {
            background-color: #2E3A45;
        }
    """

LABEL_FONT = QtGui.QFont("Arial", 10, weight=450)
LABEL_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 1)


class LayoutButton(QtWidgets.QPushButton):
    def __init__(self, ui, layoutStyle, clickConection, *args):
        super().__init__(*args)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setStyleSheet(layoutStyle)
        self.setFont(LABEL_FONT)
        if layoutStyle == LayoutButtonStyle.ADD_LAYOUT:
            self.setFixedSize(35, 35)
        else:
            self.setFixedWidth(250)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.clicked.connect(clickConection)
