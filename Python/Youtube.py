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
import webbrowser
from pathlib import Path
from youtube_search import YoutubeSearch
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt, QTimer, QThread)
from PyQt5.QtGui import (QFont, QImage, QPixmap)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QLineEdit, QSlider,
                             QPushButton, QLabel, QWidget, QMainWindow,
                             QStatusBar, QApplication, QGridLayout, QCheckBox,
                             )


__version__ = 'v0.2.1 - "New Interface + Code Optimize"'
__author__ = 'Sebastian Kolanowski'


class _DownloadMP3(QThread):
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, id, path, parent=None):
        QThread.__init__(self, parent)
        self.id = id
        self.path = path

    def run(self):
        ydl_opts = {'outtmpl': self.path + '%(title)s.%(ext)s',
                    'audio-format': 'bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        }], }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.id])


class _DownloadMP4(QThread):
    notifyProgress = QtCore.pyqtSignal(int)

    def __init__(self, id, path, parent=None):
        QThread.__init__(self, parent)
        self.id = id
        self.path = path

    def run(self):
        ydl_opts = {'outtmpl': self.path + '%(title)s.%(ext)s',
                    'format': 'best'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.id])


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        super().__init__(parent)
        Title = "Youtube App"
        self.setWindowTitle(Title)
        self.setFixedWidth(700)
        self.setFixedHeight(100)
        self.generalLayout = QHBoxLayout()
        _centralWidget = QWidget(self)
        _centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(_centralWidget)
        self.timer = QTimer(self)
        self.i = 0
        self.queue = []
        self.ifSkip = 0
        self.showed = 0
        self.duration = 0
        # <===> PLATFORMA/SYSTEM OPERACYJNY <===>
        self.platform = platform.system()
        self.downloads_path = str(Path.home() / "Downloads")
        if self.platform == "Windows":
            self.downloads_path += "\\"
            self.setFont(QFont('Calibri', 12))
        else:
            self.downloads_path += "/"
            self.setFont(QFont('PatrickHand', 12))
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
        self.volText = QLabel("Głośność 🔈: ")
        self.volText.setFixedWidth(80)
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
        self.left = QPushButton("⬅️ Poprzednia")
        self.right = QPushButton("Następna ➡️")
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
        self.skip.setFixedWidth(80)
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
        self.downMp1 = QPushButton("MP3 ⬇")
        self.downMv1 = QPushButton("MP4 ⬇")
        self.p1 = QPushButton("PLY ▶️")
        self.p1.setFixedWidth(100)
        self.yt1 = QPushButton("YT 🌍")
        self.yt1.setFixedWidth(100)

        self.image2 = QImage()
        self.imgL2 = QLabel()
        self.downMp2 = QPushButton("MP3 ⬇")
        self.downMv2 = QPushButton("MP4 ⬇")
        self.p2 = QPushButton("PLY ▶️")
        self.p2.setFixedWidth(100)
        self.yt2 = QPushButton("YT 🌍")
        self.yt2.setFixedWidth(100)

        self.image3 = QImage()
        self.imgL3 = QLabel()
        self.downMp3 = QPushButton("MP3 ⬇")
        self.downMv3 = QPushButton("MP4 ⬇")
        self.p3 = QPushButton("PLY ▶️")
        self.p3.setFixedWidth(100)
        self.yt3 = QPushButton("YT 🌍")
        self.yt3.setFixedWidth(100)

        self.image4 = QImage()
        self.imgL4 = QLabel()
        self.downMp4 = QPushButton("MP3 ⬇")
        self.downMv4 = QPushButton("MP4 ⬇")
        self.p4 = QPushButton("PLY ▶️")
        self.p4.setFixedWidth(100)
        self.yt4 = QPushButton("YT 🌍")
        self.yt4.setFixedWidth(100)

        self.image5 = QImage()
        self.imgL5 = QLabel()
        self.downMp5 = QPushButton("MP3 ⬇")
        self.downMv5 = QPushButton("MP4 ⬇")
        self.p5 = QPushButton("PLY ▶️")
        self.p5.setFixedWidth(100)
        self.yt5 = QPushButton("YT 🌍")
        self.yt5.setFixedWidth(100)

        self.image6 = QImage()
        self.imgL6 = QLabel()
        self.downMp6 = QPushButton("MP3 ⬇")
        self.downMv6 = QPushButton("MP4 ⬇")
        self.p6 = QPushButton("PLY ▶️")
        self.p6.setFixedWidth(100)
        self.yt6 = QPushButton("YT 🌍")
        self.yt6.setFixedWidth(100)

