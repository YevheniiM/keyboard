from PyQt5 import QtCore, QtWidgets


class BoxLayoutFactory():
    def __init__(self, centralWidget):
        self.centralWidget = centralWidget

    def getLayout(self, layoutType, geometry, margins, objectName):
        horizontalLayoutWidget_ = QtWidgets.QWidget(self.centralWidget)
        horizontalLayoutWidget_.setGeometry(QtCore.QRect(*geometry))
        horizontalLayoutWidget_.setObjectName("horizontalLayoutWidget_")
        layout = layoutType(horizontalLayoutWidget_)
        layout.setContentsMargins(*margins)
        layout.setObjectName(objectName)
        return layout
