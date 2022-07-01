#!/usr/bin/env python
# -*- coding: utf-8 -*-
# github.com/joetats/youtube_search/blob/master/youtube_search/__init__.py
# https://stackoverflow.com/questions/18054500/how-to-use-youtube-dl-from-a-python-program

import locale
import mpv
import sys
import os
import requests
import vlc
import pafy
import platform
import time
import webbrowser
import tempfile
from pathlib import Path
from youtube_search import YoutubeSearch
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt, QTimer, QThread)
from PyQt5.QtGui import (QFont, QImage, QPixmap, QIcon)
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QCheckBox,
    QComboBox,
    QWidget,
    QLabel,
    QSlider,
    QStatusBar,
    QStyle,
    QMessageBox,
    QStyleFactory,
    QFontDialog
    )

import Download as Dv
import HistoryS


__version__ = 'v0.0.1'
__author__ = "Sebastian Kolanowski"


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Odtwarzacz Youtube")
        self.resize(700, 800)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)

        self.wyswietlono = False
        self.zmienna = 0
        self.timer = QTimer(self)
        self.worker = QThread()

        # <===> PLATFORMA/SYSTEM OPERACYJNY <===>

        self.tempWysz = tempfile.gettempdir()

        self.platforma = platform.system()
        self.sciezkaPob = str(Path.home() / "Downloads")
        if self.platforma == "Windows":
            self.setWindowIcon(QIcon(".\\Icons\\Youtube.png"))
            self.sciezkaPob += "\\"
            self.tempWysz += "\\YTHistory.txt"
            self.setFont(QFont("Calibri", 12))
        else:
            self.setWindowIcon(QIcon("./Icons/Youtube.png"))
            self.sciezkaPob += "/"
            self.tempWysz += "/YTHistory.txt"
            self.setFont(QFont("PatrickHand", 12))

        # <===> PLATFORMA/SYSTEM OPERACYJNY <===>

        self.themeChList = QStyleFactory.keys()
        self.setWindowIcon(QIcon("./Icons/Youtube.png"))
        self.setFont(QFont("PatrickHand", 12))

        self.player = mpv.MPV(
            ytdl=True,
            vo='null',
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True
            )

        self._createMenu()
        self._createUi()
        self._createStatusBar()

    def _createUi(self):

        self.obszarWysz = QHBoxLayout()

        self.poleWysz = QComboBox()
        self.poleWysz.setEditable(True)
        self.poleWysz.setPlaceholderText(
            "Podaj tytuł filmu/utworu do wyszukania"
        )
        if os.path.isfile(self.tempWysz):
            historia = []
            with open(self.tempWysz, "r") as f:
                historia = f.read().splitlines()
            f.close()
            for f in historia:
                if not f == "":
                    self.poleWysz.addItem(f)

        self.przyciskWysz = QPushButton("Szukaj")
        self.przyciskWysz.setIcon(self.style().standardIcon(
            QStyle.SP_FileDialogContentsView)
        )
        self.przyciskWysz.clicked.connect(self._getVideo)

        self.obszarWysz.addWidget(self.poleWysz)
        self.obszarWysz.addWidget(self.przyciskWysz)

        self.generalLayout.addLayout(self.obszarWysz)
        self.generalLayout.setAlignment(self.obszarWysz, Qt.AlignTop)

        self.obszarInfo = QVBoxLayout()

        self.stronaWynikow = QLabel()
        self.stronaWynikow.setText(str(self.zmienna + 1))
        self.stronaWynikow.setAlignment(QtCore.Qt.AlignCenter)

        self.stronaWLewo = QPushButton()
        self.stronaWLewo.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowLeft)
        )
        self.stronaWLewo.clicked.connect(self._decrease)

        self.stronaWPrawo = QPushButton()
        self.stronaWPrawo.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowRight)
        )
        self.stronaWPrawo.clicked.connect(self._increase)

        self.stronaWysz = QHBoxLayout()
        self.stronaWysz.addWidget(self.stronaWLewo)
        self.stronaWysz.addWidget(self.stronaWynikow)
        self.stronaWysz.addWidget(self.stronaWPrawo)

        self.obszarInfo.addLayout(self.stronaWysz)

        self.utworInfo = QVBoxLayout()

        self.utworPob = QLabel()
        self.utworPob.setText("Nic nie jest pobierane.")
        self.utworPob.setAlignment(QtCore.Qt.AlignCenter)

        self.utworOdt = QLabel()
        self.utworOdt.setText("Nic nie jest odtwarzane.")
        self.utworOdt.setAlignment(QtCore.Qt.AlignCenter)

        self.utworKol = QLabel()
        self.utworKol.setText("Kolejka jest pusta.")
        self.utworKol.setAlignment(QtCore.Qt.AlignCenter)

        self.utworReset = QPushButton()
        self.utworReset.setIcon(
            self.style().standardIcon(QStyle.SP_BrowserReload)
        )

        self.utworPozycja = QSlider(Qt.Horizontal)
        self.utworPozycja.setMaximum(100)
        self.utworPozycja.setMinimum(0)
        self.utworPozycja.sliderMoved.connect(lambda: self._position())

        self.utworCzas = QLabel()
        self.utworCzas.setText("0/0")
        self.utworCzas.setAlignment(QtCore.Qt.AlignCenter)

        self.utworPop = QPushButton()
        self.utworPop.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipBackward)
        )
        self.utworNas = QPushButton()
        self.utworNas.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipForward)
        )

        self.infoCzas = QHBoxLayout()

        self.infoCzas.addWidget(self.utworReset)
        self.infoCzas.addWidget(self.utworPozycja)
        self.infoCzas.addWidget(self.utworCzas)
        self.infoCzas.addWidget(self.utworPop)
        self.infoCzas.addWidget(self.utworNas)

        self.utworInfo.addWidget(self.utworPob)
        self.utworInfo.addWidget(self.utworOdt)
        self.utworInfo.addWidget(self.utworKol)
        self.utworInfo.addLayout(self.infoCzas)

        self.obszarInfo.addLayout(self.utworInfo)

        self.kontrolki = QHBoxLayout()

        self.stop = QPushButton("Zatrzymaj")
        self.stop.setIcon(self.style().standardIcon(
            QStyle.SP_MediaStop)
        )
        self.wstrzymaj = QPushButton("Wstrzymaj")
        self.wstrzymaj.setIcon(self.style().standardIcon(
            QStyle.SP_MediaPause)
        )

        self.wycisz = QPushButton("Wycisz")
        self.wycisz.setIcon(
            self.style().standardIcon(QStyle.SP_MediaVolume)
        )

        self.powtarzanie = QCheckBox("Powtarzaj")

        self.suwakGlos = QSlider(Qt.Horizontal)
        self.suwakGlos.setValue(100)
        self.suwakGlos.setMaximum(100)

        self.poziomGlosu = QLabel()
        self.poziomGlosu.setText("100")

        self.kontrolki.addWidget(self.wstrzymaj)
        self.kontrolki.addWidget(self.stop)
        self.kontrolki.addWidget(self.wycisz)
        self.kontrolki.addWidget(self.powtarzanie)
        self.kontrolki.addWidget(self.suwakGlos)
        self.kontrolki.addWidget(self.poziomGlosu)

        self.obszar = QGridLayout()

        for i in range(0, 6):
            przyciski = QGridLayout()

            odtworz = QPushButton("Odt")
            odtworz.setIcon(self.style().standardIcon(
                QStyle.SP_MediaPlay)
            )
            odtworz.clicked.connect(
                lambda checked, arg=i: self._play(self.ident[arg]))
            dodaj = QPushButton("Lst")
            dodaj.setIcon(self.style().standardIcon(
                QStyle.SP_DialogApplyButton)
            )
            dodaj.clicked.connect(
                lambda checked, arg=i: self._add(self.ident[arg]))
            pobMp3 = QPushButton("MP3")
            pobMp3.setIcon(self.style().standardIcon(
                QStyle.SP_DialogSaveButton)
            )
            pobMp3.clicked.connect(
                lambda checked, arg=i: self._downloadAudio(
                    self.ident[arg],
                    self.title[arg]
                )
            )
            pobMp4 = QPushButton("MP4")
            pobMp4.setIcon(self.style().standardIcon(
                QStyle.SP_DialogSaveButton)
            )
            pobMp4.clicked.connect(
                lambda checked, arg=i: self._downloadVideo(
                    self.ident[arg],
                    self.title[arg]
                )
            )
            if i < 3:
                odtworz.setObjectName("odtworz" + str(i))
                dodaj.setObjectName("dodaj" + str(i))
                pobMp3.setObjectName("pobierzMp3" + str(i))
                pobMp4.setObjectName("pobierzMp4" + str(i))
                przyciski.setObjectName("przyciski" + str(i))
                przyciski.addWidget(odtworz, 0, 0)
                przyciski.addWidget(dodaj, 0, 1)
                przyciski.addWidget(pobMp3, 1, 0)
                przyciski.addWidget(pobMp4, 1, 1)
                self.obszar.addLayout(przyciski, 1, i)
            else:
                odtworz.setObjectName("odtworz" + str(i))
                dodaj.setObjectName("dodaj" + str(i))
                pobMp3.setObjectName("pobierzMp3" + str(i))
                pobMp4.setObjectName("pobierzMp4" + str(i))
                przyciski.setObjectName("przyciski" + str(i))
                przyciski.addWidget(odtworz, 0, 0)
                przyciski.addWidget(dodaj, 0, 1)
                przyciski.addWidget(pobMp3, 1, 0)
                przyciski.addWidget(pobMp4, 1, 1)
                self.obszar.addLayout(przyciski, 3, i-3)

        self.obrazNr1 = QImage()
        self.obrazDNr1 = QLabel()
        self.obrazDNr1.setAlignment(QtCore.Qt.AlignCenter)

        self.obrazNr2 = QImage()
        self.obrazDNr2 = QLabel()
        self.obrazDNr2.setAlignment(QtCore.Qt.AlignCenter)

        self.obrazNr3 = QImage()
        self.obrazDNr3 = QLabel()
        self.obrazDNr3.setAlignment(QtCore.Qt.AlignCenter)

        self.obrazNr4 = QImage()
        self.obrazDNr4 = QLabel()
        self.obrazDNr4.setAlignment(QtCore.Qt.AlignCenter)

        self.obrazNr5 = QImage()
        self.obrazDNr5 = QLabel()
        self.obrazDNr5.setAlignment(QtCore.Qt.AlignCenter)

        self.obrazNr6 = QImage()
        self.obrazDNr6 = QLabel()
        self.obrazDNr6.setAlignment(QtCore.Qt.AlignCenter)

        self.obszar.addWidget(self.obrazDNr1, 0, 0)
        self.obszar.addWidget(self.obrazDNr2, 0, 1)
        self.obszar.addWidget(self.obrazDNr3, 0, 2)
        self.obszar.addWidget(self.obrazDNr4, 2, 0)
        self.obszar.addWidget(self.obrazDNr5, 2, 1)
        self.obszar.addWidget(self.obrazDNr6, 2, 2)

    def _getVideo(self):
        if self.poleWysz.currentText() == "":
            self._play("dQw4w9WgXcQ")
        else:
            if self.poleWysz.findText(self.poleWysz.currentText()) == -1:
                self.poleWysz.addItem(self.poleWysz.currentText())
                with open(self.tempWysz, "w") as f:
                    for i in range(0, self.poleWysz.count() + 1):
                        f.write("%s\n" % self.poleWysz.itemText(i))
                f.close()

        self.ident = []
        self.time = []
        self.title = []
        self.mylist = []
        self.channel = []
        self.wynikiWysz = YoutubeSearch(
            "'" + self.poleWysz.currentText() + "'", max_results=60
        ).to_dict()

        for v in self.wynikiWysz:
            self.ident.append(v["id"])
            self.time.append(v["duration"])
            self.title.append(v["title"])
            self.mylist.append(v["thumbnails"][0])
            self.channel.append(v["channel"])

        if len(self.wynikiWysz) >= 6:
            self._updateUi()

    def _updateUi(self):
        if not self.wyswietlono:
            self.generalLayout.addLayout(self.obszar)
            self.generalLayout.addLayout(self.obszarInfo)
            self.generalLayout.addLayout(self.kontrolki)

            self.stop.clicked.connect(lambda: self.player.stop())
            self.wstrzymaj.clicked.connect(lambda: self._pauza())
            self.wycisz.clicked.connect(lambda: self._mute())
            self.powtarzanie.stateChanged.connect(lambda: self._loop())
            self.suwakGlos.valueChanged.connect(self._volume)

            self.utworReset.clicked.connect(lambda: self._reset())
            self.utworPop.clicked.connect(
                lambda: self.player.playlist_prev("force")
            )
            self.utworNas.clicked.connect(
                lambda: self.player.playlist_next("force")
            )

            self.timer.timeout.connect(self._music)
            self.timer.start(100)

        self.wyswietlono = True

        self.obrazNr1.loadFromData(
            requests.get(self.mylist[(self.zmienna * 6) + 0]).content
        )

        zdj1 = QPixmap(self.obrazNr1)
        self.obrazDNr1.setPixmap(zdj1.scaled(200, 100))

        self.obrazNr2.loadFromData(
            requests.get(self.mylist[(self.zmienna * 6) + 1]).content
        )

        zdj2 = QPixmap(self.obrazNr2)
        self.obrazDNr2.setPixmap(zdj2.scaled(200, 100))

        self.obrazNr3.loadFromData(
            requests.get(self.mylist[(self.zmienna * 6) + 2]).content
        )

        zdj3 = QPixmap(self.obrazNr3)
        self.obrazDNr3.setPixmap(zdj3.scaled(200, 100))

        self.obrazNr4.loadFromData(
            requests.get(self.mylist[(self.zmienna * 6) + 3]).content
        )

        zdj4 = QPixmap(self.obrazNr4)
        self.obrazDNr4.setPixmap(zdj4.scaled(200, 100))

        self.obrazNr5.loadFromData(
            requests.get(self.mylist[(self.zmienna * 6) + 4]).content
        )

        zdj5 = QPixmap(self.obrazNr5)
        self.obrazDNr5.setPixmap(zdj5.scaled(200, 100))

        self.obrazNr6.loadFromData(
            requests.get(self.mylist[(self.zmienna * 6) + 5]).content
        )

        zdj6 = QPixmap(self.obrazNr6)
        self.obrazDNr6.setPixmap(zdj6.scaled(200, 100))

        self.obrazDNr1.setToolTip(
            "Tytuł: "
            + self.title[(self.zmienna * 6) + 0]
            + "\nKanał: "
            + self.channel[(self.zmienna * 6) + 0]
            + "\nCzas Trwania: "
            + self.time[(self.zmienna * 6) + 0]
        )

        self.obrazDNr2.setToolTip(
            "Tytuł: "
            + self.title[(self.zmienna * 6) + 1]
            + "\nKanał: "
            + self.channel[(self.zmienna * 6) + 1]
            + "\nCzas Trwania: "
            + self.time[(self.zmienna * 6) + 1]
        )

        self.obrazDNr3.setToolTip(
            "Tytuł: "
            + self.title[(self.zmienna * 6) + 2]
            + "\nKanał: "
            + self.channel[(self.zmienna * 6) + 2]
            + "\nCzas Trwania: "
            + self.time[(self.zmienna * 6) + 2]
        )

        self.obrazDNr4.setToolTip(
            "Tytuł: "
            + self.title[(self.zmienna * 6) + 3]
            + "\nKanał: "
            + self.channel[(self.zmienna * 6) + 3]
            + "\nCzas Trwania: "
            + self.time[(self.zmienna * 6) + 3]
        )

        self.obrazDNr5.setToolTip(
            "Tytuł: "
            + self.title[(self.zmienna * 6) + 4]
            + "\nKanał: "
            + self.channel[(self.zmienna * 6) + 4]
            + "\nCzas Trwania: "
            + self.time[(self.zmienna * 6) + 4]
        )

        self.obrazDNr6.setToolTip(
            "Tytuł: "
            + self.title[(self.zmienna * 6) + 5]
            + "\nKanał: "
            + self.channel[(self.zmienna * 6) + 5]
            + "\nCzas Trwania: "
            + self.time[(self.zmienna * 6) + 5]
        )

    def _downloadAudio(self, id, title):
        if not self.worker.isRunning():
            self.worker = Dv._DownloadMP3(id, self.sciezkaPob, self.utworPob)
            self.worker.start()
            self.worker.quit()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("W tym momencie pobierany jest inny plik.")
            msg.setInformativeText(
                "W tym momencie jest uruchomione pobieranie"
                + " innego pliku w tle. Proszę poczekać, aż plik zostanie"
                + " pobrany albo zatrzymać pobieranie i spróbować ponownie."
            )
            msg.setWindowTitle("Błąd w pobieraniu")
            msg.setDetailedText(title)
            msg.addButton(QMessageBox.Ok)
            zatrzymaj = msg.addButton("Zatrzymaj", QMessageBox.YesRole)
            zatrzymaj.clicked.connect(self._stopWorker)
            msg.exec()

    def _downloadVideo(self, id, title):
        if not self.worker.isRunning():
            self.worker = Dv._DownloadMP4(id, self.sciezkaPob, self.utworPob)
            self.worker.start()
            self.worker.quit()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("W tym momencie pobierany jest inny plik.")
            msg.setInformativeText(
                "W tym momencie jest uruchomione pobieranie"
                + " innego pliku w tle. Proszę poczekać, aż plik zostanie"
                + " pobrany albo zatrzymać pobieranie i spróbować ponownie."
            )
            msg.setWindowTitle("Błąd w pobieraniu")
            msg.setDetailedText(title)
            msg.addButton(QMessageBox.Ok)
            zatrzymaj = msg.addButton("Zatrzymaj", QMessageBox.YesRole)
            zatrzymaj.clicked.connect(self._stopWorker)
            msg.exec()

    def _stopWorker(self):
        self.worker.terminate()
        self.utworPob.setText("Pobieranie zatrzymane.")

    def _play(self, identyfikator):
        self.player.play(
            "https://www.youtube.com/watch?v=" + identyfikator
        )

    def _add(self, identyfikator):
        self.player.playlist_append(
            "https://www.youtube.com/watch?v=" + identyfikator
        )

    def _reset(self):
        self.player.time_pos = 0

    def _pauza(self):
        if self.player.pause:
            self.wstrzymaj.setText("Wstrzymaj")
            self.wstrzymaj.setIcon(self.style().standardIcon(
                QStyle.SP_MediaPause)
            )
        else:
            self.wstrzymaj.setText("Wznów")
            self.wstrzymaj.setIcon(self.style().standardIcon(
                QStyle.SP_MediaPlay)
            )
        self.player.command("cycle", "pause")

    def _mute(self):
        if self.player.mute:
            self.player.command("cycle", "mute")
            self.wycisz.setText("Wycisz")
            self.wycisz.setIcon(
                self.style().standardIcon(QStyle.SP_MediaVolume)
            )
        else:
            self.player.command("cycle", "mute")
            self.wycisz.setText("Odcisz")
            self.wycisz.setIcon(
                self.style().standardIcon(QStyle.SP_MediaVolumeMuted)
            )

    def _volume(self):
        self.player.volume = self.suwakGlos.value()
        self.poziomGlosu.setText(str(self.suwakGlos.value()))

    def _loop(self):
        if self.powtarzanie.checkState() != 0:
            self.player.loop = True
        else:
            self.player.loop = False

    def _music(self):
        if len(self.player.playlist) != 0:
            if len(self.player.playlist) == 1:
                self.utworKol.setText("W kolejce teraz odtwarzany.")
            elif len(self.player.playlist) > 1:
                self.utworKol.setText(
                    "W kolejce: " + str(len(self.player.playlist))
                )
            if type(self.player._get_property("duration")) is float:
                self.utworPozycja.setMaximum(
                    int(self.player._get_property("duration"))
                )
                self.utworCzas.setText(time.strftime("%H:%M:%S", time.gmtime(
                    self.player.time_pos))
                    + "/"
                    + time.strftime("%H:%M:%S", time.gmtime(
                        self.player._get_property("duration")))
                    )
            else:
                self.utworCzas.setText("0/0")
            if type(self.player.time_pos) is float:
                self.utworPozycja.setValue(int(self.player.time_pos))
                self.utworOdt.setText(self.player._get_property("media-title"))
            else:
                self.utworPozycja.setMaximum(100)
                self.utworKol.setText("Kolejka jest pusta.")
                self.utworCzas.setText("0/0")
                self.utworOdt.setText("Nic nie jest odtwarzane.")

    def _position(self):
        self.player.time_pos = int(self.utworPozycja.value())

    def _increase(self):
        if self.zmienna < int(len(self.wynikiWysz) / 6) - 1:
            self.zmienna += 1
            self.stronaWynikow.setText(str(self.zmienna + 1))
            self._updateUi()

    def _decrease(self):
        if self.zmienna > 0:
            self.zmienna -= 1
            self.stronaWynikow.setText(str(self.zmienna + 1))
            self._updateUi()

    def _showSHistory(self):
        self.w = HistoryS.oknoHistorii(self.poleWysz, self.tempWysz)
        self.w.show()

    def _showOHistory(self):
        self.w.show()

    def _selectFont(self):
        font, ok = QFontDialog.getFont(self.font(), self)
        if ok:
            self.setFont(font)

    def _createMenu(self):
        menu = self.menuBar().addMenu("Menu")
        menu.addAction("Czcionka", self._selectFont)
        theme = menu.addMenu("Motywy")
        for i in self.themeChList:
            theme.addAction(i, lambda arg=i: app.setStyle(arg))
        menu.addAction("Wyłącz", self.close)
        historia = self.menuBar().addMenu("Historia")
        historia.addAction("Wyszukiwania", self._showSHistory)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Wersja: " + __version__ + ", Autor: " + __author__)
        self.setStatusBar(status)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    locale.setlocale(locale.LC_NUMERIC, 'C')
    window = Window()
    window.show()
    app.exec()
