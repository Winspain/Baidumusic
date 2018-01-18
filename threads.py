# -*- coding: utf-8 -*-
# @Time    : 2018/1/13 16:11
# @Author  : Winspain
# @File    : threads.py
# @Software: PyCharm

import requests
import re
import json
from PyQt4 import QtCore

class SpiderThread(QtCore.QThread):
    mp3_names = []
    singerSignal = QtCore.pyqtSignal(str)
    numSignal = QtCore.pyqtSignal(str)
    '''百度音乐下载多线程'''
    def __init__(self,singer,re_path,download_num,parent=None):
        super(SpiderThread,self).__init__(parent)
        self.singer = singer
        self.re_path = re_path
        self.download_num = download_num
    '''根据sid下载MP3'''
    def getMp3bySid(self,sid):
        # sid = '121353608'
        api = 'http://musicapi.qianqian.com/v1/restserver/ting?method=baidu.ting.song.play&\
        format=jsonp&callback=jQuery1720792158255930808_1514470134592&songid=%s&_=1514470135604' % sid
        response = requests.get(api)
        data = response.text
        data = re.findall(r'\((.*)\)', data)[0]
        data = json.loads(data)
        mp3_name = data['songinfo']['title']
        mp3_url = data['bitrate']['file_link']
        '''发送请求'''
        response = requests.get(mp3_url)
        '''持久化'''
        fileName = '%s.mp3' % mp3_name
        filePath = self.re_path
        with open(filePath + '%s.mp3' % mp3_name, 'wb') as f:
            f.write(response.content)
        '''将歌曲名打印到UI界面'''
        self.mp3_names.append(mp3_name)
    '''根据查询内容和页数获取sid'''
    def getSidsbyName(query, pages):
        api = 'http://music.baidu.com/search/song?'
        data = 's=1&key=%s&jump=0&start=%s&size=20&third_type=0' % (query,pages)
        response = requests.get(url=api, params=data)
        html = response.text  # html中双引号为quot
        # print(html.encode("iso-8859-1").decode('utf-8'))
        '''sid&quot;:311782498'''
        sids = re.findall(r'sid&quot;:(\d+)', html)
        return sids
    '''根据歌手查找歌曲总数'''
    def getSize(query):
        api = 'http://music.baidu.com/search'
        data = {
            'key': query,
        }
        response = requests.get(url=api, params=data)
        html = response.text
        ''''total':76'''
        total = re.findall(r'(\'total\':\d+)', html)
        totals = re.findall(r'(\d+)', str(total))
        return totals[0]
    '''根据歌曲总数返回页数'''
    def getPages(num):
        num = int(num)
        quote = num // 20  # 取商
        remain = num % 20  # 取余数
        value = []
        if remain != 0:
            while quote > 0:
                value.insert(0, quote * 20)
                quote -= 1
            value.insert(0, 0)
        else:
            while quote > 1:
                value.insert(0, (quote - 1) * 20)
                quote -= 1
            value.insert(0, 0)
        return value

    def run(self):
        allSids = []
        totalSongs = SpiderThread.getSize(query= self.singer)
        totalPages = SpiderThread.getPages(num= totalSongs)
        for i in totalPages:
            allSid = SpiderThread.getSidsbyName(query= self.singer,pages= i)
            allSids.extend(allSid)
        nums = int(self.download_num)
        for countnums in range(nums):
            SpiderThread.getMp3bySid(self,allSids[countnums])
            self.singerSignal.emit(str(self.mp3_names))
        self.numSignal.emit(str(totalSongs))

