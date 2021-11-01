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
import time
from pathlib import Path
from youtube_search import YoutubeSearch
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtGui import (QFont, QImage, QPixmap)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QLineEdit, QSlider,
                             QPushButton, QLabel, QWidget, QMainWindow,
                             QStatusBar, QApplication, QGridLayout, QCheckBox,
                             )


__version__ = 'v0.1.14 - "Timestamp"'
__author__ = 'Sebastian Kolanowski'


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        super().__init__(parent)
        Title = "Youtube App"
        self.setFont(QFont('PatrickHand', 12))
        self.setWindowTitle(Title)
        self.setFixedWidth(650)
        self.setFixedHeight(100)
        self.generalLayout = QHBoxLayout()
        _centralWidget = QWidget(self)
        _centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(_centralWidget)
        self.timer = QTimer(self)
        self.showed = 0
        self.duration = 0
        self.queue = []
        self.ifSkip = 0
        self.i = 0
        # <===> PLATFORMA/SYSTEM OPERACYJNY <===>
        self.platform = platform.system()
        self.downloads_path = str(Path.home() / "Downloads")
        if self.platform == "Windows":
            self.downloads_path += "\\"
        else:
            self.downloads_path += "/"
        # <===> PLATFORMA/SYSTEM OPERACYJNY <===>
        self.Instance = vlc.Instance('--no-video')
        self.player = self.Instance.media_player_new()

        self._createMenu()
        self._createUi()
        self._createStatusBar()

    def _createUi(self):
        self.main = QVBoxLayout()

        self.butt1 = QPushButton("Pauza/Wznów")
        self.butt2 = QPushButton("Zatrzymaj")
        self.volText = QLabel("Volume: ")
        self.volText.setFixedWidth(50)
        self.volVal = QLabel()
        self.volVal.setText("100")
        self.volVal.setFixedWidth(30)
        self.repeat = QCheckBox("Powtarzaj")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setValue(100)
        self.slider.setMaximum(100)
        self.slider.setFixedWidth(150)
        self.controls = QHBoxLayout()
        self.controls.addWidget(self.butt1)
        self.controls.addWidget(self.butt2)
        self.controls.addWidget(self.repeat)
        self.controls.addWidget(self.volText)
        self.controls.addWidget(self.slider)
        self.controls.addWidget(self.volVal)

        self.text = QLineEdit()
        self.text.setPlaceholderText("Podaj tytuł filmu/utworu do wyszukania")
        self.button = QPushButton("Szukaj")
        self.button.clicked.connect(self._getVideo)
        self.search = QHBoxLayout()
        self.search.addWidget(self.text)
        self.search.addWidget(self.button)
        self.main.addLayout(self.search)

        self.strona = QLabel()
        self.strona.setText(str(self.i+1))
        self.strona.setAlignment(QtCore.Qt.AlignCenter)
        self.left = QPushButton("Poprzednia")
        self.right = QPushButton("Następna")
        self.right.clicked.connect(self._increase)
        self.left.clicked.connect(self._decrease)
        self.page = QHBoxLayout()
        self.page.addWidget(self.left)
        self.page.addWidget(self.strona)
        self.page.addWidget(self.right)

        self.played = QLabel()
        self.played.setText("Nic nie jest odtwarzane...")
        self.played.setAlignment(QtCore.Qt.AlignCenter)

        self.queueLen = QLabel()
        self.queueLen.setText("Kolejka jest pusta...")
        self.queueLen.setAlignment(QtCore.Qt.AlignCenter)

        self.kon = QLabel("Kontrolki do odtwarzacza")
        self.kon.setAlignment(QtCore.Qt.AlignCenter)

        self.musicProgress = QHBoxLayout()
        self.skip = QPushButton("Skip")
        self.skip.setFixedWidth(75)
        self.progVal = QLabel("0/0")
        self.progVal.setFixedWidth(90)
        self.musicBar = QSlider(Qt.Horizontal)
        self.musicBar.setMaximum(1000)
        self.musicBar.setValue(0)
        self.musicBar.sliderMoved.connect(self._progress)
        self.musicProgress.addWidget(self.musicBar)
        self.musicProgress.addWidget(self.progVal)
        self.musicProgress.addWidget(self.skip)

        self.generalLayout.addLayout(self.main)

