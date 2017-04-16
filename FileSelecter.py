

import sys, os
from PyQt4 import QtGui, QtCore

class FileSelecter(QtGui.QWidget):

    onPathChanged = QtCore.pyqtSignal(str)

    def __init__(self, file_path):
        super(FileSelecter, self).__init__()
        hbox = QtGui.QHBoxLayout()
        self.path = file_path
        self.pathEdit = QtGui.QLineEdit(file_path)
        self.bt = QtGui.QPushButton("Open")
        self.bt.clicked.connect(self.openClicked)

        self.bt_refresh = QtGui.QPushButton("Goto")
        self.bt_refresh.clicked.connect(self.refreshClicked)

        hbox.addWidget(self.pathEdit)
        hbox.addWidget(self.bt_refresh)
        hbox.addWidget(self.bt)

        self.setLayout(hbox)

    def openClicked(self):
        fname = QtGui.QFileDialog.getExistingDirectory(None, "Chose a Directory", '/home')
        if os.path.isdir(fname):
            print fname
            self.pathEdit.setText(fname)
            self.path = fname
            self.onPathChanged.emit(fname)
        pass

    def refreshClicked(self):
        path = unicode(self.pathEdit.text())
        if os.path.exists(path) and os.path.isdir(path):
            self.setPath(path)
        else:
            QtGui.QMessageBox.information(self, 'Error Path', 'Please input a valid path\n'+path)
#            reply = QtGui.QMessageBox.question(self, 'Error Path',
#                                               path, QtGui.QMessageBox.Yes)
        pass


    def getPath(self):
        return os.path.abspath(unicode(self.path))

    def setPath(self, path):
        if os.path.isdir(path):
            print path
            self.pathEdit.setText(path)
            self.path = path
            self.onPathChanged.emit(path)
        pass

#        sender = self.sender()
#        self.statusBar().showMessage(sender.text() + ' was pressed')



