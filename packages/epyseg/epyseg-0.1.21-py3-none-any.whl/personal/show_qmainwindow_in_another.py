from PyQt5 import QtCore, QtGui, QtSvg
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath, QLinearGradient, QPolygon, QPixmap, QImage, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView, qApp, QActionGroup, QMessageBox, QFileDialog, QMenu, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QSizePolicy, QPushButton,  QComboBox, QSpacerItem, QRadioButton, QToolButton, QCheckBox

from PyQt5.QtCore import pyqtSignal

class MainWindow1(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent) 
        button = QPushButton('Test')
        button.clicked.connect(self.newWindow)
        label = QLabel('MainWindow1')

        centralWidget = QWidget()
        vbox = QVBoxLayout(centralWidget)
        vbox.addWidget(label)
        vbox.addWidget(button)
        self.setCentralWidget(centralWidget)

    def newWindow(self):
        self.mainwindow2 = MainWindow2(self)
        self.mainwindow2.closed.connect(self.show)
        self.mainwindow2.show()
        self.hide()

class MainWindow2(QMainWindow):

    # QMainWindow doesn't have a closed signal, so we'll make one.
    closed = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.parent = parent
        label = QLabel('MainWindow2', self)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

def startmain():
    app = QApplication(sys.argv)
    mainwindow1 = MainWindow1()
    mainwindow1.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    startmain()