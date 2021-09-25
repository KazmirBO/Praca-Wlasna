#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from PyQt5 import *
# from PyQt5.QtWebKitWidgets import *
# import json
import os
import sys
import requests
from playsound import playsound
from youtube_search import YoutubeSearch
# github.com/joetats/youtube_search/blob/master/youtube_search/__init__.py
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QWidget, QMainWindow,
                             QStatusBar, QApplication, QGridLayout)


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Title = "Youtube music/video search."
        self.setFont(QFont('PatrickHand', 12))
        self.setWindowTitle(self.Title)
        self.resize(630, 1)
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)

        self._createMenu()
        self._createDisplay()
        self._createStatusBar()

    def _createDisplay(self):
        self.main = QVBoxLayout()
        self.video = QGridLayout()
        self.search = QHBoxLayout()

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

        self.id = []
        self.mylist = []
        self.title = []
        self.results = YoutubeSearch("'" + self.text.text() + "'",
                                     max_results=6).to_dict()

        for v in self.results:
            self.id.append(v['id'])
            self.title.append(v['title'])
            self.mylist.append(v['thumbnails'][0])

        # ----------------------------------------------------------------------

        self.image1 = QImage()
        self.image1.loadFromData(requests.get(self.mylist[0]).content)
        self.imgL1 = QLabel()
        self.zdj1 = QPixmap(self.image1)
        self.imgL1.setPixmap(self.zdj1.scaled(200, 100))
        self.downMp1 = QPushButton("Pobierz mp3")
        self.downMp1.setFixedWidth(200)
        self.play1 = QPushButton("Odtwórz 30s")
        self.play1.setFixedWidth(200)
        self.downMp1.clicked.connect(lambda: self._do(self.id[0]))
        self.play1.clicked.connect(lambda: self._pl(self.title[0], self.id[0]))

        # ----------------------------------------------------------------------

        self.image2 = QImage()
        self.image2.loadFromData(requests.get(self.mylist[1]).content)
        self.imgL2 = QLabel()
        self.zdj2 = QPixmap(self.image2)
        self.imgL2.setPixmap(self.zdj2.scaled(200, 100))
        self.downMp2 = QPushButton("Pobierz mp3")
        self.downMp2.setFixedWidth(200)
        self.play2 = QPushButton("Odtwórz 30s")
        self.play2.setFixedWidth(200)
        self.downMp2.clicked.connect(lambda: self._do(self.id[1]))
        self.play2.clicked.connect(lambda: self._pl(self.title[1], self.id[1]))

        # ----------------------------------------------------------------------

        self.image3 = QImage()
        self.image3.loadFromData(requests.get(self.mylist[2]).content)
        self.imgL3 = QLabel()
        self.zdj3 = QPixmap(self.image3)
        self.imgL3.setPixmap(self.zdj3.scaled(200, 100))
        self.downMp3 = QPushButton("Pobierz mp3")
        self.downMp3.setFixedWidth(200)
        self.play3 = QPushButton("Odtwórz 30s")
        self.play3.setFixedWidth(200)
        self.downMp3.clicked.connect(lambda: self._do(self.id[2]))
        self.play3.clicked.connect(lambda: self._pl(self.title[2], self.id[2]))

        # ----------------------------------------------------------------------

        self.image4 = QImage()
        self.image4.loadFromData(requests.get(self.mylist[3]).content)
        self.imgL4 = QLabel()
        self.zdj4 = QPixmap(self.image4)
        self.imgL4.setPixmap(self.zdj4.scaled(200, 100))
        self.downMp4 = QPushButton("Pobierz mp3")
        self.downMp4.setFixedWidth(200)
        self.play4 = QPushButton("Odtwórz 30s")
        self.play4.setFixedWidth(200)
        self.downMp4.clicked.connect(lambda: self._do(self.id[3]))
        self.play4.clicked.connect(lambda: self._pl(self.title[3], self.id[3]))

        # ----------------------------------------------------------------------

        self.image5 = QImage()
        self.image5.loadFromData(requests.get(self.mylist[4]).content)
        self.imgL5 = QLabel()
        self.zdj5 = QPixmap(self.image5)
        self.imgL5.setPixmap(self.zdj5.scaled(200, 100))
        self.downMp5 = QPushButton("Pobierz mp3")
        self.downMp5.setFixedWidth(200)
        self.play5 = QPushButton("Odtwórz 30s")
        self.play5.setFixedWidth(200)
        self.downMp5.clicked.connect(lambda: self._do(self.id[4]))
        self.play5.clicked.connect(lambda: self._pl(self.title[4], self.id[4]))

        # ----------------------------------------------------------------------

        self.image6 = QImage()
        self.image6.loadFromData(requests.get(self.mylist[5]).content)
        self.imgL6 = QLabel()
        self.zdj6 = QPixmap(self.image6)
        self.imgL6.setPixmap(self.zdj6.scaled(200, 100))
        self.downMp6 = QPushButton("Pobierz mp3")
        self.downMp6.setFixedWidth(200)
        self.play6 = QPushButton("Odtwórz 30s")
        self.play6.setFixedWidth(200)
        self.downMp6.clicked.connect(lambda: self._do(self.id[5]))
        self.play6.clicked.connect(lambda: self._pl(self.title[5], self.id[5]))

        # ----------------------------------------------------------------------

        self.video.addWidget(self.imgL1, 0, 0)
        self.video.addWidget(self.downMp1, 1, 0)
        self.video.addWidget(self.play1, 2, 0)
        self.video.addWidget(self.imgL4, 3, 0)
        self.video.addWidget(self.downMp4, 4, 0)
        self.video.addWidget(self.play4, 5, 0)

        self.video.addWidget(self.imgL2, 0, 1)
        self.video.addWidget(self.downMp2, 1, 1)
        self.video.addWidget(self.play2, 2, 1)
        self.video.addWidget(self.imgL5, 3, 1)
        self.video.addWidget(self.downMp5, 4, 1)
        self.video.addWidget(self.play5, 5, 1)

        self.video.addWidget(self.imgL3, 0, 2)
        self.video.addWidget(self.downMp3, 1, 2)
        self.video.addWidget(self.play3, 2, 2)
        self.video.addWidget(self.imgL6, 3, 2)
        self.video.addWidget(self.downMp6, 4, 2)
        self.video.addWidget(self.play6, 5, 2)

    def _do(self, id):
        os.system("youtube-dl -x --audio-format=mp3 -o '%(title)s.%(ext)s' '"
                  + id + "'")

    def _pl(self, title, id):
        os.system("youtube-dl -x --postprocessor-args '-ss 00:00:00.00 -t "
                  + "00:00:30.00' --audio-format=mp3 '" + id + "'")
        playsound(title + "-" + id + ".mp3")
        os.system("rm '" + title + "-" + id + ".mp3'")

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
