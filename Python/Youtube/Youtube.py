#!/usr/bin/env python
# -*- coding: utf-8 -*-
# github.com/joetats/youtube_search/blob/master/youtube_search/__init__.py
# https://stackoverflow.com/questions/18054500/how-to-use-youtube-dl-from-a-python-program

import sys
import requests
import vlc
import pafy
import platform
import time
import webbrowser
from pathlib import Path
from youtube_search import YoutubeSearch
from PyQt5 import (QtCore)
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtGui import (QFont, QImage, QPixmap, QIcon)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout, QLineEdit, QSlider,
                             QPushButton, QLabel, QWidget, QMainWindow,
                             QStatusBar, QApplication, QGridLayout, QCheckBox,
                             QStyleFactory, QComboBox, QStyle
                             )

import Download as Dv


__version__ = 'v0.2.4 - "Download Progress"'
__author__ = 'Sebastian Kolanowski'


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Youtube App")
        self.setWindowIcon(QIcon("./Icons/Youtube.png"))
        self.setFixedWidth(700)
        self.setFixedHeight(100)
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)
        # <===> PLATFORMA/SYSTEM OPERACYJNY <===>
        self.platforma = platform.system()
        self.sciezkaPob = str(Path.home() / "Downloads")
        if self.platforma == "Windows":
            self.sciezkaPob += "\\"
            self.setFont(QFont('Calibri', 12))
        else:
            self.sciezkaPob += "/"
            self.setFont(QFont('PatrickHand', 12))
        # <===> PLATFORMA/SYSTEM OPERACYJNY <===>
        self.themeChList = QStyleFactory.keys()
        self.zmienna = 0
        self.kolejkaOdt = []
        self.czyPom = 0
        self.wyswietlono = 0
        self.czasTrwania = 0
        self.timer = QTimer(self)
        self.Instance = vlc.Instance('--no-video')
        self.odtwarzacz = self.Instance.media_player_new()

        self._createMenu()
        self._createUi()
        self._createStatusBar()

    def _createUi(self):
        self.obszarGl = QVBoxLayout()

        self.themeCh = QComboBox()
        self.themeCh.addItems(self.themeChList)
        self.themeCh.currentIndexChanged.connect(self._changeTheme)
        self.poleWysz = QLineEdit()
        self.poleWysz.setPlaceholderText("Podaj tytuł filmu/utworu do wyszukania")
        self.przyciskWysz = QPushButton("Szukaj")
        self.przyciskWysz.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
        self.przyciskWysz.clicked.connect(self._getVideo)
        self.obszarWysz = QHBoxLayout()
        self.obszarWysz.addWidget(self.themeCh)
        self.obszarWysz.addWidget(self.poleWysz)
        self.obszarWysz.addWidget(self.przyciskWysz)
        self.obszarGl.addLayout(self.obszarWysz)

        self.stronaWynikow = QLabel()
        self.stronaWynikow.setText(str(self.zmienna+1))
        self.stronaWynikow.setAlignment(QtCore.Qt.AlignCenter)
        self.stronaWLewo = QPushButton()
        self.stronaWLewo.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.stronaWPrawo = QPushButton()
        self.stronaWPrawo.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        self.stronaWPrawo.clicked.connect(self._increase)
        self.stronaWLewo.clicked.connect(self._decrease)
        self.stronaWysz = QHBoxLayout()
        self.stronaWysz.addWidget(self.stronaWLewo)
        self.stronaWysz.addWidget(self.stronaWynikow)
        self.stronaWysz.addWidget(self.stronaWPrawo)

        self.progresPob = QLabel()
        self.progresPob.setText("Nic nie jest pobierane...")
        self.progresPob.setAlignment(QtCore.Qt.AlignCenter)

        self.terazOdt = QLabel()
        self.terazOdt.setText("Nic nie jest odtwarzane...")
        self.terazOdt.setAlignment(QtCore.Qt.AlignCenter)

        self.rozmiarKolejki = QLabel()
        self.rozmiarKolejki.setText("Kolejka jest pusta...")
        self.rozmiarKolejki.setAlignment(QtCore.Qt.AlignCenter)

        self.kontrolkiOdt = QLabel("Kontrolki do odtwarzacza")
        self.kontrolkiOdt.setAlignment(QtCore.Qt.AlignCenter)

        self.przyciskPauzy = QPushButton("Pauza")
        self.przyciskPauzy.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.przyciskZatrzymania = QPushButton("Zatrzymaj")
        self.przyciskZatrzymania.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.przyciskDzwieku = QPushButton("Wycisz")
        self.przyciskDzwieku.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.wartoscDzwieku = QLabel()
        self.wartoscDzwieku.setText("100")
        self.wartoscDzwieku.setFixedWidth(30)
        self.powtarzanieUtworu = QCheckBox("Powtarzaj")
        self.poziomGlosu = QSlider(Qt.Horizontal)
        self.poziomGlosu.setValue(100)
        self.poziomGlosu.setMaximum(100)
        self.poziomGlosu.setFixedWidth(150)
        self.obszarKontrolek = QHBoxLayout()
        self.obszarKontrolek.addWidget(self.przyciskPauzy)
        self.obszarKontrolek.addWidget(self.przyciskZatrzymania)
        self.obszarKontrolek.addWidget(self.powtarzanieUtworu)
        self.obszarKontrolek.addWidget(self.przyciskDzwieku)
        self.obszarKontrolek.addWidget(self.poziomGlosu)
        self.obszarKontrolek.addWidget(self.wartoscDzwieku)

        self.pasekProgresu = QSlider(Qt.Horizontal)
        self.pasekProgresu.setMaximum(1000)
        self.pasekProgresu.setValue(0)
        self.pasekProgresu.sliderMoved.connect(self._progress)
        self.wartoscProgresu = QLabel("0/0")
        self.wartoscProgresu.setFixedWidth(80)
        self.przyciskPominiecia = QPushButton("Pomiń")
        self.przyciskPominiecia.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.przyciskPominiecia.setFixedWidth(90)
        self.obszarProgresu = QHBoxLayout()
        self.obszarProgresu.addWidget(self.pasekProgresu)
        self.obszarProgresu.addWidget(self.wartoscProgresu)
        self.obszarProgresu.addWidget(self.przyciskPominiecia)

        self.generalLayout.addLayout(self.obszarGl)

