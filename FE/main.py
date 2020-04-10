from PyQt5 import QtCore, QtGui, QtWidgets

from LayoutButton import LayoutButton, LayoutButtonStyle
from DragButton import DragButton
from BoxLayoutFactory import BoxLayoutFactory
from RemapMode import RemapMode
from Shorthands import Shorthands
from TestTextBox import TestTextBox
from AIHelper import AIHelper, TextStyle
from DataManager import DataManager
from LayoutManager import LayoutManager
import utils as U

import json
import copy


defaultKeyboardLayout = [
    '`:1:2:3:4:5:6:7:8:9:0:-:=:backspace'.split(':'),
    'tab:Q:W:E:R:T:Y:U:I:O:P:[:]'.split(':'),
    'caps lock:A:S:D:F:G:H:J:K:L:;:\':enter'.split(':'),
    'shift:Z:X:C:V:B:N:M:,:.:/:shift'.split(':'),
    'ctrl:fn:win:alt:space:alt:ctrl:'.split(':')
]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowIcon(QtGui.QIcon("resources/letter.svg"))
        self.width = 1050
        self.height = 850
        MainWindow.resize(self.width, self.height)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setStyleSheet("""
            background-color: #232F3F;
        """)
        self.centralWidget.setObjectName("centralWidget")
        self.boxLayoutFactory = BoxLayoutFactory(self.centralWidget)

        ############################################################
        ### stores and amanges all info about layouts and remaps ###
        ############################################################
        self.dataManager = DataManager()

        #################################################
        ### manages layout buttons and related events ###
        #################################################
        self.layoutManager = LayoutManager(self, self.boxLayoutFactory)

        self.rows = [self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            ((self.width - 920) // 2, 410 + 73 * i, 920, 80),
            (0, 10, 0, 0),
            f"row{i}"
        ) for i in range(5)]

        MainWindow.setCentralWidget(self.centralWidget)

        #########################################
        ### program doesn't work without this ###
        #########################################
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.width - 60, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        ###################################
        ### configures mode of pressing ###
        ###################################
        self.modeWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QVBoxLayout,
            (20, 110, 200, 140),
            (10, 10, 0, -1),
            "modeWidget"
        )

        self.mode = RemapMode()
        self.mode.longPress.toggled.connect(
            lambda : self.mode.saveRadioState()
        )
        self.mode.multPress.toggled.connect(
            lambda : self.mode.saveRadioState()
        )
        self.mode.value.editingFinished.connect(
            lambda : self.mode.saveValue()
        )
        [self.modeWidget.addWidget(m) for m in self.mode.widgets]

        ###########################
        ### configures ai tools ###
        ###########################
        self.aiWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QVBoxLayout,
            (220, 108, 200, 105),
            (10, 10, 0, -1),
            "aiWidget"
        )

        self.aiHelper = AIHelper()
        self.aiHelper.correction.toggled.connect(
            lambda : self.aiHelper.saveAIState()
        )
        self.aiHelper.completion.toggled.connect(
            lambda : self.aiHelper.saveAIState()
        )
        [self.aiWidget.addWidget(m) for m in self.aiHelper.widgets]
        # ====== AI HELPER ======

        # ====== TEXT STYLE =====
        self.textStyleWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QVBoxLayout,
            (220, 210, 200, 100),
            (10, 10, 0, -1),
            "textStyleWidget"
        )

        self.textStyle = TextStyle()
        # TODO: save text typing style
        # self.aiHelper.on.toggled.connect(
        #     lambda : self.aiHelper.saveRadioState(self.layouts, self.currentLayout)
        # )
        # self.aiHelper.off.toggled.connect(
        #     lambda : self.aiHelper.saveRadioState(self.layouts, self.currentLayout)
        # )
        [self.textStyleWidget.addWidget(m) for m in self.textStyle.widgets]
        # ====== TEXT STYLE ======

        # ====== SHORTHANDS configuration =====
        # TODO: split into separate
        self.shorthandsManagerWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QGridLayout,
            (390, 113, 480, 100),
            (10, 10, 0, -1),
            "shorthandsManagerWidget"
        )
        self.wrapper = QtWidgets.QWidget()
        self.wrapper.setGeometry(QtCore.QRect(390, 220, 450, 120))
        self.wrapper.setObjectName("wrapper")
        self.scroll = QtWidgets.QScrollArea(self.centralWidget)
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
        # ====== SHORTHANDS configuration =====

        # ====== TEST TEXT box =====
        self.textBoxWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            ((self.width - 900) // 2, 340, 900, 80),
            (0, 0, 0, 0),
            "textBoxWidget"
        )
        self.textBoxWidget.addWidget(TestTextBox())
        # ====== TEST TEXT box =====

        # ===== SAVE button =====
        # TODO: split into separete files
        self.controlButtons = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (self.width - 164, self.height - 75, 125, 35),
            (0, 0, 0, 0),
            "controlButtons"
        )
        BUTTON_FONT = QtGui.QFont("Arial", 10, weight=450)
        BUTTON_FONT.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)
        self.controlButton = QtWidgets.QPushButton("Save")
        self.controlButton.setStyleSheet("""
            QPushButton {
                width: 125px;
                height: 35px;
                background-color: #F7B500;
                border-radius: 9px;
                color: #474F5C;
                padding-top: 2px;
                padding-bottom: 3px;
            }
            QPushButton:hover {
                background-color: #FCCF00;
            }
        """)
        self.controlButton.setFont(BUTTON_FONT)
        self.controlButton.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.controlButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.controlButton.clicked.connect(self.dataManager.dump)
        self.controlButtons.addWidget(self.controlButton)
        # ===== SAVE button =====

        self.initLayout(self.dataManager.currentLayout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def renderShorthandsManager(self):
        for i in reversed(range(self.shorthandsManagerWidget.count())): 
            self.shorthandsManagerWidget.itemAt(i).widget().setParent(None)

        self.shorthandsManagerWidget.addWidget(self.shorthands.mainLabel, 0, 0)
        self.shorthandsManagerWidget.addWidget(self.shorthands.shorthandTip, 1, 0)
        self.shorthandsManagerWidget.addWidget(self.shorthands.fullTextTip, 1, 1)
        self.shorthandsManagerWidget.addWidget(self.shorthands.shorthandInput, 2, 0)
        self.shorthandsManagerWidget.addWidget(self.shorthands.fullTextInput, 2, 1)
        self.shorthandsManagerWidget.addWidget(self.shorthands.shorthandAdder, 2, 2)

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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def initLayout(self, layoutIndex):
        for n in range(len(self.rows)):
            for i in reversed(range(self.rows[n].count())): 
                self.rows[n].itemAt(i).widget().setParent(None)

        for n, keyboardRow in enumerate(defaultKeyboardLayout):
            for button in keyboardRow:
                self.rows[n].addWidget(DragButton(layoutIndex, self.dataManager.remaps, button))

    def switchLayout(self, newLayoutIndex):
        print(self.dataManager.remaps, newLayoutIndex)
        self.layoutManager.updateButtonsStyle(newLayoutIndex)
        self.shorthands.saveShorthandState()
        print(self.dataManager.layouts)
        self.dataManager.setCurrentLayoutIndex(newLayoutIndex)

        self.mode.loadModeState()
        self.aiHelper.loadAIState()
        self.shorthands.loadShorthandState()
        self.initLayout(newLayoutIndex)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app.setApplicationName("KeyAccess")
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
