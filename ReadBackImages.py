
import sys, os
from PyQt4 import QtGui, QtCore
from FileSelecter import *
from ImageFile import *


class ReadBackImages(QtGui.QWidget):
    def __init__(self, file_path, parent = None, file_length = 0):
        super(ReadBackImages, self).__init__(parent = None)
        print "ReadbackImage init"

        self.hbox = QtGui.QVBoxLayout(self)
#        self.setLayout(self.hbox)
#        self.testLabel = QtGui.QLabel("test")
#        self.hbox.addWidget(self.testLabel)
#
#        self.setShown(True)

        self.selecter = FileSelecter(file_path)
        self.selecter.onPathChanged.connect(self.pathChanged)
        self.hbox.addWidget(self.selecter)
#
#        self.images_ui = QtGui.QListWidget()
#        self.hbox.addWidget(self.images_ui)
#        image = ImageFile("test")
#        self.hbox.addWidget(image)
#        widgetItem = QtGui.QListWidgetItem(self.images_ui)
#
#        self.images_ui.setItemWidget(widgetItem, image)
#        self.images_ui.addItem(widgetItem)

        self.images_ui = QtGui.QListWidget(self)
        self.images_ui.itemDoubleClicked.connect(self.itemDoubleClicked)
#        self.images_ui.itemClicked.connect(self.itemClicked)


        self.hbox.addWidget(self.images_ui)
        self.update()
#

    def update(self):
        self.images = []
        self.images_ui.clear()
        path = self.selecter.getPath()
        files = []
        files = os.listdir(path)
#        print "update_path:" + path
        if path != "/":
            files.insert(0, "..")

        for f in files:
            # Create QCustomQWidget
            full_path = os.path.join(self.selecter.getPath(), f)
#            print full_path
            myQCustomQWidget = ImageFile(full_path)
            # Create QListWidgetItem
            myQListWidgetItem = QtGui.QListWidgetItem(self.images_ui)
            # Set size hint#        self.update()
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())#
            myQListWidgetItem.setData(0, QtCore.QVariant(myQCustomQWidget))
            # Add QListWidgetItem into QListWidget#        self.images_ui.itemClicked.connect(self.itemClicked)
            self.images_ui.addItem(myQListWidgetItem)#        self.setShown(True)
            self.images_ui.setItemWidget(myQListWidgetItem, myQCustomQWidget)#        self.show()
            self.images.append(myQCustomQWidget)



    def itemClicked(self, item):
        image = item.data(0).toPyObject()
        QtGui.QMessageBox.information(self, "ListWidget", "You clicked: "+image.getName())

    def itemDoubleClicked(self, item):
        image = item.data(0).toPyObject()
        print item
#        QtGui.QMessageBox.information(self, "ListWidget", "You itemDoubleClicked: "+image.getPath())
        self.selecter.setPath(image.getPath())

    def pathChanged(self, path):
        self.update()

    def getSelectImage(self):
        item = self.images_ui.currentItem()
        if isinstance(item, QtGui.QListWidgetItem):
            image = item.data(0).toPyObject()
            return image
        return None