# <--------------------------------------------------------------------------->

        self.obrazNr1 = QImage()
        self.obrazDNr1 = QLabel()
        self.obrazDNr1.setAlignment(QtCore.Qt.AlignCenter)
        self.pobierzMp1 = QPushButton("MP3")
        self.pobierzMp1.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.pobierzMv1 = QPushButton("MP4")
        self.pobierzMv1.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.odtworz1 = QPushButton("Odt")
        self.odtworz1.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.odtworzWeb1 = QPushButton("YT")
        self.odtworzWeb1.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.obrazNr2 = QImage()
        self.obrazDNr2 = QLabel()
        self.obrazDNr2.setAlignment(QtCore.Qt.AlignCenter)
        self.pobierzMp2 = QPushButton("MP3")
        self.pobierzMp2.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.pobierzMv2 = QPushButton("MP4")
        self.pobierzMv2.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.odtworz2 = QPushButton("Odt")
        self.odtworz2.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.odtworzWeb2 = QPushButton("YT")
        self.odtworzWeb2.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.obrazNr3 = QImage()
        self.obrazDNr3 = QLabel()
        self.obrazDNr3.setAlignment(QtCore.Qt.AlignCenter)
        self.pobierzMp3 = QPushButton("MP3")
        self.pobierzMp3.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.pobierzMv3 = QPushButton("MP4")
        self.pobierzMv3.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.odtworz3 = QPushButton("Odt")
        self.odtworz3.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.odtworzWeb3 = QPushButton("YT")
        self.odtworzWeb3.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.obrazNr4 = QImage()
        self.obrazDNr4 = QLabel()
        self.obrazDNr4.setAlignment(QtCore.Qt.AlignCenter)
        self.pobierzMp4 = QPushButton("MP3")
        self.pobierzMp4.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.pobierzMv4 = QPushButton("MP4")
        self.pobierzMv4.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.odtowrz4 = QPushButton("Odt")
        self.odtowrz4.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.odtworzWeb4 = QPushButton("YT")
        self.odtworzWeb4.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.obrazNr5 = QImage()
        self.obrazDNr5 = QLabel()
        self.obrazDNr5.setAlignment(QtCore.Qt.AlignCenter)
        self.pobierzMp5 = QPushButton("MP3")
        self.pobierzMp5.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.pobierzMv5 = QPushButton("MP4")
        self.pobierzMv5.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.odtworz5 = QPushButton("Odt")
        self.odtworz5.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.odtworzWeb5 = QPushButton("YT")
        self.odtworzWeb5.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.obrazNr6 = QImage()
        self.obrazDNr6 = QLabel()
        self.obrazDNr6.setAlignment(QtCore.Qt.AlignCenter)
        self.pobierzMp6 = QPushButton("MP3")
        self.pobierzMp6.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.pobierzMv6 = QPushButton("MP4")
        self.pobierzMv6.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.odtworz6 = QPushButton("Odt")
        self.odtworz6.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.odtworzWeb6 = QPushButton("YT")
        self.odtworzWeb6.setIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

