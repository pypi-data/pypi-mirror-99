# maybe if double click --> browse further in it
# is that really simpler that infinite click inside ??? not so sure but maybe in a way or maybe not because loose spatial info
# but simpler given the complexity
# could use this to update letters etc or to add components to it in an almost infinite way
# test of the stuff
# think about it but not so bad but more complex for several selections
# maybe have both in parallel



from xml.etree import cElementTree as etree
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPalette, QPainter, QColor, QIcon, QPen
from PyQt5.QtSvg import QSvgGenerator
from PyQt5.QtWidgets import QMenu, QApplication, QMainWindow, QPushButton, QWidget, QLabel, QScrollArea, \
    QAction, QProgressBar, QDockWidget, QSpinBox, QComboBox, QGridLayout, QDialog, QGroupBox, QDoubleSpinBox, \
    QVBoxLayout, QTreeView, QFrame, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QAbstractItemView


class Window(QWidget):
    def __init__(self, xml):
        QWidget.__init__(self)
        self.tree = QTreeWidget(self)
        # allow multiple selection or not
        # rather allow single selection or too complex --> maybe block browse in if multiple selection
        # self.tree.setSelectionMode(QAbstractItemView.MultiSelection)





        self.tree.header().hide()
        self.importTree(xml)
        self.button = QPushButton('Export', self)
        self.button.clicked.connect(self.exportTree)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        layout.addWidget(self.button)
        # connect the model to detect selection changed
        self.tree.selectionModel().selectionChanged.connect(self.display_sel)

    def importTree(self, xml):
        def build(item, root):
            for element in root:
                child = QTreeWidgetItem(
                    item, [element.attrib['text']])
                child.setFlags(
                    child.flags() | QtCore.Qt.ItemIsEditable)
                build(child, element)
            item.setExpanded(True)
        root = etree.fromstring(xml)
        build(self.tree.invisibleRootItem(), root)

    def display_sel(self):
        index = self.tree.currentIndex()
        item = self.tree.currentItem()
        print('sel', index, item)

        indices = self.tree.selectionModel().selectedIndexes()
        items = self.tree.selectedItems()
        print('sel', indices, items)
        message = str(index.row())+" "+str(index.column())  # parfait --> peut retrouver le truc
        print('text',item.text(index.column())) # ça marche mais comment le detecter en click
        # QMessageBox::information(this, "Info:", message);
        print(message)


    def exportTree(self):


        def build(item, root):
            for row in range(item.childCount()):
                child = item.child(row)
                element = etree.SubElement(
                    root, 'node', text=child.text(0))
                build(child, element)
        root = etree.Element('root')
        build(self.tree.invisibleRootItem(), root)
        from xml.dom import minidom
        print(minidom.parseString(etree.tostring(root)).toprettyxml())




if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window("""\
<?xml version="1.0" ?>
<root>
    <node text="Couple (0)">
        <node text="Parent (0)">
            <node text="Child (0)"/>
            <node text="Child (1)"/>
        </node>
        <node text="Parent (1)">
            <node text="Child (0)"/>
            <node text="Child (1)"/>
        </node>
    </node>
    <node text="Couple (1)">
        <node text="Parent (0)">
            <node text="Child (0)"/>
            <node text="Child (1)"/>
        </node>
        <node text="Parent (1)">
            <node text="Child (0)"/>
            <node text="Child (1)"/>
        </node>
    </node>
</root>
        """)
    window.setGeometry(800, 300, 300, 300)
    window.show()
    sys.exit(app.exec_())