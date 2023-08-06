
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class MyStyle(QtWidgets.QProxyStyle):
    toolTipTimeouts = {}
    def styleHint(self, hint, option, widget, returnData):
        if hint == QtWidgets.QStyle.SH_ToolTip_WakeUpDelay:
            try:
                return self.toolTipTimeouts[widget]
            except:
                pass
        return QtWidgets.QProxyStyle.styleHint(self, hint, option, widget, returnData)

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # [...]
        self.widget = QtWidgets()
        self.style().toolTipTimeouts[self.widget] = 0
        #optional, if you need to remove widgets at a certain point,
        #allowing the garbage collector to free up memory
        self.widget.destroyed.connect(self.style().toolTipTimeouts.pop)

app = QtWidgets.QApplication(sys.argv)
app.setStyle(MyStyle())

# app = QApplication(sys.argv)
#     vdp = VectorialDrawPane2(active=True)
#
#     main = MainWindow(qt_viewer=vdp)
#     main.show()
#
#     # vdp.show()

sys.exit(app.exec_())


