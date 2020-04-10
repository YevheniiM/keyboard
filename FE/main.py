from PyQt5 import QtCore, QtGui, QtWidgets

from LayoutButton import LayoutButton, LayoutButtonStyle
from DragButton import DragButton
from BoxLayoutFactory import BoxLayoutFactory
from RemapMode import RemapMode
from Shorthands import Shorthands
from TestTextBox import TestTextBox
from AIHelper import AIHelper, TextStyle
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
        MainWindow.setObjectName("KeyAccess")
        MainWindow.setWindowTitle("KeyAccess")
        MainWindow.setWindowIconText("KeyAccess")
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

        # ====== INIT CONFIGS ======
        self.remaps = [{}]
        self.layouts = [{
            'name': 'Layout 1',
            'mode': {
                'type': 'long_press',
                'value': 1
                },
            'key_strings' : {},
            'ai': {
                'correction': False,
                'completion': False
            }
        }]
        self.currentLayout = 0
        # ====== INIT CONFIGS ======

        # ====== LAYOUT SWITCHER ======
        self.layoutsSwitcher = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (12, 0, self.width - 50, 80),
            (20, 20, 0, 0),
            "layoutsSwithcer"
        )
        self.layoutAdderWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (self.width - 91, 10, 70, 80),
            (0, 0, 0, 0),
            "layoutAdder"
        )
        self.layoutsSwitcher.setAlignment(QtCore.Qt.AlignLeft)
        self.layoutsSwitcher.setSpacing(25)
        self.layoutButtons = [LayoutButton(self,
                                            LayoutButtonStyle.ACTIVE_LAYOUT,
                                            lambda : self.switchLayout(0),
                                            lambda : self.changeLayoutName(0),
                                            "LAYOUT 1")]
        self.layoutAdder = LayoutButton(self,
                                        LayoutButtonStyle.ADD_LAYOUT,
                                        self.addLayout,
                                        None,
                                        "+")

        [self.layoutsSwitcher.addWidget(layoutButton) for layoutButton in self.layoutButtons]
        self.layoutAdderWidget.addWidget(self.layoutAdder)
        # ====== LAYOUT SWITCHER ======

        self.rows = [self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            ((self.width - 920) // 2, 410 + 73 * i, 920, 80),
            (0, 10, 0, 0),
            f"row{i}"
        ) for i in range(5)]

        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.width - 60, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        # ====== MODE configuration widget =====
        self.modeWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QVBoxLayout,
            (20, 110, 200, 140),
            (10, 10, 0, -1),
            "modeWidget"
        )

        self.mode = RemapMode()
        self.mode.longPress.toggled.connect(
            lambda : self.mode.saveRadioState(self.layouts, self.currentLayout)
        )
        self.mode.multPress.toggled.connect(
            lambda : self.mode.saveRadioState(self.layouts, self.currentLayout)
        )
        self.mode.value.editingFinished.connect(
            lambda : self.mode.saveValue(self.layouts, self.currentLayout)
        )
        [self.modeWidget.addWidget(m) for m in self.mode.widgets]
        # ====== MODE configuration widget ======

        # ====== AI HELPER =====
        self.aiWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QVBoxLayout,
            (220, 108, 200, 105),
            (10, 10, 0, -1),
            "aiWidget"
        )

        self.aiHelper = AIHelper()
        self.aiHelper.correction.toggled.connect(
            lambda : self.aiHelper.saveAIState(self.layouts, self.currentLayout)
        )
        self.aiHelper.completion.toggled.connect(
            lambda : self.aiHelper.saveAIState(self.layouts, self.currentLayout)
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
        # self.aiHelper.on.toggled.connect(
        #     lambda : self.aiHelper.saveRadioState(self.layouts, self.currentLayout)
        # )
        # self.aiHelper.off.toggled.connect(
        #     lambda : self.aiHelper.saveRadioState(self.layouts, self.currentLayout)
        # )
        [self.textStyleWidget.addWidget(m) for m in self.textStyle.widgets]
        # ====== TEXT STYLE ======

        # ====== SHORTHANDS configuration =====
        self.shorthandsManagerWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QGridLayout,
            (390, 113, 480, 100),
            (10, 10, 0, -1),
            "shorthandsManagerWidget"
        )
        # self.shorthandsListWidget = self.boxLayoutFactory.getLayout(
        #     QtWidgets.QGridLayout,
        #     (370, 180, 450, 200),
        #     (0, 0, 0, 0),
        #     "shorthandsListWidget"
        # )

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
        self.controlButton.clicked.connect(self.saveRemaps)
        self.controlButtons.addWidget(self.controlButton)
        # ===== SAVE button =====

        self.initLayout(self.currentLayout)

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

    def saveRemaps(self):
        self.shorthands.saveShorthandState(self.layouts, self.currentLayout)

        resultFile = {'layouts': []}
        for n, remap in enumerate(self.remaps):
            resultFile['layouts'].append({
                'name': self.layouts[n]['name'],
                'keymap': remap,
                'mode': self.layouts[n]['mode'],
                'key_strings': self.layouts[n]['key_strings'],
                'ai': self.layouts[n]['ai']
            })
        # UNCOMMENT FOR DEPLOY
        # options = QtWidgets.QFileDialog.Options()
        # fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
        #                                                         QtWidgets.QWidget(),
        #                                                         "Save configuration file",
        #                                                         "config.json",
        #                                                         "JSON (*.json)",
        #                                                         options=options
        #                                                     )
        # fileName = '../BE/advanced_layout/helpers/config.json'
        fileName = '../FE/config.json'
        if fileName != '':
            with open(fileName, 'w') as jf:
                json.dump(resultFile, jf)
        self.notify()

    def notify(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("The configuration file has been saved")
        # msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Configuration file saved")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            
        retval = msg.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def initLayout(self, layoutIndex):
        for n in range(len(self.rows)):
            for i in reversed(range(self.rows[n].count())): 
                self.rows[n].itemAt(i).widget().setParent(None)

        for n, keyboardRow in enumerate(defaultKeyboardLayout):
            for button in keyboardRow:
                self.rows[n].addWidget(DragButton(layoutIndex, self.remaps, button))

    def addLayout(self):
        for layoutButton in self.layoutButtons:
            self.layoutsSwitcher.removeWidget(layoutButton)

        layoutIndex = len(self.layoutButtons)
        self.layoutButtons.append(
            LayoutButton(self, LayoutButtonStyle.DEFAULT_STYLE,
                        lambda : self.switchLayout(layoutIndex),
                        lambda : self.changeLayoutName(layoutIndex),
                         f"LAYOUT {layoutIndex + 1}"
                         )
        )

        for layoutButton in self.layoutButtons:
            self.layoutsSwitcher.addWidget(layoutButton)

        self.remaps.append({})
        self.layouts.append({
            'name': f"LAYOUT {layoutIndex + 1}",
            'mode': {
                'type': 'long_press',
                'value': 1
                },
            'key_strings': {},
            'ai': {
                'correction': False,
                'completion': False
            }
        })
        if len(self.layoutButtons) == 3:
            self.layoutAdder.setEnabled(False)

    def changeLayoutName(self, layoutIndex):
        [self.layoutsSwitcher.removeWidget(layoutButton) for layoutButton in self.layoutButtons]
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
        [self.layoutsSwitcher.addWidget(layoutButton) for layoutButton in self.layoutButtons]
        changeNameLine.setFocus()
    
    @staticmethod
    def toUpper(editLine):
        text = editLine.text()
        editLine.setText("")
        editLine.setText(text.upper())

    def applyNameChanged(self, buttonBuff, layoutIndex):
        print('changing name')
        for i in reversed(range(self.layoutsSwitcher.count())): 
            self.layoutsSwitcher.itemAt(i).widget().setParent(None)
        editLine = self.layoutButtons.pop(layoutIndex)

        self.layouts[layoutIndex]['name'] = editLine.text()
        buttonBuff.setText(editLine.text())
        self.layoutButtons.insert(layoutIndex, buttonBuff)
        [self.layoutsSwitcher.addWidget(layoutButton) for layoutButton in self.layoutButtons]

    def switchLayout(self, layoutIndex):
        print(self.remaps, layoutIndex)
        self.layoutButtons[self.currentLayout].setStyleSheet(LayoutButtonStyle.DEFAULT_STYLE)
        self.layoutButtons[layoutIndex].setStyleSheet(LayoutButtonStyle.ACTIVE_LAYOUT)
        self.shorthands.saveShorthandState(self.layouts, self.currentLayout)
        print(self.layouts)
        self.currentLayout = layoutIndex

        self.mode.loadModeState(self.layouts, layoutIndex)
        self.aiHelper.loadAIState(self.layouts, layoutIndex)
        self.shorthands.loadShorthandState(self.layouts, layoutIndex)
        self.initLayout(layoutIndex)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app.setApplicationName("KeyAccess")
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
