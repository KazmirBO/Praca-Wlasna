import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
                             QHBoxLayout, QWidget
                             )


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)

        self.tab = [0, 1, 2, 3, 4, 5]
        self.initUI()

    def initUI(self):
        for count in range(0, 6):
            nr = self.tab[count]
            Buttons = QPushButton(str(nr))
            Buttons.clicked.connect(lambda checked, arg=nr: print(arg))
            Buttons.setObjectName("button" + str(nr))
            self.generalLayout.addWidget(Buttons)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec()
