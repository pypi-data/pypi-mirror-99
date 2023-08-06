# ça marche --> faire un instant tooltip

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPalette, QPainter, QColor, QIcon, QStandardItemModel, QStandardItem, QCursor
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtWidgets import QMenu, QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QScrollArea, \
    QAction, QListWidgetItem, QProgressBar, QDockWidget, QSpinBox, QComboBox, QGridLayout, QColorDialog, QDialog, \
    QDialogButtonBox, QTreeView, QToolTip
from PyQt5 import QtCore, QtGui

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.view = QTreeView(self)
        self.view.setMouseTracking(True)
        self.view.entered.connect(self.handleItemEntered)
        model = QStandardItemModel(self)
        for text in 'One Two Three Four Five'.split():
            model.appendRow(QStandardItem(text))
        self.view.setModel(model)
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

    def handleItemEntered(self, index):
        if index.isValid():
            QToolTip.showText(
                QCursor.pos(),
                index.data(),
                self.view.viewport(),
                self.view.visualRect(index)
                )

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 200, 200)
    window.show()
    sys.exit(app.exec_())