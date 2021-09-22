#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, requests, json
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *
from youtube_search import YoutubeSearch


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Title = "Youtube music/video search."
        self.setFont(QFont('PatrickHand', 12))
        self.setWindowTitle(self.Title)
        self.resize(925, 255)
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)

        self._createMenu()
        self._createDisplay()
        self._createStatusBar()

    def _createDisplay(self):
        self.main = QVBoxLayout()
        self.search = QHBoxLayout()
        self.video = QHBoxLayout()

        self.text = QLineEdit()
        self.button = QPushButton("Szukaj")
        self.button.clicked.connect(self._getVideo)
        self.search.addWidget(self.text)
        self.search.addWidget(self.button)

        self.main.addLayout(self.search)
        self.main.addLayout(self.video)
        self.generalLayout.addLayout(self.main)

    def _getVideo(self):
        for i in reversed(range(self.video.count())):
            self.video.itemAt(i).widget().setParent(None)
        self.image1 = QImage()
        self.image2 = QImage()
        self.image3 = QImage()
        self.id = []
        self.mylist = []
        self.results = YoutubeSearch("'"+self.text.text()+"'", max_results=3).to_dict()
        for v in self.results:
            self.id.append(v['id'])
            self.mylist.append(v['thumbnails'][0])

        # print(self.id)
        # print(self.mylist)
        self.image1.loadFromData(requests.get(self.mylist[0]).content)
        self.image2.loadFromData(requests.get(self.mylist[1]).content)
        self.image3.loadFromData(requests.get(self.mylist[2]).content)
        self.image_label1 = QLabel()
        self.zdj1 = QPixmap(self.image1)
        self.image_label2 = QLabel()
        self.zdj2 = QPixmap(self.image2)
        self.image_label3 = QLabel()
        self.zdj3 = QPixmap(self.image3)
        self.image_label1.setPixmap(self.zdj1.scaled(200, 100))
        self.image_label2 = QLabel()
        self.image_label2.setPixmap(self.zdj2.scaled(200, 100))
        self.image_label3 = QLabel()
        self.image_label3.setPixmap(self.zdj3.scaled(200, 100))
        self.down1 = QPushButton("Pobierz")
        self.down2 = QPushButton("Pobierz")
        self.down3 = QPushButton("Pobierz")
        self.down1.clicked.connect(self._download1)
        self.down2.clicked.connect(self._download2)
        self.down3.clicked.connect(self._download3)
        self.video.addWidget(self.image_label1)
        self.video.addWidget(self.down1)
        self.video.addWidget(self.image_label2)
        self.video.addWidget(self.down2)
        self.video.addWidget(self.image_label3)
        self.video.addWidget(self.down3)

    def _download1(self):
        os.system("youtube-dl -x --audio-format=mp3 '" + self.id[0] + "'")

    def _download2(self):
        os.system("youtube-dl -x --audio-format=mp3 '" + self.id[1] + "'")

    def _download3(self):
        os.system("youtube-dl -x --audio-format=mp3 '" + self.id[2] + "'")

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Hello World!")
        self.setStatusBar(status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
