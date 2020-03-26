from PyQt5 import QtWidgets, QtGui
import utils as U


class RemapMode():
    def __init__(self):
        self.label = U.initLabel("Mode Setup", (60, 15))
        self.longPress = U.initRadioButton("Long Press")
        self.multPress = U.initRadioButton("Multiple Press")
        self.value = U.initLineEdit(validator=QtGui.QIntValidator)
        self.widgets = [self.label, self.longPress, self.multPress, self.value]

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