# <--------------------------------------------------------------------------->

        self.pobierzMp1.clicked.connect(lambda: self._do(self.ident[(self.zmienna*6)+0]))
        self.pobierzMv1.clicked.connect(lambda: self._dv(self.ident[(self.zmienna*6)+0]))
        self.odtworz1.clicked.connect(
            lambda: self._pl(self.ident[(self.zmienna*6)+0], self.title[(self.zmienna*6)+0],
                             self.time[(self.zmienna*6)+0]))

        self.pobierzMp2.clicked.connect(lambda: self._do(self.ident[(self.zmienna*6)+1]))
        self.pobierzMv2.clicked.connect(lambda: self._dv(self.ident[(self.zmienna*6)+1]))
        self.odtworz2.clicked.connect(
            lambda: self._pl(self.ident[(self.zmienna*6)+1], self.title[(self.zmienna*6)+1],
                             self.time[(self.zmienna*6)+1]))

        self.pobierzMp3.clicked.connect(lambda: self._do(self.ident[(self.zmienna*6)+2]))
        self.pobierzMv3.clicked.connect(lambda: self._dv(self.ident[(self.zmienna*6)+2]))
        self.odtworz3.clicked.connect(
            lambda: self._pl(self.ident[(self.zmienna*6)+2], self.title[(self.zmienna*6)+2],
                             self.time[(self.zmienna*6)+2]))

        self.pobierzMp4.clicked.connect(lambda: self._do(self.ident[(self.zmienna*6)+3]))
        self.pobierzMv1.clicked.connect(lambda: self._dv(self.ident[(self.zmienna*6)+3]))
        self.odtowrz4.clicked.connect(
            lambda: self._pl(self.ident[(self.zmienna*6)+3], self.title[(self.zmienna*6)+3],
                             self.time[(self.zmienna*6)+3]))

        self.pobierzMp5.clicked.connect(lambda: self._do(self.ident[(self.zmienna*6)+4]))
        self.pobierzMv5.clicked.connect(lambda: self._dv(self.ident[(self.zmienna*6)+4]))
        self.odtworz5.clicked.connect(
            lambda: self._pl(self.ident[(self.zmienna*6)+4], self.title[(self.zmienna*6)+4],
                             self.time[(self.zmienna*6)+4]))

        self.pobierzMp6.clicked.connect(lambda: self._do(self.ident[(self.zmienna*6)+5]))
        self.pobierzMv6.clicked.connect(lambda: self._dv(self.ident[(self.zmienna*6)+5]))
        self.odtworz6.clicked.connect(
            lambda: self._pl(self.ident[(self.zmienna*6)+5], self.title[(self.zmienna*6)+5],
                             self.time[(self.zmienna*6)+5]))

# <--------------------------------------------------------------------------->

        self.obszarWideo = QGridLayout()

        self.obszarPob1 = QHBoxLayout()
        self.obszarPob1.addWidget(self.pobierzMp1)
        self.obszarPob1.addWidget(self.pobierzMv1)
        self.obszarPob2 = QHBoxLayout()
        self.obszarPob2.addWidget(self.pobierzMp2)
        self.obszarPob2.addWidget(self.pobierzMv2)
        self.obszarPob3 = QHBoxLayout()
        self.obszarPob3.addWidget(self.pobierzMp3)
        self.obszarPob3.addWidget(self.pobierzMv3)
        self.obszarPob4 = QHBoxLayout()
        self.obszarPob4.addWidget(self.pobierzMp4)
        self.obszarPob4.addWidget(self.pobierzMv4)
        self.obszarPob5 = QHBoxLayout()
        self.obszarPob5.addWidget(self.pobierzMp5)
        self.obszarPob5.addWidget(self.pobierzMv5)
        self.obszarPob6 = QHBoxLayout()
        self.obszarPob6.addWidget(self.pobierzMp6)
        self.obszarPob6.addWidget(self.pobierzMv6)

