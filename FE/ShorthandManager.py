from PyQt5 import QtWidgets, QtCore

from Shorthands import Shorthands
from BoxLayoutFactory import BoxLayoutFactory
# from DataManager import DataManager

class ShorthandManager:
    def __init__(self, parent, boxLayoutFactory):
        self.parent = parent
        self.parent.shorthandsManagerWidget = boxLayoutFactory.getLayout(
            QtWidgets.QGridLayout,
            (390, 113, 480, 100),
            (10, 10, 0, -1),
            "shorthandsManagerWidget"
        )
        self.wrapper = QtWidgets.QWidget()
        self.wrapper.setGeometry(QtCore.QRect(390, 220, 450, 120))
        self.wrapper.setObjectName("wrapper")
        self.scroll = QtWidgets.QScrollArea(self.parent.centralWidget)
        self.scroll.setGeometry(QtCore.QRect(390, 220, 450, 130))
        self.scroll.setWidget(self.wrapper)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        self.wrapper.setLayout(QtWidgets.QGridLayout())

        self.shorthands = Shorthands(self.renderShorthandsList)
        self.renderShorthandsManager()
        self.renderShorthandsList()

    def saveShorthandState(self):
        self.shorthands.saveShorthandState()

    def loadShorthandState(self):
        self.shorthands.loadShorthandState()

    def renderShorthandsManager(self):
        for i in reversed(range(self.parent.shorthandsManagerWidget.count())): 
            self.parent.shorthandsManagerWidget.itemAt(i).widget().setParent(None)

        self.parent.shorthandsManagerWidget.addWidget(self.shorthands.mainLabel, 0, 0)
        self.parent.shorthandsManagerWidget.addWidget(self.shorthands.shorthandTip, 1, 0)
        self.parent.shorthandsManagerWidget.addWidget(self.shorthands.fullTextTip, 1, 1)
        self.parent.shorthandsManagerWidget.addWidget(self.shorthands.shorthandInput, 2, 0)
        self.parent.shorthandsManagerWidget.addWidget(self.shorthands.fullTextInput, 2, 1)
        self.parent.shorthandsManagerWidget.addWidget(self.shorthands.shorthandAdder, 2, 2)

    def renderShorthandsList(self):
        for i in reversed(range(self.wrapper.layout().count())): 
            self.wrapper.layout().itemAt(i).widget().setParent(None)

        shorthands = list(self.shorthands.getShorthandsList())
        if len(shorthands) == 1:
            self.wrapper.setGeometry(QtCore.QRect(390, 220, 450, 30))
        else:
            self.wrapper.setGeometry(QtCore.QRect(390, 220, 450,
                                    20 * len(shorthands)))
        for shorthand in shorthands:
            for n, widget in enumerate(shorthand[1]):
                self.wrapper.layout().addWidget(widget, shorthand[0], n)