# <--------------------------------------------------------------------------->

        self.image1 = QImage()
        self.imgL1 = QLabel()
        self.downMp1 = QPushButton("Pobierz mp3")
        self.downMp1.setFixedWidth(200)
        self.downMv1 = QPushButton("Pobierz mp4")
        self.downMv1.setFixedWidth(200)
        self.p1 = QPushButton("Odtwórz")
        self.p1.setFixedWidth(200)

        self.image2 = QImage()
        self.imgL2 = QLabel()
        self.downMp2 = QPushButton("Pobierz mp3")
        self.downMp2.setFixedWidth(200)
        self.downMv2 = QPushButton("Pobierz mp4")
        self.downMv2.setFixedWidth(200)
        self.p2 = QPushButton("Odtwórz")
        self.p2.setFixedWidth(200)

        self.image3 = QImage()
        self.imgL3 = QLabel()
        self.downMp3 = QPushButton("Pobierz mp3")
        self.downMp3.setFixedWidth(200)
        self.downMv3 = QPushButton("Pobierz mp4")
        self.downMv3.setFixedWidth(200)
        self.p3 = QPushButton("Odtwórz")
        self.p3.setFixedWidth(200)

        self.image4 = QImage()
        self.imgL4 = QLabel()
        self.downMp4 = QPushButton("Pobierz mp3")
        self.downMp4.setFixedWidth(200)
        self.downMv4 = QPushButton("Pobierz mp4")
        self.downMv4.setFixedWidth(200)
        self.p4 = QPushButton("Odtwórz")
        self.p4.setFixedWidth(200)

        self.image5 = QImage()
        self.imgL5 = QLabel()
        self.downMp5 = QPushButton("Pobierz mp3")
        self.downMp5.setFixedWidth(200)
        self.downMv5 = QPushButton("Pobierz mp4")
        self.downMv5.setFixedWidth(200)
        self.p5 = QPushButton("Odtwórz")
        self.p5.setFixedWidth(200)

        self.image6 = QImage()
        self.imgL6 = QLabel()
        self.downMp6 = QPushButton("Pobierz mp3")
        self.downMp6.setFixedWidth(200)
        self.downMv6 = QPushButton("Pobierz mp4")
        self.downMv6.setFixedWidth(200)
        self.p6 = QPushButton("Odtwórz")
        self.p6.setFixedWidth(200)

# <--------------------------------------------------------------------------->

        self.downMp1.clicked.connect(lambda: self._do(self.id[(self.i*6)+0]))
        self.downMv1.clicked.connect(lambda: self._dv(self.id[(self.i*6)+0]))
        self.p1.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+0], self.title[(self.i*6)+0],
                             self.time[(self.i*6)+0]))

        self.downMp2.clicked.connect(lambda: self._do(self.id[(self.i*6)+1]))
        self.downMv2.clicked.connect(lambda: self._dv(self.id[(self.i*6)+1]))
        self.p2.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+1], self.title[(self.i*6)+1],
                             self.time[(self.i*6)+1]))

        self.downMp3.clicked.connect(lambda: self._do(self.id[(self.i*6)+2]))
        self.downMv3.clicked.connect(lambda: self._dv(self.id[(self.i*6)+2]))
        self.p3.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+2], self.title[(self.i*6)+2],
                             self.time[(self.i*6)+2]))

        self.downMp4.clicked.connect(lambda: self._do(self.id[(self.i*6)+3]))
        self.downMv1.clicked.connect(lambda: self._dv(self.id[(self.i*6)+3]))
        self.p4.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+3], self.title[(self.i*6)+3],
                             self.time[(self.i*6)+3]))

        self.downMp5.clicked.connect(lambda: self._do(self.id[(self.i*6)+4]))
        self.downMv5.clicked.connect(lambda: self._dv(self.id[(self.i*6)+4]))
        self.p5.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+4], self.title[(self.i*6)+4],
                             self.time[(self.i*6)+4]))

        self.downMp6.clicked.connect(lambda: self._do(self.id[(self.i*6)+5]))
        self.downMv6.clicked.connect(lambda: self._dv(self.id[(self.i*6)+5]))
        self.p6.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+5], self.title[(self.i*6)+5],
                             self.time[(self.i*6)+5]))

