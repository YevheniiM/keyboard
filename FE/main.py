from PyQt5 import QtCore, QtGui, QtWidgets

from LayoutButton import LayoutButton, LayoutButtonStyle
from DragButton import DragButton
from BoxLayoutFactory import BoxLayoutFactory
from RemapMode import RemapMode
from Shorthands import Shorthands
from TestTextBox import TestTextBox

import json


defaultKeyboardLayout = [
    '`:1:2:3:4:5:6:7:8:9:0:-:=:backspace'.split(':'),
    'tab:Q:W:E:R:T:Y:U:I:O:P:[:]'.split(':'),
    'caps lock:A:S:D:F:G:H:J:K:L:;:\':enter'.split(':'),
    'shift:Z:X:C:V:B:N:M:,:.:/:shift'.split(':'),
    'ctrl:fn:win:alt:space:alt:ctrl:'.split(':')
]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(930, 650)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setStyleSheet("background-color: #232F3F")
        self.centralWidget.setObjectName("centralWidget")
        self.boxLayoutFactory = BoxLayoutFactory(self.centralWidget)

        self.layoutsSwitcher = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (0, 0, 920, 80),
            (10, 10, 0, 0),
            "layoutsSwithcer"
        )

        self.controlButtons = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (0, 80, 230, 130),
            (10, 10, 0, 0),
            "controlButtons"
        )

        self.rows = [self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (0, 280 + 73 * i, 920, 80),
            (10, 10, 0, 0),
            f"row{i}"
        ) for i in range(5)]

        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 890, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        # ===== SAVE button =====
        # self.controlButton = QtWidgets.QPushButton("Save")
        # self.controlButton.setStyleSheet("""
        #     QPushButton {
        #         background-color: #54a0ff;
        #         border: none;
        #         border-radius: 2%;
        #     }
        #     QPushButton:hover {
        #         background-color: #2e86de;
        #     }
        # """)
        # self.controlButton.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # self.controlButton.setCursor(QtCore.Qt.PointingHandCursor)
        # self.controlButton.clicked.connect(self.saveRemaps)
        # self.controlButtons.addWidget(self.controlButton)
        # ===== SAVE button =====

        self.remaps = [{}]
        self.layouts = [{
            'mode': {
                'type': 'long_press',
                'value': 1
                },
            'key_strings' : {}
        }]
        self.currentLayout = 0

        # ====== MODE configuration widget =====
        self.modeWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QVBoxLayout,
            (10, 80, 125, 140),
            (0, -9, 0, -1),
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

        # key strings configuration widget
        # self.shorthandsWidget = self.boxLayoutFactory.getLayout(
        #     QtWidgets.QGridLayout,
        #     (340, 80, 890, 80),
        #     (0, 0, 0, 0),
        #     "shorthandsWidget"
        # )
        self.wrapper = QtWidgets.QWidget()
        self.wrapper.setGeometry(QtCore.QRect(370, 90, 520, 121))
        self.wrapper.setObjectName("wrapper")
        self.scroll = QtWidgets.QScrollArea(self.centralWidget)
        self.scroll.setGeometry(QtCore.QRect(370, 90, 520, 121))
        self.scroll.setWidget(self.wrapper)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #58DDE8;
                border-radius: 2%;
            }
        """)
        self.wrapper.setStyleSheet("""
            background-color: #58DDE8;
            border-radius: 2%;
        """)
        self.wrapper.setLayout(QtWidgets.QGridLayout())
        self.shorthands = Shorthands(self.renderShorthands)
        self.renderShorthands()
        # end key strings configuration widget

        # test text box start
        self.textBoxWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (10, 210, 910, 80),
            (0, -9, 0, -1),
            "textBoxWidget"
        )
        # self.testTextBox = TestTextBox()
        # [self.textBoxWidget.addWidget(widget) for widget in self.testTextBox.widgets]
        self.textBoxWidget.addWidget(TestTextBox())
        # test text box end

        self.layoutButtons = [
            LayoutButton(self, LayoutButtonStyle.ACTIVE_LAYOUT, lambda : self.switchLayout(0), "Layout 1"),
            LayoutButton(self, LayoutButtonStyle.ADD_LAYOUT, self.addLayout, "+")
            ]

        [self.layoutsSwitcher.addWidget(layoutButton) for layoutButton in self.layoutButtons]

        self.initLayout(self.currentLayout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def renderShorthands(self):
        for i in reversed(range(self.wrapper.layout().count())): 
            self.wrapper.layout().itemAt(i).widget().setParent(None)

        widgets2render = list(self.shorthands.getWidgets())
        self.wrapper.setGeometry(QtCore.QRect(370, 90, 450,
                                33 * (len(widgets2render) + 1)))
        for shorthand in widgets2render:
            for n, widget in enumerate(shorthand[1]):
                self.wrapper.layout().addWidget(widget, shorthand[0], n)
        self.wrapper.layout().addWidget(self.shorthands.shorthandAdder,
                                        len(widgets2render), 0,
                                        len(widgets2render), 4,
                                        QtCore.Qt.AlignCenter)

    def saveRemaps(self):
        resultFile = {'layouts': []}
        for n, remap in enumerate(self.remaps):
            resultFile['layouts'].append({
                'keymap': remap,
                'mode': self.layouts[n]['mode'],
            })
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
                                                                QtWidgets.QWidget(),
                                                                "Save configuration file",
                                                                "config.json",
                                                                "JSON (*.json)",
                                                                options=options
                                                            )
        if fileName != '':
            with open(fileName, 'w') as jf:
                json.dump(resultFile, jf)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def initLayout(self, layoutIndex):
        for n in range(len(self.rows)):
            for i in reversed(range(self.rows[n].count())): 
                self.rows[n].itemAt(i).widget().setParent(None)

        for n, keyboardRow in enumerate(defaultKeyboardLayout):
            # newButton = DragButton(layoutIndex, self.remaps, f"row {n}")
            # self.rows[n].addWidget(newButton)
            for button in keyboardRow:
                self.rows[n].addWidget(DragButton(layoutIndex, self.remaps, button))

    def addLayout(self):
        for layoutButton in self.layoutButtons:
            self.layoutsSwitcher.removeWidget(layoutButton)

        layoutIndex = len(self.layoutButtons) - 1
        self.layoutButtons.insert(-1, 
            LayoutButton(self, LayoutButtonStyle.DEFAULT_STYLE,
                        lambda : self.switchLayout(layoutIndex),
                         f"Layout {len(self.layoutButtons)}")
        )

        for layoutButton in self.layoutButtons:
            self.layoutsSwitcher.addWidget(layoutButton)

        self.remaps.append({})
        self.layouts.append({
            'mode': {
                'type': 'long_press',
                'value': 1
                },
            'key_strings': {}
        })

    def switchLayout(self, layoutIndex):
        print(self.remaps, layoutIndex)
        self.layoutButtons[self.currentLayout].setStyleSheet(LayoutButtonStyle.DEFAULT_STYLE)
        self.layoutButtons[layoutIndex].setStyleSheet(LayoutButtonStyle.ACTIVE_LAYOUT)
        self.shorthands.saveShorthandState(self.layouts, self.currentLayout)
        self.currentLayout = layoutIndex

        self.mode.loadModeState(self.layouts, layoutIndex)
        self.shorthands.loadShorthandState(self.layouts, layoutIndex)
        self.initLayout(layoutIndex)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
