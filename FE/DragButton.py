from PyQt5 import QtCore, QtGui, QtWidgets


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


class DragButton(QtWidgets.QPushButton):
    def __init__(self, layoutIndex, remaps, button, *args):
        if button in remaps[layoutIndex]:
            button = remaps[layoutIndex][button]
        super().__init__(button, *args)
        self.remaps = remaps
        self.layoutIndex = layoutIndex
        self.setObjectName("DragButton")
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
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos
        self.setCursor(QtCore.Qt.ClosedHandCursor)

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.OpenHandCursor)
        if self.__mousePressPos is not None:
            widgets = widgetsAt(QtGui.QCursor.pos())
            for widget in widgets:
                if widget.objectName() == self.objectName():
                    if widget.text() != self.text():
                        self.remaps[self.layoutIndex][widget.text()] = self.text()
                        widget.setText(self.text())
                        break

            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return
        self.setCursor(QtCore.Qt.PointingHandCursor)

        super(DragButton, self).mouseReleaseEvent(event)
