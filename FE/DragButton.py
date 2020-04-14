from PyQt5 import QtCore, QtGui, QtWidgets
import string


def widgetsAt(pos):
    widgets = []
    widgetAt = QtWidgets.qApp.widgetAt(pos)

    while widgetAt:
        widgets.append(widgetAt)

        # Make widget invisible to further enquiries
        widgetAt.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        widgetAt = QtWidgets.qApp.widgetAt(pos)

    # Restore attribute
    for widget in widgets:
        widget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

    return widgets


class DragButtonStyle:
    DEFAULT_STYLE = """
        QPushButton {
            border: 2px groove #4F5A61;
            border-radius: 10px;
            background: rgba(48, 55, 59, 0.2);
            color: rgb(123,160,176);
            margin: 7px 1px;
        }
        QPushButton:hover {
            background: rgba(48, 55, 59, 0.8);
        }
        QPushButton:clicked {
            background-color: #2e86de;
        }
    """
    DRAG_STYLE = """
        QPushButton:hover {
            background-color: #2e86de;
        }
    """
    REMAPPED_TARGET_STYLE = """
        QPushButton {
            border: 2px groove #4F5A61;
            border-radius: 10px;
            background: rgba(56, 93, 122, 0.6);
            color: white;
            margin: 7px 1px;
            font-weight: 500;
        }
    """
    REMAPPED_SOURCE_STYLE = """
        QPushButton {
            border: 2px groove #4F5A61;
            border-radius: 10px;
            background: rgba(85, 107, 122, 0.6);
            color: #676767;
            margin: 7px 1px;
        }
    """


specialButtonSizes = {
    "tab": 1.25,
    "caps lock": 1.5,
    "shift": 1.75,
    "backspace": 1.25,
    "enter": 1.5,
    "ctrl": 1.25,
    "fn": 1,
    "win": 1,
    "alt": 1,
    "": 2
}


class DragButton(QtWidgets.QPushButton):
    def __init__(self, layoutIndex, remaps, button, *args):
        remapped = False
        if button in remaps[layoutIndex]:
            button = '/'.join(remaps[layoutIndex][button])
            remapped = True
        else:
            self.defaultText = button
        super().__init__(button, *args)
        self.remaps = remaps
        self.layoutIndex = layoutIndex
        self.setObjectName("DragButton")
        self.setStyleSheet(DragButtonStyle.DEFAULT_STYLE)
        if button in string.ascii_uppercase:
            font = QtGui.QFont("Arial", 9)
            font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, .75)
            self.setFont(font)
        if button == "":
            self.setStyleSheet("background: rgba(0, 0, 0, 0.0);")
        if button in specialButtonSizes:
            self.setFixedSize(int(70) * specialButtonSizes[button], 70)
        if remapped:
            self.setStyleSheet(DragButtonStyle.REMAPPED_TARGET_STYLE)
            # self.setFont(QtGui.QFont("Arial", 10, weight=500))

        remapSources = []
        for x in remaps[layoutIndex].items():
            remapSources += x[1]
        if button in remapSources:
            self.setStyleSheet(DragButtonStyle.REMAPPED_SOURCE_STYLE)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
        self.raise_()
        self.setCursor(QtCore.Qt.OpenHandCursor)

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            # self.setStyleSheet(DragButtonStyle.DRAG_STYLE)
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)
            self.raise_()
            self.__mouseMovePos = globalPos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.OpenHandCursor)
        if self.__mousePressPos is not None:
            widgets = widgetsAt(QtGui.QCursor.pos())
            for widget in widgets:
                if widget.objectName() == self.objectName() and widget.text() != self.text():
                    if not widget.defaultText in self.remaps[self.layoutIndex]:
                        self.remaps[self.layoutIndex][widget.defaultText] = [widget.defaultText]
                    if not self.text() in self.remaps[self.layoutIndex][widget.defaultText]\
                        and len(self.remaps[self.layoutIndex][widget.defaultText]) < 3:
                        self.remaps[self.layoutIndex][widget.defaultText].append(self.defaultText)
                        widget.setText('/'.join(
                            self.remaps[self.layoutIndex][widget.defaultText]
                        ))
                        self.setStyleSheet(DragButtonStyle.REMAPPED_SOURCE_STYLE)
                        widget.setStyleSheet(DragButtonStyle.REMAPPED_TARGET_STYLE)
                    else:
                        self.setStyleSheet(self.styleSheet())
                    break

            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return
        self.setCursor(QtCore.Qt.PointingHandCursor)

        super(DragButton, self).mouseReleaseEvent(event)