# <--------------------------------------------------------------------------->

        self.downMp1.clicked.connect(lambda: self._do(
            self.id[(self.i*6)+0], self.downMp1))
        self.downMv1.clicked.connect(lambda: self._dv(self.id[(self.i*6)+0]))
        self.p1.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+0], self.title[(self.i*6)+0],
                             self.time[(self.i*6)+0]))

        self.downMp2.clicked.connect(lambda: self._do(
            self.id[(self.i*6)+1], self.downMp2))
        self.downMv2.clicked.connect(lambda: self._dv(self.id[(self.i*6)+1]))
        self.p2.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+1], self.title[(self.i*6)+1],
                             self.time[(self.i*6)+1]))

        self.downMp3.clicked.connect(lambda: self._do(
            self.id[(self.i*6)+2], self.downMp3))
        self.downMv3.clicked.connect(lambda: self._dv(self.id[(self.i*6)+2]))
        self.p3.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+2], self.title[(self.i*6)+2],
                             self.time[(self.i*6)+2]))

        self.downMp4.clicked.connect(lambda: self._do(
            self.id[(self.i*6)+3], self.downMp4))
        self.downMv1.clicked.connect(lambda: self._dv(self.id[(self.i*6)+3]))
        self.p4.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+3], self.title[(self.i*6)+3],
                             self.time[(self.i*6)+3]))

        self.downMp5.clicked.connect(lambda: self._do(
            self.id[(self.i*6)+4], self.downMp5))
        self.downMv5.clicked.connect(lambda: self._dv(self.id[(self.i*6)+4]))
        self.p5.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+4], self.title[(self.i*6)+4],
                             self.time[(self.i*6)+4]))

        self.downMp6.clicked.connect(lambda: self._do(
            self.id[(self.i*6)+5], self.downMp6))
        self.downMv6.clicked.connect(lambda: self._dv(self.id[(self.i*6)+5]))
        self.p6.clicked.connect(
            lambda: self._pl(self.id[(self.i*6)+5], self.title[(self.i*6)+5],
                             self.time[(self.i*6)+5]))

# <--------------------------------------------------------------------------->

        self.video = QGridLayout()

        self.do1 = QHBoxLayout()
        self.do1.addWidget(self.downMp1)
        self.do1.addWidget(self.downMv1)
        self.do2 = QHBoxLayout()
        self.do2.addWidget(self.downMp2)
        self.do2.addWidget(self.downMv2)
        self.do3 = QHBoxLayout()
        self.do3.addWidget(self.downMp3)
        self.do3.addWidget(self.downMv3)
        self.do4 = QHBoxLayout()
        self.do4.addWidget(self.downMp4)
        self.do4.addWidget(self.downMv4)
        self.do5 = QHBoxLayout()
        self.do5.addWidget(self.downMp5)
        self.do5.addWidget(self.downMv5)
        self.do6 = QHBoxLayout()
        self.do6.addWidget(self.downMp6)
        self.do6.addWidget(self.downMv6)

# <--------------------------------------------------------------------------->

        self.od1 = QHBoxLayout()
        self.od1.addWidget(self.p1)
        self.od1.addWidget(self.yt1)
        self.od2 = QHBoxLayout()
        self.od2.addWidget(self.p2)
        self.od2.addWidget(self.yt2)
        self.od3 = QHBoxLayout()
        self.od3.addWidget(self.p3)
        self.od3.addWidget(self.yt3)
        self.od4 = QHBoxLayout()
        self.od4.addWidget(self.p4)
        self.od4.addWidget(self.yt4)
        self.od5 = QHBoxLayout()
        self.od5.addWidget(self.p5)
        self.od5.addWidget(self.yt5)
        self.od6 = QHBoxLayout()
        self.od6.addWidget(self.p6)
        self.od6.addWidget(self.yt6)

