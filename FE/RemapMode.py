from PyQt5 import QtWidgets, QtGui
import utils as U


REMAP_MODE_LABEL_STYLE = """
    QLabel {
        color: #F7B500;
        border: none;
        padding: 3px 5px 4px 30px;
        max-width: 100px;
        max-height: 17px;
        margin-right: 5px;
        margin-top: 0px;
    }
"""

RADIO_BUTTON_STYLE = """
    QRadioButton {
        background-color: #58DDE8;
        padding: 5px 14px;
        border: none;
        border-radius: 2%;
        margin-right: 5px;
    }
"""

REMAP_MODE_LINE_STYLE = """
    QLineEdit {
        background-color: #58DDE8;
        border: none;
        border-radius: 2%;
        padding: 3px 10px 5px 10px;
        margin-bottom: 0px;
        max-width: 100px;
    }
"""


class RemapMode():
    def __init__(self):
        self.label = U.initLabel("KEYBOARD SETTINGS", (60, 15))
        self.longPress = U.initRadioButton("Long Press")
        self.multPress = U.initRadioButton("Multiple Press")
        self.value = U.initLineEdit(validator=QtGui.QIntValidator)
        self._setStyles()
        self.widgets = [self.label, self.longPress, self.multPress, self.value]

    def _setStyles(self):
        self.label.setStyleSheet(REMAP_MODE_LABEL_STYLE)
        self.value.setStyleSheet(REMAP_MODE_LINE_STYLE)
        self.longPress.setStyleSheet(RADIO_BUTTON_STYLE)
        self.multPress.setStyleSheet(RADIO_BUTTON_STYLE)

    def saveRadioState(self, layouts, layoutIndex):
        layouts[layoutIndex]['mode']['type'] = 'long_press' \
                                                if self.longPress.isChecked() \
                                                else 'multiple_press'

    def saveValue(self, layouts, layoutIndex):
        layouts[layoutIndex]['mode']['value'] = int(self.value.text())

    def loadModeState(self, layouts, layoutIndex):
        self.value.setText(str(layouts[layoutIndex]['mode']['value']))
        self.longPress.setChecked(layouts[layoutIndex]['mode']['type'] == 'long_press')
        self.multPress.setChecked(layouts[layoutIndex]['mode']['type'] == 'multiple_press')
