from PyQt5 import QtCore, QtGui, QtWidgets
from LayoutButton import LayoutButton, LayoutButtonStyle
from DragButton import DragButton


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
        MainWindow.resize(867, 525)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 861, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.layoutsSwitcher = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.layoutsSwitcher.setContentsMargins(10, 10, 0, 0)
        self.layoutsSwitcher.setObjectName("layoutsSwitcher")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 80, 861, 80))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.row0 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.row0.setContentsMargins(10, 10, 0, 0)
        self.row0.setObjectName("row0")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(0, 160, 861, 80))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.row1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.row1.setContentsMargins(10, 10, 0, 0)
        self.row1.setObjectName("row1")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(0, 240, 861, 80))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.row2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.row2.setContentsMargins(10, 10, 0, 0)
        self.row2.setObjectName("row2")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(0, 320, 861, 80))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.row3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.row3.setContentsMargins(10, 10, 0, 0)
        self.row3.setObjectName("row3")
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(0, 400, 861, 80))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.row4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.row4.setContentsMargins(10, 10, 0, 0)
        self.row4.setObjectName("row4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 867, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.remaps = [{}]

        self.rows = [self.row0, self.row1, self.row2, self.row3, self.row4]
        self.layouts = []
        self.currentLayout = 0

        self.layoutButtons = [
            LayoutButton(self, LayoutButtonStyle.ACTIVE_LAYOUT, lambda : self.switchLayout(0), "Layout 1"),
            LayoutButton(self, LayoutButtonStyle.ADD_LAYOUT, self.addLayout, "+")
            ]

        [ui.layoutsSwitcher.addWidget(layoutButton) for layoutButton in self.layoutButtons]

        self.initLayout(0)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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

    def switchLayout(self, layoutIndex):
        print(self.remaps, layoutIndex)
        self.layoutButtons[self.currentLayout].setStyleSheet(LayoutButtonStyle.DEFAULT_STYLE)
        self.layoutButtons[layoutIndex].setStyleSheet(LayoutButtonStyle.ACTIVE_LAYOUT)
        self.currentLayout = layoutIndex
        self.initLayout(layoutIndex)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
