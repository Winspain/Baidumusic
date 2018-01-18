# -*- coding: utf-8 -*-
# @Time    : 2017/12/28 21:33
# @Author  : Winspain
# @File    : spider.py
# @Software: PyCharm
import sys
import re
from PyQt4 import QtGui
from BD import Ui_MainWindow

class baiduMusic(QtGui.QMainWindow,Ui_MainWindow):
    mp3_names = []
    def __init__(self):
        super(baiduMusic,self).__init__()
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.dLoad)
        self.pushButton_click.clicked.connect(self.filePath)    #注意不要写成filepath()实例化

    def dLoad(self):
        from threads import SpiderThread
        singers = self.lineEdit.text()
        re_path = self.lineEdit_path.text()
        download_num = self.lineEdit_download.text()
        self.bwThread = SpiderThread(str(singers),str(re_path),str(download_num))
        #SpiderThread的初始化函数中加入参数，就可以再线程中直接加入变量
        self.bwThread.singerSignal.connect(self.pInfo)
        self.bwThread.singerSignal.connect(self.slotStart) #将每次mp3_name的信号返回
        self.bwThread.numSignal.connect(self.numInfo)
        self.bwThread.start()

    '''打印歌曲名信息'''
    def pInfo(self,ls):
        self.textBrowser.setText(ls)

    '''打印歌曲总数目'''
    def numInfo(self,ls):
        self.lineEdit_songs.setText(ls)

    '''打印文件路径'''
    def filePath(self):
        relate_path = QtGui.QFileDialog.getExistingDirectory(self,'open file')
        self.lineEdit_path.setText(relate_path + '\\')  #给末尾加上\，使文件夹路径正确

    '''进度条'''
    def slotStart(self):
        num = int(self.lineEdit_download.text())
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(num)
        countNum2 = self.textBrowser.toPlainText()  #实时的mp3_name实现进度条动态效果
        countNums = len(re.findall(r',',countNum2))+1   #将字符串中的逗号匹配出来以确定元素个数
        for self.countNum in range(num):
            self.progressBar.setValue(countNums)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = baiduMusic()
    window.show()
    sys.exit(app.exec_())