# <--------------------------------------------------------------------------->

        self.video = QGridLayout()

        self.video.addWidget(self.imgL1, 0, 0)
        self.video.addWidget(self.downMp1, 1, 0)
        self.video.addWidget(self.downMv1, 2, 0)
        self.video.addWidget(self.p1, 3, 0)
        self.video.addWidget(self.imgL4, 4, 0)
        self.video.addWidget(self.downMp4, 5, 0)
        self.video.addWidget(self.downMv4, 6, 0)
        self.video.addWidget(self.p4, 7, 0)

        self.video.addWidget(self.imgL2, 0, 1)
        self.video.addWidget(self.downMp2, 1, 1)
        self.video.addWidget(self.downMv2, 2, 1)
        self.video.addWidget(self.p2, 3, 1)
        self.video.addWidget(self.imgL5, 4, 1)
        self.video.addWidget(self.downMp5, 5, 1)
        self.video.addWidget(self.downMv5, 6, 1)
        self.video.addWidget(self.p5, 7, 1)

        self.video.addWidget(self.imgL3, 0, 2)
        self.video.addWidget(self.downMp3, 1, 2)
        self.video.addWidget(self.downMv3, 2, 2)
        self.video.addWidget(self.p3, 3, 2)
        self.video.addWidget(self.imgL6, 4, 2)
        self.video.addWidget(self.downMp6, 5, 2)
        self.video.addWidget(self.downMv6, 6, 2)
        self.video.addWidget(self.p6, 7, 2)

# <--------------------------------------------------------------------------->

    def _getVideo(self):
        if self.text.text() == '':
            self._pl("dQw4w9WgXcQ", "Never Gonna Give You Up")

        self.id = []
        self.time = []
        self.mylist = []
        self.title = []
        self.results = YoutubeSearch("'" + self.text.text() + "'",
                                     max_results=60).to_dict()

        for v in self.results:
            self.id.append(v['id'])
            self.time.append(v['duration'])
            self.title.append(v['title'])
            self.mylist.append(v['thumbnails'][0])

        self.i = 0
        self.strona.setText(str(self.i+1))
        if len(self.results) >= 6:
            self._updateUi()

# <--------------------------------------------------------------------------->

    def _increase(self):
        if self.i < int(len(self.results)/6)-1 and self.showed == 1:
            self.i += 1
            self.strona.setText(str(self.i+1))
            self._updateUi()

    def _decrease(self):
        if self.i > 0 and self.showed == 1:
            self.i -= 1
            self.strona.setText(str(self.i+1))
            self._updateUi()

# <--------------------------------------------------------------------------->

    def _updateUi(self):
        if self.showed == 0:
            self.setFixedHeight(800)
            self.main.addLayout(self.video)
            self.main.addLayout(self.page)
            self.main.addWidget(self.played)
            self.main.addWidget(self.queueLen)
            self.main.addWidget(self.kon)
            self.main.addLayout(self.musicProgress)
            self.main.addLayout(self.controls)

            self.butt1.clicked.connect(lambda: self._pause())
            self.butt2.clicked.connect(lambda: self._stop())
            self.slider.valueChanged.connect(self._volume)
            self.skip.clicked.connect(lambda: self._skip())

            self.timer.timeout.connect(self._music)
            self.timer.start(100)

        self.showed = 1

# <--------------------------------------------------------------------------->

        self.image1.loadFromData(requests.get(
            self.mylist[(self.i*6)+0]).content)
        zdj1 = QPixmap(self.image1)
        self.imgL1.setPixmap(zdj1.scaled(200, 100))

# <--------------------------------------------------------------------------->

        self.image2.loadFromData(requests.get(
            self.mylist[(self.i*6)+1]).content)
        zdj2 = QPixmap(self.image2)
        self.imgL2.setPixmap(zdj2.scaled(200, 100))

# <--------------------------------------------------------------------------->

        self.image3.loadFromData(requests.get(
            self.mylist[(self.i*6)+2]).content)
        zdj3 = QPixmap(self.image3)
        self.imgL3.setPixmap(zdj3.scaled(200, 100))