# <--------------------------------------------------------------------------->

        self.obszarOdt1 = QHBoxLayout()
        self.obszarOdt1.addWidget(self.odtworz1)
        self.obszarOdt1.addWidget(self.odtworzWeb1)
        self.obszarOdt2 = QHBoxLayout()
        self.obszarOdt2.addWidget(self.odtworz2)
        self.obszarOdt2.addWidget(self.odtworzWeb2)
        self.obszarOdt3 = QHBoxLayout()
        self.obszarOdt3.addWidget(self.odtworz3)
        self.obszarOdt3.addWidget(self.odtworzWeb3)
        self.obszarOdt4 = QHBoxLayout()
        self.obszarOdt4.addWidget(self.odtowrz4)
        self.obszarOdt4.addWidget(self.odtworzWeb4)
        self.obszarOdt5 = QHBoxLayout()
        self.obszarOdt5.addWidget(self.odtworz5)
        self.obszarOdt5.addWidget(self.odtworzWeb5)
        self.obszarOdt6 = QHBoxLayout()
        self.obszarOdt6.addWidget(self.odtworz6)
        self.obszarOdt6.addWidget(self.odtworzWeb6)

# <--------------------------------------------------------------------------->

        self.obszarWideo.addWidget(self.obrazDNr1, 0, 0)
        self.obszarWideo.addLayout(self.obszarPob1, 1, 0)
        self.obszarWideo.addLayout(self.obszarOdt1, 2, 0)
        self.obszarWideo.addWidget(self.obrazDNr4, 3, 0)
        self.obszarWideo.addLayout(self.obszarPob4, 4, 0)
        self.obszarWideo.addLayout(self.obszarOdt4, 5, 0)

        self.obszarWideo.addWidget(self.obrazDNr2, 0, 1)
        self.obszarWideo.addLayout(self.obszarPob2, 1, 1)
        self.obszarWideo.addLayout(self.obszarOdt2, 2, 1)
        self.obszarWideo.addWidget(self.obrazDNr5, 3, 1)
        self.obszarWideo.addLayout(self.obszarPob5, 4, 1)
        self.obszarWideo.addLayout(self.obszarOdt5, 5, 1)

        self.obszarWideo.addWidget(self.obrazDNr3, 0, 2)
        self.obszarWideo.addLayout(self.obszarPob3, 1, 2)
        self.obszarWideo.addLayout(self.obszarOdt3, 2, 2)
        self.obszarWideo.addWidget(self.obrazDNr6, 3, 2)
        self.obszarWideo.addLayout(self.obszarPob6, 4, 2)
        self.obszarWideo.addLayout(self.obszarOdt6, 5, 2)

# <--------------------------------------------------------------------------->

    def _getVideo(self):
        if self.poleWysz.text() == '':
            self._pl("dQw4w9WgXcQ", "Never Gonna Give You Up", "3:33")

        self.ident = []
        self.time = []
        self.title = []
        self.mylist = []
        self.channel = []
        self.wynikiWysz = YoutubeSearch("'" + self.poleWysz.text() + "'",
                                     max_results=60).to_dict()

        for v in self.wynikiWysz:
            self.ident.append(v['id'])
            self.time.append(v['duration'])
            self.title.append(v['title'])
            self.mylist.append(v['thumbnails'][0])
            self.channel.append(v['channel'])

        self.zmienna = 0
        self.stronaWynikow.setText(str(self.zmienna+1))
        if len(self.wynikiWysz) >= 6:
            self._updateUi()

