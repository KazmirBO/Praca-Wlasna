#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, random, os, atexit, platform
# from PyQt5 import *
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QHBoxLayout, QWidget, QGridLayout, QSpinBox,
                             QMainWindow, QApplication, QLabel, QLineEdit)


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Title = "Test program"
        self.setWindowTitle(self.Title)
        self.resize(1, 1)
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)
        self._createDisplay()
        pass

    def __del__(self):
        self.expo()
        pass

    def _createDisplay(self):
        self.main = QGridLayout()
        self.count = QSpinBox()
        self.count.setFixedWidth(50)
        self.count.valueChanged.connect(self.create)
        self.impo()
        self.generalLayout.addWidget(self.count)
        self.generalLayout.addLayout(self.main)
        pass

    def create(self):
        i = 0
        self.max = int(self.count.value())
        if self.max >= 0:
            for i in reversed(range(self.main.count())):
                self.main.itemAt(i).widget().setParent(None)
                pass
            pass
        for i in range(self.max):
            self.main.addWidget(QLineEdit(), int(i%2), int(i/2))
            pass
        pass

    def impo(self):
        if platform.system() == 'Linux':
            self.response = '/tmp/test.txt'
            if os.path.isfile(self.response) == False:
                f = open(self.response, 'w')
                f.write("0")
                f.close()
                pass
            pass
        elif platform.system() == 'Windows':
            self.response = './test.txt'
            if os.path.isfile(self.response) == False:
                f = open(self.response, 'w')
                f.write("0")
                f.close()
                pass
            pass
        pass

        stats = []
        with open(self.response, 'r') as f:
            stats = f.read().splitlines()
        f.close()
        self.count.setValue(int(stats[0]))
        pass

    def expo(self):
        with open(self.response, 'w') as f:
            # f.write('%s\n' % value/text())
            f.write('%s\n' % self.max)
        pass

    pass

def window():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
    pass

if __name__ == '__main__':
    window()