# <--------------------------------------------------------------------------->

        self.image4.loadFromData(requests.get(
            self.mylist[(self.i*6)+3]).content)
        zdj4 = QPixmap(self.image4)
        self.imgL4.setPixmap(zdj4.scaled(200, 100))

# <--------------------------------------------------------------------------->

        self.image5.loadFromData(requests.get(
            self.mylist[(self.i*6)+4]).content)
        zdj5 = QPixmap(self.image5)
        self.imgL5.setPixmap(zdj5.scaled(200, 100))

# <--------------------------------------------------------------------------->

        self.image6.loadFromData(requests.get(
            self.mylist[(self.i*6)+5]).content)
        zdj6 = QPixmap(self.image6)
        self.imgL6.setPixmap(zdj6.scaled(200, 100))

# <--------------------------------------------------------------------------->

# <===> TESTED <=================================================> TESTED <===>

    def _do(self, id):
        ydl_opts = {'outtmpl': self.downloads_path + '%(title)s.%(ext)s',
                    'audio-format': 'bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        }], }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([id])

# <===> TESTED <=================================================> TESTED <===>

# <--------------------------------------------------------------------------->

# <===> TESTED <=================================================> TESTED <===>

    def _dv(self, id):
        ydl_opts = {'outtmpl': self.downloads_path + '%(title)s.%(ext)s',
                    'format': 'best'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([id])

# <===> TESTED <=================================================> TESTED <===>

# <--------------------------------------------------------------------------->

    def _pl(self, id, title, time):
        if self.player.is_playing() and self.ifSkip == 0:
            self.queue.append(id)
            self.queue.append(title)
            self.queue.append(time)
            self.queueLen.setText("W kolejce: " + str(int(len(self.queue)/3)))
        else:
            self.duration = time
            self.played.setText("Teraz odtwarzane: " + title)
            video = pafy.new("https://www.youtube.com/watch?v=" + id)
            best = video.getbest()
            playurl = best.url
            Media = self.Instance.media_new(playurl)
            Media.get_mrl()
            self.player.set_media(Media)
            self.player.play()
            self.musicBar.setValue(0)

# <--------------------------------------------------------------------------->

    def _pause(self):
        self.player.pause()

# <--------------------------------------------------------------------------->

    def _progress(self):
        self.player.set_position(self.musicBar.value()/1000)

# <--------------------------------------------------------------------------->

    def _music(self):
        self.musicBar.setValue(int(self.player.get_position()*1000))
        self.progVal.setText(
            time.strftime('%M:%S', time.gmtime(self.player.get_time()/1000))
            + "/" + str(self.duration))
        if self.repeat.checkState() != 0:
            if self.player.get_position()*100 >= 99:
                self.player.set_position(0)
        else:
            if self.player.is_playing() == 0:
                if len(self.queue) > 0 and self.player.get_position()*100 > 90:
                    self._pl(self.queue.pop(0), self.queue.pop(
                        0), self.queue.pop(0))
                    if len(self.queue) <= 0:
                        self.queueLen.setText("Kolejka jest pusta...")

# <--------------------------------------------------------------------------->

    def _stop(self):
        self.player.stop()
        self.played.setText("Nic nie jest odtwarzane...")
        self.musicBar.setValue(0)

# <--------------------------------------------------------------------------->

    def _skip(self):
        if len(self.queue) > 0:
            self.ifSkip = 1
            self._pl(self.queue.pop(0), self.queue.pop(0), self.queue.pop(0))
            self.ifSkip = 0
            if len(self.queue) <= 0:
                self.queueLen.setText("Kolejka jest pusta...")
            else:
                self.queueLen.setText("W kolejce: "
                                      + str(int(len(self.queue)/3)))

# <--------------------------------------------------------------------------->

    def _volume(self):
        self.player.audio_set_volume(self.slider.value())
        self.volVal.setText(str(self.slider.value()))

# <--------------------------------------------------------------------------->

    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction('&Exit', self.close)

# <--------------------------------------------------------------------------->

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Wersja: " + __version__
                           + ", Autor: " + __author__)
        self.setStatusBar(status)

# <--------------------------------------------------------------------------->


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
