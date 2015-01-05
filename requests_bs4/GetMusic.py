#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import string
import time
import os

dirName = '/home/quentin/music/' # define your directory to save the music
musicUrl = 'http://luoo.800edu.net/low/luoo/radio'
numberUrl = 'http://www.luoo.net'

def getTheMaxNumber():
    # get the html
    numberResponse = requests.get(numberUrl)
    numberResponse.encoding = 'utf-8'
    numberSoup = BeautifulSoup(numberResponse.text, 'lxml')
    # parse the html and get the number
    numberText = (numberSoup.find_all('div', 'vol-item-lg')[0]).text

    maxNumber = int(re.findall(r'\d+', numberText)[0])
    return maxNumber

def downloadMusic(id):
    albumUrl = 'http://www.luoo.net/music/%d' % id
    albumResponse = requests.get(albumUrl)
    albumResponse.encoding = 'utf-8'
    albumSoup = BeautifulSoup(albumResponse.text, 'lxml')
    albumId = (albumSoup.find_all('span', 'vol-number rounded')[0]).text
    # add _ to albumName avoid make directory failed
    albumName = (albumSoup.find_all('span', 'vol-title')[0]).text.replace(' ', '_')
    musicList = (albumSoup.find_all('a', 'trackname btn-play'))

    # get the name of directory to save the music
    currentDir = 'vol_' + albumId + '-' + albumName + '/'
    saveDir = dirName + currentDir
    isExists = os.path.exists(saveDir)
    if not isExists:
        os.makedirs(saveDir)

    for i in range(1, len(musicList) + 1):
        currentMusicName = musicList[i - 1].text.replace(' ', '_').replace('._', '.').strip('(').strip(')')
        cmd1 = 'wget ' + musicUrl + str(int(albumId)) + '/' + string.zfill(i,2) + '.mp3 ' + '-O ' + saveDir + currentMusicName + '.mp3'
        cmd2 = 'wget ' + musicUrl + str(int(albumId)) + '/' + str(i) + '.mp3 ' + '-O ' + saveDir + currentMusicName + '.mp3'

        if os.system(cmd1.encode('utf-8')) != 0:
            os.system(cmd2.encode('utf-8'))

def musicMain():
    # frist, We should get the max number of the website
    maxNumber = getTheMaxNumber()
    # second, we should get the current number which we have download of the website
    numberFile = open(dirName + 'number.txt', 'r+')
    for line in numberFile.readlines():
        currentNumber = int(line.strip().split('\t')[0])

    # compare
    if maxNumber > currentNumber:
        for i in range(currentNumber + 1, maxNumber + 1):
            try:
                downloadMusic(i)
            except:
                numberFile.write(str(i-2) + '\t' + time.strftime('%Y-%m-%d %H:%M:%S') + '\tERROR\n')
                numberFile.close()
                return
        # after download the music, should write the right number to number.txt
        numberFile.write(str(maxNumber) + '\t' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        numberFile.close()
    else:
        # do nothing
        print '您已经下载了所有的期数，谢谢！\n'
        return

if __name__ == '__main__':
    musicMain()