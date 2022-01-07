import os
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QTableWidget,
    QWidget,
    QPushButton,
    QTableWidgetItem
)

# Plik z klasą i funkcjami do obsługi historii.


class oknoHistorii(QWidget):
    def __init__(self, tempOdt):
        super().__init__()
        self.setWindowTitle("Historia Odtwarzania")
        self.resize(400, 100)
        self.tempOdt = tempOdt
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.count = 0
        self.dane = []

        if os.path.isfile(self.tempOdt):
            with open(self.tempOdt) as f:
                for line in f:
                    self.dane.append(line.rstrip('\n'))

        self.table.setColumnCount(3)
        self.table.setRowCount(int(len(self.dane)/3))
        self.table.setMinimumWidth(500)
        self.table.setMinimumHeight(500)
        self.table.setHorizontalHeaderLabels(["Id", "Tytuł", "Czas Trwania"])

        print(int(len(self.dane)))
        for i in range(0, int(len(self.dane)/3)):
            for j in range(0, 3):
                self.table.setItem(
                    i, j, QTableWidgetItem(str(self.dane[self.count])))
                self.count += 1

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        self.exit = QPushButton("Wyjdź")
        self.exit.clicked.connect(lambda: self.close())

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.exit)
        self.setLayout(self.layout)
