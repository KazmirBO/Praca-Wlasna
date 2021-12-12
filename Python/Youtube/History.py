import os
from PyQt5.QtWidgets import (QVBoxLayout, QWidget, QLabel, QHBoxLayout,
                             QComboBox, QPushButton)

# Plik z klasą i funkcjami do obsługi historii.


class oknoHistorii(QWidget):
    def __init__(self, history, tempKat):
        super().__init__()
        self.resize(400, 100)
        self.history = history
        self.tempKat = tempKat
        self.layout = QVBoxLayout()
        self.tekst = QLabel("Wybierz, który rekord usunąć:")
        self.rekord = QComboBox()

        self.polePrzy = QHBoxLayout()
        self.usun = QPushButton("Usuń")
        self.usun.clicked.connect(self._usun)
        self.exit = QPushButton("Wyjdź")
        self.exit.clicked.connect(lambda: self.close())
        self.polePrzy.addWidget(self.usun)
        self.polePrzy.addWidget(self.exit)

        for i in range(0, self.history.count()):
            self.rekord.addItem(self.history.itemText(i))

        self.layout.addWidget(self.tekst)
        self.layout.addWidget(self.rekord)
        self.layout.addLayout(self.polePrzy)
        self.setLayout(self.layout)

    def _usun(self):
        if os.path.isfile(self.tempKat):
            f = open(self.tempKat, 'r')
            lst = []
            for line in f:
                print(self.rekord.currentText() + " " + line)
                if str(self.rekord.currentText()) + "\n" in line:
                    line = line.replace(self.rekord.currentText(), '')
                lst.append(line)
            f.close()
            f = open(self.tempKat, 'w')
            for line in lst:
                f.write(line)
            f.close()
            self.rekord.removeItem(self.rekord.findData(
                self.rekord.currentText())
            )

            self.history.clear()
            self.rekord.clear()

            if os.path.isfile(self.tempKat):
                historia = []
                with open(self.tempKat, 'r') as f:
                    historia = f.read().splitlines()
                f.close()
                for f in historia:
                    if not f == '':
                        self.history.addItem(f)
                        self.rekord.addItem(f)
