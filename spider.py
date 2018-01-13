# -*- coding: utf-8 -*-
# @Time    : 2017/12/28 21:33
# @Author  : Winspain
# @File    : spider.py
# @Software: PyCharm
import sys
import requests
import re
import json
from PyQt4 import QtCore, QtGui, uic
from BD import Ui_MainWindow

class baiduMusic(QtGui.QMainWindow,Ui_MainWindow):
    mp3_names = []
    def __init__(self):
        super(baiduMusic,self).__init__()
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.dLoad)

    def dLoad(self):
        from threads import SpiderThread
        singers = self.lineEdit.text()
        self.bwThread = SpiderThread(str(singers))
        self.bwThread.singerSignal.connect(self.pInfo)
        self.bwThread.start()
    def pInfo(self,ls):
        self.textBrowser.setText(ls)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = baiduMusic()
    window.show()
    sys.exit(app.exec_())

