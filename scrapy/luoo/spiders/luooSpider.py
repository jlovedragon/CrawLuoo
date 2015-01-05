#!/usr/bin/env python
#-*- coding: utf-8 -*-

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider
from luoo.items import LuooItem
import os
import re
import string
import time

# the initial directory to save music, you can change it to fit you
dirName = '/home/quentin/music/'
# the link of music
musicUrl = 'http://luoo.800edu.net/low/luoo/radio'

class luooSpider(CrawlSpider):
    name = 'luooSpider'
    allowed_domains = ['luoo.net']
    start_urls = ['http://www.luoo.net/']

    def parse(self, response):
        sel = Selector(response)
        # find the text including the ablum's name and id
        title = sel.xpath('//div[@class="vol-item-lg"]/a[@class="title"]/text()').extract()
        number = re.findall(r'\d+', title[0].encode('utf-8'))
        maxNumber = int(number[0].encode('utf-8'))
        numberFile = open(dirName + 'number.txt', 'r+')
        for line in numberFile.readlines():
            currentNumber = int(line.strip().split('\t')[0])

        # compare
        if maxNumber > currentNumber:
            for i in range(currentNumber + 1, maxNumber + 1):
                musicListUrl = 'http://www.luoo.net/music/%d' %i
                yield Request(url = musicListUrl, callback=self.parseMusicList)
            numberFile.write(str(maxNumber) + "\t" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            numberFile.close()
        else:
            # do nothing
            print '您已经下载了所有的期数，谢谢！\n'
            return

    def parseMusicList(self, response):
        sel = Selector(response)
        item = LuooItem()
        albumIdList = sel.xpath('//span[@class="vol-number rounded"]/text()').extract()
        albumNameList = sel.xpath('//span[@class="vol-title"]/text()').extract()
        # albumCount = sel.xpath('//ul/li[@class="track-item rounded"]').extract()

        # music name
        musicList = sel.xpath('//a[@class="trackname btn-play"]/text()').extract()
        
        albumId = albumIdList[0].encode('utf-8')
        #print 'title = %s' % title[0].encode('utf-8')
        albumName = albumNameList[0].encode('utf-8').replace(" ", "_")
        albumCount = len(musicList)

        currentDir = 'vol_' + albumId + '_' + albumName + '/'

        saveDir = dirName + currentDir

        isExists = os.path.exists(saveDir)
        if not isExists:
            os.makedirs(saveDir)

        for i in range(1, albumCount + 1):
            currentMusicName = musicList[i - 1].encode('utf-8').replace(" ", "_").replace('._', '.').strip('(').strip(')')
            cmd1 = 'wget ' + musicUrl + str(int(albumId)) + '/' + string.zfill(i,2) + '.mp3 ' + '-O ' + saveDir + currentMusicName + '.mp3'
        cmd2 = 'wget ' + musicUrl + str(int(albumId)) + '/' + str(i) + '.mp3 ' + '-O ' + saveDir + currentMusicName + '.mp3'

        if os.system(cmd1.encode('utf-8')) != 0:
            os.system(cmd2.encode('utf-8'))