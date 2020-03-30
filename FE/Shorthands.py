from PyQt5 import QtWidgets, QtCore
import utils as U


class ShorthandStyle:
    EDIT_LINE_STYLE = """
        QLineEdit {
            background-color: #395663;
            border-radius: 2%;
            padding: 3px 10px 5px 10px;
            color: #58DDE8;
        }
    """

    BUTTON_STYLE = """
        QPushButton {
            width: 80px;
            height: 25px;
            background-color: #1dd1a1;
            border-radius: 2%;
        }
        QPushButton:hover {
            background-color: #395663;
        }
    """

class _Shorthand():
    def __init__(self, key='', value=''):
        self.keyLabel = U.initLabel("Shorthand:", (50, 15))
        self.key = U.initLineEdit(key)
        self.valueLabel = U.initLabel("Full String:", (50, 15))
        self.value = U.initLineEdit(value)
        # ||
        # || possible feature for future
        # \/
        # self.checkbox = U.initCheckbox("Use this")
        self._setStyles()
        self.widgets = [self.keyLabel, self.key,
                        self.valueLabel, self.value,]
                        # self.checkbox]

    def _setStyles(self):
        self.key.setStyleSheet(ShorthandStyle.EDIT_LINE_STYLE)
        self.value.setStyleSheet(ShorthandStyle.EDIT_LINE_STYLE)


class Shorthands():
    def __init__(self, renderer):
        self.shorthands = [_Shorthand()]#, Shorthand(), Shorthand()]
        self.shorthandAdder = self._initShorthandAdder()
        self.renderer = renderer

    def getWidgets(self):
        for n, shorthand in enumerate(self.shorthands):
            yield n, shorthand.widgets

    def saveShorthandState(self, layouts, layoutIndex):
        for shorthand in self.shorthands:
            if shorthand.key.text() and shorthand.value.text():
                layouts[layoutIndex]['key_strings'][shorthand.key.text()] = shorthand.value.text()
            # ||
            # || possible feature for future
            # \/
            # if shorthand.checkbox.isChecked() and shorthand.key.text() and shorthand.value.text():
            #     layouts[layoutIndex]['key_strings'][shorthand.key.text()] = shorthand.value.text()
            # elif not shorthand.checkbox.isChecked()\
            #     and shorthand.key.text() in layouts[layoutIndex]['key_strings']:
            #     del layouts[layoutIndex]['key_strings'][shorthand.key.text()]

    def loadShorthandState(self, layouts, layoutIndex):
        self.shorthands = []
        for key, value in layouts[layoutIndex]['key_strings'].items():
            self.shorthands.append(_Shorthand(key, value))
        if len(self.shorthands) == 0:
            self.shorthands = [_Shorthand()]
        self.renderer()

    def _initShorthandAdder(self):
        button = QtWidgets.QPushButton("+")
        button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        button.setCursor(QtCore.Qt.PointingHandCursor)
        button.setStyleSheet(ShorthandStyle.BUTTON_STYLE)
        button.clicked.connect(self._addShorthand)
        return button

    def _addShorthand(self):
        self.shorthands.append(_Shorthand())
        self.renderer()
