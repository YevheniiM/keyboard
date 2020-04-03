from PyQt5 import QtWidgets, QtGui


def initLabel(labelText, size):
    label = QtWidgets.QLabel()
    label.setFixedSize(*size)
    label.setText(labelText)
    return label


def initRadioButton(radioButtonName):
    radioButton = QtWidgets.QRadioButton(radioButtonName)
    return radioButton


def initLineEdit(defaultValue='', validator=None, fixedWidth=100):
    value = QtWidgets.QLineEdit(defaultValue)
    if validator is not None:
        value.setValidator(validator())
    value.setFixedWidth(fixedWidth)
    return value


def initCheckbox(checkBoxName):
    checkBox = QtWidgets.QCheckBox(checkBoxName)
    return checkBox
