from PyQt5 import QtWidgets, QtGui

from DataManager import DataManager
import utils as U


REMAP_MODE_LABEL_STYLE = """
    QLabel {
        color: #F7B500;
        border: none;
        max-width: 200px;
        max-height: 17px;
        margin-right: 5px;
        margin-top: 0px;
    }
"""

RADIO_BUTTON_STYLE = """
    QRadioButton {
        border: none;
        padding-left: 3px;
        border-radius: 2%;
        margin-right: 5px;
        color: #424E59;
    }
    QRadioButton:checked {
        color: white;
    }
"""

REMAP_MODE_LINE_STYLE = """
    QLineEdit {
        background-color: #1D2939;
        border-radius: 4px;
        padding: 4px 10px 6px 10px;
        color: white;
        margin-left: 3px;
    }
"""

LABEL_FONT = QtGui.QFont("Arial", 9, weight=400)
LABEL_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 1)

RADIO_BUTTON_FONT = QtGui.QFont("Arial", 10, weight=400)
RADIO_BUTTON_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)

INPUT_LINE_FONT = QtGui.QFont('consolas', 10, weight=420)
INPUT_LINE_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)

class RemapMode():
    def __init__(self):
        self.label = U.initLabel("KEYBOARD SETTINGS", (60, 15))
        self.longPress = U.initRadioButton("Long Press")
        self.multPress = U.initRadioButton("Multiple Press")
        self.value = U.initLineEdit(validator=QtGui.QIntValidator, fixedWidth=150)
        self._setStyles()
        self.widgets = [self.label, self.multPress, self.longPress, self.value]
        self.dataManager = DataManager()

    def _setStyles(self):
        self.label.setStyleSheet(REMAP_MODE_LABEL_STYLE)
        self.label.setFont(LABEL_FONT)
        self.value.setStyleSheet(REMAP_MODE_LINE_STYLE)
        self.value.setFont(INPUT_LINE_FONT)
        self.longPress.setStyleSheet(RADIO_BUTTON_STYLE)
        self.multPress.setStyleSheet(RADIO_BUTTON_STYLE)
        self.longPress.setFont(RADIO_BUTTON_FONT)
        self.multPress.setFont(RADIO_BUTTON_FONT)

    def saveRadioState(self):
        self.dataManager.setModeType('long_press' \
                                    if self.longPress.isChecked() \
                                    else 'multiple_press')

    def saveValue(self):
        self.dataManager.setModeValue(int(self.value.text()))

    def loadModeState(self):
        self.value.setText(str(self.dataManager.getModeValue()))
        self.longPress.setChecked(self.dataManager.getModeType() == 'long_press')
        self.multPress.setChecked(self.dataManager.getModeType() == 'multiple_press')
