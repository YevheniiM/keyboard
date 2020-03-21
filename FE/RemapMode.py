from PyQt5 import QtWidgets, QtGui


class RemapMode():
    def __init__(self):
        self.label = self._initLabel()
        self.longPress = self._initRadioButton("Long Press")
        self.multPress = self._initRadioButton("Multiple Press")
        self.value = self._initValue()
        self.widgets = [self.label, self.longPress, self.multPress, self.value]

    @staticmethod
    def _initLabel():
        label = QtWidgets.QLabel()
        label.setText("Mode Setup")
        return label

    @staticmethod
    def _initRadioButton(radioButtonName):
        radioButton = QtWidgets.QRadioButton(radioButtonName)
        return radioButton

    @staticmethod
    def _initValue():
        value = QtWidgets.QLineEdit()
        value.setValidator(QtGui.QIntValidator())
        value.setFixedWidth(100)
        return value

    def saveRadioState(self, layouts, layoutIndex):
        layouts[layoutIndex]['mode']['type'] = 'long_press' \
                                                if self.longPress.isChecked() \
                                                else 'multiple_press'

    def saveValue(self, layouts, layoutIndex):
        layouts[layoutIndex]['mode']['value'] = int(self.value.text())

    def setModeState(self, layouts, layoutIndex):
        self.value.setText(str(layouts[layoutIndex]['mode']['value']))
        self.longPress.setChecked(layouts[layoutIndex]['mode']['type'] == 'long_press')
        self.multPress.setChecked(layouts[layoutIndex]['mode']['type'] == 'multiple_press')
