from PyQt5 import QtWidgets, QtGui, QtCore


class TestTextBox(QtWidgets.QWidget):
    def __init__(self):
        super(TestTextBox, self).__init__()
        self.label = QtWidgets.QLabel("Click in this area to test layout.", self)
        self.label.setFixedSize(910, 60)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("""
            border: 2px dashed #424E59;
            color: #424E59;
        """)
        self.font = QtGui.QFont("Ubuntu Mono", 11)
        self.font.setStyleHint(QtGui.QFont.Monospace)
        self.font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 2)
        self.label.setFont(self.font)

        self.labels = []
        self._testModeOn = False

    def keyPressEvent(self, ev):
        if self.currentIndex == len(self.labels):
            super(TestTextBox, self).keyPressEvent(ev)
            return
        if ev.text() == self.labels[self.currentIndex].text():
            self.labels[self.currentIndex].setStyleSheet("""
                color: #424E59;
            """)
        else:
            self.labels[self.currentIndex].setStyleSheet("""
                color: #EA5C29;
            """)
        self.currentIndex += 1
        if self.currentIndex < len(self.labels):
            self._initCurrentLetterStyle()
        super(TestTextBox, self).keyPressEvent(ev)

    def mousePressEvent(self, event):
        if not self._testModeOn:
            self._testModeOn = True
            self._prepareTest()
        self.setFocus()
        super(TestTextBox, self).mousePressEvent(event)

    def _prepareTest(self):
        self.label.deleteLater()
        self.label = None
        self.labels = [QtWidgets.QLabel(letter)\
                        for letter in 'sphinx of black quartz; judge my vow.']
        for label in self.labels:
            label.setStyleSheet("""
                color: white;
            """)
            label.setFont(self.font)
            label.setFixedSize(12, 20)
            label.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(180, 0, 180, 0)
        self.layout().setSpacing(0)
        [self.layout().addWidget(label) for label in self.labels]
        
        self.currentIndex = 0
        self._initCurrentLetterStyle()

    def _initCurrentLetterStyle(self):
        self.labels[self.currentIndex].setStyleSheet("""
            background: rgba(85, 107, 122, 0.5);
            color: #ccc;
            padding-left: 2px;
        """)


    # def __init__(self):
    #     self.line = QtWidgets.QLineEdit()
    #     self.line.setStyleSheet("""
    #         border: none;
    #         color: #424E59;
    #     """)
    #     font = QtGui.QFont("Ubuntu Mono", 11)
    #     font.setStyleHint(QtGui.QFont.Monospace)
    #     font.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 2)

    #     self.line.setFont(font)

    #     self.line.setFixedWidth(10)
    #     self._placeHolder = "this is a test text"
    #     self.line.textEdited.connect(self.keyPressEvent)
    #     self._entered = 0

    #     self.label = QtWidgets.QLabel()
    #     self.label.setText(self._placeHolder)
    #     self.label.setStyleSheet("""
    #         border: none;
    #         color: white;
    #     """)
    #     self.label.setFont(font)

    #     self.widgets = [self.line, self.label]

    # def keyPressEvent(self, key):
    #     self.line.setFocus()
    #     self.line.setFixedWidth(self.line.width() + 11)
    #     self._placeHolder = self._placeHolder[1:]
    #     self.label.setText(self._placeHolder)
    #     self._entered += 1
    #     self.line.setCursorPosition(self._entered)

