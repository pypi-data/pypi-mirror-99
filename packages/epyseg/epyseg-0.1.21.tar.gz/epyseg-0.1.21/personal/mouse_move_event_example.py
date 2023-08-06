import sys
from PyQt5 import QtCore, QtGui
import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QToolTip, QTabWidget, QVBoxLayout


class MyWindow(QWidget) :
    def __init__(self):
        QWidget.__init__(self)
        tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        tabs.addTab(self.tab1, "Tab 1")
        tabs.addTab(self.tab2, "Tab 2")
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)
        self.setMouseTracking(True)

    def setMouseTracking(self, flag):
        def recursive_set(parent):
            for child in parent.findChildren(QtCore.QObject):
                try:
                    child.setMouseTracking(flag)
                except:
                    pass
                recursive_set(child)
        QWidget.setMouseTracking(self, flag)
        recursive_set(self)

    def mouseMoveEvent(self, event):
        print( 'mouseMoveEvent: x=%d, y=%d' % (event.x(), event.y()), self.sender())

        # QToolTip.hideText()
        # QToolTip.showText(event.pos(), 'this is a test')

        # check if tab1 is under mouse


        # dirty way but maybe ok
        print(self.tab1.underMouse())
        if self.tab1.underMouse():
            QToolTip.hideText()
            QToolTip.showText(self.tab1.mapToGlobal(QPoint(0, 0)), "tab1" )
        elif    self.tab2.underMouse():
            QToolTip.hideText()
            QToolTip.showText(self.tab2.mapToGlobal(QPoint(0, 0)), "tab2" )





app = QApplication(sys.argv)
window = MyWindow()
window.setFixedSize(640, 480)
window.show()
sys.exit(app.exec_())