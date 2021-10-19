#!/usr/bin/env python
# -*- coding: utf-8 -*-
# github.com/joetats/youtube_search/blob/master/youtube_search/__init__.py
# https://stackoverflow.com/questions/18054500/how-to-use-youtube-dl-from-a-python-program

import sys
import requests
import vlc
import pafy
import youtube_dl
import platform
from pathlib import Path
from youtube_search import YoutubeSearch
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QLineEdit, QSlider,
                             QPushButton, QLabel, QWidget, QMainWindow,
                             QStatusBar, QApplication, QGridLayout, QLCDNumber,
                             )


__version__ = "v0.1.7"
__author__ = "Sebastian Kolanowski"

platform = platform.system()
downloads_path = str(Path.home() / "Downloads")
if platform == "Windows":
    downloads_path += "\\"
else:
    downloads_path += "/"
Instance = vlc.Instance('--no-video')
player = Instance.media_player_new()


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Title = "Youtube music/video downloader."
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
        self.controls = QHBoxLayout()

        self.butt1 = QPushButton("Pauza/Wznów")
        self.butt2 = QPushButton("Zatrzymaj")
        self.volText = QLabel("Volume: ")
        self.volText.setFixedWidth(50)
        self.volVal = QLCDNumber()
        self.volVal.display(100)
        self.volVal.setFixedWidth(70)
        self.volVal.setFixedHeight(30)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setValue(100)
        self.slider.setFixedWidth(150)
        self.controls.addWidget(self.butt1)
        self.controls.addWidget(self.butt2)
        self.controls.addWidget(self.volText)
        self.controls.addWidget(self.slider)
        self.controls.addWidget(self.volVal)

        self.text = QLineEdit()
        self.text.setPlaceholderText("Podaj tytuł filmu/utworu do wyszukania")
        self.button = QPushButton("Szukaj")
        self.button.clicked.connect(self._getVideo)
        self.search.addWidget(self.text)
        self.search.addWidget(self.button)

        self.main.addLayout(self.search)
        self.main.addLayout(self.video)

        self.played = QLabel()
        self.played.setText("Nic nie jest odtwarzane...")
        self.played.setAlignment(QtCore.Qt.AlignCenter)

        self.kon = QLabel("Kontrolki do odtwarzacza")
        self.kon.setAlignment(QtCore.Qt.AlignCenter)

        self.proBar = QSlider(Qt.Horizontal)

        self.main.addWidget(self.played)
        self.main.addWidget(self.kon)
        self.main.addWidget(self.proBar)
        self.main.addLayout(self.controls)
        self.generalLayout.addLayout(self.main)

        # ---------------------------------------------------------------------

    def _getVideo(self):
        if self.text.text() == '':
            self.text.setText("Epic Sax Guy")
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

        # ---------------------------------------------------------------------

        self.image1 = QImage()
        self.image1.loadFromData(requests.get(self.mylist[0]).content)
        self.imgL1 = QLabel()
        self.zdj1 = QPixmap(self.image1)
        self.imgL1.setPixmap(self.zdj1.scaled(200, 100))
        self.downMp1 = QPushButton("Pobierz mp3")
        self.downMp1.setFixedWidth(200)
        self.downMv1 = QPushButton("Pobierz mp4")
        self.downMv1.setFixedWidth(200)
        self.p1 = QPushButton("Odtwórz")
        self.p1.setFixedWidth(200)
        self.downMp1.clicked.connect(lambda: self._do(self.id[0]))
        self.downMv1.clicked.connect(lambda: self._dv(self.id[0]))
        self.p1.clicked.connect(lambda: self._pl(self.id[0], self.title[0]))

        # ---------------------------------------------------------------------

        self.image2 = QImage()
        self.image2.loadFromData(requests.get(self.mylist[1]).content)
        self.imgL2 = QLabel()
        self.zdj2 = QPixmap(self.image2)
        self.imgL2.setPixmap(self.zdj2.scaled(200, 100))
        self.downMp2 = QPushButton("Pobierz mp3")
        self.downMp2.setFixedWidth(200)
        self.downMv2 = QPushButton("Pobierz mp4")
        self.downMv2.setFixedWidth(200)
        self.p2 = QPushButton("Odtwórz")
        self.p2.setFixedWidth(200)
        self.downMp2.clicked.connect(lambda: self._do(self.id[1]))
        self.downMv2.clicked.connect(lambda: self._dv(self.id[1]))
        self.p2.clicked.connect(lambda: self._pl(self.id[1], self.title[1]))

        # ---------------------------------------------------------------------

        self.image3 = QImage()
        self.image3.loadFromData(requests.get(self.mylist[2]).content)
        self.imgL3 = QLabel()
        self.zdj3 = QPixmap(self.image3)
        self.imgL3.setPixmap(self.zdj3.scaled(200, 100))
        self.downMp3 = QPushButton("Pobierz mp3")
        self.downMp3.setFixedWidth(200)
        self.downMv3 = QPushButton("Pobierz mp4")
        self.downMv3.setFixedWidth(200)
        self.p3 = QPushButton("Odtwórz")
        self.p3.setFixedWidth(200)
        self.downMp3.clicked.connect(lambda: self._do(self.id[2]))
        self.downMv3.clicked.connect(lambda: self._dv(self.id[2]))
        self.p3.clicked.connect(lambda: self._pl(self.id[2], self.title[2]))

        # ---------------------------------------------------------------------

        self.image4 = QImage()
        self.image4.loadFromData(requests.get(self.mylist[3]).content)
        self.imgL4 = QLabel()
        self.zdj4 = QPixmap(self.image4)
        self.imgL4.setPixmap(self.zdj4.scaled(200, 100))
        self.downMp4 = QPushButton("Pobierz mp3")
        self.downMp4.setFixedWidth(200)
        self.downMv4 = QPushButton("Pobierz mp4")
        self.downMv4.setFixedWidth(200)
        self.p4 = QPushButton("Odtwórz")
        self.p4.setFixedWidth(200)
        self.downMp4.clicked.connect(lambda: self._do(self.id[3]))
        self.downMv1.clicked.connect(lambda: self._dv(self.id[3]))
        self.p4.clicked.connect(lambda: self._pl(self.id[3], self.title[3]))

        # ---------------------------------------------------------------------

        self.image5 = QImage()
        self.image5.loadFromData(requests.get(self.mylist[4]).content)
        self.imgL5 = QLabel()
        self.zdj5 = QPixmap(self.image5)
        self.imgL5.setPixmap(self.zdj5.scaled(200, 100))
        self.downMp5 = QPushButton("Pobierz mp3")
        self.downMp5.setFixedWidth(200)
        self.downMv5 = QPushButton("Pobierz mp4")
        self.downMv5.setFixedWidth(200)
        self.p5 = QPushButton("Odtwórz")
        self.p5.setFixedWidth(200)
        self.downMp5.clicked.connect(lambda: self._do(self.id[4]))
        self.downMv5.clicked.connect(lambda: self._dv(self.id[4]))
        self.p5.clicked.connect(lambda: self._pl(self.id[4], self.title[4]))

        # ---------------------------------------------------------------------

        self.image6 = QImage()
        self.image6.loadFromData(requests.get(self.mylist[5]).content)
        self.imgL6 = QLabel()
        self.zdj6 = QPixmap(self.image6)
        self.imgL6.setPixmap(self.zdj6.scaled(200, 100))
        self.downMp6 = QPushButton("Pobierz mp3")
        self.downMp6.setFixedWidth(200)
        self.downMv6 = QPushButton("Pobierz mp4")
        self.downMv6.setFixedWidth(200)
        self.p6 = QPushButton("Odtwórz")
        self.p6.setFixedWidth(200)
        self.downMp6.clicked.connect(lambda: self._do(self.id[5]))
        self.downMv6.clicked.connect(lambda: self._dv(self.id[5]))
        self.p6.clicked.connect(lambda: self._pl(self.id[5], self.title[5]))

        # ---------------------------------------------------------------------

        self.video.addWidget(self.imgL1, 0, 0)
        self.video.addWidget(self.downMp1, 1, 0)
        self.video.addWidget(self.downMv1, 2, 0)
        self.video.addWidget(self.p1, 3, 0)
        self.video.addWidget(self.imgL4, 4, 0)
        self.video.addWidget(self.downMp4, 5, 0)
        self.video.addWidget(self.downMv4, 6, 0)
        self.video.addWidget(self.p4, 7, 0)

        # ---------------------------------------------------------------------

        self.video.addWidget(self.imgL2, 0, 1)
        self.video.addWidget(self.downMp2, 1, 1)
        self.video.addWidget(self.downMv2, 2, 1)
        self.video.addWidget(self.p2, 3, 1)
        self.video.addWidget(self.imgL5, 4, 1)
        self.video.addWidget(self.downMp5, 5, 1)
        self.video.addWidget(self.downMv5, 6, 1)
        self.video.addWidget(self.p5, 7, 1)

        # ---------------------------------------------------------------------

        self.video.addWidget(self.imgL3, 0, 2)
        self.video.addWidget(self.downMp3, 1, 2)
        self.video.addWidget(self.downMv3, 2, 2)
        self.video.addWidget(self.p3, 3, 2)
        self.video.addWidget(self.imgL6, 4, 2)
        self.video.addWidget(self.downMp6, 5, 2)
        self.video.addWidget(self.downMv6, 6, 2)
        self.video.addWidget(self.p6, 7, 2)

        # ---------------------------------------------------------------------

        # <===> TESTED <=========================================> TESTED <===>

    def _do(self, id):
        ydl_opts = {'outtmpl': downloads_path + '%(title)s.%(ext)s',
                    'audio-format': 'bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        }], }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([id])

        # <===> TESTED <=========================================> TESTED <===>

    def _dv(self, id):
        ydl_opts = {'outtmpl': downloads_path + '%(title)s.%(ext)s',
                    'format': 'best'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([id])

        # <===> TESTED <=========================================> TESTED <===>

        # ---------------------------------------------------------------------

    def _pl(self, id, title):
        if player.is_playing():
            self.stop()
        self.played.setText("Teraz odtwarzane: " + title)
        video = pafy.new("https://www.youtube.com/watch?v=" + id)
        best = video.getbest()
        playurl = best.url
        Media = Instance.media_new(playurl)
        Media.get_mrl()
        player.set_media(Media)
        player.play()
        self.butt1.clicked.connect(lambda: self.pause())
        self.butt2.clicked.connect(lambda: self.stop())
        self.slider.valueChanged.connect(self._volume)
        self.proBar.valueChanged.connect(self.progress)

        # ---------------------------------------------------------------------

    def pause(self):
        player.pause()

        # ---------------------------------------------------------------------

    def progress(self):
        player.set_position(self.proBar.value()/100)

        # ---------------------------------------------------------------------

    def stop(self):
        player.stop()
        self.played.setText("Nic nie jest odtwarzane...")

        # ---------------------------------------------------------------------

    def _volume(self):
        player.audio_set_volume(self.slider.value())
        self.volVal.display(self.slider.value())

        # ---------------------------------------------------------------------

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

        # ---------------------------------------------------------------------

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Wersja: " + __version__
                           + ", Autor: " + __author__)
        self.setStatusBar(status)

        # ---------------------------------------------------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
