from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPalette, QPainter, QColor, QIcon, QPen
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtWidgets import QMenu, QApplication, QMainWindow, QPushButton, QWidget, QLabel, QScrollArea, \
    QAction, QProgressBar, QDockWidget, QSpinBox, QComboBox, QGridLayout, QDialog, QGroupBox, QDoubleSpinBox, \
    QVBoxLayout, QTreeView, QFrame, QHBoxLayout

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.parents = []
        self.dbdata = data
        self.rootItem = TreeItem([u"NameOfColumn"])
        self.setupModelData(self.dbdata, self.rootItem)

    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole:

            prev_value = self.getValue(index)

            item = index.internalPointer()

            item.setData((value.toString()))#unicode(value.toString())

            return True
        else:
            return False


    def removeRows(self, position=0, count=1, parent=QtCore.QModelIndex()):
        node = self.nodeFromIndex(parent)
        self.beginRemoveRows(parent, position, position + count - 1)
        node.childItems.pop(position)
        self.endRemoveRows()


    def nodeFromIndex(self, index):
        if index.isValid():
            return index.internalPointer()
        else:
            return self.rootItem


    def getValue(self, index):
        item = index.internalPointer()
        return item.data(index.column())


    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()


    def data(self, index, role):
        if not index.isValid():
            return None
        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()
        return QtCore.QVariant(item.data(index.column()))


    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable


    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.rootItem.data(section)[0])

        return None


    def index(self, row, column, parent):
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()


    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)


    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()


    def setupModelData(self, lines, parent):
        ind = []
        self.parents.append(parent)
        ind.append(0)
        col_numb = parent.columnCount()
        numb = 0

        for line in lines:
            numb += 1
            lineData = line[0]
            self.parents[-1].appendChild(TreeItem(lineData, self.parents[-1]))

            columnData = line[1]

            self.parents.append(self.parents[-1].child(self.parents[-1].childCount() - 1))

            for j in columnData:
                self.parents[-1].appendChild(TreeItem(j, self.parents[-1]))
            if len(self.parents) > 0:
                self.parents.pop()


class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData

        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

    def setData(self, data):
        self.itemData = data

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    app = QApplication([])

    model = TreeModel(data=[])
    dialog = QDialog()

    dialog.setMinimumSize(300, 150)
    layout = QVBoxLayout(dialog)

    tv = QTreeView(dialog)
    tv.setModel(model)
    tv.setAlternatingRowColors(True)
    layout.addWidget(tv)

    # label = QLabel("Search for the following person")
    # layout.addWidget(label)
    frame = QFrame(dialog)
    layout.addWidget(frame)

    dialog.exec_()

    app.closeAllWindows()

    # main = MainWindow(qt_viewer=vdp)
    # main.show()


    sys.exit(app.exec_())
