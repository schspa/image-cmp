# -*- coding: utf-8 -*-

"""
In this example, we create a simple
window in PyQt4.
"""

from ReadBackImages import *


def layoutToWidget(layout):
    widget = QtGui.QWidget()
    widget.setLayout(layout)
    return widget

class Example(QtGui.QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()


    def initUI(self):

        self.initToolbar()

        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('icon/icon.png'))
        self.initMainWidget()

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.setGeometry(300, 300, 800, 600)
        self.move(qr.topLeft())

    def initToolbar(self):
        cmpAction = QtGui.QAction(QtGui.QIcon('icon/cmp.png'), 'New', self)
        cmpAction.triggered.connect(self.cmpAction_def)
        self.tb_cmp = self.addToolBar('Cmp')

        self.tb_cmp.addAction(cmpAction)

    def newAction_def(self):
        pass

    def editAction_def(self):
        pass

    def delAction_def(self):
        pass

    def cmpAction_def(self):
        print "cmpAction_def"
        images = []
        min_len = sys.maxint
        for rbImages in self.readbackImages:
            image = rbImages.getSelectImage()
            len = os.path.getsize(image.getPath())
            if (len < min_len):
                min_len = len
            images.append(image)
        print images
        print min_len
        for image in images:
            image.caculateMd5(min_len)
        pass

    def initMainWidget(self):
        print "init Main Widget"
        sys.stdout.flush()
        self.rootWidget = QtGui.QWidget()
        self.rootView = QtGui.QVBoxLayout()
        self.rootWidget.setLayout(self.rootView)
        self.readbackImages = []
        hbox = QtGui.QHBoxLayout()
        self.readbackImages.append(ReadBackImages("/home/schspa"))
        self.readbackImages.append(ReadBackImages("/home"))
        for rbImages in self.readbackImages:
            hbox.addWidget(rbImages)

        self.rootView.addWidget(layoutToWidget(hbox))
        self.setCentralWidget(self.rootWidget)




'''
    def closeEvent(self, event):

        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
'''


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
