from PyQt5 import QtWidgets, QtCore, QtGui

from DataManager import DataManager
import utils as U


class ShorthandStyle:
    MAIN_LABEL = """
        QLabel {
            color: #F7B500;
            border: none;
            max-width: 200px;
            max-height: 17px;
            margin-right: 5px;
            margin-top: 0px;
        }
    """

    TIP_LABEL = """
        QLabel {
            border: none;
            border-radius: 2%;
            margin-right: 5px;
            color: #6D7278;
        }
    """

    EDIT_LINE_STYLE = """
        QLineEdit {
            background-color: #1D2939;
            border-radius: 4px;
            padding: 4px 10px 6px 10px;
            color: white;
        }
    """

    BUTTON_STYLE = """
        QPushButton {
            width: 60px;
            height: 25px;
            background-color: #F7B500;
            border-radius: 9px;
            color: #474F5C;
            padding-top: 2px;
            padding-bottom: 3px;
        }
        QPushButton:hover {
            background-color: #FCCF00;
        }
    """

    REMOVE_BUTTON_STYLE = """
        QPushButton {
            opacity: 0;
            color: #6D7278;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #2E3A45;
        }
    """


LABEL_FONT = QtGui.QFont("Arial", 9, weight=400)
LABEL_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 1)

TIP_LABEL_FONT = QtGui.QFont("Arial", 10, weight=400)
TIP_LABEL_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)

INPUT_LINE_FONT = QtGui.QFont('consolas', 10, weight=420)
INPUT_LINE_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)

BUTTON_FONT = QtGui.QFont("Arial", 10, weight=450)
BUTTON_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)

class _Shorthand():
    def __init__(self, onRemove, key='', value='', index=0):
        self.index = index
        self.key = U.initLabel(key, (120, 15))
        self.value = U.initLabel(value, (240, 15))
        self.remove = QtWidgets.QPushButton()
        self.remove.clicked.connect(lambda : onRemove(self.index))
        self._setStyles()
        self.widgets = [self.key, self.value, self.remove]

    def _setStyles(self):
        self.key.setStyleSheet(ShorthandStyle.TIP_LABEL)
        self.key.setFont(INPUT_LINE_FONT)
        self.value.setStyleSheet(ShorthandStyle.TIP_LABEL)
        self.value.setFont(INPUT_LINE_FONT)
        self.remove.setStyleSheet(ShorthandStyle.REMOVE_BUTTON_STYLE)
        self.remove.setFixedSize(21, 21)
        self.remove.setCursor(QtCore.Qt.PointingHandCursor)
        self.remove.setIcon(QtGui.QIcon("resources/remove_icon.svg"))
        self.remove.setIconSize(QtCore.QSize(17, 17))


class Shorthands():
    def __init__(self, renderer):
        self.mainLabel = U.initLabel("SHORTHANDS", (130, 15))
        self.shorthandTip = U.initLabel("Shorthand", (80, 15))
        self.fullTextTip = U.initLabel("Full Text", (80, 15))
        self.shorthandInput = U.initLineEdit(fixedWidth=110)
        self.fullTextInput = U.initLineEdit(fixedWidth=270)
        self.shorthandAdder = self._initShorthandAdder()

        self._setStyles()

        self.shorthands = []
        self.renderer = renderer
        self.dataManager = DataManager()

    def getShorthandsList(self):
        for n, shorthand in enumerate(self.shorthands):
            yield n, shorthand.widgets

    def saveShorthandState(self):
        for shorthand in self.shorthands:
            self.dataManager.addShorthand(shorthand.key.text(),
                                            shorthand.value.text())

    def loadShorthandState(self):
        self.shorthands = []
        for i, (key, value) in enumerate(self.dataManager.getShorthands().items()):
            self.shorthands.append(_Shorthand(
                self._removeShorthand, key, value, i))
        self.renderer()

    def _setStyles(self):
        self.mainLabel.setStyleSheet(ShorthandStyle.MAIN_LABEL)
        self.mainLabel.setFont(LABEL_FONT)
        self.shorthandTip.setStyleSheet(ShorthandStyle.TIP_LABEL)
        self.shorthandTip.setFont(TIP_LABEL_FONT)
        self.fullTextTip.setStyleSheet(ShorthandStyle.TIP_LABEL)
        self.fullTextTip.setFont(TIP_LABEL_FONT)
        self.shorthandInput.setStyleSheet(ShorthandStyle.EDIT_LINE_STYLE)
        self.shorthandInput.setFont(INPUT_LINE_FONT)
        self.fullTextInput.setStyleSheet(ShorthandStyle.EDIT_LINE_STYLE)
        self.fullTextInput.setFont(INPUT_LINE_FONT)

    def _initShorthandAdder(self):
        button = QtWidgets.QPushButton("Add")
        button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button.setCursor(QtCore.Qt.PointingHandCursor)
        button.setStyleSheet(ShorthandStyle.BUTTON_STYLE)
        button.setFont(BUTTON_FONT)
        button.clicked.connect(self._addShorthand)
        return button

    def _addShorthand(self):
        if not (self.shorthandInput.text() and self.fullTextInput.text()):
            return
        self.shorthands.insert(0, _Shorthand(self._removeShorthand,
                                            self.shorthandInput.text(),
                                            self.fullTextInput.text()))
        for i in range(1, len(self.shorthands)):
            self.shorthands[i].index = i
        self.shorthandInput.setText('')
        self.fullTextInput.setText('')

        self.saveShorthandState()
        self.renderer()

    def _removeShorthand(self, index):
        self.dataManager.removeShorthand(self.shorthands.pop(index).key.text())

        for i in range(index, len(self.shorthands)):
            self.shorthands[i].index = i

        self.renderer()
