from PyQt5 import QtCore, QtGui, QtWidgets

from LayoutButton import LayoutButton, LayoutButtonStyle
from BoxLayoutFactory import BoxLayoutFactory
from DataManager import DataManager

import utils as U


class LayoutManager:
    def __init__(self, parent, boxLayoutFactory):
        self.parent = parent
        self.currentLayout = 0
        self.boxLayoutFactory = boxLayoutFactory
        self.dataManager = DataManager()
        self.parent.layoutsSwitcher = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (12, 0, self.parent.width - 50, 80),
            (20, 20, 0, 0),
            "layoutsSwithcer"
        )
        self.parent.layoutAdderWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (self.parent.width - 91, 10, 70, 80),
            (0, 0, 0, 0),
            "layoutAdder"
        )
        self.parent.layoutsSwitcher.setAlignment(QtCore.Qt.AlignLeft)
        self.parent.layoutsSwitcher.setSpacing(25)
        self.layoutButtons = [LayoutButton(self,
                                            LayoutButtonStyle.ACTIVE_LAYOUT,
                                            lambda : self.parent.switchLayout(0),
                                            lambda : self.changeLayoutName(0),
                                            "LAYOUT 1")]
        self.layoutAdder = LayoutButton(self,
                                        LayoutButtonStyle.ADD_LAYOUT,
                                        self.addLayout,
                                        None,
                                        "+")

        [self.parent.layoutsSwitcher.addWidget(layoutButton) for layoutButton in self.layoutButtons]
        self.parent.layoutAdderWidget.addWidget(self.layoutAdder)

    def addLayout(self):
        for layoutButton in self.layoutButtons:
            self.parent.layoutsSwitcher.removeWidget(layoutButton)

        layoutIndex = len(self.layoutButtons)
        self.layoutButtons.append(
            LayoutButton(self, LayoutButtonStyle.DEFAULT_STYLE,
                        lambda : self.parent.switchLayout(layoutIndex),
                        lambda : self.changeLayoutName(layoutIndex),
                         f"LAYOUT {layoutIndex + 1}"
                         )
        )

        for layoutButton in self.layoutButtons:
            self.parent.layoutsSwitcher.addWidget(layoutButton)

        self.dataManager.addNewLayout()
        if len(self.layoutButtons) == 3:
            self.layoutAdder.setEnabled(False)

    def changeLayoutName(self, layoutIndex):
        [self.parent.layoutsSwitcher.removeWidget(layoutButton) for layoutButton in self.layoutButtons]
        buttonBuff = self.layoutButtons.pop(layoutIndex)

        LABEL_FONT = QtGui.QFont("Arial", 10, weight=450)
        LABEL_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 1)
        changeNameLine = U.initLineEdit(buttonBuff.text(), fixedWidth=250)
        changeNameLine.selectAll()
        changeNameLine.setStyleSheet("""
            border: none;
            background-color: #1D2939;
            border-radius: 4px;
            padding: 6px 10px 6px 10px;
            margin-bottom: 7px;
            color: white;
        """)
        changeNameLine.setAlignment(QtCore.Qt.AlignCenter)
        changeNameLine.setFont(LABEL_FONT)
        changeNameLine.editingFinished.connect(
                lambda : self.applyNameChanged(buttonBuff, layoutIndex)
            )
        changeNameLine.textEdited.connect(lambda: self.toUpper(changeNameLine))
        self.layoutButtons.insert(layoutIndex, changeNameLine)
        [self.parent.layoutsSwitcher.addWidget(layoutButton) for layoutButton in self.layoutButtons]
        changeNameLine.setFocus()
    
    @staticmethod
    def toUpper(editLine):
        text = editLine.text()
        editLine.setText("")
        editLine.setText(text.upper())

    def applyNameChanged(self, buttonBuff, layoutIndex):
        for i in reversed(range(self.parent.layoutsSwitcher.count())): 
            self.parent.layoutsSwitcher.itemAt(i).widget().setParent(None)
        editLine = self.layoutButtons.pop(layoutIndex)

        self.dataManager.setLayoutName(editLine.text())
        buttonBuff.setText(editLine.text())
        self.layoutButtons.insert(layoutIndex, buttonBuff)
        [self.parent.layoutsSwitcher.addWidget(layoutButton) for layoutButton in self.layoutButtons]
    
    def updateButtonsStyle(self, newLayoutIndex):
        self.layoutButtons[self.dataManager.currentLayout].setStyleSheet(LayoutButtonStyle.DEFAULT_STYLE)
        self.layoutButtons[newLayoutIndex].setStyleSheet(LayoutButtonStyle.ACTIVE_LAYOUT)


