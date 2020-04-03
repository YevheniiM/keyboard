from PyQt5 import QtWidgets, QtCore, QtGui
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


LABEL_FONT = QtGui.QFont("Arial", 9, weight=400)
LABEL_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 1)

TIP_LABEL_FONT = QtGui.QFont("Arial", 10, weight=400)
TIP_LABEL_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)

INPUT_LINE_FONT = QtGui.QFont('consolas', 10, weight=420)
INPUT_LINE_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)

BUTTON_FONT = QtGui.QFont("Arial", 10, weight=450)
BUTTON_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)

class _Shorthand():
    def __init__(self, key='', value=''):
        self.key = U.initLabel(key, (110, 15))
        self.value = U.initLabel(value, (270, 15))
        self._setStyles()
        self.widgets = [self.key, self.value]

    def _setStyles(self):
        self.key.setStyleSheet(ShorthandStyle.TIP_LABEL)
        self.key.setFont(INPUT_LINE_FONT)
        self.value.setStyleSheet(ShorthandStyle.TIP_LABEL)
        self.value.setFont(INPUT_LINE_FONT)


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

    def getShorthandsList(self):
        for n, shorthand in enumerate(self.shorthands):
            yield n, shorthand.widgets

    def saveShorthandState(self, layouts, layoutIndex):
        for shorthand in self.shorthands:
            if shorthand.key.text() and shorthand.value.text():
                layouts[layoutIndex]['key_strings'][shorthand.key.text()] = shorthand.value.text()

    def loadShorthandState(self, layouts, layoutIndex):
        self.shorthands = []
        for key, value in layouts[layoutIndex]['key_strings'].items():
            self.shorthands.append(_Shorthand(key, value))
        if len(self.shorthands) == 0:
            self.shorthands = [_Shorthand()]
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
        self.shorthands.insert(0, _Shorthand(self.shorthandInput.text(),
                                            self.fullTextInput.text()))
        self.shorthandInput.setText('')
        self.fullTextInput.setText('')
        self.renderer()