# <--------------------------------------------------------------------------->

    def _updateUi(self):
        if self.wyswietlono == 0:
            self.setFixedHeight(800)
            self.obszarGl.addLayout(self.obszarWideo)
            self.obszarGl.addLayout(self.stronaWysz)
            self.obszarGl.addWidget(self.progresPob)
            self.obszarGl.addWidget(self.terazOdt)
            self.obszarGl.addWidget(self.rozmiarKolejki)
            self.obszarGl.addWidget(self.kontrolkiOdt)
            self.obszarGl.addLayout(self.obszarProgresu)
            self.obszarGl.addLayout(self.obszarKontrolek)

            self.przyciskPauzy.clicked.connect(lambda: self._pause())
            self.przyciskZatrzymania.clicked.connect(lambda: self._stop())
            self.przyciskDzwieku.clicked.connect(lambda: self._mute())
            self.poziomGlosu.valueChanged.connect(self._volume)
            self.przyciskPominiecia.clicked.connect(lambda: self._skip())

            self.timer.timeout.connect(self._music)
            self.timer.start(100)

            self.odtworzWeb1.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.ident[(self.zmienna*6)+0]))
            self.odtworzWeb2.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.ident[(self.zmienna*6)+1]))
            self.odtworzWeb3.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.ident[(self.zmienna*6)+2]))
            self.odtworzWeb4.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.ident[(self.zmienna*6)+3]))
            self.odtworzWeb5.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.ident[(self.zmienna*6)+4]))
            self.odtworzWeb6.clicked.connect(lambda: webbrowser.open(
                "https://www.youtube.com/watch?v=" + self.ident[(self.zmienna*6)+5]))

        self.wyswietlono = 1

# <--------------------------------------------------------------------------->

        self.obrazNr1.loadFromData(requests.get(
            self.mylist[(self.zmienna*6)+0]).content)
        zdj1 = QPixmap(self.obrazNr1)
        self.obrazDNr1.setPixmap(zdj1.scaled(200, 100))

        self.obrazNr2.loadFromData(requests.get(
            self.mylist[(self.zmienna*6)+1]).content)
        zdj2 = QPixmap(self.obrazNr2)
        self.obrazDNr2.setPixmap(zdj2.scaled(200, 100))

        self.obrazNr3.loadFromData(requests.get(
            self.mylist[(self.zmienna*6)+2]).content)
        zdj3 = QPixmap(self.obrazNr3)
        self.obrazDNr3.setPixmap(zdj3.scaled(200, 100))

        self.obrazNr4.loadFromData(requests.get(
            self.mylist[(self.zmienna*6)+3]).content)
        zdj4 = QPixmap(self.obrazNr4)
        self.obrazDNr4.setPixmap(zdj4.scaled(200, 100))

        self.obrazNr5.loadFromData(requests.get(
            self.mylist[(self.zmienna*6)+4]).content)
        zdj5 = QPixmap(self.obrazNr5)
        self.obrazDNr5.setPixmap(zdj5.scaled(200, 100))

        self.obrazNr6.loadFromData(requests.get(
            self.mylist[(self.zmienna*6)+5]).content)
        zdj6 = QPixmap(self.obrazNr6)
        self.obrazDNr6.setPixmap(zdj6.scaled(200, 100))

# <--------------------------------------------------------------------------->

        self.obrazDNr1.setToolTip("Tytuł: " + self.title[(self.zmienna*6)+0]
                              + "\nKanał: " + self.channel[(self.zmienna*6)+0])
        self.obrazDNr2.setToolTip("Tytuł: " + self.title[(self.zmienna*6)+1]
                              + "\nKanał: " + self.channel[(self.zmienna*6)+1])
        self.obrazDNr3.setToolTip("Tytuł: " + self.title[(self.zmienna*6)+2]
                              + "\nKanał: " + self.channel[(self.zmienna*6)+2])
        self.obrazDNr4.setToolTip("Tytuł: " + self.title[(self.zmienna*6)+3]
                              + "\nKanał: " + self.channel[(self.zmienna*6)+3])
        self.obrazDNr5.setToolTip("Tytuł: " + self.title[(self.zmienna*6)+4]
                              + "\nKanał: " + self.channel[(self.zmienna*6)+4])
        self.obrazDNr6.setToolTip("Tytuł: " + self.title[(self.zmienna*6)+5]
                              + "\nKanał: " + self.channel[(self.zmienna*6)+5])

# <--------------------------------------------------------------------------->

    def _do(self, id):
        self.worker = Dv._DownloadMP3(id, self.sciezkaPob, self.progresPob)
        self.worker.start()
        self.worker.quit()

    def _dv(self, id):
        self.worker = Dv._DownloadMP4(id, self.sciezkaPob, self.progresPob)
        self.worker.start()
        self.worker.quit()

