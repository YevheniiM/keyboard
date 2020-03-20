from PyQt5 import QtCore, QtGui, QtWidgets


defaultKeyboardLayout = [
    '`:1:2:3:4:5:6:7:8:9:0:-:='.split(':'),
    'tab:q:w:e:r:t:y:u:i:o:p:[:]'.split(':'),
    'caps lock:a:s:d:f:g:h:j:k:l:;\':enter'.split(':'),
    'shift:z:x:c:v:b:n:m:,:.:/:shift'.split(':'),
    'ctrl:fn:win:alt:space:alt:ctrl'.split(':')
]

remaps = [{}]


def widgets_at(pos):
    """Return ALL widgets at `pos`

    Arguments:
        pos (QPoint): Position at which to get widgets

    """

    widgets = []
    widget_at = QtWidgets.qApp.widgetAt(pos)

    while widget_at:
        widgets.append(widget_at)

        # Make widget invisible to further enquiries
        widget_at.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        widget_at = QtWidgets.qApp.widgetAt(pos)

    # Restore attribute
    for widget in widgets:
        widget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

    return widgets

class DragButton(QtWidgets.QPushButton):
    def __init__(self, layoutIndex, *args):
        super().__init__(*args)
        self.layoutIndex = layoutIndex

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
        self.raise_()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            widgets = widgets_at(QtGui.QCursor.pos())
            for widget in widgets:
                if widget.objectName() == self.objectName():
                    if widget.text() != self.text():
                        remaps[self.layoutIndex][widget.text()] = self.text()
                        widget.setText(self.text())
                        break

            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(DragButton, self).mouseReleaseEvent(event)

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

        self.rows = [self.row0, self.row1, self.row2, self.row3, self.row4]
        self.layouts = []
        self.layoutButtons = [QtWidgets.QPushButton("Layout 1"), QtWidgets.QPushButton("+")]

        self.layoutButtons[0].setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.layoutButtons[0].clicked.connect(lambda : self.switchLayout(0))
        ui.layoutsSwitcher.addWidget(self.layoutButtons[0])

        self.layoutButtons[1].setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.layoutButtons[1].clicked.connect(self.addLayout)
        ui.layoutsSwitcher.addWidget(self.layoutButtons[1])

        self.init_layout(0)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def init_layout(self, layoutIndex):
        for n in range(len(self.rows)):
            for i in reversed(range(self.rows[n].count())): 
                self.rows[n].itemAt(i).widget().setParent(None)

        for n, keyboardRow in enumerate(defaultKeyboardLayout):
            for button in keyboardRow:
                if button in remaps[layoutIndex]:
                    newButton = DragButton(layoutIndex, remaps[layoutIndex][button])
                else:
                    newButton = DragButton(layoutIndex, button)

                newButton.setObjectName("DragButton")
                newButton.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                self.rows[n].addWidget(newButton)

    def addLayout(self):
        for layoutButton in self.layoutButtons:
            self.layoutsSwitcher.removeWidget(layoutButton)
        self.layoutButtons.insert(-1, QtWidgets.QPushButton(f"Layout {len(self.layoutButtons)}"))
        self.layoutButtons[-2].setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        layoutIndex = len(self.layoutButtons) - 2
        self.layoutButtons[-2].clicked.connect(lambda : self.switchLayout(layoutIndex))
        for layoutButton in self.layoutButtons:
            self.layoutsSwitcher.addWidget(layoutButton)

        remaps.append({})

    def switchLayout(self, layoutIndex):
        print(remaps, layoutIndex)
        self.init_layout(layoutIndex)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