# <--------------------------------------------------------------------------->

        self.video.addWidget(self.imgL1, 0, 0)
        self.video.addLayout(self.do1, 1, 0)
        self.video.addLayout(self.od1, 2, 0)
        self.video.addWidget(self.imgL4, 3, 0)
        self.video.addLayout(self.do4, 4, 0)
        self.video.addLayout(self.od4, 5, 0)

        self.video.addWidget(self.imgL2, 0, 1)
        self.video.addLayout(self.do2, 1, 1)
        self.video.addLayout(self.od2, 2, 1)
        self.video.addWidget(self.imgL5, 3, 1)
        self.video.addLayout(self.do5, 4, 1)
        self.video.addLayout(self.od5, 5, 1)

        self.video.addWidget(self.imgL3, 0, 2)
        self.video.addLayout(self.do3, 1, 2)
        self.video.addLayout(self.od3, 2, 2)
        self.video.addWidget(self.imgL6, 3, 2)
        self.video.addLayout(self.do6, 4, 2)
        self.video.addLayout(self.od6, 5, 2)

# <--------------------------------------------------------------------------->

    def _getVideo(self):
        if self.text.text() == '':
            self._pl("dQw4w9WgXcQ", "Never Gonna Give You Up")

        self.id = []
        self.time = []
        self.title = []
        self.mylist = []
        self.channel = []
        self.results = YoutubeSearch("'" + self.text.text() + "'",
                                     max_results=60).to_dict()

        for v in self.results:
            self.id.append(v['id'])
            self.time.append(v['duration'])
            self.title.append(v['title'])
            self.mylist.append(v['thumbnails'][0])
            self.channel.append(v['channel'])

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
            self.setFixedHeight(780)
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

            self.yt1.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.id[(self.i*6)+0]))
            self.yt2.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.id[(self.i*6)+1]))
            self.yt3.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.id[(self.i*6)+2]))
            self.yt4.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.id[(self.i*6)+3]))
            self.yt5.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.id[(self.i*6)+4]))
            self.yt6.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.id[(self.i*6)+5]))

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

        self.imgL1.setToolTip("Tytuł: " + self.title[(self.i*6)+0]
                              + "\nKanał: " + self.channel[(self.i*6)+0])
        self.imgL2.setToolTip("Tytuł: " + self.title[(self.i*6)+1]
                              + "\nKanał: " + self.channel[(self.i*6)+1])
        self.imgL3.setToolTip("Tytuł: " + self.title[(self.i*6)+2]
                              + "\nKanał: " + self.channel[(self.i*6)+2])
        self.imgL4.setToolTip("Tytuł: " + self.title[(self.i*6)+3]
                              + "\nKanał: " + self.channel[(self.i*6)+3])
        self.imgL5.setToolTip("Tytuł: " + self.title[(self.i*6)+4]
                              + "\nKanał: " + self.channel[(self.i*6)+4])
        self.imgL6.setToolTip("Tytuł: " + self.title[(self.i*6)+5]
                              + "\nKanał: " + self.channel[(self.i*6)+5])

# <--------------------------------------------------------------------------->

# <===> WORK IN PROGRESS <=============================> WORK IN PROGRESS <===>

    def _do(self, id, button):
        self.worker = _DownloadMP3(id, self.downloads_path)
        self.worker.start()

# <===> WORK IN PROGRESS <=============================> WORK IN PROGRESS <===>

# <--------------------------------------------------------------------------->

# <===> WORK IN PROGRESS <=============================> WORK IN PROGRESS <===>

    def _dv(self, id):
        self.worker = _DownloadMP4(id, self.downloads_path)
        self.worker.start()

# <===> WORK IN PROGRESS <=============================> WORK IN PROGRESS <===>

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
