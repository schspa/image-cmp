
import os
import hashlib
from PyQt4 import QtGui, QtCore
import time

class ImageFile (QtGui.QWidget):
    def __init__ (self, file_path, parent = None):
        super(ImageFile, self).__init__()

        self.path, self.name = os.path.split(file_path)
        self.file_len = 0;
        self.textQVBoxLayout = QtGui.QVBoxLayout()
        self.textUpQLabel    = QtGui.QLabel()
        self.textDownQLabel  = QtGui.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QtGui.QHBoxLayout()
        self.iconQLabel      = QtGui.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        self.sumThread = None
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(221, 34, 34);
        ''')
        self.md5sum = "md5sum"
        self.md5sum_len = 0

        if os.path.isdir(os.path.abspath(file_path)):
            self.setIcon("icon/folder.png")
            self.setTextDown("")
            self.setTextUp(self.name)
        else:
            self.setIcon("icon/folder-tar.png")
            self.setTextDown("00000000000000000000000000000000")
            self.file_len = os.path.getsize(file_path)
            self.setTextUp(self.name + "   " + str(self.file_len))
            self.caculateMd5()
#        self.show()

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))

    def getName(self):
        return self.name

    def getMd5(self):
        return self.md5sum

    def getPath(self):
        return os.path.abspath(os.path.join(unicode(self.path), unicode(self.name)))

    def caculateMd5(self, length = 0):
        if self.sumThread != None:
            self.sumThread.stop()
        if not os.path.isfile(self.getPath()):
            return
        if length == 0:
            length = os.path.getsize(self.getPath())
        self.md5sum_len = length
        self.sumThread = md5CaculateThread(self.getPath(), length)
        self.sumThread.progress.connect(self.md5CaculateProgress)
        self.sumThread.done.connect(self.md5CaculateDone)
        self.sumThread.start()

    def md5CaculateDone(self, md5sum):
        self.md5sum = md5sum
        self.setTextDown(md5sum + "  " + str(self.md5sum_len))
    def md5CaculateProgress(self, progress):
        self.md5sum = str(progress)
        self.setTextDown(self.md5sum)

class md5CaculateThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    done = QtCore.pyqtSignal(str)
    def __init__(self, filepath, length):
        super(md5CaculateThread, self).__init__()
        self.length = length
        self.filepath = filepath
        self.is_run = True
    def __delete__(self, instance):
        self.is_run = False
        self.quit()

    def run(self):
        size = self.length
        total_size = size
        myhash = hashlib.md5()
        f = file(self.filepath, 'rb')
        last_print_time = time.clock()
        is_blank = True
        while size > 0 and self.is_run:
            current_time = time.clock()
            if current_time - last_print_time > 0.3 :
                self.progress.emit(size)
            if size > 8096:
                b = f.read(8096)
                size = size - 8096;
            else:
                b = f.read(size)
                size = 0;
            if not b:
                break
            myhash.update(b)
            if (is_blank and len(b) != b.count("\0")):
                is_blank = False
        f.close()
        if (is_blank):
            self.done.emit("blank file")
        else:
            self.done.emit(myhash.hexdigest())
    def stop(self):
        self.is_run = False
