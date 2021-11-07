import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QLineEdit, QLabel)
from PyQt5.QtCore import pyqtSlot


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Sample Dynamic LineEdit'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 1000
        self.i = 40
        self.j = 80
        self.counter = 1
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        # self.textbox = QLineEdit(self)
        # self.textbox.move(20, 20)
        # self.textbox.resize(280, 40)

        # Create a button in the window
        self.button = QPushButton('Add Line Edit', self)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        # this creates a new field and label everytime the button is clicked
        self.textbox = QLineEdit(self)
        self.label = QLabel(self)
        self.label.setText(str(self.counter))
        self.label.move(5, self.i)
        self.button.move(20, self.j)
        self.textbox.move(20, self.i)
        self.textbox.resize(280, 40)
        # dynamic object names
        self.textbox.setObjectName("text" + str(self.counter))
        self.textbox.show()
        self.label.show()
        self.i += 40
        self.j += 40
        self.counter += 1
        print(self.textbox.objectName())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
