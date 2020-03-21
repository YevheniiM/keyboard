from PyQt5 import QtCore, QtGui, QtWidgets
from LayoutButton import LayoutButton, LayoutButtonStyle
from DragButton import DragButton
from BoxLayoutFactory import BoxLayoutFactory
from RemapMode import RemapMode

import json


defaultKeyboardLayout = [
    '`:1:2:3:4:5:6:7:8:9:0:-:='.split(':'),
    'tab:q:w:e:r:t:y:u:i:o:p:[:]'.split(':'),
    'caps lock:a:s:d:f:g:h:j:k:l:;:\':enter'.split(':'),
    'shift:z:x:c:v:b:n:m:,:.:/:shift'.split(':'),
    'ctrl:fn:win:alt:space:alt:ctrl'.split(':')
]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.boxLayoutFactory = BoxLayoutFactory(self.centralWidget)

        self.layoutsSwitcher = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (0, 0, 890, 80),
            (10, 10, 0, 0),
            "layoutsSwithcer"
        )

        self.controlButtons = self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (0, 80, 230, 80),
            (10, 10, 0, 0),
            "controlButtons"
        )

        self.rows = [self.boxLayoutFactory.getLayout(
            QtWidgets.QHBoxLayout,
            (0, 160 + 80 * i, 890, 80),
            (10, 10, 0, 0),
            f"row{i}"
        ) for i in range(5)]

        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 890, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.controlButton = QtWidgets.QPushButton("Save")
        self.controlButton.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.controlButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.controlButton.clicked.connect(self.saveRemaps)
        self.controlButtons.addWidget(self.controlButton)

        self.modeWidget = self.boxLayoutFactory.getLayout(
            QtWidgets.QVBoxLayout,
            (240, 80, 890, 80),
            (0, 0, 0, 0),
            "modeWidget"
        )

        self.remaps = [{}]
        self.layouts = [{'mode': {
            'type': 'long_press',
            'value': 1
        }}]
        self.currentLayout = 0

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

        self.layoutButtons = [
            LayoutButton(self, LayoutButtonStyle.ACTIVE_LAYOUT, lambda : self.switchLayout(0), "Layout 1"),
            LayoutButton(self, LayoutButtonStyle.ADD_LAYOUT, self.addLayout, "+")
            ]

        [self.layoutsSwitcher.addWidget(layoutButton) for layoutButton in self.layoutButtons]

        self.initLayout(self.currentLayout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def saveRemaps(self):
        resultFile = {'layouts': []}
        for n, remap in enumerate(self.remaps):
            resultFile['layouts'].append({
                'keymap': remap,
                'mode': self.layouts[n]['mode'],
            })
        with open('test.json', 'w') as jf:
            json.dump(resultFile, jf)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def initLayout(self, layoutIndex):
        for n in range(len(self.rows)):
            for i in reversed(range(self.rows[n].count())): 
                self.rows[n].itemAt(i).widget().setParent(None)

        for n, keyboardRow in enumerate(defaultKeyboardLayout):
            newButton = DragButton(layoutIndex, self.remaps, f"row {n}")
            self.rows[n].addWidget(newButton)
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
        self.layouts.append({'mode': {
            'type': 'long_press',
            'value': 1
        }})

    def switchLayout(self, layoutIndex):
        print(self.remaps, layoutIndex)
        self.layoutButtons[self.currentLayout].setStyleSheet(LayoutButtonStyle.DEFAULT_STYLE)
        self.layoutButtons[layoutIndex].setStyleSheet(LayoutButtonStyle.ACTIVE_LAYOUT)
        self.currentLayout = layoutIndex
        self.mode.setModeState(self.layouts, layoutIndex)
        self.initLayout(layoutIndex)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
