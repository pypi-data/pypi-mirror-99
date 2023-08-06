import sys


from PyQt5.QtGui import QPalette, QPainter, QColor, QIcon
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtWidgets import QMenu, QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QScrollArea, \
    QAction, QListWidgetItem, QProgressBar, QDockWidget, QSpinBox, QComboBox, QGridLayout, QColorDialog, QDialog, \
    QDialogButtonBox
from PyQt5 import QtCore, QtGui


class MyButtonGroup(QtCore.QObject):
       trigger = QtCore.pyqtSignal((),(bool,))

       def addButton(self, button):
           button.clicked.connect(self.trigger.emit)

       def removeButton(self, button):
           button.clicked.disconnect(self.trigger.emit)


class MyWindow(QWidget):
       def __init__(self):
           QWidget.__init__(self, None)

           self.group = MyButtonGroup()
           button1 = QPushButton("button1")
           button2 = QPushButton("button2")
           self.group.addButton(button1)
           self.group.addButton(button2)
           self.group.trigger.connect(self.do_something)

           layout = QVBoxLayout(self)
           layout.addWidget(button1)
           layout.addWidget(button2)

       def do_something(self, x=False):
           print('hello')


if __name__ == '__main__':
       app = QApplication([])
       window = MyWindow()
       window.show()
       app.exec_()