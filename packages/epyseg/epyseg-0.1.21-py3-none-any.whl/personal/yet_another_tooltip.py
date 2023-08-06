#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
    def initUI(self):
        hbox = QHBoxLayout(self)
        self.lbl = MyLabel(self)
        self.lbl.setText("foo")
        self.lbl.setToolTip("bar")
        hbox.addWidget(self.lbl)
        label2 = QLabel('another label')
        hbox.addWidget(label2)
        label2.setToolTip('a normal tooltip')
        self.setLayout(hbox)
        self.show()


class MyLabel(QLabel):
    def __init__(self,*args,**kwargs):
        QLabel.__init__(self,*args,**kwargs)
        self._timer = QtCore.QBasicTimer()
        self._timer.start(100, self)
        self._value = 0
        self._last_event_pos = None

    def event(self,event):
        if event.type() == QtCore.QEvent.ToolTip:
            self._last_event_pos = event.globalPos()
            return True
        elif event.type() == QtCore.QEvent.Leave:
            self._last_event_pos = None
            QToolTip.hideText()
        return QLabel.event(self,event)

    def timerEvent(self, x):
        self._value += 1
        if self._last_event_pos:
            QToolTip.hideText()
            QToolTip.showText(self._last_event_pos, "bar: %03d" % self._value)
        self.setText("foo: %03d" % self._value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())