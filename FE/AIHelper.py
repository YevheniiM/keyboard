from PyQt5 import QtWidgets, QtGui
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

SUBLABEL_STYLE = """
    QLabel {
        border: none;
        border-radius: 2%;
        margin-right: 5px;
        color: #6D7278;
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

TIP_LABEL_FONT = QtGui.QFont("Arial", 10, weight=400)
TIP_LABEL_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)


class AIHelper():
    def __init__(self):
        self.label = U.initLabel("AI HELPER", (60, 15))
        self.on = U.initRadioButton("Correction")
        self.off = U.initRadioButton("Completion")

        self._setStyles()
        self.widgets = [self.label, self.on, self.off]

    def _setStyles(self):
        self.label.setStyleSheet(REMAP_MODE_LABEL_STYLE)
        self.label.setFont(LABEL_FONT)
        self.on.setStyleSheet(RADIO_BUTTON_STYLE)
        self.on.setFont(RADIO_BUTTON_FONT)
        self.off.setStyleSheet(RADIO_BUTTON_STYLE)
        self.off.setFont(RADIO_BUTTON_FONT)


class TextStyle():
    def __init__(self):
        self.subLabel = U.initLabel("Text Style", (80, 15))
        self.informal = U.initRadioButton("Informal")
        self.formal = U.initRadioButton("Formal")

        self._setStyles()
        self.widgets = [self.subLabel, self.informal, self.formal]

    def _setStyles(self):
        self.subLabel.setStyleSheet(SUBLABEL_STYLE)
        self.subLabel.setFont(TIP_LABEL_FONT)
        self.informal.setStyleSheet(RADIO_BUTTON_STYLE)
        self.informal.setFont(RADIO_BUTTON_FONT)
        self.formal.setStyleSheet(RADIO_BUTTON_STYLE)
        self.formal.setFont(RADIO_BUTTON_FONT)

    # def saveRadioState(self, layouts, layoutIndex):
    #     layouts[layoutIndex]['mode']['type'] = 'long_press' \
    #                                             if self.on.isChecked() \
    #                                             else 'multiple_press'

    # def saveValue(self, layouts, layoutIndex):
        # layouts[layoutIndex]['mode']['value'] = int(self.value.text())

    # def loadModeState(self, layouts, layoutIndex):
    #     # self.value.setText(str(layouts[layoutIndex]['mode']['value']))
    #     self.on.setChecked(layouts[layoutIndex]['mode']['type'] == 'long_press')
    #     self.off.setChecked(layouts[layoutIndex]['mode']['type'] == 'multiple_press')
