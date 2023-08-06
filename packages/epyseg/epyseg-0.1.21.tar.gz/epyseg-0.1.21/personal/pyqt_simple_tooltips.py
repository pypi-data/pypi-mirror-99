#!/usr/bin/python

# maybe also try  https://doc.qt.io/archives/qt-4.8/stylesheet-examples.html#customizing-qtooltip

import sys

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication
from PyQt5.QtGui import QFont


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

        # QToolTip.hideText()
        # QToolTip.showText(QPoint(150, 150), 'this is a test')


    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))



        # self.setToolTip('This is a <b>QWidget</b> widget')

        self.btn = QPushButton('Button', self)
        self.btn.setToolTip('This is a <b>QPushButton</b> widget')
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(50, 50)


        self.btn.clicked.connect(self.show_stuff)

        # btn.toolTip().show()
        # print(btn.toolTip())

        # QToolTip.showText(QPoint(150,150), 'this is a test', btn)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()


    def show_stuff(self):
        QToolTip.hideText()
        QToolTip.showText(QPoint(150, 150), 'this is a test')


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()