# <--------------------------------------------------------------------------->

    def _increase(self):
        if self.zmienna < int(len(self.wynikiWysz)/6)-1:
            self.zmienna += 1
            self.stronaWynikow.setText(str(self.zmienna+1))
            self._updateUi()

    def _decrease(self):
        if self.zmienna > 0:
            self.zmienna -= 1
            self.stronaWynikow.setText(str(self.zmienna+1))
            self._updateUi()

# <--------------------------------------------------------------------------->

    def _pl(self, id, title, time):
        if self.odtwarzacz.is_playing() and self.czyPom == 0:
            self.kolejkaOdt.append(id)
            self.kolejkaOdt.append(title)
            self.kolejkaOdt.append(time)
            self.rozmiarKolejki.setText("W kolejce: " + str(int(len(self.kolejkaOdt)/3)))
        else:
            self.czasTrwania = time
            self.terazOdt.setText("Teraz odtwarzane: " + title)
            video = pafy.new(id)
            best = video.getbest()
            playurl = best.url
            Media = self.Instance.media_new(playurl)
            Media.get_mrl()
            self.odtwarzacz.set_media(Media)
            self.odtwarzacz.play()
            self.pasekProgresu.setValue(0)

# <--------------------------------------------------------------------------->

    def _pause(self):
        self.odtwarzacz.pause()
        """if self.odtwarzacz.get_pause() == 1:
            self.odtwarzacz.set_pause(0)
            self.przyciskPauzy.setText("Pause")
            self.przyciskPauzy.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.odtwarzacz.set_pause(1)
            self.przyciskPauzy.setText("Unpause")
            self.przyciskPauzy.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))"""

    def _mute(self):
        if self.odtwarzacz.audio_get_mute():
            self.odtwarzacz.audio_set_mute(False)
            self.przyciskDzwieku.setText("Wycisz")
            self.przyciskDzwieku.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        else:
            self.odtwarzacz.audio_set_mute(True)
            self.przyciskDzwieku.setText("Odcisz")
            self.przyciskDzwieku.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))


    def _stop(self):
        self.odtwarzacz.stop()
        self.terazOdt.setText("Nic nie jest odtwarzane...")
        self.pasekProgresu.setValue(0)

    def _skip(self):
        if len(self.kolejkaOdt) > 0:
            self.czyPom = 1
            self._pl(self.kolejkaOdt.pop(0), self.kolejkaOdt.pop(0), self.kolejkaOdt.pop(0))
            self.czyPom = 0
            if len(self.kolejkaOdt) <= 0:
                self.rozmiarKolejki.setText("Kolejka jest pusta...")
            else:
                self.rozmiarKolejki.setText("W kolejce: "
                                      + str(int(len(self.kolejkaOdt)/3)))

    def _volume(self):
        self.odtwarzacz.audio_set_volume(self.poziomGlosu.value())
        self.wartoscDzwieku.setText(str(self.poziomGlosu.value()))

    def _progress(self):
        self.odtwarzacz.set_position(self.pasekProgresu.value()/1000)

    def _music(self):
        self.pasekProgresu.setValue(int(self.odtwarzacz.get_position()*1000))
        self.wartoscProgresu.setText(
            time.strftime('%M:%S', time.gmtime(self.odtwarzacz.get_time()/1000))
            + "/" + str(self.czasTrwania))
        if self.powtarzanieUtworu.checkState() != 0:
            if self.odtwarzacz.get_position()*100 >= 99:
                self.odtwarzacz.set_position(0)
        else:
            if self.odtwarzacz.is_playing() == 0:
                if len(self.kolejkaOdt) > 0 and self.odtwarzacz.get_position()*100 > 90:
                    self._pl(self.kolejkaOdt.pop(0), self.kolejkaOdt.pop(
                        0), self.kolejkaOdt.pop(0))
                    if len(self.kolejkaOdt) <= 0:
                        self.rozmiarKolejki.setText("Kolejka jest pusta...")

# <--------------------------------------------------------------------------->

    def _changeTheme(self):
        app.setStyle(self.themeCh.currentText())

    def _createMenu(self):
        menu = self.menuBar().addMenu('Menu')
        menu.addAction('Wyłącz', self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage('Wersja: ' + __version__
                           + ', Autor: ' + __author__)
        self.setStatusBar(status)

# <--------------------------------------------------------------------------->


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
