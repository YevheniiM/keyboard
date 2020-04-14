from PyQt5 import QtWidgets

import json


class DataManager:
    class __DataManager:
        def __init__(self):
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
        
        def setCurrentLayoutIndex(self, newLayoutIndex):
            self.currentLayout = newLayoutIndex

        def addNewLayout(self):
            self.remaps.append({})
            layoutIndex = len(self.layouts)
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
        
        def dump(self):
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
            fileName = '../BE/advanced_layout/helpers/config.json'
            # fileName = '../FE/config.json'
            if fileName != '':
                with open(fileName, 'w') as jf:
                    json.dump(resultFile, jf)
            self.notify()

        @staticmethod
        def notify():
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)

            msg.setText("The configuration file has been saved")
            # msg.setInformativeText("This is additional information")
            msg.setWindowTitle("Configuration file saved")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

            msg.exec_()

        def setModeType(self, modeType):
            self.layouts[self.currentLayout]['mode']['type'] = modeType

        def getModeType(self):
            return self.layouts[self.currentLayout]['mode']['type']

        def setModeValue(self, modeValue):
            self.layouts[self.currentLayout]['mode']['value'] = modeValue

        def getModeValue(self):
            return self.layouts[self.currentLayout]['mode']['value']

        def setAIType(self, AIType):
            self.layouts[self.currentLayout]['ai'] = AIType

        def getAIType(self):
            return self.layouts[self.currentLayout]['ai']

        def addShorthand(self, shorthandKey, shorthandValue):
            self.layouts[self.currentLayout]['key_strings'][shorthandKey] = shorthandValue

        def removeShorthand(self, shorthandKey):
            del self.layouts[self.currentLayout]['key_strings'][shorthandKey]

        def getShorthands(self):
            return self.layouts[self.currentLayout]['key_strings']

        def setLayoutName(self, layoutName):
            self.layouts[self.currentLayout]['name'] = layoutName

    instance = None
    def __init__(self):
        if DataManager.instance is None:
            DataManager.instance = DataManager.__DataManager()

    def __getattr__(self, name):
        return getattr(self.instance, name)
