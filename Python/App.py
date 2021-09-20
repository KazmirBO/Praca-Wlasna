#!/usr/bin/env python
# UTF-8

import sys, os
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
                             QSpinBox, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QFormLayout, QMainWindow, QStatusBar, QWidget,
                             QFileDialog, QScrollArea, QPushButton, QMessageBox)


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.response = 'Default-character.chr'
        self.Title = "Character Sheet - WFRP 4e - " + self.response
        self.setFont(QFont('PatrickHand', 12))
        self.setWindowTitle(self.Title)
        self.resize(1200, 800)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self._centralWidget.resize(1890, 980)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self._centralWidget)
        self.setCentralWidget(self.scroll)
        self._createMenu()
        self._createDisplay()
        self._createStatusBar()

        # ----------------------------------------------------------------------

    def _createDisplay(self):
        self.Classes = QComboBox()
        self.Classes.addItems(["Academics", "Burghers", "Courtiers",
                               "Peasants", "Rangers", "Riverfolk", "Rouges",
                               "Warriors"])

        self.Species = QComboBox()
        self.Species.addItems(
            ["Human", "Dwarf", "Hlafling", "High Elf", "Wood Elf"])

        self.Level = QComboBox()
        self.Level.addItems(["1", "2", "3", "4"])

        self.Status = QComboBox()
        self.Status.addItems(["Brass", "Silver", "Gold"])

        self.SLevel = QComboBox()
        self.SLevel.addItems(["1", "2", "3", "4", "5"])

        self.top = QVBoxLayout()
        self.line1 = QHBoxLayout()
        self.line2 = QHBoxLayout()
        self.line3 = QHBoxLayout()
        self.line4 = QHBoxLayout()

        self.Name = QLineEdit()
        self.Name.setPlaceholderText("Character Name")
        self.Car = QLineEdit()
        self.Car.setPlaceholderText("Character Career...")
        self.CarP = QLineEdit()
        self.CarP.setPlaceholderText("... and Carrer Path")
        self.Age = QLineEdit()
        self.Age.setInputMask("999 yo")
        self.Age.setPlaceholderText("Age")
        self.Height = QLineEdit()
        self.Height.setInputMask("9'9'', 999 cm")
        self.Height.setPlaceholderText("Height")
        self.Hair = QLineEdit()
        self.Hair.setPlaceholderText("Hair")
        self.Eyes = QLineEdit()
        self.Eyes.setPlaceholderText("Eyes")

        self.Name.setMinimumWidth(120)
        self.Age.setFixedWidth(70)
        self.Height.setFixedWidth(100)

        self.line1.addWidget(QLabel("Name: "))
        self.line1.addWidget(self.Name)
        self.line1.addWidget(QLabel("Species: "))
        self.line1.addWidget(self.Species)
        self.line1.addWidget(QLabel("Class: "))
        self.line1.addWidget(self.Classes)

        self.line2.addWidget(QLabel("Career: "))
        self.line2.addWidget(self.Car)
        self.line2.addWidget(QLabel("Career Level: "))
        self.line2.addWidget(self.Level)

        self.line3.addWidget(QLabel("Career Path: "))
        self.line3.addWidget(self.CarP)
        self.line3.addWidget(QLabel("Status: "))
        self.line3.addWidget(self.Status)
        self.line3.addWidget(self.SLevel)

        self.line4.addWidget(QLabel("Age: "))
        self.line4.addWidget(self.Age)
        self.line4.addWidget(QLabel("Height: "))
        self.line4.addWidget(self.Height)
        self.line4.addWidget(QLabel("Hair: "))
        self.line4.addWidget(self.Hair)
        self.line4.addWidget(QLabel("Eyes: "))
        self.line4.addWidget(self.Eyes)

        self.top.addLayout(self.line1)
        self.top.addLayout(self.line2)
        self.top.addLayout(self.line3)
        self.top.addLayout(self.line4)
        self.top.addStretch()

        # ----------------------------------------------------------------------

        self.ch = QGridLayout()

        self.ch.addWidget(QLabel(), 0, 0)
        self.ch.addWidget(QLabel("WS"), 0, 1)
        self.ch.addWidget(QLabel("BS"), 0, 2)
        self.ch.addWidget(QLabel("S"), 0, 3)
        self.ch.addWidget(QLabel("T"), 0, 4)
        self.ch.addWidget(QLabel("I"), 0, 5)
        self.ch.addWidget(QLabel("Ag"), 0, 6)
        self.ch.addWidget(QLabel("Dex"), 0, 7)
        self.ch.addWidget(QLabel("Int"), 0, 8)
        self.ch.addWidget(QLabel("WP"), 0, 9)
        self.ch.addWidget(QLabel("Fel"), 0, 10)
        self.ch.addWidget(QLabel("Initial: "), 1, 0)

        self.WSi = QSpinBox()
        self.BSi = QSpinBox()
        self.Si = QSpinBox()
        self.Ti = QSpinBox()
        self.Ii = QSpinBox()
        self.Agi = QSpinBox()
        self.Dexi = QSpinBox()
        self.Inti = QSpinBox()
        self.WPi = QSpinBox()
        self.Feli = QSpinBox()

        self.ch.addWidget(self.WSi, 1, 1)
        self.ch.addWidget(self.BSi, 1, 2)
        self.ch.addWidget(self.Si, 1, 3)
        self.ch.addWidget(self.Ti, 1, 4)
        self.ch.addWidget(self.Ii, 1, 5)
        self.ch.addWidget(self.Agi, 1, 6)
        self.ch.addWidget(self.Dexi, 1, 7)
        self.ch.addWidget(self.Inti, 1, 8)
        self.ch.addWidget(self.WPi, 1, 9)
        self.ch.addWidget(self.Feli, 1, 10)

        self.ch.addWidget(QLabel("Advances: "), 2, 0)

        self.WSa = QSpinBox()
        self.BSa = QSpinBox()
        self.Sa = QSpinBox()
        self.Ta = QSpinBox()
        self.Ia = QSpinBox()
        self.Aga = QSpinBox()
        self.Dexa = QSpinBox()
        self.Inta = QSpinBox()
        self.WPa = QSpinBox()
        self.Fela = QSpinBox()

        self.ch.addWidget(self.WSa, 2, 1)
        self.ch.addWidget(self.BSa, 2, 2)
        self.ch.addWidget(self.Sa, 2, 3)
        self.ch.addWidget(self.Ta, 2, 4)
        self.ch.addWidget(self.Ia, 2, 5)
        self.ch.addWidget(self.Aga, 2, 6)
        self.ch.addWidget(self.Dexa, 2, 7)
        self.ch.addWidget(self.Inta, 2, 8)
        self.ch.addWidget(self.WPa, 2, 9)
        self.ch.addWidget(self.Fela, 2, 10)

        self.ch.addWidget(QLabel("Current: "), 3, 0)

        self.WSc = QSpinBox()
        self.WSc.setReadOnly(True)
        self.BSc = QSpinBox()
        self.BSc.setReadOnly(True)
        self.Sc = QSpinBox()
        self.Sc.setReadOnly(True)
        self.Tc = QSpinBox()
        self.Tc.setReadOnly(True)
        self.Ic = QSpinBox()
        self.Ic.setReadOnly(True)
        self.Agc = QSpinBox()
        self.Agc.setReadOnly(True)
        self.Dexc = QSpinBox()
        self.Dexc.setReadOnly(True)
        self.Intc = QSpinBox()
        self.Intc.setReadOnly(True)
        self.WPc = QSpinBox()
        self.WPc.setReadOnly(True)
        self.Felc = QSpinBox()
        self.Felc.setReadOnly(True)

        self.ch.addWidget(self.WSc, 3, 1)
        self.ch.addWidget(self.BSc, 3, 2)
        self.ch.addWidget(self.Sc, 3, 3)
        self.ch.addWidget(self.Tc, 3, 4)
        self.ch.addWidget(self.Ic, 3, 5)
        self.ch.addWidget(self.Agc, 3, 6)
        self.ch.addWidget(self.Dexc, 3, 7)
        self.ch.addWidget(self.Intc, 3, 8)
        self.ch.addWidget(self.WPc, 3, 9)
        self.ch.addWidget(self.Felc, 3, 10)

        self.chara = QVBoxLayout()

        self.characteristic = QLabel("CHARACTERISTICS")
        self.characteristic.setAlignment(QtCore.Qt.AlignCenter)
        self.chara.addWidget(self.characteristic)
        self.chara.addLayout(self.ch)
        self.chara.addStretch()

        # ----------------------------------------------------------------------

        self.WSi.valueChanged.connect(self.WSrefresh)
        self.WSa.valueChanged.connect(self.WSrefresh)

        self.BSi.valueChanged.connect(self.BSrefresh)
        self.BSa.valueChanged.connect(self.BSrefresh)

        self.Si.valueChanged.connect(self.Srefresh)
        self.Sa.valueChanged.connect(self.Srefresh)

        self.Ti.valueChanged.connect(self.Trefresh)
        self.Ta.valueChanged.connect(self.Trefresh)

        self.Ii.valueChanged.connect(self.Irefresh)
        self.Ia.valueChanged.connect(self.Irefresh)

        self.Agi.valueChanged.connect(self.Agrefresh)
        self.Aga.valueChanged.connect(self.Agrefresh)

        self.Dexi.valueChanged.connect(self.Dexrefresh)
        self.Dexa.valueChanged.connect(self.Dexrefresh)

        self.Inti.valueChanged.connect(self.Intrefresh)
        self.Inta.valueChanged.connect(self.Intrefresh)

        self.WPi.valueChanged.connect(self.WPrefresh)
        self.WPa.valueChanged.connect(self.WPrefresh)

        self.Feli.valueChanged.connect(self.Felrefresh)
        self.Fela.valueChanged.connect(self.Felrefresh)

        # ----------------------------------------------------------------------

        self.fate = QFormLayout()
        self.FText = QLabel("FATE")
        self.Fate = QSpinBox()
        self.Fortune = QSpinBox()
        self.FText.setAlignment(QtCore.Qt.AlignCenter)

        self.fate.addRow(self.FText)
        self.fate.addRow(QLabel("Fate: "), self.Fate)
        self.fate.addRow(QLabel("Fortune: "), self.Fortune)

        # ----------------------------------------------------------------------

        self.move = QVBoxLayout()
        self.mstat = QFormLayout()
        self.MText = QLabel("MOVEMENT")
        self.MText.setAlignment(QtCore.Qt.AlignCenter)
        self.Movement = QSpinBox()
        self.Walk = QSpinBox()
        self.Run = QSpinBox()

        self.mstat.addRow(QLabel("Movement: "), self.Movement)
        self.mstat.addRow(QLabel("Walk: "), self.Walk)
        self.mstat.addRow(QLabel("Run: "), self.Run)

        self.move.addWidget(self.MText)
        self.move.addLayout(self.mstat)
        self.move.addStretch()

        self.Movement.valueChanged.connect(self.Mrefresh)
        self.Walk.valueChanged.connect(self.Mrefresh)
        self.Run.valueChanged.connect(self.Mrefresh)

        # ----------------------------------------------------------------------

        self.EText = QLabel("EXPERIENCE")
        self.EText.setAlignment(QtCore.Qt.AlignCenter)
        self.exp = QFormLayout()
        self.Current = QSpinBox()
        self.Spent = QSpinBox()
        self.Total = QSpinBox()
        self.Current.setMaximum(10000)
        self.Spent.setMaximum(10000)
        self.Total.setMaximum(10000)
        self.Current.setFixedWidth(80)
        self.Spent.setFixedWidth(80)
        self.Total.setFixedWidth(80)

        self.exp.addRow(self.EText)
        self.exp.addRow(QLabel("Current: "), self.Current)
        self.exp.addRow(QLabel("Spent: "), self.Spent)
        self.exp.addRow(QLabel("Total: "), self.Total)

        self.Current.valueChanged.connect(self.Erefresh)
        self.Spent.valueChanged.connect(self.Erefresh)
        self.Total.valueChanged.connect(self.Erefresh)

        # ----------------------------------------------------------------------

        self.resi = QVBoxLayout()
        self.resibottom = QFormLayout()
        self.RText = QLabel("RESILIENCE")
        self.RText.setAlignment(QtCore.Qt.AlignCenter)
        self.Resi = QSpinBox()
        self.Reso = QSpinBox()
        self.Motivation = QLineEdit()

        self.resibottom.addRow(QLabel("Resilience: "), self.Resi)
        self.resibottom.addRow(QLabel("Resolve: "), self.Reso)
        self.resibottom.addRow(QLabel("Motivation: "), self.Motivation)

        self.resi.addWidget(self.RText)
        self.resi.addLayout(self.resibottom)
        self.resi.addStretch()

        # ----------------------------------------------------------------------

        self.amb = QFormLayout()
        self.SAP = QLineEdit()
        self.SAP.setPlaceholderText("Short")
        self.LAP = QLineEdit()
        self.LAP.setPlaceholderText("Long")
        self.par = QFormLayout()
        self.SAG = QLineEdit()
        self.SAG.setPlaceholderText("Short")
        self.LAG = QLineEdit()
        self.LAG.setPlaceholderText("Long")
        self.members = QLineEdit()
        self.members.setPlaceholderText("Members")
        self.partyName = QLineEdit()
        self.partyName.setPlaceholderText("Party name")
        self.ambitions = QLabel("AMBITIONS")
        self.ambitions.setAlignment(QtCore.Qt.AlignCenter)
        self.party = QLabel("PARTY")
        self.party.setAlignment(QtCore.Qt.AlignCenter)

        # ----------------------------------------------------------------------

        self.amb.addRow(self.ambitions)
        self.amb.addRow(QLabel("Short-term: "), self.SAP)
        self.amb.addRow(QLabel("Long-term: "), self.LAP)
        self.par.addRow(self.party)
        self.par.addRow(QLabel("Party name: "), self.partyName)
        self.par.addRow(QLabel("Short-term: "), self.SAG)
        self.par.addRow(QLabel("Long-term: "), self.LAG)
        self.par.addRow(QLabel("Members: "), self.members)

        # ----------------------------------------------------------------------

        self.middle = QHBoxLayout()
        self.middle.addLayout(self.chara)
        self.middle.addLayout(self.fate)
        self.middle.addLayout(self.move)
        self.middle.addLayout(self.exp)
        self.middle.addLayout(self.resi)
        self.middle.addLayout(self.amb)
        self.middle.addLayout(self.par)

        # ----------------------------------------------------------------------

        self.bottom = QGridLayout()
        self.basic1 = QGridLayout()
        self.basic2 = QGridLayout()

        # ----------------------------------------------------------------------

        self.basic1.addWidget(QLabel("Name"), 0, 0)
        self.basic1.addWidget(QLabel("Art"), 1, 0)
        self.basic1.addWidget(QLabel("Athletics"), 2, 0)
        self.basic1.addWidget(QLabel("Bribery"), 3, 0)
        self.basic1.addWidget(QLabel("Charm"), 4, 0)
        self.basic1.addWidget(QLabel("Charm animal"), 5, 0)
        self.basic1.addWidget(QLabel("Climb"), 6, 0)
        self.basic1.addWidget(QLabel("Cool"), 7, 0)
        self.basic1.addWidget(QLabel("Consume Alcohol"), 8, 0)
        self.basic1.addWidget(QLabel("Dodge"), 9, 0)
        self.basic1.addWidget(QLabel("Drive"), 10, 0)
        self.basic1.addWidget(QLabel("Endurance"), 11, 0)
        self.basic1.addWidget(QLabel("Entertain"), 12, 0)
        self.basic1.addWidget(QLabel("Gamble"), 13, 0)

        # ----------------------------------------------------------------------

        self.basic1.addWidget(QLabel("Characterisitc"), 0, 1)
        self.basic1.addWidget(QLabel("Dex"), 1, 1)
        self.basic1.addWidget(QLabel("Ag"), 2, 1)
        self.basic1.addWidget(QLabel("Fel"), 3, 1)
        self.basic1.addWidget(QLabel("Fel"), 4, 1)
        self.basic1.addWidget(QLabel("WP"), 5, 1)
        self.basic1.addWidget(QLabel("S"), 6, 1)
        self.basic1.addWidget(QLabel("WP"), 7, 1)
        self.basic1.addWidget(QLabel("T"), 8, 1)
        self.basic1.addWidget(QLabel("Ag"), 9, 1)
        self.basic1.addWidget(QLabel("Ag"), 10, 1)
        self.basic1.addWidget(QLabel("T"), 11, 1)
        self.basic1.addWidget(QLabel("Fel"), 12, 1)
        self.basic1.addWidget(QLabel("Int"), 13, 1)

        # ----------------------------------------------------------------------

        self.art = QSpinBox()
        self.ath = QSpinBox()
        self.bri = QSpinBox()
        self.chr = QSpinBox()
        self.cha = QSpinBox()
        self.cli = QSpinBox()
        self.col = QSpinBox()
        self.con = QSpinBox()
        self.dod = QSpinBox()
        self.dri = QSpinBox()
        self.end = QSpinBox()
        self.ent = QSpinBox()
        self.gam = QSpinBox()

        # ----------------------------------------------------------------------

        self.basic1.addWidget(QLabel("Adv"), 0, 2)
        self.basic1.addWidget(self.art, 1, 2)
        self.basic1.addWidget(self.ath, 2, 2)
        self.basic1.addWidget(self.bri, 3, 2)
        self.basic1.addWidget(self.chr, 4, 2)
        self.basic1.addWidget(self.cha, 5, 2)
        self.basic1.addWidget(self.cli, 6, 2)
        self.basic1.addWidget(self.col, 7, 2)
        self.basic1.addWidget(self.con, 8, 2)
        self.basic1.addWidget(self.dod, 9, 2)
        self.basic1.addWidget(self.dri, 10, 2)
        self.basic1.addWidget(self.end, 11, 2)
        self.basic1.addWidget(self.ent, 12, 2)
        self.basic1.addWidget(self.gam, 13, 2)

        # ----------------------------------------------------------------------

        self.arta = QSpinBox()
        self.arta.setReadOnly(True)
        self.atha = QSpinBox()
        self.atha.setReadOnly(True)
        self.bria = QSpinBox()
        self.bria.setReadOnly(True)
        self.chra = QSpinBox()
        self.chra.setReadOnly(True)
        self.chaa = QSpinBox()
        self.chaa.setReadOnly(True)
        self.clia = QSpinBox()
        self.clia.setReadOnly(True)
        self.cola = QSpinBox()
        self.cola.setReadOnly(True)
        self.cona = QSpinBox()
        self.cona.setReadOnly(True)
        self.doda = QSpinBox()
        self.doda.setReadOnly(True)
        self.dria = QSpinBox()
        self.dria.setReadOnly(True)
        self.enda = QSpinBox()
        self.enda.setReadOnly(True)
        self.enta = QSpinBox()
        self.enta.setReadOnly(True)
        self.gama = QSpinBox()
        self.gama.setReadOnly(True)

        # ----------------------------------------------------------------------

        self.basic1.addWidget(QLabel("Skill"), 0, 3)
        self.basic1.addWidget(self.arta, 1, 3)
        self.basic1.addWidget(self.atha, 2, 3)
        self.basic1.addWidget(self.bria, 3, 3)
        self.basic1.addWidget(self.chra, 4, 3)
        self.basic1.addWidget(self.chaa, 5, 3)
        self.basic1.addWidget(self.clia, 6, 3)
        self.basic1.addWidget(self.cola, 7, 3)
        self.basic1.addWidget(self.cona, 8, 3)
        self.basic1.addWidget(self.doda, 9, 3)
        self.basic1.addWidget(self.dria, 10, 3)
        self.basic1.addWidget(self.enda, 11, 3)
        self.basic1.addWidget(self.enta, 12, 3)
        self.basic1.addWidget(self.gama, 13, 3)

        # ----------------------------------------------------------------------

        self.art.valueChanged.connect(self.Rarta)
        self.ath.valueChanged.connect(self.Ratha)
        self.bri.valueChanged.connect(self.Rbria)
        self.chr.valueChanged.connect(self.Rchra)
        self.cha.valueChanged.connect(self.Rchaa)
        self.cli.valueChanged.connect(self.Rclia)
        self.col.valueChanged.connect(self.Rcola)
        self.con.valueChanged.connect(self.Rcona)
        self.dod.valueChanged.connect(self.Rdoda)
        self.dri.valueChanged.connect(self.Rdria)
        self.end.valueChanged.connect(self.Renda)
        self.ent.valueChanged.connect(self.Renta)
        self.gam.valueChanged.connect(self.Rgama)

        # ----------------------------------------------------------------------

        self.basic2.addWidget(QLabel("Name"), 0, 0)
        self.basic2.addWidget(QLabel("Gossip"), 1, 0)
        self.basic2.addWidget(QLabel("Haggle"), 2, 0)
        self.basic2.addWidget(QLabel("Intimidate"), 3, 0)
        self.basic2.addWidget(QLabel("Intuition"), 4, 0)
        self.basic2.addWidget(QLabel("Leadership"), 5, 0)
        self.basic2.addWidget(QLabel("Melee (basic)"), 6, 0)
        self.basic2.addWidget(QLabel("Melee"), 7, 0)
        self.basic2.addWidget(QLabel("Navigation"), 8, 0)
        self.basic2.addWidget(QLabel("Outdor Survival"), 9, 0)
        self.basic2.addWidget(QLabel("Perception"), 10, 0)
        self.basic2.addWidget(QLabel("Ride"), 11, 0)
        self.basic2.addWidget(QLabel("Row"), 12, 0)
        self.basic2.addWidget(QLabel("Stealth"), 13, 0)

        # ----------------------------------------------------------------------

        self.basic2.addWidget(QLabel("Characterisitc"), 0, 1)
        self.basic2.addWidget(QLabel("Fel"), 1, 1)
        self.basic2.addWidget(QLabel("Fel"), 2, 1)
        self.basic2.addWidget(QLabel("S"), 3, 1)
        self.basic2.addWidget(QLabel("I"), 4, 1)
        self.basic2.addWidget(QLabel("Fel"), 5, 1)
        self.basic2.addWidget(QLabel("WS"), 6, 1)
        self.basic2.addWidget(QLabel("WS"), 7, 1)
        self.basic2.addWidget(QLabel("I"), 8, 1)
        self.basic2.addWidget(QLabel("Int"), 9, 1)
        self.basic2.addWidget(QLabel("I"), 10, 1)
        self.basic2.addWidget(QLabel("Ag"), 11, 1)
        self.basic2.addWidget(QLabel("S"), 12, 1)
        self.basic2.addWidget(QLabel("Ag"), 13, 1)

        # ----------------------------------------------------------------------

        self.gos = QSpinBox()
        self.hag = QSpinBox()
        self.inm = QSpinBox()
        self.inu = QSpinBox()
        self.lea = QSpinBox()
        self.mlb = QSpinBox()
        self.mle = QSpinBox()
        self.nav = QSpinBox()
        self.out = QSpinBox()
        self.per = QSpinBox()
        self.rid = QSpinBox()
        self.row = QSpinBox()
        self.ste = QSpinBox()

        # ----------------------------------------------------------------------

        self.basic2.addWidget(QLabel("Adv"), 0, 2)
        self.basic2.addWidget(self.gos, 1, 2)
        self.basic2.addWidget(self.hag, 2, 2)
        self.basic2.addWidget(self.inm, 3, 2)
        self.basic2.addWidget(self.inu, 4, 2)
        self.basic2.addWidget(self.lea, 5, 2)
        self.basic2.addWidget(self.mlb, 6, 2)
        self.basic2.addWidget(self.mle, 7, 2)
        self.basic2.addWidget(self.nav, 8, 2)
        self.basic2.addWidget(self.out, 9, 2)
        self.basic2.addWidget(self.per, 10, 2)
        self.basic2.addWidget(self.rid, 11, 2)
        self.basic2.addWidget(self.row, 12, 2)
        self.basic2.addWidget(self.ste, 13, 2)

        # ----------------------------------------------------------------------

        self.gosa = QSpinBox()
        self.gosa.setReadOnly(True)
        self.haga = QSpinBox()
        self.haga.setReadOnly(True)
        self.inma = QSpinBox()
        self.inma.setReadOnly(True)
        self.inua = QSpinBox()
        self.inua.setReadOnly(True)
        self.leaa = QSpinBox()
        self.leaa.setReadOnly(True)
        self.mlba = QSpinBox()
        self.mlba.setReadOnly(True)
        self.mlea = QSpinBox()
        self.mlea.setReadOnly(True)
        self.nava = QSpinBox()
        self.nava.setReadOnly(True)
        self.outa = QSpinBox()
        self.outa.setReadOnly(True)
        self.pera = QSpinBox()
        self.pera.setReadOnly(True)
        self.rida = QSpinBox()
        self.rida.setReadOnly(True)
        self.rowa = QSpinBox()
        self.rowa.setReadOnly(True)
        self.stea = QSpinBox()
        self.stea.setReadOnly(True)

        # ----------------------------------------------------------------------

        self.basic2.addWidget(QLabel("Skill"), 0, 3)
        self.basic2.addWidget(self.gosa, 1, 3)
        self.basic2.addWidget(self.haga, 2, 3)
        self.basic2.addWidget(self.inma, 3, 3)
        self.basic2.addWidget(self.inua, 4, 3)
        self.basic2.addWidget(self.leaa, 5, 3)
        self.basic2.addWidget(self.mlba, 6, 3)
        self.basic2.addWidget(self.mlea, 7, 3)
        self.basic2.addWidget(self.nava, 8, 3)
        self.basic2.addWidget(self.outa, 9, 3)
        self.basic2.addWidget(self.pera, 10, 3)
        self.basic2.addWidget(self.rida, 11, 3)
        self.basic2.addWidget(self.rowa, 12, 3)
        self.basic2.addWidget(self.stea, 13, 3)

        # ----------------------------------------------------------------------

        self.bottom.addLayout(self.basic1, 0, 0)
        self.bottom.addLayout(self.basic2, 0, 1)

        # ----------------------------------------------------------------------

        self.gos.valueChanged.connect(self.Rgosa)
        self.hag.valueChanged.connect(self.Rhaga)
        self.inm.valueChanged.connect(self.Rinma)
        self.inu.valueChanged.connect(self.Rinua)
        self.lea.valueChanged.connect(self.Rleaa)
        self.mlb.valueChanged.connect(self.Rmlba)
        self.mle.valueChanged.connect(self.Rmlea)
        self.nav.valueChanged.connect(self.Rnava)
        self.out.valueChanged.connect(self.Routa)
        self.per.valueChanged.connect(self.Rpera)
        self.rid.valueChanged.connect(self.Rrida)
        self.row.valueChanged.connect(self.Rrowa)
        self.ste.valueChanged.connect(self.Rstea)

        # ----------------------------------------------------------------------

        self.generalLayout.addLayout(self.top)
        self.generalLayout.addLayout(self.middle)
        self.generalLayout.addLayout(self.bottom)
        self.generalLayout.addStretch()

        # ----------------------------------------------------------------------

    def ShowTalent(self):
        self.TalentWindow.show()

    def ShowSkill(self):
        self.SkillWindow.show()

    def Suma(self, a, b):
        return a.value()+b.value()

    def WSrefresh(self):
        self.WSc.setValue(self.Suma(self.WSi, self.WSa))
        self.Rmlba()
        self.Rmlea()

    def BSrefresh(self):
        self.BSc.setValue(self.Suma(self.BSi, self.BSa))

    def Srefresh(self):
        self.Sc.setValue(self.Suma(self.Si, self.Sa))
        self.Rclia()
        self.Rinma()
        self.Rrowa()

    def Trefresh(self):
        self.Tc.setValue(self.Suma(self.Ti, self.Ta))
        self.Rcona()
        self.Renda()

    def Irefresh(self):
        self.Ic.setValue(self.Suma(self.Ii, self.Ia))
        self.Rinua()
        self.Rnava()
        self.Rpera()

    def Agrefresh(self):
        self.Agc.setValue(self.Suma(self.Agi, self.Aga))
        self.Ratha()
        self.Rdoda()
        self.Rdria()
        self.Rrida()
        self.Rstea()

    def Dexrefresh(self):
        self.Dexc.setValue(self.Suma(self.Dexi, self.Dexa))
        self.Rarta()

    def Intrefresh(self):
        self.Intc.setValue(self.Suma(self.Inti, self.Inta))
        self.Rgama()
        self.Routa()

    def WPrefresh(self):
        self.WPc.setValue(self.Suma(self.WPi, self.WPa))
        self.Rchaa()
        self.Rcola()

    def Felrefresh(self):
        self.Felc.setValue(self.Suma(self.Feli, self.Fela))
        self.Rbria()
        self.Rchra()
        self.Renta()
        self.Rgosa()
        self.Rhaga()
        self.Rleaa()

    # --------------------------------------------------------------------------

    def Rarta(self):
        self.arta.setValue(self.Suma(self.art, self.Dexc))

    def Ratha(self):
        self.atha.setValue(self.Suma(self.ath, self.Agc))

    def Rbria(self):
        self.bria.setValue(self.Suma(self.bri, self.Felc))

    def Rchra(self):
        self.chra.setValue(self.Suma(self.chr, self.Felc))

    def Rchaa(self):
        self.chaa.setValue(self.Suma(self.cha, self.WPc))

    def Rclia(self):
        self.clia.setValue(self.Suma(self.cli, self.Sc))

    def Rcola(self):
        self.cola.setValue(self.Suma(self.col, self.WPc))

    def Rcona(self):
        self.cona.setValue(self.Suma(self.con, self.Tc))

    def Rdoda(self):
        self.doda.setValue(self.Suma(self.dod, self.Agc))

    def Rdria(self):
        self.dria.setValue(self.Suma(self.dri, self.Agc))

    def Renda(self):
        self.enda.setValue(self.Suma(self.end, self.Tc))

    def Renta(self):
        self.enta.setValue(self.Suma(self.ent, self.Felc))

    def Rgama(self):
        self.gama.setValue(self.Suma(self.gam, self.Intc))

    def Rgosa(self):
        self.gosa.setValue(self.Suma(self.gos, self.Felc))

    def Rhaga(self):
        self.haga.setValue(self.Suma(self.hag, self.Felc))

    def Rinma(self):
        self.inma.setValue(self.Suma(self.inm, self.Sc))

    def Rinua(self):
        self.inua.setValue(self.Suma(self.inu, self.Ic))

    def Rleaa(self):
        self.leaa.setValue(self.Suma(self.lea, self.Felc))

    def Rmlba(self):
        self.mlba.setValue(self.Suma(self.mlb, self.WSc))

    def Rmlea(self):
        self.mlea.setValue(self.Suma(self.mle, self.WSc))

    def Rnava(self):
        self.nava.setValue(self.Suma(self.nav, self.Ic))

    def Routa(self):
        self.outa.setValue(self.Suma(self.out, self.Intc))

    def Rpera(self):
        self.pera.setValue(self.Suma(self.per, self.Ic))

    def Rrida(self):
        self.rida.setValue(self.Suma(self.rid, self.Agc))

    def Rrowa(self):
        self.rowa.setValue(self.Suma(self.row, self.Sc))

    def Rstea(self):
        self.stea.setValue(self.Suma(self.ste, self.Agc))

    # --------------------------------------------------------------------------

    def Mrefresh(self):
        self.Walk.setValue(self.Movement.value() * 2)
        self.Run.setValue(self.Walk.value() * 2)

    def Erefresh(self):
        self.Total.setValue(self.Current.value() + self.Spent.value())

    # --------------------------------------------------------------------------

    def _createMenu(self):
        self.menu = self.menuBar().addMenu('&Menu')
        self.menu.addAction('&Get File Name', self.getFileName)
        self.menu.addAction('&Import', self.impo)
        self.menu.addAction('&Export', self.expo)
        self.menu.addAction('&Exit', self.close)
        self.menu = self.menuBar().addAction('&Help', self.help)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Hello World!")
        self.setStatusBar(status)

    def help(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Application for displaying and editing characters for " +
                    "WFRP 4e with the possibility of exporting and importing.")
        msg.setInformativeText('The above program uses files ' +
                               'with the * .chr extension.')
        msg.setWindowTitle("Help")
        msg.exec_()

    # --------------------------------------------------------------------------

    def impo(self):
        if os.path.isfile(self.response) == True:
            stats = []
            with open(self.response, 'r') as f:
                stats = f.read().splitlines()
            f.close()
            count = 0
            self.Name.setText(str(stats[0]))
            self.Species.setCurrentIndex(int(stats[1]))
            self.Classes.setCurrentIndex(int(stats[2]))
            self.Car.setText(str(stats[3]))
            self.Level.setCurrentIndex(int(stats[4]))
            self.CarP.setText(str(stats[5]))
            self.Status.setCurrentIndex(int(stats[6]))
            self.SLevel.setCurrentIndex(int(stats[7]))
            self.Age.setText(str(stats[8]))
            self.Height.setText(str(stats[9]))
            self.Hair.setText(str(stats[10]))
            self.Eyes.setText(str(stats[11]))
            self.WSi.setValue(int(stats[12]))
            self.WSa.setValue(int(stats[13]))
            self.BSi.setValue(int(stats[14]))
            self.BSa.setValue(int(stats[15]))
            self.Si.setValue(int(stats[16]))
            self.Sa.setValue(int(stats[17]))
            self.Ti.setValue(int(stats[18]))
            self.Ta.setValue(int(stats[19]))
            self.Ii.setValue(int(stats[20]))
            self.Ia.setValue(int(stats[21]))
            self.Agi.setValue(int(stats[22]))
            self.Aga.setValue(int(stats[23]))
            self.Dexi.setValue(int(stats[24]))
            self.Dexa.setValue(int(stats[25]))
            self.Inti.setValue(int(stats[26]))
            self.Inta.setValue(int(stats[27]))
            self.WPi.setValue(int(stats[28]))
            self.WPa.setValue(int(stats[29]))
            self.Feli.setValue(int(stats[30]))
            self.Fela.setValue(int(stats[31]))
            self.Fate.setValue(int(stats[32]))
            self.Fortune.setValue(int(stats[33]))
            self.Movement.setValue(int(stats[34]))
            self.Current.setValue(int(stats[35]))
            self.Spent.setValue(int(stats[36]))
            self.Resi.setValue(int(stats[37]))
            self.Reso.setValue(int(stats[38]))
            self.Motivation.setText(str(stats[39]))
            self.art.setValue(int(stats[40]))
            self.ath.setValue(int(stats[41]))
            self.bri.setValue(int(stats[42]))
            self.chr.setValue(int(stats[43]))
            self.cha.setValue(int(stats[44]))
            self.cli.setValue(int(stats[45]))
            self.col.setValue(int(stats[46]))
            self.con.setValue(int(stats[47]))
            self.dod.setValue(int(stats[48]))
            self.dri.setValue(int(stats[49]))
            self.end.setValue(int(stats[50]))
            self.ent.setValue(int(stats[51]))
            self.gam.setValue(int(stats[52]))
            self.gos.setValue(int(stats[53]))
            self.hag.setValue(int(stats[54]))
            self.inm.setValue(int(stats[55]))
            self.inu.setValue(int(stats[56]))
            self.lea.setValue(int(stats[57]))
            self.mlb.setValue(int(stats[58]))
            self.mle.setValue(int(stats[59]))
            self.nav.setValue(int(stats[60]))
            self.out.setValue(int(stats[61]))
            self.per.setValue(int(stats[62]))
            self.rid.setValue(int(stats[63]))
            self.row.setValue(int(stats[64]))
            self.ste.setValue(int(stats[65]))
            self.SAP.setText(str(stats[66]))
            self.LAP.setText(str(stats[67]))
            self.partyName.setText(str(stats[68]))
            self.SAG.setText(str(stats[69]))
            self.LAG.setText(str(stats[70]))
            self.members.setText(str(stats[71]))
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("The file " + self.response + " was not found.")
            msg.setInformativeText('Try to export the file or create it ' +
                                   'manually and then try again.')
            msg.setWindowTitle("Error")
            msg.exec_()

    # --------------------------------------------------------------------------

    def expo(self):
        with open(self.response, 'w') as f:
            # f.write('%s\n' % )
            f.write('%s\n' % self.Name.text())
            f.write('%s\n' % self.Species.currentIndex())
            f.write('%s\n' % self.Classes.currentIndex())
            f.write('%s\n' % self.Car.text())
            f.write('%s\n' % self.Level.currentIndex())
            f.write('%s\n' % self.CarP.text())
            f.write('%s\n' % self.Status.currentIndex())
            f.write('%s\n' % self.SLevel.currentIndex())
            f.write('%s\n' % self.Age.text())
            f.write('%s\n' % self.Height.text())
            f.write('%s\n' % self.Hair.text())
            f.write('%s\n' % self.Eyes.text())
            f.write('%s\n' % self.WSi.value())
            f.write('%s\n' % self.WSa.value())
            f.write('%s\n' % self.BSi.value())
            f.write('%s\n' % self.BSa.value())
            f.write('%s\n' % self.Si.value())
            f.write('%s\n' % self.Sa.value())
            f.write('%s\n' % self.Ti.value())
            f.write('%s\n' % self.Ta.value())
            f.write('%s\n' % self.Ii.value())
            f.write('%s\n' % self.Ia.value())
            f.write('%s\n' % self.Agi.value())
            f.write('%s\n' % self.Aga.value())
            f.write('%s\n' % self.Dexi.value())
            f.write('%s\n' % self.Dexa.value())
            f.write('%s\n' % self.Inti.value())
            f.write('%s\n' % self.Inta.value())
            f.write('%s\n' % self.WPi.value())
            f.write('%s\n' % self.WPa.value())
            f.write('%s\n' % self.Feli.value())
            f.write('%s\n' % self.Fela.value())
            f.write('%s\n' % self.Fate.value())
            f.write('%s\n' % self.Fortune.value())
            f.write('%s\n' % self.Movement.value())
            f.write('%s\n' % self.Current.value())
            f.write('%s\n' % self.Spent.value())
            f.write('%s\n' % self.Resi.value())
            f.write('%s\n' % self.Reso.value())
            f.write('%s\n' % self.Motivation.text())
            f.write('%s\n' % self.art.value())
            f.write('%s\n' % self.ath.value())
            f.write('%s\n' % self.bri.value())
            f.write('%s\n' % self.chr.value())
            f.write('%s\n' % self.cha.value())
            f.write('%s\n' % self.cli.value())
            f.write('%s\n' % self.col.value())
            f.write('%s\n' % self.con.value())
            f.write('%s\n' % self.dod.value())
            f.write('%s\n' % self.dri.value())
            f.write('%s\n' % self.end.value())
            f.write('%s\n' % self.ent.value())
            f.write('%s\n' % self.gam.value())
            f.write('%s\n' % self.gos.value())
            f.write('%s\n' % self.hag.value())
            f.write('%s\n' % self.inm.value())
            f.write('%s\n' % self.inu.value())
            f.write('%s\n' % self.lea.value())
            f.write('%s\n' % self.mlb.value())
            f.write('%s\n' % self.mle.value())
            f.write('%s\n' % self.nav.value())
            f.write('%s\n' % self.out.value())
            f.write('%s\n' % self.per.value())
            f.write('%s\n' % self.rid.value())
            f.write('%s\n' % self.row.value())
            f.write('%s\n' % self.ste.value())
            f.write('%s\n' % self.SAP.text())
            f.write('%s\n' % self.LAP.text())
            f.write('%s\n' % self.partyName.text())
            f.write('%s\n' % self.SAG.text())
            f.write('%s\n' % self.LAG.text())
            f.write('%s\n' % self.members.text())
            f.close()

    # --------------------------------------------------------------------------

    def getFileName(self):
        filename = QFileDialog.getOpenFileName(self, 'Select File', '',
            'Character File (*.chr);; All Files (*)')[0]
        self.response = filename.split("/")[-1]
        self.setWindowTitle("Character Sheet - WFRP 4e - " + self.response)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
