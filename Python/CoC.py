#!/usr/bin/env python
# UTF-8

import sys, random
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class StartWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Title = "Call of Cthulhu - Player Character Guide"
        self.setFont(QFont('PatrickHand', 12))
        self.setWindowTitle(self.Title)
        self.resize(500, 150)
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)

        self._createMenu()
        self._createDisplay()
        self._createStatusBar()

    def _createDisplay(self):
        self.characteristic = QGridLayout()

        self.characteristic.addWidget(QLabel("STR"), 0, 0)
        self.STR = QSpinBox()
        self.STR.setReadOnly(True)
        self.characteristic.addWidget(self.STR, 0, 1)

        self.characteristic.addWidget(QLabel("DEX"), 0, 2)
        self.DEX = QSpinBox()
        self.DEX.setReadOnly(True)
        self.characteristic.addWidget(self.DEX, 0, 3)

        self.characteristic.addWidget(QLabel("INT"), 0, 4)
        self.INT = QSpinBox()
        self.INT.setReadOnly(True)
        self.characteristic.addWidget(self.INT, 0, 5)

        self.characteristic.addWidget(QLabel("CON"), 1, 0)
        self.CON = QSpinBox()
        self.CON.setReadOnly(True)
        self.characteristic.addWidget(self.CON, 1, 1)

        self.characteristic.addWidget(QLabel("APP"), 1, 2)
        self.APP = QSpinBox()
        self.APP.setReadOnly(True)
        self.characteristic.addWidget(self.APP, 1, 3)

        self.characteristic.addWidget(QLabel("POW"), 1, 4)
        self.POW = QSpinBox()
        self.POW.setReadOnly(True)
        self.characteristic.addWidget(self.POW, 1, 5)

        self.characteristic.addWidget(QLabel("SIZ"), 2, 0)
        self.SIZ = QSpinBox()
        self.SIZ.setReadOnly(True)
        self.characteristic.addWidget(self.SIZ, 2, 1)

        self.characteristic.addWidget(QLabel("EDU"), 2, 2)
        self.EDU = QSpinBox()
        self.EDU.setReadOnly(True)
        self.characteristic.addWidget(self.EDU, 2, 3)

        # ----------------------------------------------------------------------

        self.roll = QPushButton("&Random", self)
        self.roll.clicked.connect(self.Random)

        # ----------------------------------------------------------------------

        self.generalLayout.addLayout(self.characteristic)
        self.generalLayout.addWidget(self.roll)

        # ----------------------------------------------------------------------

    def Random(self):
        self.STR.setValue(self.Roll3d6())
        self.DEX.setValue(self.Roll3d6())
        self.CON.setValue(self.Roll3d6())
        self.APP.setValue(self.Roll3d6())
        self.POW.setValue(self.Roll3d6())
        self.EDU.setValue(self.Roll3d6())
        self.SIZ.setValue(self.Roll2d6())
        self.INT.setValue(self.Roll2d6())

    def Roll3d6(self):
        suma = (random.randint(1, 6) + random.randint(1, 6)
                + random.randint(1, 6))*5
        return suma

    def Roll2d6(self):
        suma = (random.randint(1, 6) + random.randint(1, 6) + 6)*5
        return suma

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Get File Name', self.getFileName)
        # self.menu.addAction('&Import', self.impo)
        # self.menu.addAction('&Export', self.expo)
        self.menu.addAction('&Exit', self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Hello World!")
        self.setStatusBar(status)

    def getFileName(self):
        filename = QFileDialog.getOpenFileName(
            self,
            'Select File',
            '',
            'Character File (*.chr);; All Files (*)'
            )[0]
        self.response = filename.split("/")[-1]
        self.Title = "Character Sheet - Call of Cthulhu - " + self.response
        self.setWindowTitle(self.Title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    app.exec()
