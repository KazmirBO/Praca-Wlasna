#!/usr/bin/env python
# -*- coding: utf-8 -*-
# github.com/joetats/youtube_search/blob/master/youtube_search/__init__.py
# https://stackoverflow.com/questions/18054500/how-to-use-youtube-dl-from-a-python-program

import locale
import mpv
import sys
from pathlib import Path
from youtube_search import YoutubeSearch
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


__version__ = 'v0.0.1'
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
        
        obszar = QVBoxLayout()

        player = mpv.MPV(
            ytdl=True, 
            vo='null', 
            input_default_bindings=True, 
            input_vo_keyboard=True, 
            osc=True
            )
        
        poleWysz = "FIZICA - Готэм"
        
        ident = []
        time = []
        title = []
        mylist = []
        channel = []
        wynikiWysz = YoutubeSearch(
            "'" + poleWysz + "'", max_results=60
        ).to_dict()

        for v in wynikiWysz:
            ident.append(v["id"])
            time.append(v["duration"])
            title.append(v["title"])
            mylist.append(v["thumbnails"][0])
            channel.append(v["channel"])
        
        for i in range(0, 6):
            odtworz = QPushButton("Odt")
            odtworz.setIcon(self.style().standardIcon(
                QStyle.SP_MediaPlay)
            )
            odtworz.clicked.connect(
                lambda: player.play("https://www.youtube.com/watch?v=" + ident[i])
            )
            odtworz.setObjectName("odtworz" + str(i))
            obszar.addWidget(odtworz)
            
        self.generalLayout.addLayout(obszar)
        
        stop = QPushButton("Stop")
        stop.clicked.connect(lambda: player.stop())
        
        wstrzymaj = QPushButton("Wstrzymaj")
        wstrzymaj.clicked.connect(lambda: player.pause = True)
        
        self.generalLayout.addWidget(stop)
        self.generalLayout.addWidget(wstrzymaj)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    locale.setlocale(locale.LC_NUMERIC, 'C')
    window = Window()
    window.show()
    app.exec()

