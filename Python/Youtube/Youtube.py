#!/usr/bin/env python
# -*- coding: utf-8 -*-
# github.com/joetats/youtube_search/blob/master/youtube_search/__init__.py
# https://stackoverflow.com/questions/18054500/how-to-use-youtube-dl-from-a-python-program

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
# import Play
import HistoryS
import HistoryO


__version__ = 'v0.3.4 - "Hotfix"'
__author__ = "Sebastian Kolanowski"


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Odtwarzacz Youtube")
        self.resize(700, 800)
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)

        self.themeChList = QStyleFactory.keys()
        self.zmienna = 0
        self.kolejkaOdt = []
        self.czyPom = False
        self.czyPauza = False
        self.wyswietlono = False
        self.czasTrwania = 0
        self.timer = QTimer(self)
        self.worker = QThread()
        self.Instance = vlc.Instance("--no-video")
        self.odtwarzacz = self.Instance.media_player_new()

        # <===> PLATFORMA/SYSTEM OPERACYJNY <===>

        self.tempWysz = tempfile.gettempdir()
        self.tempOdt = tempfile.gettempdir()

        self.platforma = platform.system()
        self.sciezkaPob = str(Path.home() / "Downloads")
        if self.platforma == "Windows":
            self.setWindowIcon(QIcon(".\\Icons\\Youtube.png"))
            self.sciezkaPob += "\\"
            self.tempWysz += "\\YTHistory.txt"
            self.tempOdt += "\\YTVideo.txt"
            self.setFont(QFont("Calibri", 12))
        else:
            self.setWindowIcon(QIcon("./Icons/Youtube.png"))
            self.sciezkaPob += "/"
            self.tempWysz += "/YTHistory.txt"
            self.tempOdt += "/YTVideo.txt"
            self.setFont(QFont("PatrickHand", 12))

        # <===> PLATFORMA/SYSTEM OPERACYJNY <===>

        self._createMenu()
        self._createUi()
        self._createStatusBar()

    def _createUi(self):
        self.obszarGl = QVBoxLayout()

        self.poleWysz = QComboBox()
        self.poleWysz.setEditable(True)
        self.poleWysz.setPlaceholderText(
            "Podaj tytuł filmu/utworu do wyszukania")
        if os.path.isfile(self.tempWysz):
            historia = []
            with open(self.tempWysz, "r") as f:
                historia = f.read().splitlines()
            f.close()
            for f in historia:
                if not f == "":
                    self.poleWysz.addItem(f)

        self.przyciskWysz = QPushButton("Szukaj")
        self.przyciskWysz.setIcon(
            self.style().standardIcon(QStyle.SP_FileDialogContentsView)
        )
        self.przyciskWysz.clicked.connect(self._getVideo)

        self.obszarWysz = QHBoxLayout()
        self.obszarWysz.addWidget(self.poleWysz)
        self.obszarWysz.addWidget(self.przyciskWysz)

        self.obszarGl.addLayout(self.obszarWysz)
        self.obszarGl.setAlignment(self.obszarWysz, Qt.AlignTop)

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

        self.progresPob = QLabel()
        self.progresPob.setText("Nic nie jest pobierane.")
        self.progresPob.setAlignment(QtCore.Qt.AlignCenter)

        self.terazOdt = QLabel()
        self.terazOdt.setText("Nic nie jest odtwarzane.")
        self.terazOdt.setAlignment(QtCore.Qt.AlignCenter)

        self.rozmiarKolejki = QLabel()
        self.rozmiarKolejki.setText("Kolejka jest pusta.")
        self.rozmiarKolejki.setAlignment(QtCore.Qt.AlignCenter)

        self.przyciskPauzy = QPushButton("Pauza")
        self.przyciskPauzy.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPause)
        )

        self.przyciskZatrzymania = QPushButton("Zatrzymaj")
        self.przyciskZatrzymania.setIcon(
            self.style().standardIcon(QStyle.SP_MediaStop)
        )

        self.przyciskDzwieku = QPushButton("Wycisz")
        self.przyciskDzwieku.setIcon(
            self.style().standardIcon(QStyle.SP_MediaVolume)
        )

        self.wartoscDzwieku = QLabel()
        self.wartoscDzwieku.setText("100")

        self.powtarzanieUtworu = QCheckBox("Powtarzaj")

        self.poziomGlosu = QSlider(Qt.Horizontal)
        self.poziomGlosu.setValue(100)
        self.poziomGlosu.setMaximum(100)

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
        self.pasekProgresu.sliderMoved.connect(
            lambda: self.odtwarzacz.set_position(
                self.pasekProgresu.value() / 1000
            )
        )

        self.wartoscProgresu = QLabel("0/0")

        self.przyciskPominiecia = QPushButton("Następny")
        self.przyciskPominiecia.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipForward)
        )

        self.obszarProgresu = QHBoxLayout()
        self.obszarProgresu.addWidget(self.pasekProgresu)
        self.obszarProgresu.addWidget(self.wartoscProgresu)
        self.obszarProgresu.addWidget(self.przyciskPominiecia)

        self.generalLayout.addLayout(self.obszarGl)

        self.obszarWideo = QGridLayout()

        for i in range(0, 6):
            """obrazNr = QImage()
            obrazNr.setObjectName("obrazNr" + str(i))

            obrazDNr = QLabel()
            obrazDNr.setAlignment(QtCore.Qt.AlignCenter)
            obrazDNr.setObjectName("obrazDNr" + str(i))"""

            pobierzMp = QPushButton("MP3")
            pobierzMp.setIcon(self.style().standardIcon(
                QStyle.SP_DialogSaveButton)
            )
            pobierzMp.clicked.connect(
                lambda checked, arg=i: self._downloadAudio(
                    self.ident[(self.zmienna * 6) + arg],
                    self.title[(self.zmienna * 6) + arg]
                    )
            )
            pobierzMp.setObjectName("pobierzMv" + str(i))

            pobierzMv = QPushButton("MP4")
            pobierzMv.setIcon(self.style().standardIcon(
                QStyle.SP_DialogSaveButton)
            )
            pobierzMv.clicked.connect(
                lambda checked, arg=i: self._downloadVideo(
                    self.ident[(self.zmienna * 6) + arg],
                    self.title[(self.zmienna * 6) + arg]
                )
            )
            pobierzMv.setObjectName("pobierzMv" + str(i))

            odtworz = QPushButton("Odt")
            odtworz.setIcon(self.style().standardIcon(
                QStyle.SP_MediaPlay)
            )
            odtworz.clicked.connect(
                lambda checked, arg=i: self._play(
                    self.ident[(self.zmienna * 6) + arg],
                    self.title[(self.zmienna * 6) + arg],
                    self.time[(self.zmienna * 6) + arg]
                )
            )
            odtworz.setObjectName("odtworz" + str(i))

            odtworzWeb = QPushButton("YT")
            odtworzWeb.setIcon(self.style().standardIcon(
                QStyle.SP_FileDialogInfoView)
            )
            odtworzWeb.clicked.connect(
                lambda checked, arg=i: webbrowser.open(
                    "https://www.youtube.com/watch?v="
                    + self.ident[(self.zmienna * 6) + arg]
                )
            )
            odtworzWeb.setObjectName("odtworzWeb" + str(i))

            obszarPob = QHBoxLayout()
            obszarPob.addWidget(pobierzMp)
            obszarPob.addWidget(pobierzMv)
            obszarPob.setObjectName("obszarPob" + str(i))
            obszarOdt = QHBoxLayout()
            obszarOdt.addWidget(odtworz)
            obszarOdt.addWidget(odtworzWeb)
            obszarOdt.setObjectName("obszarOdt" + str(i))

            if i <= 2:
                self.obszarWideo.addLayout(obszarPob, 1, i % 3)
                self.obszarWideo.addLayout(obszarOdt, 2, i % 3)

            else:
                self.obszarWideo.addLayout(obszarPob, 4, i % 3)
                self.obszarWideo.addLayout(obszarOdt, 5, i % 3)

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

        self.obszarWideo.addWidget(self.obrazDNr1, 0, 0)
        self.obszarWideo.addWidget(self.obrazDNr4, 3, 0)

        self.obszarWideo.addWidget(self.obrazDNr2, 0, 1)
        self.obszarWideo.addWidget(self.obrazDNr5, 3, 1)

        self.obszarWideo.addWidget(self.obrazDNr3, 0, 2)
        self.obszarWideo.addWidget(self.obrazDNr6, 3, 2)

    def _getVideo(self):
        if self.poleWysz.currentText() == "":
            self._play("dQw4w9WgXcQ", "Never Gonna Give You Up", "3:33")
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

        self.zmienna = 0
        self.stronaWynikow.setText(str(self.zmienna + 1))
        if len(self.wynikiWysz) >= 6:
            self._updateUi()

    def _updateUi(self):
        if not self.wyswietlono:
            self.obszarGl.addLayout(self.obszarWideo)
            self.obszarGl.addLayout(self.stronaWysz)
            self.obszarGl.addWidget(self.progresPob)
            self.obszarGl.addWidget(self.terazOdt)
            self.obszarGl.addWidget(self.rozmiarKolejki)
            self.obszarGl.addLayout(self.obszarProgresu)
            self.obszarGl.addLayout(self.obszarKontrolek)

            self.przyciskPauzy.clicked.connect(lambda: self._pause())

            self.przyciskZatrzymania.clicked.connect(lambda: self._stop())

            self.przyciskDzwieku.clicked.connect(lambda: self._mute())

            self.poziomGlosu.valueChanged.connect(self._volume)

            self.przyciskPominiecia.clicked.connect(lambda: self._skip())

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
            self.worker = Dv._DownloadMP3(id, self.sciezkaPob, self.progresPob)
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
            self.worker = Dv._DownloadMP4(id, self.sciezkaPob, self.progresPob)
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
        self.progresPob.setText("Pobieranie zatrzymane.")

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

    def _play(self, id, title, time):
        if self.odtwarzacz.is_playing() and not self.czyPom:
            self.kolejkaOdt.append(id)
            self.kolejkaOdt.append(title)
            self.kolejkaOdt.append(time)
            self.rozmiarKolejki.setText(
                "W kolejce: " + str(int(len(self.kolejkaOdt) / 3))
            )
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
            with open(self.tempOdt, 'a') as f:
                f.write(id + "\n")
                f.write(title + "\n")
                f.write(time + "\n")
        """
        Play.Play(self.odtwarzacz, self.kolejkaOdt, self.rozmiarKolejki,
                 self.czasTrwania, self.terazOdt, self.Instance,
                 self.pasekProgresu, id, title, time, self.czyPom)
        """

    def _showSHistory(self):
        self.w = HistoryS.oknoHistorii(self.poleWysz, self.tempWysz)
        self.w.show()

    def _showOHistory(self):
        self.w = HistoryO.oknoHistorii(self.tempOdt)
        self.w.show()

    def _pause(self):
        if not self.czyPauza:
            self.odtwarzacz.pause()
            self._setPause()
        else:
            self._setPlay()
            self.odtwarzacz.pause()

    def _setPause(self):
        self.przyciskPauzy.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay)
        )
        self.przyciskPauzy.setText("Wznów")
        self.czyPauza = True

    def _setPlay(self):
        self.przyciskPauzy.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPause)
        )
        self.przyciskPauzy.setText("Pauza")
        self.czyPauza = False

    def _mute(self):
        if self.odtwarzacz.audio_get_mute():
            self.odtwarzacz.audio_set_mute(False)
            self.przyciskDzwieku.setText("Wycisz")
            self.przyciskDzwieku.setIcon(
                self.style().standardIcon(QStyle.SP_MediaVolume)
            )
        else:
            self.odtwarzacz.audio_set_mute(True)
            self.przyciskDzwieku.setText("Odcisz")
            self.przyciskDzwieku.setIcon(
                self.style().standardIcon(QStyle.SP_MediaVolumeMuted)
            )

    def _stop(self):
        self.odtwarzacz.stop()
        self.terazOdt.setText("Nic nie jest odtwarzane.")
        self.pasekProgresu.setValue(0)
        self._setPlay()

    def _skip(self):
        if len(self.kolejkaOdt) > 0:
            self.czyPom = True
            self._play(
                self.kolejkaOdt.pop(0),
                self.kolejkaOdt.pop(0),
                self.kolejkaOdt.pop(0)
            )
            self.czyPom = False
            if len(self.kolejkaOdt) <= 0:
                self.rozmiarKolejki.setText("Kolejka jest pusta.")
            else:
                self.rozmiarKolejki.setText(
                    "W kolejce: " + str(int(len(self.kolejkaOdt) / 3))
                )

            self._setPlay()

    def _volume(self):
        self.odtwarzacz.audio_set_volume(self.poziomGlosu.value())
        self.wartoscDzwieku.setText(str(self.poziomGlosu.value()))

    def _music(self):
        self.pasekProgresu.setValue(int(self.odtwarzacz.get_position() * 1000))
        self.wartoscProgresu.setText(
            time.strftime("%M:%S", time.gmtime(
                self.odtwarzacz.get_time() / 1000))
            + "/"
            + str(self.czasTrwania)
        )
        if self.powtarzanieUtworu.checkState() != 0:
            if self.odtwarzacz.get_position() * 100 >= 99:
                self.odtwarzacz.set_position(0)
        else:
            if self.odtwarzacz.is_playing() == 0:
                if len(self.kolejkaOdt) > 0:
                    if self.odtwarzacz.get_position() * 100 >= 99:
                        self._play(
                            self.kolejkaOdt.pop(0),
                            self.kolejkaOdt.pop(0),
                            self.kolejkaOdt.pop(0),
                        )
                        if len(self.kolejkaOdt) <= 0:
                            self.rozmiarKolejki.setText("Kolejka jest pusta.")
                        self._setPlay()

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
        historia.addAction("Odtwarzania", self._showOHistory)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Wersja: " + __version__ + ", Autor: " + __author__)
        self.setStatusBar(status)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
