from functools import partial

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton

# modified from https://stackoverflow.com/questions/35394361/pyqt5-no-fill-in-color-dialog
class NoColorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color_widget = QtWidgets.QColorDialog()
        self.color_widget.setWindowFlags(QtCore.Qt.Widget)

        self.color_widget.setOptions(#QtWidgets.QColorDialog.ShowAlphaChannel | really not great to have alpha there especially because it does not show effect of alpha on color...
            QtWidgets.QColorDialog.DontUseNativeDialog |
            QtWidgets.QColorDialog.NoButtons)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.color_widget)
        hbox = QtWidgets.QHBoxLayout()

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Ok).setDefault(True)  # force Ok as default
        buttons.button(QDialogButtonBox.Cancel).setAutoDefault(False)  # prevent Cancel to be the default button

        preview_button = QPushButton('No Color/transparent')
        preview_button.clicked.connect(self.no_color)
        buttons.addButton(preview_button, QDialogButtonBox.ApplyRole)

        hbox.addWidget(buttons)
        layout.addLayout(hbox)

    def no_color(self):
        self.done(3)

    def selectedColor(self):
        return self.color_widget.currentColor() #ça marche en fait

if __name__ == '__main__':

# tt marche

    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = NoColorDialog()
    dialog.show()

    result = dialog.exec_()

    # print(result)

    if result == QDialog.Accepted:
        c = dialog.selectedColor()
        #     if color.isValid():
        # c = QColorDialog.getColor()
        # print(c.name())
        if c.isValid():  # make sure the user did not cancel otherwise ignore
            print(c.name())
    elif result == QDialog.Rejected:
        print('cancel')
    else:
        print(None)

    # return None

    sys.exit(0)